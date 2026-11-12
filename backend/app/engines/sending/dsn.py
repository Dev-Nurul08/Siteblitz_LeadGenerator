"""
Bounce / delivery-status parser (module only; E4 feeds it the messages it reads over IMAP).

parse_bounce(raw) reads an RFC 3464 delivery-status report (multipart/report; report-type=delivery-status) or a
common plain-text bounce (Exim, Yahoo, old Gmail and Outlook styles) and returns:

    kind                 HARD    5.1.x (mailbox / user unknown, bad domain, null MX 5.1.10)
                         POLICY  5.7.x (authentication, spam, policy)
                         SOFT    4.x.x (mailbox full, deferred, try later)
                         UNKNOWN anything else (including 5.x codes outside 5.1 / 5.7) - a person looks at it
    status               the enhanced status code (e.g. "5.1.1") when one was found
    smtp_code            the 3-digit SMTP reply code when one was found
    recipient            the failed recipient address
    original_message_id  the Message-ID of the message that bounced (from the attached message / headers)

The enhanced status code decides when present. Without one (e.g. Yahoo's "554 delivery error: dd This user doesn't
have a yahoo.com account"), the reply text decides with the phrase lists below; no clear phrase = UNKNOWN.
"""

import re
from dataclasses import dataclass
from email import message_from_bytes, message_from_string, policy
from email.message import Message
from typing import Optional, Union

HARD, POLICY, SOFT, UNKNOWN = "HARD", "POLICY", "SOFT", "UNKNOWN"

_STATUS = re.compile(r"(?<![\d.])([245])\.(\d{1,3})\.(\d{1,3})(?![\d.])")
_SMTP_CODE = re.compile(r"(?<![\d.\[])([45]\d\d)(?:[ \-:]|$)", re.MULTILINE)
_ADDRESS = re.compile(r"<?([A-Za-z0-9._%+'\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,63})>?")
_MESSAGE_ID = re.compile(r"^\s*Message-ID:\s*(<[^>\s]+>)", re.IGNORECASE | re.MULTILINE)

_HARD_PHRASES = ("user unknown", "unknown user", "no such user", "no such mailbox", "does not exist",
                 "doesn't exist", "doesn't have a", "does not have a", "recipient not found", "address not found",
                 "mailbox unavailable", "mailbox not found", "invalid recipient", "recipient address rejected: user",
                 "account has been disabled", "mailbox is disabled", "null mx", "nullmx",
                 "does not accept mail", "couldn't be found", "could not be found", "domain not found",
                 "host not found", "nxdomain")
_POLICY_PHRASES = ("spam", "blocked", "blacklist", "blocklist", "policy", "dmarc", "spf", "dkim",
                   "authentication", "unauthenticated", "not authorized", "reputation", "access denied",
                   "content restrictions", "rejected for policy")
_SOFT_PHRASES = ("mailbox full", "over quota", "quota exceeded", "temporarily", "try again later",
                 "temporary failure", "deferred", "delayed", "will retry", "still trying")

_BOUNCE_SENDERS = ("mailer-daemon", "postmaster", "mail delivery subsystem", "mail delivery system")
_BOUNCE_SUBJECTS = ("undeliver", "delivery status notification", "returned mail", "delivery failure",
                    "mail delivery failed", "failure notice", "delivery has failed", "not delivered",
                    "delivery delayed", "warning: message")


@dataclass
class BounceResult:
    is_bounce: bool
    kind: str
    status: Optional[str] = None
    smtp_code: Optional[int] = None
    recipient: Optional[str] = None
    original_message_id: Optional[str] = None
    diagnostic: Optional[str] = None
    action: Optional[str] = None   # RFC 3464 Action: failed / delayed / delivered / relayed / expanded


def classify_status(status: Optional[str]) -> Optional[str]:
    if not status:
        return None
    klass, subject = status.split(".")[:2]
    if klass == "4":
        return SOFT
    if klass == "5" and subject == "1":
        return HARD
    if klass == "5" and subject == "7":
        return POLICY
    if klass == "2":
        return None   # success / delivered report: not a bounce
    return UNKNOWN


def classify_text(text: str, smtp_code: Optional[int]) -> str:
    lowered = (text or "").lower()
    if smtp_code is not None and 400 <= smtp_code < 500:
        return SOFT
    # Policy phrases are checked before "does not exist"-style phrases: "blocked ... user unknown" style mixtures
    # are rare, and a policy block wrongly treated as a hard bounce would suppress a real address.
    if any(p in lowered for p in _POLICY_PHRASES):
        return POLICY
    if any(p in lowered for p in _HARD_PHRASES):
        return HARD
    if any(p in lowered for p in _SOFT_PHRASES):
        return SOFT
    return UNKNOWN


def _parse(raw: Union[bytes, str, Message]) -> Message:
    if isinstance(raw, Message):
        return raw
    if isinstance(raw, bytes):
        return message_from_bytes(raw, policy=policy.compat32)
    return message_from_string(raw, policy=policy.compat32)


def _payload_text(part: Message) -> str:
    payload = part.get_payload(decode=True)
    if payload is None:
        inner = part.get_payload()
        if isinstance(inner, list):
            return "\n".join(_payload_text(p) if isinstance(p, Message) else str(p) for p in inner)
        return str(inner or "")
    charset = part.get_content_charset() or "utf-8"
    try:
        return payload.decode(charset, errors="replace")
    except LookupError:
        return payload.decode("utf-8", errors="replace")


