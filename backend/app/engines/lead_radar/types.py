"""
Lead-Radar Condition Strategy — Core Types, Enums, and Dataclasses.

Implements all specifications from the 2026-11-06 Global Lead Engine strategy:
- 6 distinct facts per business (Section 2)
- Condition Library identifiers: G1-G7, W1-W16, I1-I8, D1-D12, C1-C6, J1-J2 (Sections 3 & 11.2)
- Segments: A (Actively looking), Warm context, B (Needs it, intent unknown), C (Stop/solved), UNKNOWN (Section 4)
- 17 Combination Recipes: R1 to R17 (Section 6)
- Revenue estimation confidence ladder & category types (Section 7)
- 6-tier deterministic ranking sort keys (Section 8)
- Absence certificate & Regional profiles (Sections 10 & 11)
"""

from dataclasses import dataclass, field
from datetime import datetime
import enum
from typing import Any, Dict, List, Optional, Tuple


# ─── SECTION 2: THE SIX SEPARATE FACTS PER BUSINESS ─────────────


class OwnedPresence(str, enum.Enum):
    """Fact 1: What type of digital presence does the business own?"""
    OWN_DOMAIN = "OWN_DOMAIN"  # e.g. company.com
    BUILDER_SUBDOMAIN = "BUILDER_SUBDOMAIN"  # e.g. company.wixsite.com, wordpress.com
    PARENT_COMPANY_PAGE = "PARENT_COMPANY_PAGE"  # branch listed on corporate parent site
    SOCIAL_ONLY = "SOCIAL_ONLY"  # only Facebook page, Instagram, LinkedIn, etc.
    MARKETPLACE_ONLY = "MARKETPLACE_ONLY"  # only Zomato, Swiggy, Practo, IndiaMART, Amazon
    LINK_IN_BIO = "LINK_IN_BIO"  # linktr.ee, beacons, etc.
    NONE_FOUND = "NONE_FOUND"  # 3-path absence search completed with 0 matches
    UNRESOLVED = "UNRESOLVED"  # not yet comprehensively searched or conflicting results


class Availability(str, enum.Enum):
    """Fact 2: Is the official web destination technically reachable?"""
    WORKING = "WORKING"  # HTTP 200, valid SSL, renders content
    PARKED = "PARKED"  # Domain registered but parked / registrar page
    COMING_SOON = "COMING_SOON"  # 'Under construction' or 'coming soon' splash page
    DNS_FAIL = "DNS_FAIL"  # NXDOMAIN, no A/AAAA records
    CERTIFICATE_FAIL = "CERTIFICATE_FAIL"  # Expired, self-signed, hostname mismatch SSL
    REPEATED_SERVER_FAIL = "REPEATED_SERVER_FAIL"  # 5xx error on >= 2 checks at least 24h apart
    REDIRECTED = "REDIRECTED"  # Redirects to unrelated destination or parked domain
    UNKNOWN = "UNKNOWN"  # Not checked or no URL to test


class CustomerTaskCovered(str, enum.Enum):
    """Fact 3: What primary customer task is supported on their destination?"""
    INFORMATION = "INFORMATION"  # Basic about, hours, location, FAQ
    PRODUCT_EVALUATION = "PRODUCT_EVALUATION"  # Menu, catalogue, spec sheets, portfolio
    ENQUIRY = "ENQUIRY"  # Contact form, quote request, RFQ
    BOOKING = "BOOKING"  # Table reservation, appointment booking, patient slot
    ORDERING = "ORDERING"  # Full checkout, e-commerce cart, digital payment
    LOCATION = "LOCATION"  # Directions, store finder, branch details
    NONE_NEEDED = "NONE_NEEDED"  # Walk-in only, closed entity, non-procuring
    UNKNOWN = "UNKNOWN"


class TaskQuality(str, enum.Enum):
    """Fact 4: Does the core customer task actually work?"""
    WORKS = "WORKS"  # Smooth completion end-to-end
    INCOMPLETE = "INCOMPLETE"  # Step missing (e.g. menu button with no menu, broken PDF)
    FAILS_REPRODUCIBLY = "FAILS_REPRODUCIBLY"  # Form 500s, booking widget crashed, submit hangs
    NOT_TESTED = "NOT_TESTED"


