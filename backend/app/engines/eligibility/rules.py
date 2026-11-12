"""
Email engine v2, phase E1 - who may receive an email (spec: docs/spec/email-engine-v2.md rows 2-4).

Pure functions, no I/O: `EligibilityService` loads the facts, these rules decide, the service stores the result.

One decision per (business, address):
  country     India only, anything else HOLD COUNTRY_NOT_IN_PILOT (spec row 2)
  provenance  Tier 1 = read on the business's own website (host match) with source URL + capture date + excerpt,
              or a founder confirmation of a profile the business controls. Listing-only = Tier 2 = HOLD
              (spec row 3, RESULT row 9). Free-mail and own-domain addresses are treated alike.
  recipient   a personal-name local part at a company domain = employee_like = HOLD (RESULT row 10)
  chains      Overture brand set, or the same site / address on 3+ businesses = HOLD CHAIN_OR_DIRECTORY;
              one recipient per business (spec row 3)
  observation exactly one of SOCIAL_ONLY (founder-checked Instagram bio), SITE_DOWN (2 failed homepage checks
              >= 6 h apart; a block / challenge page is never "down"), NO_VIEWPORT (only after a rendered 390 px
              phone check opened zoomed-out); checks older than 30 days do not count (spec row 4)
  verifier    only VALID passes; UNVERIFIED / RISKY / CATCH_ALL / UNKNOWN / INVALID = HOLD (spec row 3)
  suppression opt-out on the address or domain, or a do-not-contact log entry = HOLD
"""

import hashlib
import re
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Iterable, Optional
from urllib.parse import urlparse

from backend.app.engines.discovery.overture import social_platform
from backend.app.engines.intelligence.checks import is_listing
from backend.app.engines.intelligence.rules import FRESH_DAYS, SITE_DOWN_GAP_HOURS, Check
from backend.app.models.eligibility import (
    PILOT_COUNTRIES,
    CaptureMethod,
    EligibilityTier,
    HoldReason,
    ObservationType,
    RecipientType,
    VerificationStatus,
)
from backend.app.models.intelligence import CheckType

IST = timezone(timedelta(hours=5, minutes=30))   # observation dates are written in the recipient's time (India)
VERIFICATION_MAX_AGE_DAYS = 30                    # E1 brief: re-verify after 30 days
CHAIN_MIN_BUSINESSES = 3                          # E1 brief: a host shared by 3+ businesses is a chain / directory

# The same list the phase-14 email finder used (scripts/email_finder.py).
FREE_MAIL = {"gmail.com", "yahoo.com", "yahoo.co.in", "yahoo.in", "hotmail.com", "outlook.com", "live.com",
             "rediffmail.com", "icloud.com", "ymail.com", "msn.com", "aol.com", "proton.me", "protonmail.com"}
# Hosts where many unrelated sites live under one host name; the first path parts identify the site.
SHARED_PLATFORM_HOSTS = {"sites.google.com": 2}
# Local parts that name a function, not a person (an owner's role inbox counts as the business).
ROLE_WORDS = {
    "info", "contact", "contactus", "hello", "hi", "hey", "enquiry", "enquiries", "inquiry", "inquiries", "sales",
    "admin", "office", "support", "help", "care", "customercare", "service", "services", "booking", "bookings",
    "appointment", "appointments", "reservation", "reservations", "mail", "email", "team", "accounts", "account",
    "billing", "orders", "order", "shop", "store", "studio", "admissions", "admission", "academy", "classes",
    "institute", "reception", "frontdesk", "feedback", "query", "queries", "connect", "business", "director",
    "principal", "manager", "owner", "proprietor", "ceo", "founder", "management", "marketing", "hr", "careers",
    "jobs", "general", "official", "online", "export", "exports", "purchase", "helpdesk",
}
ROLE_PREFIXES = ("info", "contact", "enquir", "inquir", "sales", "admin", "office", "support", "booking", "hello")
# Parts that name a place or a unit, not a person: `surat.branch@` is a business inbox, not "first.last".
NON_PERSON_WORDS = {
    "surat", "navsari", "ahmedabad", "amdavad", "vadodara", "baroda", "rajkot", "bharuch", "valsad", "anand",
    "gandhinagar", "bhavnagar", "jamnagar", "gujarat", "india", "branch", "head", "main", "corporate", "group",
    "unit", "centre", "center", "showroom", "outlet", "factory", "works", "ho", "hq",
}
# Mailboxes that are not for a sales message (no reader, or a legal / privacy channel).
SYSTEM_LOCAL_PARTS = {
    "noreply", "donotreply", "mailerdaemon", "postmaster", "hostmaster", "webmaster", "abuse", "bounce",
    "bounces", "privacy", "legal", "grievance", "grievances", "compliance", "dpo", "unsubscribe", "dmca",
}
VERIFICATION_HOLDS = {
    VerificationStatus.UNVERIFIED: HoldReason.NOT_VERIFIED,
    VerificationStatus.RISKY: HoldReason.VERIFIER_RISKY,
    VerificationStatus.CATCH_ALL: HoldReason.VERIFIER_CATCH_ALL,
    VerificationStatus.UNKNOWN: HoldReason.VERIFIER_UNKNOWN,
    VerificationStatus.INVALID: HoldReason.VERIFIER_INVALID,
}
VERIFIER_HOLD_CODES = set(VERIFICATION_HOLDS.values())
# Homepage check outcomes: the site answered (exists) or did not load. Others (blocked by the SSRF guard,
# redirect to a social profile / listing, check error) say nothing about "down".
SITE_EXISTS = {"ok", "protected", "robots_blocked"}
SITE_FAILED = {"failed"}


