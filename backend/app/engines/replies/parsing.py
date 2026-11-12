"""
Reading one inbound message (phase E4). Pure functions, no network, no database.

parse_message(raw) gives the headers the reply loop needs, the plain text, and the text split into
    new_text   what the sender wrote now (quoted history and our own unsubscribe line removed)
    signature  the part below a "-- " line (kept apart: a newsletter footer saying "unsubscribe" is not a stop)
    quoted     everything that was cut away
and a kind:
    DSN        delivery status notification (multipart/report; report-type=delivery-status, or what the E2 DSN
               parser recognises: mailer-daemon / postmaster senders, "Undeliverable" subjects)
    FEEDBACK   ARF feedback report (report-type=feedback-report): a provider's spam complaint
    AUTOMATED  read receipt (report-type=disposition-notification) or Precedence: bulk / junk / list
    AUTO_REPLY out-of-office / auto-responder: Auto-Submitted (not "no"), X-Autoreply, X-Autorespond,
               Precedence: auto_reply, or a typical out-of-office subject (English, Hindi, Gujarati)
    HUMAN      everything else

ooo_return_date(text, received) finds a return date in an out-of-office text ("until 20 November", "back on
23/11/2026", "20 नवंबर तक", "Monday 23 November"): day + month name (English, Hindi, Gujarati), dd/mm/yyyy (Indian
order), yyyy-mm-dd, "Month dd". Without a year, the next such date on or after the day it arrived. A date before
the message or more than 90 days after it is ignored (review after 14 days instead).
"""

import hashlib
import html
import re
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta, timezone
from email import message_from_bytes, policy
from email.message import EmailMessage
from email.utils import getaddresses, parsedate_to_datetime
from typing import Optional

from backend.app.engines.sending import dsn

MAX_TEXT_CHARS = 20000   # what is kept of a body; a reply is short, an attachment is never kept
MAX_RETURN_DAYS = 90

KIND_HUMAN, KIND_AUTO_REPLY, KIND_DSN, KIND_FEEDBACK, KIND_AUTOMATED = (
    "HUMAN", "AUTO_REPLY", "DSN", "FEEDBACK", "AUTOMATED")

_MSGID = re.compile(r"<[^<>\s]+>")

# Typical out-of-office / auto-reply subjects (lower case). Hindi and Gujarati as Gmail / Outlook show them.
OOO_SUBJECTS = (
    "out of office", "out of the office", "automatic reply", "auto reply", "auto-reply", "autoreply",
    "auto response", "auto-response", "autoresponse", "away from the office", "away from office", "on leave",
    "on vacation", "on holiday", "vacation reply", "i am away", "i'm away",
    "स्वचालित उत्तर", "स्वतः उत्तर", "कार्यालय से बाहर", "छुट्टी पर", "अवकाश",
    "સ્વયંસંચાલિત જવાબ", "ઓફિસની બહાર", "રજા પર",
)
# Body openings of an out-of-office text without auto-reply headers (only for short messages with no question).
OOO_BODY = (
    "i am out of the office", "i am out of office", "i'm out of the office", "i'm out of office",
    "i am currently out of", "i'm currently out of", "i am on leave", "i'm on leave", "i am away", "i'm away",
    "i am on vacation", "i'm on vacation", "thank you for your email. i am", "thank you for your message. i am",
    "main chhutti par", "main chutti par", "mai chhutti par", "मैं छुट्टी पर", "मैं कार्यालय से बाहर", "मैं अवकाश पर",
    "हम छुट्टी पर", "હું રજા પર", "હું ઓફિસની બહાર",
)
OOO_BODY_MAX_WORDS = 60

# Lines where a quoted earlier message starts (everything from there down is history).
_QUOTE_STARTS = (
    re.compile(r"^\s*On\b.{0,300}\bwrote:\s*$", re.IGNORECASE | re.DOTALL),
    re.compile(r"^\s*-{2,}\s*Original Message\s*-{2,}", re.IGNORECASE),
    re.compile(r"^\s*-{2,}\s*Forwarded message\s*-{2,}", re.IGNORECASE),
    re.compile(r"^\s*_{10,}\s*$"),                                         # Outlook separator line
    re.compile(r"^\s*(From|Von|De)\s*:\s*.+$", re.IGNORECASE),              # Outlook header block (with Sent: below)
    re.compile(r"^.{0,300}(ने लिखा|એ લખ્યું|wrote)\s*:\s*$", re.DOTALL),    # Gmail in Hindi / Gujarati
    re.compile(r"^\s*Le\b.{0,300}a écrit\s*:\s*$", re.IGNORECASE | re.DOTALL),
    re.compile(r"^\s*Sent from my (iPhone|Android|phone|mobile)", re.IGNORECASE),
)
_OUR_FOOTER = re.compile(r'^\s*>*\s*Reply\s+"?stop"?\s+or\s+unsubscribe\s+here:.*$', re.IGNORECASE)
_SIGNATURE_DELIMITER = re.compile(r"^--\s*$")