class BuyingStatus(str, enum.Enum):
    """Fact 5: Is the business actively in the market for web solutions?"""
    EXPLICITLY_SEEKING = "EXPLICITLY_SEEKING"  # RFP, tender, job post, public request < 30 days
    EXPLICITLY_NOT_SEEKING = "EXPLICITLY_NOT_SEEKING"  # Authorized person stated no need
    SUPPLIER_ALREADY_CHOSEN = "SUPPLIER_ALREADY_CHOSEN"  # Agency or in-house team actively handling
    UNKNOWN = "UNKNOWN"


class Authority(str, enum.Enum):
    """Fact 6: Who holds purchasing authority for this digital presence?"""
    LOCAL_OWNER = "LOCAL_OWNER"  # Independent owner/operator who can make decisions
    FRANCHISEE = "FRANCHISEE"  # Franchisee bound by franchisor digital rules
    PARENT_COMPANY = "PARENT_COMPANY"  # Headquarters controls all digital assets
    PROCUREMENT_TEAM = "PROCUREMENT_TEAM"  # Formal committee / public tender required
    UNRESOLVED = "UNRESOLVED"


@dataclass
class SixFacts:
    """The foundational 6 facts stored per business entity."""
    owned_presence: OwnedPresence = OwnedPresence.UNRESOLVED
    availability: Availability = Availability.UNKNOWN
    customer_task_covered: CustomerTaskCovered = CustomerTaskCovered.UNKNOWN
    task_quality: TaskQuality = TaskQuality.NOT_TESTED
    buying_status: BuyingStatus = BuyingStatus.UNKNOWN
    authority: Authority = Authority.UNRESOLVED

    # Foundational validation flags
    identity_verified: bool = False  # official ID or 2+ matching identity fields
    currently_active: bool = False  # owner confirmed or 2 independent activity signals in 90 days
    absence_search_done: bool = False  # 3 discovery paths tested
    repeated_failure: bool = False  # same failure on 2 checks >= 24h apart

    def to_dict(self) -> Dict[str, Any]:
        return {
            "owned_presence": self.owned_presence.value,
            "availability": self.availability.value,
            "customer_task_covered": self.customer_task_covered.value,
            "task_quality": self.task_quality.value,
            "buying_status": self.buying_status.value,
            "authority": self.authority.value,
            "identity_verified": self.identity_verified,
            "currently_active": self.currently_active,
            "absence_search_done": self.absence_search_done,
            "repeated_failure": self.repeated_failure,
        }


# ─── SECTION 4: SEGMENTATION & WARM CONTEXT ─────────────────────


class Segment(str, enum.Enum):
    """Strategic buying segment."""
    A = "A"  # Actively looking: open tender, public request, active evaluation
    B = "B"  # Needs it, not shown to be looking: active + task gap + demand
    C = "C"  # Stop: declined, solved, supplier chosen, platform enough, deferred
    UNKNOWN = "UNKNOWN"  # Missing data, unresolved identity, no observed gap


# ─── SECTION 3: CONDITION IDENTIFIERS ───────────────────────────


