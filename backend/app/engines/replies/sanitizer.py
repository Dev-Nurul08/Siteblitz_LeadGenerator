"""
Sanitizer for thread text that goes to the model (spec row 14; RESULT row 19: "a real sanitizer for emails/phones in
thread text"). It removes email addresses (incl. UPI handles and "name at domain dot com"), phone numbers (Indian
mobiles and landlines in any common spacing, international numbers) and links (http(s), www., bare domains with a
common ending). The founder still sees the original text; only the model's copy is cleaned.

The writer's own check (backend/app/engines/writer/writer.py model_payload / model_task) still runs afterwards and
refuses a request that looks like it carries an address or a number, so the two guards overlap on purpose.
"""

import re

EMAIL_TOKEN = "(email removed)"
PHONE_TOKEN = "(phone removed)"
LINK_TOKEN = "(link removed)"

_EMAIL = re.compile(r"[\w.+'-]+@[\w-]+(?:\.[\w-]+)+", re.UNICODE)
_UPI = re.compile(r"\b[\w.-]{2,}@[a-z]{2,}\b", re.IGNORECASE)                 # name@okicici (no dot after @)
# "owner at gmail dot com", "owner [at] gmail [dot] com": "at" / "dot" must stand alone (not inside "chat").
_SEP_OPEN, _SEP_CLOSE = r"(?:\s+|\s*[\[(]\s*)", r"(?:\s+|\s*[\])]\s*)"
_SPELLED_EMAIL = re.compile(r"\b[\w.+-]+" + _SEP_OPEN + r"(?:at|AT)" + _SEP_CLOSE + r"[\w-]+" + _SEP_OPEN
                            + r"(?:dot|DOT)" + _SEP_CLOSE + r"[a-z]{2,}\b")
_URL = re.compile(r"(?:https?://|www\.)[^\s<>()\"']+", re.IGNORECASE)
_TLDS = ("com", "in", "net", "org", "co", "io", "biz", "info", "shop", "store", "online", "site", "website",
         "app", "dev", "me", "us", "uk", "xyz", "club", "live", "page", "link", "ly", "gl", "to")
_BARE_DOMAIN = re.compile(r"\b(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+(?:" + "|".join(_TLDS) + r")\b(?:/[^\s]*)?",
                          re.IGNORECASE)
# A run of digits with spaces, dots, dashes or brackets in between, optionally starting with + : at least 8 digits.
_PHONE = re.compile(r"(?<![\w₹])\+?\(?\d(?:[\s().-]{0,3}\d){7,15}(?![\w])")


_DATE_OR_TIME = re.compile(r"\d{1,2}[-./]\d{1,2}[-./]\d{2,4}|\d{1,2}[.:]\d{2}\s*-\s*\d{1,2}[.:]\d{2}")


def _is_phone(value: str) -> bool:
    """10+ digits is a number; 8-9 digits too, unless it is written like a date (17-11-2026) or a time range."""
    digits = re.sub(r"\D", "", value)
    if len(digits) >= 10:
        return True
    return len(digits) >= 8 and not _DATE_OR_TIME.fullmatch(value.strip())


def _phone(match: re.Match) -> str:
    return PHONE_TOKEN if _is_phone(match.group()) else match.group()


def sanitize(text: str) -> str:
    """Email addresses, phone numbers and links removed. Order matters: URLs and emails before bare domains."""
    if not text:
        return ""
    out = _URL.sub(LINK_TOKEN, text)
    out = _EMAIL.sub(EMAIL_TOKEN, out)
    out = _SPELLED_EMAIL.sub(EMAIL_TOKEN, out)
    out = _UPI.sub(EMAIL_TOKEN, out)
    out = _BARE_DOMAIN.sub(LINK_TOKEN, out)
    out = _PHONE.sub(_phone, out)
    return out


def leftovers(text: str) -> list[str]:
    """What still looks like an address, a number or a link after sanitizing (should be empty)."""
    found = []
    for pattern in (_URL, _EMAIL, _UPI, _BARE_DOMAIN):
        found += [m.group() for m in pattern.finditer(text or "")]
    found += [m.group() for m in _PHONE.finditer(text or "") if _is_phone(m.group())]
    return found