@dataclass
class ParsedMessage:
    message_id: Optional[str]
    in_reply_to: Optional[str]
    references: list[str]
    from_address: Optional[str]
    from_name: Optional[str]
    reply_to: Optional[str]
    to_addresses: list[str]
    subject: str
    date: Optional[datetime]
    text: str                      # the whole plain text (decoded, HTML turned into text)
    new_text: str
    signature: str
    quoted: str
    kind: str
    auto_signals: list[str] = field(default_factory=list)
    report_type: Optional[str] = None
    raw_size: int = 0
    raw_sha256: str = ""
    bounce: Optional[dsn.BounceResult] = None
    feedback: Optional[dict] = None


def _first_address(value) -> tuple[Optional[str], Optional[str]]:
    pairs = getaddresses([str(value)]) if value else []
    for name, address in pairs:
        if address and "@" in address:
            return address.strip().lower(), (name or "").strip() or None
    return None, None


def message_ids(value) -> list[str]:
    return _MSGID.findall(str(value or ""))


def html_to_text(markup: str) -> str:
    """Rough HTML -> text: quoted blocks (blockquote, gmail_quote) dropped, tags removed, entities decoded."""
    text = re.sub(r"(?is)<(script|style|head)\b.*?</\1>", " ", markup)
    text = re.sub(r"(?is)<blockquote\b.*?</blockquote>", "\n", text)
    text = re.sub(r'(?is)<div[^>]+class="[^"]*gmail_quote[^"]*".*', "\n", text)
    text = re.sub(r"(?i)<br\s*/?>|</p>|</div>|</li>|</tr>", "\n", text)
    text = re.sub(r"(?s)<[^>]+>", " ", text)
    text = html.unescape(text)
    return "\n".join(" ".join(line.split()) for line in text.splitlines())


def _part_text(part) -> str:
    try:
        content = part.get_content()
    except (LookupError, UnicodeError, AssertionError, KeyError, ValueError):
        payload = part.get_payload(decode=True) or b""
        content = payload.decode("utf-8", errors="replace")
    return content if isinstance(content, str) else ""


def body_text(message: EmailMessage) -> str:
    """The plain-text body (preferred) or the HTML body as text. Attachments are never read."""
    try:
        part = message.get_body(preferencelist=("plain", "html"))
    except (KeyError, AttributeError):
        part = None
    if part is None:
        for candidate in message.walk():
            if candidate.get_content_maintype() == "text" and not candidate.get_filename():
                part = candidate
                break
    if part is None:
        return ""
    text = _part_text(part)
    if part.get_content_subtype() == "html":
        text = html_to_text(text)
    return text.replace("\r\n", "\n").replace("\r", "\n")[:MAX_TEXT_CHARS]


def split_reply(text: str) -> tuple[str, str, str]:
    """(new text, signature, quoted history). Lines starting with '>' are history; the first quote-start line
    (On ... wrote:, -----Original Message-----, an Outlook From: block, ...) cuts everything below it."""
    lines = text.replace("\r\n", "\n").split("\n")
    new, quoted = [], []
    cut = None
    for index, line in enumerate(lines):
        # "On Tue, 17 Nov 2026 at 09:01, Name <a@b> wrote:" is often wrapped over two lines.
        joined = line if index + 1 >= len(lines) else line + " " + lines[index + 1]
        if any(p.match(line) for p in _QUOTE_STARTS) or (
                re.match(r"^\s*On\b", line) and re.search(r"\bwrote:\s*$", joined) and not line.strip().endswith(".")):
            if re.match(r"^\s*(From|Von|De)\s*:", line, re.IGNORECASE) and not _outlook_block(lines, index):
                new.append(line)
                continue
            cut = index
            break
        if line.lstrip().startswith(">"):
            quoted.append(line)
            continue
        if _OUR_FOOTER.match(line):
            quoted.append(line)
            continue
        new.append(line)
    if cut is not None:
        quoted += lines[cut:]
    signature: list[str] = []
    for index, line in enumerate(new):
        if _SIGNATURE_DELIMITER.match(line):
            signature = new[index + 1:]
            new = new[:index]
            break
    return "\n".join(new).strip(), "\n".join(signature).strip(), "\n".join(quoted).strip()


def _outlook_block(lines: list[str], index: int) -> bool:
    """An Outlook quote header: From: followed within 4 lines by Sent: / Date: / To: / Subject:."""
    following = " ".join(lines[index + 1:index + 5]).lower()
    return any(key in following for key in ("sent:", "date:", "to:", "subject:", "gesendet:", "envoyé"))