class ConditionID(str, enum.Enum):
    # Gates: G1 to G7
    G1 = "G1"  # Correct business identity
    G2 = "G2"  # Evidence may be used
    G3 = "G3"  # Same buying unit (merge duplicates)
    G4 = "G4"  # Not a non-procuring body (ATM, landmark)
    G5 = "G5"  # Closed for good
    G6 = "G6"  # Branch cannot buy (parent controls)
    G7 = "G7"  # Operating now (2 signals in 90d)

    # Website and customer-task conditions: W1 to W16
    W1 = "W1"  # No owned website found (after 3-path absence check)
    W2 = "W2"  # Needed task has nowhere to happen
    W3 = "W3"  # Official site keeps failing (repeated failure)
    W4 = "W4"  # Browser security warning (SSL invalid)
    W5 = "W5"  # Core action broken reproducibly
    W6 = "W6"  # Mobile task fails on 2 screen sizes
    W7 = "W7"  # Key buying info missing (pricing, menu, timings)
    W8 = "W8"  # Business info conflicts across sources
    W9 = "W9"  # Parent site ignores branch-specific tasks
    W10 = "W10"  # Language gap (2+ requests in unserved language)
    W11 = "W11"  # Poor real-user speed (CrUX poor band)
    W12 = "W12"  # Live material/ad points to dead page
    W13 = "W13"  # Accessibility barrier blocks task (keyboard failure)
    W14 = "W14"  # Audience access failure (device/network/format block)
    W15 = "W15"  # Local-format failure (currency, address, script)
    W16 = "W16"  # Platform-only destination excludes intended customers

    # Intent conditions: I1 to I8
    I1 = "I1"  # Explicitly asking for website help (<30d)
    I2 = "I2"  # Open website tender (SAM.gov, TED, GeM, CPPP)
    I3 = "I3"  # Evaluating suppliers now
    I4 = "I4"  # Wants to replace current supplier
    I5 = "I5"  # Coming-soon or launching-soon page
    I6 = "I6"  # Recently registered domain, parked (<90d)
    I7 = "I7"  # Hiring a web/digital role
    I8 = "I8"  # New builder site, still incomplete (<90d)

    # Demand conditions: D1 to D12
    D1 = "D1"  # Running ads into a gap (active ad to broken/missing task)
    D2 = "D2"  # Customers keep asking same unanswered question (3+ in 90d)
    D3 = "D3"  # Real customer activity (10+ reviews in 90d)
    D4 = "D4"  # Actively promoting (2+ promotions in 90d)
    D5 = "D5"  # Wants direct sales channel
    D6 = "D6"  # Several locations, confused journey
    D7 = "D7"  # Opened, moved or expanded; web did not follow (<90d)
    D8 = "D8"  # Buyer prequalification requirement unmet online
    D9 = "D9"  # Out-of-area / export / tourist buyers need material
    D10 = "D10"  # Peers solve task they don't (75%+ of 20+ peers)
    D11 = "D11"  # Messaging workflow bottleneck ("DM to order" friction)
    D12 = "D12"  # Commission-marketplace dependence + wants direct

    # Stop conditions: C1 to C6
    C1 = "C1"  # Authorised person declined
    C2 = "C2"  # Need already solved by current site
    C3 = "C3"  # Supplier or in-house team already owns project
    C4 = "C4"  # Owner says non-website setup is sufficient, no gap
    C5 = "C5"  # Owner explicitly deferred
    C6 = "C6"  # Existing platform solution is enough (don't penalize)

    # Jurisdiction conditions: J1, J2
    J1 = "J1"  # Verified digital-information legal duty
    J2 = "J2"  # Proposed solution is deliverable and permitted


class ConditionStrength(str, enum.Enum):
    STRONG = "STRONG"
    MEDIUM = "MEDIUM"
    WEAK = "WEAK"
    SUPPORTING = "SUPPORTING"


@dataclass
class ConditionResult:
    """Evaluation result of a single condition."""
    condition_id: ConditionID
    name: str
    is_met: bool
    strength: ConditionStrength
    evidence: str
    source: str
    evaluated_at: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "condition_id": self.condition_id.value,
            "name": self.name,
            "is_met": self.is_met,
            "strength": self.strength.value,
            "evidence": self.evidence,
            "source": self.source,
            "evaluated_at": self.evaluated_at.isoformat(),
        }


# ─── SECTION 6: COMBINATION RECIPES (R1 - R17) ──────────────────


class RecipeID(str, enum.Enum):
    R1 = "R1"  # Open mandate (G1 + I1 + authority + still open) -> A
    R2 = "R2"  # Open tender (I2 + eligible + correct entity) -> A
    R3 = "R3"  # Replacement (I4 + current problem + decision open) -> A
    R4 = "R4"  # Founder's case, corrected (G7 active + 2+ sources + D4 promoting + W1 no site + W2 task gap) -> B
    R5 = "R5"  # Social attention, unanswered questions (Social-only + D2 + W7) -> B
    R6 = "R6"  # Ad leads to a broken page (D1 + W5/W12) -> B
    R7 = "R7"  # Live business, dead site (G7 + W3 + W12) -> B
    R8 = "R8"  # Booking bottleneck (Appointment business + D2 booking requests + W5 or W2) -> B
    R9 = "R9"  # Marketplace business wants direct (D12 + D5 + W2) -> B
    R10 = "R10"  # Branches, confused journey (D6 + W8/W9 + authority) -> B
    R11 = "R11"  # Moved, web didn't follow (D7 + W8) -> B
    R12 = "R12"  # Export buyers can't evaluate (D9 + W7/W10) -> B
    R13 = "R13"  # Mobile failure under demand (W6 + D2/D3) -> B
    R14 = "R14"  # Accessibility blocked (G7 + W13) -> B
    R15 = "R15"  # Self-built site, one task missing (I8 + W2 + D2) -> B
    R16 = "R16"  # Launch underway, supplier chosen (I5/I6 + C3) -> C
    R17 = "R17"  # Something in motion (G7 + D4 + any of I5-I7) -> Warm


