"""
Email engine v2, phase E1 - verifier ladder (spec row 3: only a VALID address may be emailed).

Ladder, cheapest first:
  1. SyntaxMxVerifier  address syntax + DNS MX lookup (free). Null MX (RFC 7505) or no MX and no A/AAAA = INVALID.
                       A pass is stored as UNVERIFIED with `mx_ok: true`: an MX record does not prove a mailbox.
  2. BouncerVerifier   Bouncer real-time API (paid, $8 per 1,000 in spec row 20), only when BOUNCER_API_KEY is set.
                       Docs read 2026-11-12: GET https://api.usebouncer.com/v1.1/email/verify?email=..&timeout=..,
                       header `x-api-key`; `status` deliverable | risky | undeliverable | unknown; `domain.acceptAll`
                       yes | no | unknown; 402 = no credits, 429 = rate limit (1,000 / minute by default).
Without a key the address stays UNVERIFIED (HOLD NOT_VERIFIED) - the app never pretends.
A verifier that could not answer (network error, HTTP error, DNS timeout) returns `status=None`; nothing is cached,
so the next run asks again. Results are cached by EligibilityService and re-checked after 30 days.
"""

import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Awaitable, Callable, Optional

import httpx

from backend.app.models.eligibility import VerificationStatus

EMAIL_SYNTAX = re.compile(r"[a-z0-9][a-z0-9._%+-]{0,63}@[a-z0-9-]+(?:\.[a-z0-9-]+)*\.[a-z]{2,24}")
BOUNCER_ENDPOINT = "https://api.usebouncer.com/v1.1/email/verify"
BOUNCER_TIMEOUT_SECONDS = 10      # Bouncer's own default for `timeout` (maximum 30)
DNS_TIMEOUT_SECONDS = 8.0


@dataclass
class VerifierResult:
    provider: str
    status: Optional[VerificationStatus]   # None = no answer; never cached
    detail: dict = field(default_factory=dict)


class EmailVerifier(ABC):
    """One rung of the ladder."""

    provider: str = ""

    @abstractmethod
    async def verify(self, email: str) -> VerifierResult:
        ...


# ─── 1. syntax + MX ──────────────────────────────────────────────────────────


@dataclass
class MxAnswer:
    mx_hosts: list = field(default_factory=list)
    null_mx: bool = False
    has_address: bool = False           # A / AAAA record (RFC 5321 implicit MX) when there is no MX
    domain_exists: bool = True
    error: Optional[str] = None         # timeout / no nameserver answer: unknown, not INVALID


async def dns_mx_lookup(domain: str) -> MxAnswer:
    """MX lookup with dnspython (pure Python). Network: DNS only."""
    import dns.asyncresolver
    import dns.exception
    import dns.resolver

    resolver = dns.asyncresolver.Resolver()
    resolver.lifetime = DNS_TIMEOUT_SECONDS
    try:
        answer = await resolver.resolve(domain, "MX")
        records = [(r.preference, str(r.exchange).rstrip(".").lower()) for r in answer]
        null = len(records) == 1 and records[0][1] in ("", ".")
        return MxAnswer(mx_hosts=[host for _, host in sorted(records) if host], null_mx=null)
    except dns.resolver.NXDOMAIN:
        return MxAnswer(domain_exists=False)
    except dns.resolver.NoAnswer:
        pass
    except (dns.exception.Timeout, dns.resolver.NoNameservers) as exc:
        return MxAnswer(error=type(exc).__name__)
    except Exception as exc:   # malformed names and other resolver errors
        return MxAnswer(error=f"{type(exc).__name__}: {str(exc)[:120]}")
    for rtype in ("A", "AAAA"):
        try:
            await resolver.resolve(domain, rtype)
            return MxAnswer(has_address=True)
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
            continue
        except Exception as exc:
            return MxAnswer(error=f"{type(exc).__name__}")
    return MxAnswer()