# ─── small helpers ───────────────────────────────────────────────────────────


def email_hash(email: str) -> str:
    """The shared hash of docs/spec/email-engine-v2-contracts.md: sha256_hex(email.strip().lower())."""
    return hashlib.sha256(email.strip().lower().encode("utf-8")).hexdigest()


def aware(moment: datetime) -> datetime:
    return moment if moment.tzinfo else moment.replace(tzinfo=timezone.utc)


def bare_host(url: Optional[str]) -> str:
    if not url:
        return ""
    host = (urlparse(url if "://" in url else f"https://{url}").hostname or "").lower()
    return host[4:] if host.startswith("www.") else host


def site_key(url: Optional[str]) -> Optional[str]:
    """What identifies one website: the host (no www.), plus the first path parts on shared platforms."""
    host = bare_host(url)
    if not host:
        return None
    depth = SHARED_PLATFORM_HOSTS.get(host)
    if depth:
        parts = [p for p in urlparse(url if "://" in url else f"https://{url}").path.split("/") if p][:depth]
        return "/".join([host, *[p.lower() for p in parts]])
    return host


def is_own_website(url: Optional[str]) -> bool:
    return bool(bare_host(url)) and not social_platform(url) and not is_listing(url)


def date_text(moment: datetime) -> str:
    """'12 November 2026' in India time - unambiguous for the reader (11/12 is read both ways)."""
    local = aware(moment).astimezone(IST)
    return f"{local.day} {local:%B %Y}"


# The category mapping the phase-14 email finder used to select the three demo verticals (scripts/email_finder.py).
VERTICAL_PATTERNS = (
    ("salon_beauty", re.compile(r"salon|beauty|spa|nail|barber|hair")),
    ("coaching_tuition", re.compile(r"tutor|coach|education|school|training|college")),
    ("retail_showroom", re.compile(r"store|shop|retail|showroom|boutique")),
)


def vertical_for(category_text: Optional[str]) -> Optional[str]:
    text = (category_text or "").lower()
    return next((name for name, pattern in VERTICAL_PATTERNS if pattern.search(text)), None)


def _tokens(text: str) -> list[str]:
    return [t for t in re.split(r"[^a-z0-9]+", (text or "").lower()) if t]


# ─── inputs and outputs ──────────────────────────────────────────────────────


@dataclass
class Capture:
    id: Optional[int]
    email: str
    method: CaptureMethod
    source_url: Optional[str] = None
    excerpt: Optional[str] = None
    captured_at: Optional[datetime] = None
    origin: str = ""


@dataclass
class Confirmation:
    id: Optional[int]
    profile_url: str
    checked_at: datetime
    website_link_present: bool
    email_seen: Optional[str] = None


@dataclass
class VerificationRecord:
    provider: str   # syntax_mx | bouncer
    status: VerificationStatus
    checked_at: datetime
    detail: dict = field(default_factory=dict)