@dataclass
class RecipeMatch:
    """Outcome of matching an established sales combination recipe."""
    recipe_id: RecipeID
    name: str
    target_segment: Segment
    is_matched: bool
    required_conditions: List[ConditionID]
    matched_conditions: List[ConditionID]
    opening_fact: str
    pitch_angle: str
    never_say: str
    recommended_solution: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "recipe_id": self.recipe_id.value,
            "name": self.name,
            "target_segment": self.target_segment.value,
            "is_matched": self.is_matched,
            "required_conditions": [c.value for c in self.required_conditions],
            "matched_conditions": [c.value for c in self.matched_conditions],
            "opening_fact": self.opening_fact,
            "pitch_angle": self.pitch_angle,
            "never_say": self.never_say,
            "recommended_solution": self.recommended_solution,
        }


# ─── SECTION 7: REVENUE ESTIMATION & CONFIDENCE LADDER ──────────


class RevenueConfidence(str, enum.Enum):
    HIGH = "HIGH"  # Filed statutory accounts for entity & period
    MEDIUM = "MEDIUM"  # Real operating inputs (seats, rooms, staff) + calibrated rates
    LOW = "LOW"  # Uncalibrated utilisation, review rates, or headcount
    UNAVAILABLE = "UNAVAILABLE"  # Only listings/ads; unbounded reviews; cannot report honest band


class BusinessCategory(str, enum.Enum):
    RESTAURANT = "RESTAURANT"
    CLINIC = "CLINIC"
    SALON = "SALON"
    HOTEL = "HOTEL"
    RETAIL = "RETAIL"
    MANUFACTURER_EXPORTER = "MANUFACTURER_EXPORTER"
    PROFESSIONAL_SERVICES = "PROFESSIONAL_SERVICES"
    EDUCATION = "EDUCATION"
    GYM = "GYM"
    REAL_ESTATE_BROKER = "REAL_ESTATE_BROKER"
    OTHER = "OTHER"


@dataclass
class RevenueEstimate:
    """Calibrated revenue range with explicit confidence ladder label."""
    category: BusinessCategory
    confidence: RevenueConfidence
    min_annual_revenue: Optional[float] = None
    max_annual_revenue: Optional[float] = None
    currency: str = "USD"
    formula_used: str = ""
    input_signals: Dict[str, Any] = field(default_factory=dict)
    notes: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "category": self.category.value,
            "confidence": self.confidence.value,
            "min_annual_revenue": self.min_annual_revenue,
            "max_annual_revenue": self.max_annual_revenue,
            "currency": self.currency,
            "formula_used": self.formula_used,
            "input_signals": self.input_signals,
            "notes": self.notes,
        }


# ─── SECTION 8: 6-TIER DETERMINISTIC RANKING ────────────────────


class OpportunityClass(int, enum.Enum):
    OPEN_MANDATE = 4  # Open tender or explicit request
    BROKEN_TASK_WITH_DEMAND = 3  # Working ad or customers hitting reproducible failure
    MISSING_TASK_WITH_DEMAND = 2  # Active business with no booking/menu/enquiry
    RESEARCH_CANDIDATE = 1  # Unresolved absence or uncorroborated single signal


class EvidenceQuality(int, enum.Enum):
    OWNER_OR_FIRST_PARTY = 4  # Owner direct post, primary website, official filing
    CORROBORATED = 3  # 2+ independent upstream sources (not copies)
    SINGLE_SOURCE = 2  # Single verified platform (e.g. Overture Meta record)
    PROXY = 1  # Inferred from category or area averages


class TaskSeverity(int, enum.Enum):
    IMPOSSIBLE = 4  # Zero way to complete task anywhere
    OBSTRUCTED = 3  # Fails reproducibly (500, crash, keyboard barrier)
    INFO_INCOMPLETE = 2  # Essential prices, menu, or hours missing
    COSMETIC = 1  # Visual styling or minor speed issue


