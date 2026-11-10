"""
Website Intelligence rules — pure functions, no I/O (spec: docs/spec/website-intelligence.md).

Input: stored checks + business facts. Output: verdict, confidence, need score, tier, reasons.
Every number here is a row of the locked spec; the row number is noted next to it.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Optional

from backend.app.models.intelligence import (
    CheckType,
    EvidenceConfidence,
    LeadTier,
    OutreachReadiness,
    WebsiteVerdict,
)

LEAD_VERDICTS = {
    WebsiteVerdict.NO_SITE_VERIFIED,
    WebsiteVerdict.SOCIAL_ONLY_VERIFIED,
    WebsiteVerdict.SITE_DOWN_CONFIRMED,
}

# Spec row 9 — OSM amenity values that are never website prospects.
SKIP_AMENITIES = {
    "atm", "bank", "fuel", "place_of_worship", "townhall", "police", "post_office",
    "school", "university", "college", "hospital", "parking", "toilets",
}
# The same institutions as Overture basic_category fragments (Overture has no amenity tags).
# "school" is not a fragment: a substring match also skipped specialty_school (coaching classes)
# and preschool, which are businesses in the coaching/tuition vertical (QA-038). Schools are
# listed as exact categories below instead.
SKIP_CATEGORY_FRAGMENTS = (
    "atm", "bank", "gas_station", "fuel", "place_of_worship", "temple", "mosque", "church",
    "government", "police", "post_office", "university", "college", "hospital", "parking",
)
SKIP_CATEGORIES_EXACT = {
    "school", "elementary_school", "middle_school", "high_school", "public_school",
    "school_district_office", "education_office",
}

# Spec row 11 — listing sites whose page is not the business's own website.
AGGREGATOR_HOSTS = ("zomato.com", "swiggy.com", "justdial.com", "practo.com")

# Spec row 13 — service fit.
FIT_10 = ("dent", "salon", "hair", "beauty")
FIT_7 = ("clinic", "doctor", "medical", "gym", "fitness", "restaurant", "cafe", "coffee", "hotel",
         "lawyer", "legal", "accountant", "accounting", "estate", "school", "education",
         "coaching", "tutor")

FRESH_DAYS = 30          # spec row 7: checks younger than 30 days
SITE_DOWN_GAP_HOURS = 6  # spec row 6: two failures at least 6 h apart


@dataclass
class Check:
    id: Optional[int]
    type: CheckType
    outcome: str
    target: Optional[str] = None
    detail: dict = field(default_factory=dict)
    observed_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class Facts:
    name: str
    categories: list[str]
    phone: Optional[str]
    email: Optional[str]
    social_platforms: list[str]
    raw_records: list[dict]          # raw source payloads (OSM element / Overture row)
    include_franchises: bool = False
    suppressed: bool = False


@dataclass
class Assessment:
    verdict: WebsiteVerdict
    confidence: EvidenceConfidence
    need_score: Optional[float]
    tier: LeadTier
    readiness: OutreachReadiness
    breakdown: Optional[dict]
    reasons: list[dict]
    summary: str


def _aware(moment: datetime) -> datetime:
    return moment if moment.tzinfo else moment.replace(tzinfo=timezone.utc)


def skip_reason(facts: Facts) -> Optional[str]:
    """Spec row 9. Returns a human sentence when the business must never be a lead."""
    for raw in facts.raw_records:
        tags = raw.get("tags") or {}
        if not facts.include_franchises:
            for key in ("brand", "brand:wikidata", "operator"):
                if tags.get(key):
                    return f"Chain / brand ({key}={tags[key]})"
            if raw.get("brand_wikidata") or raw.get("brand_name"):
                return f"Chain / brand ({raw.get('brand_name') or raw.get('brand_wikidata')})"
        if tags.get("amenity") in SKIP_AMENITIES:
            return f"Not a website prospect (amenity={tags['amenity']})"
        if tags.get("shop") == "vacant":
            return "Closed (shop=vacant)"
        for key in tags:
            if key.startswith(("disused:", "abandoned:", "was:")):
                return f"Closed or moved ({key})"
        category = (raw.get("basic_category") or "").lower()
        if category in SKIP_CATEGORIES_EXACT or any(
                fragment in category for fragment in SKIP_CATEGORY_FRAGMENTS):
            return f"Not a website prospect (category={category})"
    return None


def decide_verdict(checks: list[Check], facts: Facts, now: Optional[datetime] = None
                   ) -> tuple[WebsiteVerdict, EvidenceConfidence, str]:
    """Spec rows 1, 6, 7, 8, 15."""
    now = now or datetime.now(timezone.utc)
    if any(c.type == CheckType.MANUAL_ACTIVITY and c.outcome == "inactive" for c in checks):
        return WebsiteVerdict.SKIP, EvidenceConfidence.HIGH, "You marked it closed / inactive."
    reason = next((c.detail.get("reason") for c in checks
                   if c.type == CheckType.SKIP_RULE and c.outcome == "skip"), None)
    if reason:
        return WebsiteVerdict.SKIP, EvidenceConfidence.HIGH, reason

    if any(c.type == CheckType.MANUAL_SEARCH and c.outcome == "found" for c in checks):
        return WebsiteVerdict.OWN_SITE_VERIFIED, EvidenceConfidence.HIGH, "You found its website."
    if any(c.type == CheckType.DOMAIN_GUESS and c.outcome == "matched" for c in checks):
        return (WebsiteVerdict.OWN_SITE_VERIFIED, EvidenceConfidence.HIGH,
                "A guessed domain opened and named this business.")
    fetches = [c for c in checks if c.type == CheckType.SITE_FETCH]
    if any(c.outcome in ("ok", "protected") for c in fetches):
        return WebsiteVerdict.OWN_SITE_VERIFIED, EvidenceConfidence.HIGH, "Its website opened."

    failures = sorted((_aware(c.observed_at) for c in fetches if c.outcome == "failed"))
    if failures:
        if failures[-1] - failures[0] >= timedelta(hours=SITE_DOWN_GAP_HOURS):
            return (WebsiteVerdict.SITE_DOWN_CONFIRMED, EvidenceConfidence.HIGH,
                    f"Listed website failed {len(failures)} times, ≥ {SITE_DOWN_GAP_HOURS} h apart.")
        return (WebsiteVerdict.UNKNOWN, EvidenceConfidence.LOW,
                f"Listed website failed once; check again after {SITE_DOWN_GAP_HOURS} h.")
    if any(c.outcome in ("blocked", "error") for c in fetches):
        return WebsiteVerdict.UNKNOWN, EvidenceConfidence.LOW, "The website check could not run."

    guesses = [c for c in checks if c.type == CheckType.DOMAIN_GUESS]
    if not guesses or any(c.outcome == "error" for c in guesses):
        return WebsiteVerdict.UNKNOWN, EvidenceConfidence.LOW, "Domain checks did not complete."

    has_social = bool(facts.social_platforms)
    verdict = WebsiteVerdict.SOCIAL_ONLY_VERIFIED if has_social else WebsiteVerdict.NO_SITE_VERIFIED
    cutoff = now - timedelta(days=FRESH_DAYS)
    searched = [c for c in checks if c.type in (CheckType.SEARCH, CheckType.MANUAL_SEARCH)
                and c.outcome == "none" and _aware(c.observed_at) >= cutoff]
    stale = any(_aware(c.observed_at) < cutoff for c in guesses)
    if searched and not stale:
        return verdict, EvidenceConfidence.HIGH, "No independent website after all checks incl. a search."
    return (verdict, EvidenceConfidence.MEDIUM,
            "No website identified — limited verification (no search recorded yet).")


def _gap_points(verdict: WebsiteVerdict, checks: list[Check]) -> tuple[Optional[int], str]:
    """Spec row 10."""
    if verdict == WebsiteVerdict.NO_SITE_VERIFIED:
        return 60, "No website found anywhere"
    if verdict == WebsiteVerdict.SOCIAL_ONLY_VERIFIED:
        return 55, "Only social media, no website"
    if verdict == WebsiteVerdict.SITE_DOWN_CONFIRMED:
        return 50, "Listed website is down"
    if verdict == WebsiteVerdict.OWN_SITE_VERIFIED:
        ok = [c for c in checks if c.type == CheckType.SITE_FETCH and c.outcome == "ok"]
        if not ok:
            return 0, "Has its own website"
        latest = max(ok, key=lambda c: _aware(c.observed_at)).detail
        no_viewport = latest.get("has_viewport") is False
        no_https = latest.get("has_ssl") is False
        if no_viewport and no_https:
            return 35, "Own website is not mobile-friendly and has no HTTPS"
        if no_viewport:
            return 30, "Own website is not mobile-friendly"
        if no_https:
            return 20, "Own website has no HTTPS"
        return 0, "Has a working, mobile-friendly website"
    return None, "Not scored"


def _problem_points(verdict: WebsiteVerdict, facts: Facts, checks: list[Check]) -> tuple[int, str]:
    """Spec row 11 — strongest single observed signal, never the category alone."""
    if verdict == WebsiteVerdict.OWN_SITE_VERIFIED:
        return 0, ""
    links = [c.target or "" for c in checks if c.type == CheckType.SOURCE_TAG and c.outcome in ("found", "listing")]
    if verdict == WebsiteVerdict.SOCIAL_ONLY_VERIFIED and not facts.phone and not facts.email:
        return 10, "Customers can reach it only by social DM / WhatsApp"
    if any(host in link.lower() for link in links for host in AGGREGATOR_HOSTS):
        return 8, "Its only web page is on an aggregator (Zomato / Swiggy / Justdial / Practo)"
    return 0, ""


def _activity_points(facts: Facts, checks: list[Check], now: datetime) -> tuple[int, str]:
    """Spec row 12."""
    manual = [c for c in checks if c.type == CheckType.MANUAL_ACTIVITY and c.outcome == "active"]
    if manual:
        return 10, "You confirmed it is open"
    for raw in facts.raw_records:
        check_date = (raw.get("tags") or {}).get("check_date")
        if check_date:
            try:
                checked = datetime.fromisoformat(check_date[:10]).replace(tzinfo=timezone.utc)
                if now - checked <= timedelta(days=180):
                    return 2, f"OpenStreetMap checked it on {check_date[:10]}"
            except ValueError:
                pass
    return 0, ""


def _fit_points(categories: list[str]) -> tuple[int, str]:
    """Spec row 13."""
    text = " ".join(categories).lower()
    if any(word in text for word in FIT_10):
        return 10, "Pilot category (dentist / salon)"
    if any(word in text for word in FIT_7):
        return 7, "Category that usually needs a website"
    return 4, "Other category"


def assess(checks: list[Check], facts: Facts, now: Optional[datetime] = None) -> Assessment:
    now = now or datetime.now(timezone.utc)
    verdict, confidence, summary = decide_verdict(checks, facts, now)

    if facts.suppressed:
        readiness = OutreachReadiness.BLOCKED
    elif facts.phone or facts.email:
        readiness = OutreachReadiness.READY
    else:
        readiness = OutreachReadiness.RESEARCH

    if verdict == WebsiteVerdict.SKIP:
        return Assessment(verdict, confidence, None, LeadTier.SKIP, readiness, None, [], summary)
    if verdict == WebsiteVerdict.UNKNOWN:
        return Assessment(verdict, confidence, None, LeadTier.REVIEW, readiness, None, [], summary)

    gap, gap_text = _gap_points(verdict, checks)
    problem, problem_text = _problem_points(verdict, facts, checks)
    activity, activity_text = _activity_points(facts, checks, now)
    fit, fit_text = _fit_points(facts.categories)
    breakdown = {"website_gap": gap, "business_problem": problem,
                 "activity": activity, "service_fit": fit}
    score = float(gap + problem + activity + fit)
    # Spec acceptance: every awarded point lists the stored checks behind it.
    def ids(*types: CheckType) -> list[int]:
        return [c.id for c in checks if c.type in types and c.id is not None]

    evidence = {
        "website_gap": ids(CheckType.SOURCE_TAG, CheckType.SOCIAL_LINK, CheckType.LINK_IN_BIO,
                           CheckType.SITE_FETCH, CheckType.DOMAIN_GUESS, CheckType.SEARCH,
                           CheckType.MANUAL_SEARCH),
        "business_problem": ids(CheckType.SOCIAL_LINK, CheckType.SOURCE_TAG),
        "activity": ids(CheckType.MANUAL_ACTIVITY),
        "service_fit": [],  # from the business category, not a check
    }
    reasons = [{"part": part, "points": points, "text": text, "check_ids": evidence[part]}
               for part, points, text in (("website_gap", gap, gap_text),
                                          ("business_problem", problem, problem_text),
                                          ("activity", activity, activity_text),
                                          ("service_fit", fit, fit_text)) if points]

    # Spec row 14.
    hot_gates = (verdict in LEAD_VERDICTS and confidence == EvidenceConfidence.HIGH
                 and activity >= 7 and readiness == OutreachReadiness.READY)
    if score >= 80 and hot_gates:
        tier = LeadTier.HOT
    elif score >= 60:
        tier = LeadTier.WARM
    else:
        tier = LeadTier.COLD
    return Assessment(verdict, confidence, score, tier, readiness, breakdown, reasons, summary)


def missing_for_hot(a: Assessment) -> list[str]:
    """Plain list of what still stops a lead from being HOT (shown as the next action)."""
    if a.tier in (LeadTier.SKIP, LeadTier.HOT) or a.verdict not in LEAD_VERDICTS:
        return []
    missing = []
    if a.confidence != EvidenceConfidence.HIGH:
        missing.append("Record a search for its name + city")
    if (a.breakdown or {}).get("activity", 0) < 7:
        missing.append("Confirm it is open (call or visit)")
    if a.readiness != OutreachReadiness.READY:
        missing.append("Find a phone number or email")
    return missing