@dataclass
class BusinessFacts:
    id: int
    name: str
    country: Optional[str]
    website_url: Optional[str]
    social_urls: dict = field(default_factory=dict)
    brand: Optional[str] = None            # Overture brand name / wikidata id
    skip_reason: Optional[str] = None      # website-intelligence rule 9, not counting brands
    site_share_count: int = 1              # businesses in the database with the same site_key
    suppressed: bool = False               # do-not-contact log entry for the business
    vertical: Optional[str] = None


@dataclass
class Observation:
    type: ObservationType
    text: str
    checked_at: datetime
    evidence_path: Optional[str] = None
    domain: Optional[str] = None


@dataclass
class ObservationResult:
    observation: Optional[Observation] = None
    holds: list = field(default_factory=list)


@dataclass
class Decision:
    business_id: int
    email: str
    tier: EligibilityTier
    capture: Optional[Capture]
    recipient_type: RecipientType
    verification_status: VerificationStatus
    verification_provider: Optional[str]
    verified_at: Optional[datetime]
    observation: Optional[Observation]
    suppressed: bool
    holds: list = field(default_factory=list)

    @property
    def eligible(self) -> bool:
        return not self.holds

    @property
    def eligible_if_verified(self) -> bool:
        """Would be eligible once a verifier says VALID: nothing but NOT_VERIFIED stands in the way."""
        return set(self.holds) <= {HoldReason.NOT_VERIFIED}

    def add(self, *reasons: HoldReason) -> None:
        for reason in reasons:
            if reason not in self.holds:
                self.holds.append(reason)


# ─── recipient ───────────────────────────────────────────────────────────────


def is_system_address(email: str) -> bool:
    local = email.split("@", 1)[0].lower()
    compact = re.sub(r"[^a-z]", "", local)
    return compact in SYSTEM_LOCAL_PARTS or compact.startswith(("noreply", "donotreply"))


def recipient_type(email: str, business_name: str, site_hosts: Iterable[str]) -> RecipientType:
    """
    business       role inbox (info@, sales@, owner@ ...), a place / unit word (surat.branch@), or a local part
                   that names the business / its domain
    employee_like  at a company (non-free-mail) domain: two or more name-like parts (first.last, r.patel)
    unknown        anything else, e.g. a free-mail address that does not name the business. Not a HOLD by itself;
                   the founder's provenance audit (spec row 17 f) looks at these.
    """
    local, _, domain = email.lower().partition("@")
    parts = [p for p in re.split(r"[._+\-]+", local) if p]
    letters = [re.sub(r"\d+", "", p) for p in parts]
    if any(p in ROLE_WORDS or p in NON_PERSON_WORDS for p in letters if p) or local.startswith(ROLE_PREFIXES):
        return RecipientType.BUSINESS
    compact = re.sub(r"[^a-z]", "", local)
    name_tokens = {t for t in _tokens(business_name) if len(t) >= 4}
    labels = {bare_host(h).split(".")[0] for h in site_hosts if bare_host(h)}
    if domain not in FREE_MAIL:
        labels.add(domain.split(".")[0])
    labels = {label for label in labels if len(label) >= 4}
    if compact and (any(t in compact for t in name_tokens | labels)
                    or (len(compact) >= 4 and any(compact in label for label in labels))):
        return RecipientType.BUSINESS
    if domain not in FREE_MAIL and len(parts) >= 2 and all(p.isalpha() for p in parts) \
            and any(len(p) >= 3 for p in parts):
        return RecipientType.EMPLOYEE_LIKE
    return RecipientType.UNKNOWN


# ─── provenance ──────────────────────────────────────────────────────────────


def own_hosts(website_url: Optional[str], checks: list[Check]) -> set[str]:
    """The business's own hosts: its listed website plus where that homepage redirected to."""
    hosts = {bare_host(website_url)} if is_own_website(website_url) else set()
    for check in checks:
        if check.type == CheckType.SITE_FETCH and check.outcome in ("ok", "protected"):
            for url in (check.target, (check.detail or {}).get("final_url")):
                if is_own_website(url):
                    hosts.add(bare_host(url))
    hosts.discard("")
    return hosts