class DemandLevel(int, enum.Enum):
    OWNER_CONFIRMED = 4  # Owner stated demand / friction
    REPEATED_REQUESTS = 3  # 3+ distinct user questions in 90d
    ACTIVITY_ONLY = 2  # Recent reviews, promotions, or ads
    UNKNOWN = 1


class AuthorityLevel(int, enum.Enum):
    CONFIRMED = 2  # Independent local decision maker
    UNRESOLVED = 1  # Franchise, branch, or unknown


@dataclass
class DeterministicRank:
    """The 6 hierarchical sort keys from Section 8."""
    opportunity_class: OpportunityClass
    evidence_quality: EvidenceQuality
    task_severity: TaskSeverity
    demand_level: DemandLevel
    authority_level: AuthorityLevel
    freshness_timestamp: datetime

    # The 4 mandatory answers
    why_this_business: str = ""
    why_this_project: str = ""
    why_now: str = ""
    what_is_unknown: str = ""

    def sort_tuple(self) -> Tuple[int, int, int, int, int, float]:
        """Hierarchical sort tuple: earlier key always wins."""
        return (
            self.opportunity_class.value,
            self.evidence_quality.value,
            self.task_severity.value,
            self.demand_level.value,
            self.authority_level.value,
            self.freshness_timestamp.timestamp(),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "opportunity_class": self.opportunity_class.name,
            "evidence_quality": self.evidence_quality.name,
            "task_severity": self.task_severity.name,
            "demand_level": self.demand_level.name,
            "authority_level": self.authority_level.name,
            "freshness": self.freshness_timestamp.isoformat(),
            "why_this_business": self.why_this_business,
            "why_this_project": self.why_this_project,
            "why_now": self.why_now,
            "what_is_unknown": self.what_is_unknown,
        }


# ─── SECTION 10: ABSENCE CERTIFICATE ────────────────────────────


@dataclass
class AbsenceCertificate:
    """
    Auditable certificate proving an absence search was thoroughly conducted
    across all 3 discovery paths before declaring 'No owned website found'.
    """
    certificate_id: str
    business_id: int
    business_name: str
    country_code: str
    city: str
    timestamp: datetime
    paths_checked: List[str]
    queries_executed: List[str]
    profiles_inspected: List[str]
    domain_clues_tested: List[str]
    is_truly_absent: bool
    signature_hash: str
    notes: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "certificate_id": self.certificate_id,
            "business_id": self.business_id,
            "business_name": self.business_name,
            "country_code": self.country_code,
            "city": self.city,
            "timestamp": self.timestamp.isoformat(),
            "paths_checked": self.paths_checked,
            "queries_executed": self.queries_executed,
            "profiles_inspected": self.profiles_inspected,
            "domain_clues_tested": self.domain_clues_tested,
            "is_truly_absent": self.is_truly_absent,
            "signature_hash": self.signature_hash,
            "notes": self.notes,
        }


# ─── SECTION 11: REGIONAL CALIBRATION PROFILE ───────────────────


class IndianEconomicType(str, enum.Enum):
    METRO_SERVICES = "METRO_SERVICES"
    MANUFACTURING_EXPORT = "MANUFACTURING_EXPORT"
    TOURISM = "TOURISM"
    REGIONAL_TRADE_SERVICE = "REGIONAL_TRADE_SERVICE"


@dataclass
class RegionalProfile:
    """Strategic configuration profile by state/region/country."""
    region_code: str  # e.g. IN-MH, IN-GJ, US, GB, DE
    region_name: str
    country_code: str
    economic_type: Optional[IndianEconomicType] = None
    baseline_no_website_percent: float = 0.0  # Measured baseline ceiling
    check_first: List[ConditionID] = field(default_factory=list)  # Conditions to prioritize (↑)
    trust_less: List[str] = field(default_factory=list)  # Proxies/assumptions to discount (↓)
    local_sources: List[str] = field(default_factory=list)
    local_languages: List[str] = field(default_factory=list)
    target_categories: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "region_code": self.region_code,
            "region_name": self.region_name,
            "country_code": self.country_code,
            "economic_type": self.economic_type.value if self.economic_type else None,
            "baseline_no_website_percent": self.baseline_no_website_percent,
            "check_first": [c.value for c in self.check_first],
            "trust_less": self.trust_less,
            "local_sources": self.local_sources,
            "local_languages": self.local_languages,
            "target_categories": self.target_categories,
        }

