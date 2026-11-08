"""
Validated and sanitized input types shared by every API request model.

Every limit below comes from something already written down — the database column sizes in
`backend/app/models/*` or rules already in the code (ISO 3166-1 alpha-2 in the normalizer, the
email regex in the verifier). Request models use these types; response models do not, so old
rows that break a rule can still be read and fixed.

Sanitizing = remove ASCII control characters (except tab/newline), trim spaces, turn "" into None
for optional fields. Validation failures return HTTP 422 with the field name, never HTTP 500.
"""

import re
from typing import Annotated, Optional
from urllib.parse import urlparse

from pydantic import AfterValidator, BeforeValidator, StringConstraints

from backend.app.engines.enrichment.verifier import EMAIL_REGEX

_CONTROL_CHARS = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")
_PHONE = re.compile(r"^[0-9+()\-.\s/x]{3,50}$", re.IGNORECASE)
_DOMAIN = re.compile(r"^(?=.{3,255}$)([a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,63}$")


def _clean(value):
    """Strip control characters and surrounding whitespace from text input."""
    if value is None or not isinstance(value, str):
        return value
    return _CONTROL_CHARS.sub("", value).strip()


def _clean_optional(value):
    value = _clean(value)
    return None if value == "" else value


def _upper(value):
    return value.upper() if isinstance(value, str) else value


def _lower(value):
    return value.lower() if isinstance(value, str) else value


_OTHER_SCHEME = re.compile(r"^[a-z][a-z0-9+.-]*:(?!\d)", re.IGNORECASE)


def _http_url(value: str) -> str:
    """Only absolute http(s) URLs: blocks `javascript:` / `data:` links that the UI would render."""
    if "://" not in value and _OTHER_SCHEME.match(value):
        raise ValueError("must be an http(s) web address")  # javascript:, data:, mailto: …
    parsed = urlparse(value if "://" in value else f"https://{value}")
    if parsed.scheme not in ("http", "https") or not parsed.hostname or "." not in parsed.hostname:
        raise ValueError("must be an http(s) web address")
    return parsed.geturl()


def _email(value: str) -> str:
    if not EMAIL_REGEX.match(value):
        raise ValueError("must be a valid email address")
    return value


def _phone(value: str) -> str:
    if not _PHONE.match(value):
        raise ValueError("may contain only digits, spaces and + - ( ) . / x")
    return value


def _domain(value: str) -> str:
    if not _DOMAIN.match(value):
        raise ValueError("must be a domain like example.com")
    return value


def Text(max_length: Optional[int], min_length: int = 0):  # noqa: N802 — reads like a type
    """Required free text, sanitized; max_length = the DB column size (None for Text columns)."""
    return Annotated[str, BeforeValidator(_clean),
                     StringConstraints(min_length=min_length, max_length=max_length)]


def Opt(inner):  # noqa: N802
    """Optional version of a type: blank / whitespace-only input becomes None before validation."""
    return Annotated[Optional[inner], BeforeValidator(_clean_optional)]


def OptionalText(max_length: Optional[int] = None):  # noqa: N802
    """Optional free text; blank becomes None. max_length=None for unbounded DB Text columns."""
    return Opt(Annotated[str, BeforeValidator(_clean), StringConstraints(max_length=max_length)])


# ISO 3166-1 alpha-2, the same rule as BusinessNormalizer.normalize_country_code.
CountryCode = Annotated[str, BeforeValidator(lambda v: _upper(_clean(v))),
                        StringConstraints(pattern=r"^[A-Z]{2}$")]

# businesses.website_url / sources.license_url etc. are String(1000) / String(500).
HttpUrl = Annotated[str, BeforeValidator(_clean),
                    StringConstraints(max_length=1000), AfterValidator(_http_url)]

# businesses.email is String(320); opt_outs.email is String(255).
Email = Annotated[str, BeforeValidator(lambda v: _lower(_clean(v))),
                  StringConstraints(max_length=320), AfterValidator(_email)]

# businesses.phone / contacts.phone are String(50).
Phone = Annotated[str, BeforeValidator(_clean),
                  StringConstraints(max_length=50), AfterValidator(_phone)]

Domain = Annotated[str, BeforeValidator(lambda v: _lower(_clean(v))),
                   StringConstraints(max_length=255), AfterValidator(_domain)]

# sources.slug is String(100); also used as an adapter lookup key.
Slug = Annotated[str, BeforeValidator(lambda v: _lower(_clean(v))),
                 StringConstraints(pattern=r"^[a-z][a-z0-9_]{1,99}$")]