def _header(message: EmailMessage, name: str) -> str:
    try:
        return str(message.get(name, "") or "").strip()
    except (ValueError, TypeError, IndexError):
        return ""


def auto_reply_signals(message: EmailMessage, subject: str, new_text: str) -> list[str]:
    signals = []
    auto = _header(message, "Auto-Submitted").lower()
    if auto and auto != "no":
        signals.append(f"Auto-Submitted: {auto[:40]}")
    for name in ("X-Autoreply", "X-Autorespond", "X-Autoresponder", "X-Auto-Response-Suppress-Reply"):
        if _header(message, name):
            signals.append(name)
    precedence = _header(message, "Precedence").lower()
    if precedence == "auto_reply":
        signals.append("Precedence: auto_reply")
    lowered = subject.lower()
    if any(s in lowered for s in OOO_SUBJECTS):
        signals.append("out-of-office subject")
    body = " ".join(new_text.lower().split())
    if (len(body.split()) <= OOO_BODY_MAX_WORDS and "?" not in body
            and any(body.startswith(s) or f". {s}" in body[:200] for s in OOO_BODY)):
        signals.append("out-of-office text")
    return signals


def _report_type(message: EmailMessage) -> Optional[str]:
    if message.get_content_type() != "multipart/report":
        return None
    return (message.get_param("report-type") or "").lower() or None


def _feedback(message: EmailMessage) -> dict:
    """ARF (RFC 5965): the original message's Message-ID and recipient from the attached copy / headers."""
    original_id, original_to = None, None
    for part in message.walk():
        ctype = part.get_content_type()
        if ctype in ("message/rfc822", "text/rfc822-headers"):
            text = part.as_string() if ctype == "message/rfc822" else _part_text(part)
            found = re.search(r"^Message-ID:\s*(<[^>\s]+>)", text, re.IGNORECASE | re.MULTILINE)
            to = re.search(r"^To:\s*(.+)$", text, re.IGNORECASE | re.MULTILINE)
            original_id = original_id or (found.group(1) if found else None)
            if to and not original_to:
                original_to = _first_address(to.group(1))[0]
        if ctype == "message/feedback-report":
            text = _part_text(part) if not part.is_multipart() else part.as_string()
            rcpt = re.search(r"^Original-Rcpt-To:\s*(.+)$", text, re.IGNORECASE | re.MULTILINE)
            if rcpt and not original_to:
                original_to = _first_address(rcpt.group(1))[0]
    return {"original_message_id": original_id, "original_recipient": original_to}


def parse_message(raw: bytes) -> ParsedMessage:
    message: EmailMessage = message_from_bytes(raw, policy=policy.default)
    from_address, from_name = _first_address(_header(message, "From"))
    reply_to, _ = _first_address(_header(message, "Reply-To"))
    to_addresses = [a.lower() for _, a in getaddresses([_header(message, "To"), _header(message, "Cc")]) if a]
    subject = " ".join(_header(message, "Subject").split())[:500]
    try:
        sent = parsedate_to_datetime(_header(message, "Date")) if _header(message, "Date") else None
        if sent is not None and sent.tzinfo is None:
            sent = sent.replace(tzinfo=timezone.utc)
    except (TypeError, ValueError, IndexError):
        sent = None
    message_id = (message_ids(_header(message, "Message-ID")) or [None])[0]
    in_reply_to = (message_ids(_header(message, "In-Reply-To")) or [None])[0]
    references = message_ids(_header(message, "References"))
    text = body_text(message)
    new_text, signature, quoted = split_reply(text)
    report_type = _report_type(message)

    kind, bounce, feedback = KIND_HUMAN, None, None
    signals: list[str] = []
    compat = message_from_bytes(raw, policy=policy.compat32)
    if report_type == "feedback-report":
        kind, feedback = KIND_FEEDBACK, _feedback(message)
    elif report_type == "disposition-notification":
        kind = KIND_AUTOMATED
        signals.append("read receipt")
    elif report_type in ("delivery-status", "global-delivery-status") or dsn.looks_like_bounce(compat):
        parsed = dsn.parse_bounce(compat)
        if parsed.is_bounce:
            kind, bounce = KIND_DSN, parsed
    if kind == KIND_HUMAN:
        signals = auto_reply_signals(message, subject, new_text)
        if signals:
            kind = KIND_AUTO_REPLY
        elif _header(message, "Precedence").lower() in ("bulk", "junk", "list") or _header(message, "List-Id"):
            kind = KIND_AUTOMATED
            signals.append("list / bulk mail")
    return ParsedMessage(
        message_id=message_id, in_reply_to=in_reply_to, references=references, from_address=from_address,
        from_name=from_name, reply_to=reply_to, to_addresses=to_addresses, subject=subject, date=sent, text=text,
        new_text=new_text, signature=signature, quoted=quoted, kind=kind, auto_signals=signals,
        report_type=report_type, raw_size=len(raw), raw_sha256=hashlib.sha256(raw).hexdigest(), bounce=bounce,
        feedback=feedback)


