"""
Unsubscribe token, exactly as docs/spec/email-engine-v2-contracts.md fixes it (shared with the website):

    hash    = sha256_hex(email.strip().lower())
    payload = compact JSON, sorted keys: {"h": "<hash>", "m": "<send record id>", "v": 1}
    token   = base64url(payload) + "." + base64url(HMAC_SHA256(secret, base64url(payload)))   (no "=" padding)

The secret is the env value with surrounding whitespace removed, as UTF-8 bytes; shorter than 32 characters counts
as missing. The HMAC message is the base64url payload STRING (ASCII), not the raw JSON. The known-answer vector of
the contract is checked in backend/tests/test_sending/test_tokens.py.
"""

import base64
import hashlib
import hmac
import json
from typing import Optional

MIN_SECRET_CHARS = 32
TOKEN_VERSION = 1


class MissingSecret(ValueError):
    """OUTREACH_SIGNING_SECRET is unset or shorter than 32 characters."""


def email_hash(email: str) -> str:
    return hashlib.sha256(email.strip().lower().encode("utf-8")).hexdigest()


def usable_secret(raw: Optional[str]) -> Optional[str]:
    """The contract's secret rule: trimmed; shorter than 32 characters = missing (None)."""
    value = (raw or "").strip()
    return value if len(value) >= MIN_SECRET_CHARS else None


def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode("ascii").rstrip("=")


def _b64url_decode(text: str) -> bytes:
    return base64.urlsafe_b64decode(text + "=" * (-len(text) % 4))


def payload_text(h: str, m: str) -> str:
    return json.dumps({"h": h, "m": m, "v": TOKEN_VERSION}, separators=(",", ":"), sort_keys=True)


def make_token(h: str, m: str, secret: Optional[str]) -> str:
    key = usable_secret(secret)
    if key is None:
        raise MissingSecret("OUTREACH_SIGNING_SECRET is missing or shorter than 32 characters")
    encoded = _b64url(payload_text(h, m).encode("utf-8"))
    signature = hmac.new(key.encode("utf-8"), encoded.encode("ascii"), hashlib.sha256).digest()
    return f"{encoded}.{_b64url(signature)}"


def token_for_email(email: str, send_record_id: str, secret: Optional[str]) -> str:
    return make_token(email_hash(email), str(send_record_id), secret)


def verify_token(token: str, secret: Optional[str]) -> Optional[dict]:
    """The payload when the signature matches (constant-time compare), else None. The website does the real
    verification; this exists for tests and for checking a built message."""
    key = usable_secret(secret)
    if key is None or token.count(".") != 1:
        return None
    encoded, signature = token.split(".")
    expected = _b64url(hmac.new(key.encode("utf-8"), encoded.encode("ascii"), hashlib.sha256).digest())
    if not hmac.compare_digest(expected, signature):
        return None
    try:
        payload = json.loads(_b64url_decode(encoded))
    except (ValueError, UnicodeDecodeError):
        return None
    return payload if isinstance(payload, dict) and payload.get("v") == TOKEN_VERSION else None


def unsubscribe_url(base_url: str, token: str) -> str:
    # No trailing slash: the website answers /u/{token}/ with a 308 (contract, website D19).
    return f"{base_url.rstrip('/')}/u/{token}"