class SyntaxMxVerifier(EmailVerifier):
    provider = "syntax_mx"

    def __init__(self, lookup: Callable[[str], Awaitable[MxAnswer]] = dns_mx_lookup):
        self.lookup = lookup

    async def verify(self, email: str) -> VerifierResult:
        email = (email or "").strip().lower()
        if not EMAIL_SYNTAX.fullmatch(email):
            return VerifierResult(self.provider, VerificationStatus.INVALID, {"mx_ok": False, "note": "syntax"})
        domain = email.rsplit("@", 1)[1]
        answer = await self.lookup(domain)
        if answer.error:
            return VerifierResult(self.provider, None, {"error": answer.error})
        if not answer.domain_exists:
            return VerifierResult(self.provider, VerificationStatus.INVALID,
                                  {"mx_ok": False, "note": "domain does not exist (NXDOMAIN)"})
        if answer.null_mx:
            return VerifierResult(self.provider, VerificationStatus.INVALID,
                                  {"mx_ok": False, "note": "null MX (RFC 7505): the domain accepts no mail"})
        if answer.mx_hosts:
            return VerifierResult(self.provider, VerificationStatus.UNVERIFIED,
                                  {"mx_ok": True, "mx_hosts": answer.mx_hosts[:5]})
        if answer.has_address:
            return VerifierResult(self.provider, VerificationStatus.UNVERIFIED,
                                  {"mx_ok": True, "note": "no MX, A/AAAA record (implicit MX, RFC 5321)"})
        return VerifierResult(self.provider, VerificationStatus.INVALID,
                              {"mx_ok": False, "note": "no MX and no A/AAAA record"})


# ─── 2. Bouncer ──────────────────────────────────────────────────────────────


def map_bouncer(data: dict) -> VerificationStatus:
    """Bouncer `status` (+ `domain.acceptAll`) -> our status. An unexpected value is UNKNOWN, never VALID."""
    status = str(data.get("status") or "").lower()
    accept_all = str((data.get("domain") or {}).get("acceptAll") or "").lower() == "yes"
    if status == "deliverable":
        return VerificationStatus.CATCH_ALL if accept_all else VerificationStatus.VALID
    if status == "risky":
        return VerificationStatus.CATCH_ALL if accept_all else VerificationStatus.RISKY
    if status == "undeliverable":
        return VerificationStatus.INVALID
    return VerificationStatus.UNKNOWN


class BouncerVerifier(EmailVerifier):
    provider = "bouncer"

    def __init__(self, api_key: str, transport: Optional[httpx.AsyncBaseTransport] = None,
                 endpoint: str = BOUNCER_ENDPOINT):
        if not api_key:
            raise ValueError("BouncerVerifier needs an API key")
        self.api_key = api_key
        self.transport = transport   # tests pass httpx.MockTransport; production uses the network
        self.endpoint = endpoint

    async def verify(self, email: str) -> VerifierResult:
        try:
            async with httpx.AsyncClient(timeout=BOUNCER_TIMEOUT_SECONDS + 20, transport=self.transport) as client:
                response = await client.get(self.endpoint,
                                            params={"email": email, "timeout": BOUNCER_TIMEOUT_SECONDS},
                                            headers={"x-api-key": self.api_key})
        except httpx.HTTPError as exc:
            return VerifierResult(self.provider, None, {"error": f"{type(exc).__name__}"})
        if response.status_code != 200:
            # 401 bad key, 402 no credits, 429 rate limit, 5xx: no answer about the address
            return VerifierResult(self.provider, None, {"error": f"HTTP {response.status_code}"})
        try:
            data = response.json()
        except ValueError:
            return VerifierResult(self.provider, None, {"error": "response is not JSON"})
        domain = data.get("domain") or {}
        account = data.get("account") or {}
        detail = {"status": data.get("status"), "reason": data.get("reason"),
                  "accept_all": domain.get("acceptAll"), "disposable": domain.get("disposable"),
                  "free": domain.get("free"), "role": account.get("role"), "score": data.get("score")}
        if data.get("retryAfter"):
            detail["retry_after"] = data.get("retryAfter")
        return VerifierResult(self.provider, map_bouncer(data), detail)


@dataclass
class VerificationLadder:
    syntax_mx: EmailVerifier
    paid: Optional[EmailVerifier] = None

    @classmethod
    def from_settings(cls, settings) -> "VerificationLadder":
        key = getattr(settings, "BOUNCER_API_KEY", None)
        return cls(SyntaxMxVerifier(), BouncerVerifier(key) if key else None)