# ─── out-of-office return dates ─────────────────────────────────────────────

MONTHS = {
    "jan": 1, "january": 1, "feb": 2, "february": 2, "mar": 3, "march": 3, "apr": 4, "april": 4, "may": 5,
    "jun": 6, "june": 6, "jul": 7, "july": 7, "aug": 8, "august": 8, "sep": 9, "sept": 9, "september": 9,
    "oct": 10, "october": 10, "nov": 11, "november": 11, "dec": 12, "december": 12,
    # Hindi (Devanagari)
    "जनवरी": 1, "फ़रवरी": 2, "फरवरी": 2, "मार्च": 3, "अप्रैल": 4, "मई": 5, "जून": 6, "जुलाई": 7, "अगस्त": 8,
    "सितंबर": 9, "सितम्बर": 9, "अक्टूबर": 10, "अक्तूबर": 10, "नवंबर": 11, "नवम्बर": 11, "दिसंबर": 12, "दिसम्बर": 12,
    # Gujarati
    "જાન્યુઆરી": 1, "ફેબ્રુઆરી": 2, "માર્ચ": 3, "એપ્રિલ": 4, "મે": 5, "જૂન": 6, "જુલાઈ": 7, "ઓગસ્ટ": 8,
    "સપ્ટેમ્બર": 9, "ઓક્ટોબર": 10, "નવેમ્બર": 11, "ડિસેમ્બર": 12,
}
_MONTH_WORDS = "|".join(sorted((re.escape(k) for k in MONTHS), key=len, reverse=True))
_DIGITS = str.maketrans("०१२३४५६७८९૦૧૨૩૪૫૬૭૮૯", "01234567890123456789")
_DAY_MONTH = re.compile(r"(?<!\d)(\d{1,2})(?:st|nd|rd|th)?\s*(?:of\s+)?(" + _MONTH_WORDS + r")\.?(?:,?\s*(\d{4}))?",
                        re.IGNORECASE)
_MONTH_DAY = re.compile(r"(?<![\w])(" + _MONTH_WORDS + r")\.?\s+(\d{1,2})(?:st|nd|rd|th)?(?:,?\s*(\d{4}))?(?!\d)",
                        re.IGNORECASE)
_NUMERIC = re.compile(r"(?<!\d)(\d{1,2})[/.-](\d{1,2})(?:[/.-](\d{2,4}))?(?!\d)")
_ISO = re.compile(r"(?<!\d)(\d{4})-(\d{2})-(\d{2})(?!\d)")


def _resolve(day: int, month: int, year: Optional[int], received: date) -> Optional[date]:
    try:
        if year is not None:
            year = year + 2000 if year < 100 else year
            return date(year, month, day)
        candidate = date(received.year, month, day)
        if candidate < received - timedelta(days=1):
            candidate = date(received.year + 1, month, day)
        return candidate
    except ValueError:
        return None


def ooo_return_date(text: str, received: date) -> Optional[date]:
    """The latest plausible date in the text (an OOO note usually names its last day or the return day)."""
    if not text:
        return None
    text = text.translate(_DIGITS)
    found: list[date] = []
    for match in _ISO.finditer(text):
        value = _resolve(int(match.group(3)), int(match.group(2)), int(match.group(1)), received)
        if value:
            found.append(value)
    stripped = _ISO.sub(" ", text)
    for match in _DAY_MONTH.finditer(stripped):
        value = _resolve(int(match.group(1)), MONTHS[match.group(2).lower()],
                         int(match.group(3)) if match.group(3) else None, received)
        if value:
            found.append(value)
    for match in _MONTH_DAY.finditer(stripped):
        value = _resolve(int(match.group(2)), MONTHS[match.group(1).lower()],
                         int(match.group(3)) if match.group(3) else None, received)
        if value:
            found.append(value)
    for match in _NUMERIC.finditer(stripped):
        # Indian order dd/mm(/yyyy); a time like 10.30 has no third part and a day > 12 decides the order anyway.
        if match.group(3) is None and "." in match.group(0):
            continue
        value = _resolve(int(match.group(1)), int(match.group(2)),
                         int(match.group(3)) if match.group(3) else None, received)
        if value:
            found.append(value)
    plausible = [d for d in found if received <= d <= received + timedelta(days=MAX_RETURN_DAYS)]
    return max(plausible) if plausible else None