def _status_fields(part: Message) -> list[dict]:
    """message/delivery-status: groups of header-style fields (per-message, then one per recipient)."""
    payload = part.get_payload()
    blocks: list[Message] = payload if isinstance(payload, list) else []
    if not blocks:
        text = _payload_text(part)
        blocks = [message_from_string(chunk.strip() + "\n", policy=policy.compat32)
                  for chunk in re.split(r"\r?\n\s*\r?\n", text) if chunk.strip()]
    return [{k.lower(): " ".join(str(v).split()) for k, v in block.items()} for block in blocks]


def _strip_type(value: Optional[str]) -> Optional[str]:
    """'rfc822; user@example.com' -> 'user@example.com'."""
    if not value:
        return None
    found = _ADDRESS.search(value.split(";", 1)[-1])
    return found.group(1).lower() if found else None


def _original_message_id(message: Message, text: str) -> Optional[str]:
    for part in message.walk():
        ctype = part.get_content_type()
        if ctype == "message/rfc822":
            inner = part.get_payload()
            inner = inner[0] if isinstance(inner, list) and inner else inner
            if isinstance(inner, Message) and inner.get("Message-ID"):
                return str(inner.get("Message-ID")).strip()
        if ctype == "text/rfc822-headers":
            found = _MESSAGE_ID.search(_payload_text(part))
            if found:
                return found.group(1)
    found = _MESSAGE_ID.search(text)
    return found.group(1) if found else None


def looks_like_bounce(message: Message) -> bool:
    if message.get_content_type() == "multipart/report":
        return True
    sender = str(message.get("From", "")).lower()
    subject = str(message.get("Subject", "")).lower()
    return any(s in sender for s in _BOUNCE_SENDERS) or any(s in subject for s in _BOUNCE_SUBJECTS)


def parse_bounce(raw: Union[bytes, str, Message]) -> BounceResult:
    message = _parse(raw)
    texts, status_groups = [], []
    for part in message.walk():
        ctype = part.get_content_type()
        if ctype in ("message/delivery-status", "message/global-delivery-status"):
            status_groups.extend(_status_fields(part))
        elif ctype in ("text/plain", "text/html") and not part.is_multipart():
            texts.append(_payload_text(part))
    full_text = "\n".join(texts)
    # Only the report itself is classified: the copy of OUR message that bounces often carry must never decide.
    text = _report_text(full_text)
    if not looks_like_bounce(message) and not status_groups:
        return BounceResult(is_bounce=False, kind=UNKNOWN)

    status = diagnostic = recipient = action = None
    for group in status_groups:   # the first recipient group that carries a status wins
        if "status" in group or "final-recipient" in group or "original-recipient" in group:
            found = _STATUS.search(group.get("status", ""))
            if found and status is None:
                status = found.group(0)
                diagnostic = group.get("diagnostic-code")
                action = (group.get("action") or "").lower() or None
                recipient = _strip_type(group.get("final-recipient")) or _strip_type(group.get("original-recipient"))
    if recipient is None:
        recipient = _strip_type(message.get("X-Failed-Recipients"))
    if recipient is None:
        recipient = _recipient_from_text(text)

    search_text = " ".join(filter(None, [diagnostic, text]))
    if status is None:
        found = _STATUS.search(search_text)
        status = found.group(0) if found else None
    code_match = _SMTP_CODE.search(diagnostic or "") or _SMTP_CODE.search(text)
    smtp_code = int(code_match.group(1)) if code_match else None

    if action == "delayed":
        kind = SOFT
    else:
        kind = classify_status(status) or (classify_text(search_text, smtp_code) if status is None else UNKNOWN)
        if status and status.startswith("2."):
            kind = UNKNOWN
    return BounceResult(is_bounce=True, kind=kind, status=status, smtp_code=smtp_code, recipient=recipient,
                        original_message_id=_original_message_id(message, full_text),
                        diagnostic=(diagnostic or _first_error_line(text)), action=action)


_COPY_MARKERS = re.compile(r"^\s*(?:-{2,}\s*(?:Below this line|This is a copy|Original message)|"
                           r"Received:|Return-path:|Message-ID:)", re.IGNORECASE | re.MULTILINE)


def _report_text(text: str) -> str:
    found = _COPY_MARKERS.search(text)
    return text[:found.start()] if found else text


_RECIPIENT_HINTS = (
    re.compile(r"following address(?:\(es\))? failed:\s*\n\s*<?([^\s<>]+@[^\s<>]+?)>?\s*$", re.I | re.M),
    re.compile(r"fatal errors\s*-*\s*\n\s*<?([^\s<>]+@[^\s<>]+?)>?\s*$", re.I | re.M),
    re.compile(r"following recipient(?:\(s\))?[^:\n]*:\s*\n\s*<?([^\s<>]+@[^\s<>]+?)>?\s*$", re.I | re.M),
    re.compile(r"following address[^:\n]*:\s*\n\s*<?([^\s<>]+@[^\s<>:]+?)>?:?\s*$", re.I | re.M),
    re.compile(r"(?:message|mail) to\s+<?([^\s<>]+@[^\s<>]+?)>?\s+(?:could not|cannot|couldn't|was not|has not)", re.I),
    re.compile(r"^\s*<([^\s<>]+@[^\s<>]+)>:\s*$", re.M),
)


def _recipient_from_text(text: str) -> Optional[str]:
    for pattern in _RECIPIENT_HINTS:
        found = pattern.search(text)
        if found:
            address = _ADDRESS.search(found.group(1))
            if address:
                return address.group(1).lower()
    return None


def _first_error_line(text: str) -> Optional[str]:
    for line in text.splitlines():
        if _STATUS.search(line) or _SMTP_CODE.search(line.strip()):
            return line.strip()[:500]
    return None