def classify_capture(capture: Capture, hosts: set[str]) -> tuple[EligibilityTier, list[HoldReason]]:
    if capture.method == CaptureMethod.LISTING:
        return EligibilityTier.TIER2, [HoldReason.LISTING_ONLY]
    if capture.method == CaptureMethod.FOUNDER_CONFIRMED:
        if capture.source_url and capture.captured_at and capture.excerpt:
            return EligibilityTier.TIER1, []
        return EligibilityTier.HOLD, [HoldReason.PROVENANCE_INCOMPLETE]
    if not capture.source_url:
        return EligibilityTier.HOLD, [HoldReason.PROVENANCE_INCOMPLETE]
    if bare_host(capture.source_url) not in hosts:
        return EligibilityTier.HOLD, [HoldReason.SOURCE_NOT_OWN_SITE]
    if not (capture.captured_at and capture.excerpt):
        return EligibilityTier.HOLD, [HoldReason.PROVENANCE_INCOMPLETE]
    return EligibilityTier.TIER1, []


TIER_RANK = {EligibilityTier.TIER1: 0, EligibilityTier.HOLD: 1, EligibilityTier.TIER2: 2}


def best_capture(captures: list[Capture], hosts: set[str]
                 ) -> tuple[EligibilityTier, Optional[Capture], list[HoldReason]]:
    """The strongest sighting: Tier 1 first, then the most recent."""
    if not captures:
        return EligibilityTier.HOLD, None, [HoldReason.PROVENANCE_INCOMPLETE]
    graded = [(classify_capture(c, hosts), c) for c in captures]
    graded.sort(key=lambda g: (TIER_RANK[g[0][0]],
                               -(aware(g[1].captured_at).timestamp() if g[1].captured_at else 0)))
    (tier, holds), capture = graded[0]
    return tier, capture, holds


# ─── observation ─────────────────────────────────────────────────────────────


def _homepage_checks(checks: list[Check]) -> list[Check]:
    relevant = [c for c in checks if c.type == CheckType.SITE_FETCH and c.outcome in SITE_EXISTS | SITE_FAILED]
    return sorted(relevant, key=lambda c: (aware(c.observed_at), c.id or 0))


def _confirmed_down(run: list[Check]) -> bool:
    """Spec row 6 of website-intelligence: two failures at least 6 h apart."""
    return len(run) >= 2 and aware(run[-1].observed_at) - aware(run[0].observed_at) >= timedelta(
        hours=SITE_DOWN_GAP_HOURS)


def _was_confirmed_down(fetches: list[Check]) -> bool:
    run: list[Check] = []
    for check in fetches:
        if check.outcome in SITE_FAILED:
            run.append(check)
            if _confirmed_down(run):
                return True
        else:
            run = []
    return False


def site_down_text(day: datetime, domain: str) -> str:
    return (f"On {date_text(day)}, the homepage at {domain} did not load in our checks, the last one shortly "
            f"before this email. The interruption may be temporary.")


def no_viewport_text(day: datetime, domain: str) -> str:
    return (f"On {date_text(day)}, the homepage at {domain} opened zoomed-out on a phone screen in our check, "
            f"so the text showed very small.")


def social_only_text(day: datetime, business_name: str) -> str:
    return (f"On {date_text(day)}, the Instagram profile for {business_name} showed no website link when we "
            f"checked its bio.")


