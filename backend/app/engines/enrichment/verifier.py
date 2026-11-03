"""
Email Verifier module.

Performs RFC 5322 syntax validation, disposable/burner domain filtering,
role-based inbox detection, and DNS MX record lookup.
"""

from dataclasses import dataclass
import re
from typing import Optional

import dns.resolver
import structlog

from backend.app.models.contact import EmailVerificationStatus

logger = structlog.get_logger(__name__)

# RFC 5322 simplified email syntax regex
EMAIL_REGEX = re.compile(
    r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)+$"
)

# Known temporary / disposable / burner email domains
DISPOSABLE_DOMAINS = {
    "mailinator.com", "guerrillamail.com", "tempmail.com", "10minutemail.com",
    "throwawaymail.com", "sharklasers.com", "yopmail.com", "getairmail.com",
    "dispostable.com", "trashmail.com", "fakemailgenerator.com", "maildrop.cc",
    "inboxkitten.com", "mohmal.com", "crazymailing.com",
}

# Common functional / department role-based handles
ROLE_HANDLES = {
    "info", "contact", "support", "sales", "admin", "help", "hello",
    "office", "enquiries", "inquiries", "billing", "accounts", "legal",
    "jobs", "careers", "press", "media", "team", "general", "marketing",
    "feedback", "orders", "reception", "desk", "privacy", "security",
}


@dataclass
class VerificationResult:
    """Outcome of verifying an email address."""

    email: str
    status: EmailVerificationStatus
    is_valid_syntax: bool
    is_disposable: bool
    is_role_based: bool
    has_valid_mx: bool
    verification_score: float  # 0.0 to 1.0
    domain: str
    mx_records: list[str]
    details: dict


class EmailVerifier:
    """
    Validates email addresses across syntax, domain reputation,
    role classification, and MX deliverability.
    """

    def __init__(self, dns_timeout: float = 4.0):
        self.dns_timeout = dns_timeout
        self.resolver = dns.resolver.Resolver()
        self.resolver.lifetime = dns_timeout

    def verify(self, email: Optional[str]) -> VerificationResult:
        """
        Verify deliverability, syntax, and type of an email address.
        """
        if not email or not isinstance(email, str):
            return self._invalid_result(email or "", "Empty email")

        cleaned = email.strip().lower()
        if not EMAIL_REGEX.match(cleaned):
            return self._invalid_result(cleaned, "Malformed email syntax")

        local_part, domain = cleaned.split("@", 1)

        # 1. Check disposable
        is_disposable = domain in DISPOSABLE_DOMAINS
        if is_disposable:
            return VerificationResult(
                email=cleaned,
                status=EmailVerificationStatus.DISPOSABLE,
                is_valid_syntax=True,
                is_disposable=True,
                is_role_based=False,
                has_valid_mx=False,
                verification_score=0.0,
                domain=domain,
                mx_records=[],
                details={"reason": "Disposable / Burner email provider"},
            )

        # 2. Check role-based handle
        is_role_based = local_part in ROLE_HANDLES

        # 3. Check DNS MX records
        has_valid_mx = False
        mx_hosts = []
        try:
            answers = self.resolver.resolve(domain, "MX")
            mx_hosts = [str(r.exchange).rstrip(".") for r in answers]
            has_valid_mx = len(mx_hosts) > 0
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.resolver.NoNameservers):
            # Try A record fallback
            try:
                a_answers = self.resolver.resolve(domain, "A")
                has_valid_mx = len(a_answers) > 0
                if has_valid_mx:
                    mx_hosts = [domain]
            except Exception:
                has_valid_mx = False
        except Exception as e:
            logger.debug("mx_lookup_failed", domain=domain, error=str(e))
            has_valid_mx = False

        # 4. Compute deliverability confidence score
        if not has_valid_mx:
            status = EmailVerificationStatus.INVALID
            score = 0.1
        elif is_role_based:
            status = EmailVerificationStatus.ROLE_BASED
            score = 0.70  # Valid company inbox, but functional
        else:
            status = EmailVerificationStatus.VERIFIED
            score = 0.95  # Personal corporate mailbox with verified MX

        return VerificationResult(
            email=cleaned,
            status=status,
            is_valid_syntax=True,
            is_disposable=False,
            is_role_based=is_role_based,
            has_valid_mx=has_valid_mx,
            verification_score=score,
            domain=domain,
            mx_records=mx_hosts,
            details={
                "has_mx": has_valid_mx,
                "role_based": is_role_based,
                "mx_count": len(mx_hosts),
            },
        )

    def _invalid_result(self, email: str, reason: str) -> VerificationResult:
        domain = email.split("@", 1)[1] if "@" in email else ""
        return VerificationResult(
            email=email,
            status=EmailVerificationStatus.INVALID,
            is_valid_syntax=False,
            is_disposable=False,
            is_role_based=False,
            has_valid_mx=False,
            verification_score=0.0,
            domain=domain,
            mx_records=[],
            details={"reason": reason},
        )