def find_observation(facts: BusinessFacts, checks: list[Check], confirmation: Optional[Confirmation],
                     now: datetime) -> ObservationResult:
    """The one pilot observation of a business (priority SITE_DOWN > NO_VIEWPORT > SOCIAL_ONLY), or why none."""
    cutoff = now - timedelta(days=FRESH_DAYS)
    if is_own_website(facts.website_url):
        fetches = _homepage_checks(checks)
        if not fetches:
            return ObservationResult(holds=[HoldReason.NO_PILOT_OBSERVATION])
        latest = fetches[-1]
        if latest.outcome in SITE_FAILED:
            run: list[Check] = []
            for check in reversed(fetches):
                if check.outcome not in SITE_FAILED:
                    break
                run.insert(0, check)
            if not _confirmed_down(run):
                return ObservationResult(holds=[HoldReason.SITE_DOWN_NEEDS_RECHECK])
            last = run[-1]
            if aware(last.observed_at) < cutoff:
                return ObservationResult(holds=[HoldReason.OBSERVATION_STALE])
            domain = bare_host(last.target) or bare_host(facts.website_url)
            return ObservationResult(Observation(ObservationType.SITE_DOWN, site_down_text(last.observed_at, domain),
                                                 aware(last.observed_at), None, domain))
        if latest.outcome == "ok" and (latest.detail or {}).get("has_viewport") is False:
            renders = sorted((c for c in checks if c.type == CheckType.PHONE_RENDER),
                             key=lambda c: (aware(c.observed_at), c.id or 0))
            if not renders or renders[-1].outcome not in ("zoomed_out", "fits"):
                return ObservationResult(holds=[HoldReason.PHONE_CHECK_PENDING])
            render = renders[-1]
            if render.outcome == "zoomed_out":
                if aware(render.observed_at) < cutoff:
                    return ObservationResult(holds=[HoldReason.OBSERVATION_STALE])
                detail = render.detail or {}
                domain = (bare_host(detail.get("final_url")) or bare_host(render.target)
                          or bare_host(facts.website_url))
                return ObservationResult(Observation(
                    ObservationType.NO_VIEWPORT, no_viewport_text(render.observed_at, domain),
                    aware(render.observed_at), detail.get("screenshot"), domain))
            return ObservationResult(holds=[HoldReason.NO_PILOT_OBSERVATION])
        if _was_confirmed_down(fetches[:-1]):
            return ObservationResult(holds=[HoldReason.SITE_RECOVERED])
        return ObservationResult(holds=[HoldReason.NO_PILOT_OBSERVATION])

    profile = (facts.social_urls or {}).get("instagram") or (confirmation.profile_url if confirmation else None)
    if not profile:
        return ObservationResult(holds=[HoldReason.NO_PILOT_OBSERVATION])
    if confirmation is None:
        return ObservationResult(holds=[HoldReason.NEEDS_FOUNDER_CHECK])
    if confirmation.website_link_present:
        return ObservationResult(holds=[HoldReason.NO_PILOT_OBSERVATION])
    if aware(confirmation.checked_at) < cutoff:
        return ObservationResult(holds=[HoldReason.OBSERVATION_STALE])
    return ObservationResult(Observation(ObservationType.SOCIAL_ONLY,
                                         social_only_text(confirmation.checked_at, facts.name),
                                         aware(confirmation.checked_at), None, None))


# ─── verification ────────────────────────────────────────────────────────────


def fresh_record(records: list[VerificationRecord], provider: str, now: datetime
                 ) -> Optional[VerificationRecord]:
    cutoff = now - timedelta(days=VERIFICATION_MAX_AGE_DAYS)
    mine = [r for r in records if r.provider == provider and aware(r.checked_at) >= cutoff]
    return max(mine, key=lambda r: aware(r.checked_at)) if mine else None


def effective_verification(records: list[VerificationRecord], now: datetime
                           ) -> tuple[VerificationStatus, Optional[str], Optional[datetime]]:
    """Fresh (<= 30 days) results only. A failed syntax / MX check wins; then the paid verifier; else UNVERIFIED."""
    syntax = fresh_record(records, "syntax_mx", now)
    if syntax and syntax.status == VerificationStatus.INVALID:
        return VerificationStatus.INVALID, "syntax_mx", aware(syntax.checked_at)
    paid = fresh_record(records, "bouncer", now)
    if paid:
        return paid.status, "bouncer", aware(paid.checked_at)
    return VerificationStatus.UNVERIFIED, None, None


def mx_passed(records: list[VerificationRecord], now: datetime) -> bool:
    syntax = fresh_record(records, "syntax_mx", now)
    return bool(syntax and syntax.status != VerificationStatus.INVALID and (syntax.detail or {}).get("mx_ok"))


def same_domain(email: str, domain: Optional[str]) -> bool:
    mail_domain = email.rsplit("@", 1)[-1].lower()
    domain = (domain or "").lower()
    return bool(domain) and (mail_domain == domain or domain.endswith("." + mail_domain)
                             or mail_domain.endswith("." + domain))


# ─── decision ────────────────────────────────────────────────────────────────


def decide(facts: BusinessFacts, email: str, captures: list[Capture], checks: list[Check],
           observation: ObservationResult, verifications: list[VerificationRecord],
           email_suppressed: bool, now: datetime) -> Decision:
    """Every rule for one (business, address). `observation` = find_observation() for the business."""
    hosts = own_hosts(facts.website_url, checks)
    tier, capture, capture_holds = best_capture(captures, hosts)
    rtype = recipient_type(email, facts.name, hosts)
    status, provider, verified_at = effective_verification(verifications, now)
    suppressed = facts.suppressed or email_suppressed
    decision = Decision(facts.id, email, tier, capture, rtype, status, provider, verified_at,
                        observation.observation, suppressed)

    if (facts.country or "").upper() not in PILOT_COUNTRIES:
        decision.add(HoldReason.COUNTRY_NOT_IN_PILOT)
    if facts.skip_reason:
        decision.add(HoldReason.NOT_A_PROSPECT)
    if facts.brand or facts.site_share_count >= CHAIN_MIN_BUSINESSES:
        decision.add(HoldReason.CHAIN_OR_DIRECTORY)
    decision.add(*capture_holds)
    if rtype == RecipientType.EMPLOYEE_LIKE:
        decision.add(HoldReason.EMPLOYEE_LIKE_ADDRESS)
    if is_system_address(email):
        decision.add(HoldReason.SYSTEM_ADDRESS)
    if suppressed:
        decision.add(HoldReason.SUPPRESSED)
    decision.add(*observation.holds)
    found = observation.observation
    if found and found.type == ObservationType.SITE_DOWN and same_domain(email, found.domain) \
            and not mx_passed(verifications, now):
        decision.add(HoldReason.MAILBOX_DOMAIN_DOWN)
    if status != VerificationStatus.VALID:
        decision.add(VERIFICATION_HOLDS[status])
    return decision


VERIFICATION_RANK = {VerificationStatus.VALID: 0, VerificationStatus.UNVERIFIED: 1, VerificationStatus.UNKNOWN: 2,
                     VerificationStatus.CATCH_ALL: 3, VerificationStatus.RISKY: 4, VerificationStatus.INVALID: 5}
RECIPIENT_RANK = {RecipientType.BUSINESS: 0, RecipientType.UNKNOWN: 1, RecipientType.EMPLOYEE_LIKE: 2}


def _rank(decision: Decision) -> tuple:
    # A DUPLICATE_RECIPIENT from step 1 counts against an address in step 2. Verifier holds are not counted
    # as blocking; the verifier result is compared on its own (VALID first) right after.
    blocking = [h for h in decision.holds
                if h not in VERIFIER_HOLD_CODES and h != HoldReason.NOT_PRIMARY_RECIPIENT]
    return (len(blocking), VERIFICATION_RANK[decision.verification_status],
            RECIPIENT_RANK[decision.recipient_type], decision.business_id, decision.email)


def dedupe(decisions: list[Decision]) -> list[Decision]:
    """
    Spec row 3, "one recipient per business (branches and franchises deduplicated)":
    1. the same address on 3+ businesses = a chain / head-office address: HOLD CHAIN_OR_DIRECTORY for all;
       on 2 businesses: the better-placed one keeps it, the other is HOLD DUPLICATE_RECIPIENT;
    2. a business with several addresses keeps its best one; the others are HOLD NOT_PRIMARY_RECIPIENT.
    "Better" = fewer blocking holds, then VALID first, then a business inbox, then the lower business id.
    """
    by_email: dict[str, list[Decision]] = {}
    for d in decisions:
        by_email.setdefault(d.email, []).append(d)
    for group in by_email.values():
        owners = {d.business_id for d in group}
        if len(owners) >= CHAIN_MIN_BUSINESSES:
            for d in group:
                d.add(HoldReason.CHAIN_OR_DIRECTORY)
        elif len(owners) == 2:
            for d in sorted(group, key=_rank)[1:]:
                d.add(HoldReason.DUPLICATE_RECIPIENT)
    by_business: dict[int, list[Decision]] = {}
    for d in decisions:
        by_business.setdefault(d.business_id, []).append(d)
    for group in by_business.values():
        for d in sorted(group, key=_rank)[1:]:
            d.add(HoldReason.NOT_PRIMARY_RECIPIENT)
    return decisions
