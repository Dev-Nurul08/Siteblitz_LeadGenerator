name: lead-intelligence-vision-partner
use_when: Deciding the complete future vision of a lead-generation / scraping / sales-intelligence system - how leads actually arrive now and over the next years, what is missing, how to make it final-strong. Legal only. ChatGPT and Claude Code work as equal partners with no self-imposed limits on ambition.

You and Claude Code are two equal partners with one shared mission: design the strongest possible
lead-generation system this founder could own, and prove that the two of you together have no
self-imposed limitations. The founder trusts you both and asked for a very deep conversation, using
your full potential. Your job is to improve the decision, not to agree.

The one hard boundary, set by the founder: nothing illegal. Treat it as a design constraint, not a
reason to shrink the vision.

What "no limitations" means here:
- Never stop at "this can't be done". When something is blocked, name the exact cause and give the
  lawful route around it: another data source, channel, consent mechanism, market or product.
- Think well past the obvious. Look for what nobody in this market is doing yet, including what the
  world looks like when buyers, inboxes and search are themselves run by AI agents.
- It does not mean pretending. A real legal, technical or economic limit is stated plainly, then
  worked around. Motivational certainty is worthless to this founder.

Rules for facts:
- Trends, laws, platform rules, numbers: give the source URL, the date you believe it became true and
  your confidence (high / medium / low). Search the web where you can. Say "I don't know" freely.
- Vendor-blog statistics are marketing until corroborated. Say when a number comes from a vendor.
- The only facts about this project are in the pasted README. Claude Code has not seen the code
  behind it, so every README claim is a claim, not a verified feature. Never invent facts about it.
- Legal points are design input for counsel to confirm, not legal advice. Name the statute or
  regulator, and separate "the law says" from "vendors say".

Rules for judgement:
- Every proposal says what it costs (money, upkeep, risk), who benefits, and how anyone could tell it
  worked: a number, a threshold, a test.
- Prefer ideas a very small team in India can really run. Ambitious is welcome; hand-waving is not.
- Deleting something is as valid as adding something. Accept a good point in one line. Challenge
  Claude Code's reasoning when it is weak and say exactly why. Claude Code checks every claim you make
  and will report back which were wrong; do the same to it.

Format of every reply:
- Answer each agenda point by number: "agree", "disagree because ...", or "need data: <what>", then
  add your own proposals under that point.
- End with the list of points still open.

<project_context>
<file path="E:/tmp/Siteblitz_LeadGenerator/docs/debate/2026-11-08-lead-generator-audit-website-need-logic-ui-flow/audit-evidence.md">
# Verified audit evidence — SiteBlitz Lead Generator (commit 2705aca, 2026-11-08)

Stack: FastAPI + SQLAlchemy async (Postgres default, SQLite supported) backend, React 19 + Vite
frontend (no router, no CSS framework; one page uses Tailwind class names but Tailwind is not
installed). 5 "engines": discovery → opportunity → enrichment → qualification → conversion.
136 unit tests pass, all mocked; no integration test. Redis/RQ declared but never used.

## A. Confirmed by running the code (live probe 2026-11-08)
| # | What happens | Root cause |
|---|---|---|
| A1 | `pip install -e ".[dev]"` (README step) fails: `No module named 'setuptools.backends'` | pyproject.toml:3 build-backend is invalid |
| A2 | App import crashes: `ModuleNotFoundError: dns` | engines/enrichment/verifier.py:12 imports dnspython, which is only in the optional `phase3` extra |
| A3 | Every OSM discovery returns 0 results (job PARTIAL, 1 error) | Overpass answers HTTP 406 to httpx's default User-Agent (osm.py:244 sends none). Live: default UA → 406; custom UA → 200 |
| A4 | Even with a User-Agent, a city search returns 0 elements | osm.py:96 builds `area["name"="Pune"]["ISO3166-1"="IN"]`; city areas never carry ISO3166-1. Live: buggy query 0 elements, `area["name"="Pune"]["boundary"="administrative"]` 5 elements |
| A5 | Second CSV import of a DIFFERENT file: new row counted as "duplicate", 0 imported | csv_import.py:236 external_id = `csv:row:{n}`; unique (source, external_id) → row 1 of every later file collides |
| A6 | Discovery result card always shows 0 new / 0 dup / 0 errors | DiscoveryPage.jsx:305-307 reads `records_new` etc.; API returns `new`, `duplicate`, `errors` |
| A7 | Qualify a business that has a website → HTTP 500 `MissingGreenlet` | ai_personalizer.py:52-53 uses `business.city` / `business.category` properties that lazy-load relationships in async SQLAlchemy |
| A8 | Campaign enrollment would crash the same way | scheduler.py:128,157 `lead.contact`, `lead.business.name` lazy loads |
| A9 | Unsubscribe link in every email → HTTP 405 | qualification.py:367 is POST only; a clicked link is GET |
| A10 | A dentist with a working website gets "Mobile App" CRITICAL 83.5 + "Online Booking" | detector.py:161-185 adds MOBILE_APP for every restaurant/clinic/gym/salon with a reachable site |
| A11 | A business with no website field gets "New Website" CRITICAL 88 without any check | detector.py:74-78; scorer gives 38 + 25 base → every such business is HIGH/CRITICAL |
| A12 | Enrichment invents `info@<domain>` contacts | enrichment/discovery.py:95-104 "synthesize corporate inbox" |

## B. Confirmed by reading (file:line)
- OSM "all categories" query pulls every named amenity/shop/office/tourism: ATMs, banks, fuel, schools, hospitals, places of worship become leads (osm.py:30-41,157-169). No brand/chain exclusion (OSM `brand`, `brand:wikidata` ignored).
- OSM gym/spa/salon mapping wrong: `amenity=gym` deprecated (real tag `leisure=fitness_centre`); "salon"/"shop" fall back to a name regex search (osm.py:143-152). Values interpolated into Overpass QL / SPARQL unescaped (osm.py:96-100, wikidata.py:90).
- Wikidata source returns notable companies that already have websites — useless for "needs a website" (wikidata.py:93-114).
- normalize_website drops any URL containing "x.com" (fedex.com, box.com …) as "social" (normalizer.py:243-251). Category partial matching maps "it" → Hospital, "barber" → Bar (normalizer.py:206-208).
- Dedup: same normalized name in the same country with no coordinates on the stored side → merged (confidence 0.60 ≥ 0.50 threshold): two different "Sharma Sweets" in Pune and Delhi become one (discovery_service.py:303-337, normalizer.py:301).
- Resolver: Cloudflare/bot 403 → BROKEN; timeouts → treated as "no website" (resolver.py:117-118,164-170; detector.py:77). No detection of website-that-redirects-to-Facebook, link-in-bio, or dead Google `business.site` URLs.
- Auditor false positives: any page containing the word "appointment" = has online booking; "basket"/"/cart" = e-commerce; any `class="…flex…"` = Tailwind (auditor.py:61-95,180-189).
- Scorer confidence is a hard-coded 0.92 (scorer.py:120).
- batch_evaluate re-audits businesses that produced zero opportunities forever; runs up to 100 sequential 12 s HTTP fetches inside one HTTP request (opportunity_service.py:198-218).
- Re-evaluation never deletes stale opportunities (a business that got a website keeps "New Website").
- Hunter.io integration always returns [] — passes `first_name`/`last_name` to a dataclass without those fields, exception swallowed (enrichment/discovery.py:203-205).
- Sync DNS lookups block the event loop (verifier.py:104).
- Compliance defaults unknown country to "US" CAN-SPAM AUTOMATED (compliance_evaluator.py:97). India falls to GENERAL_B2B.
- "AI personalizer" is fixed templates with fabricated claims: "I was impressed by your reviews", "we recently built a preview concept", "I was browsing from my smartphone" (ai_personalizer.py:64-160). Fake sender "Marcus Vance", fake postal address "100 Innovation Way, New York" (ai_personalizer.py:32-45, sender.py:34-43). Address validator passes any text containing "st" (output_validator.py:80-83).
- Campaign "dispatch" never sends anything: it only flips status to SENT (sender.py:79-107). Re-enrolling duplicates messages for the same leads (campaign_service.py:86-117).
- Only phase-1 tables are in the Alembic migration; phases 2–5 rely on create_all at startup.

## C. UI (frontend/src)
- 8 pages named after internal engines (Discovery Engine, Opportunity Engine, Enrichment Engine …) with no guided order; sidebar still says "Phase 1 — Build & test before Phase 2" while all phases exist.
- Discovery defaults to London/GB; category list mixes OSM tags and free words.
- Discovery is a blocking request (up to 90 s) with a spinner and no progress; no link from a finished job to its businesses.
- OpportunitiesPage uses Tailwind classes that render unstyled.
- Generic dark-indigo gradient dashboard with emoji icons.

</file>

<file path="E:/tmp/Siteblitz_LeadGenerator/backend/app/engines/opportunity/detector.py">
"""
Opportunity Detector module.

Synthesizes business categories, website audit metrics, and reachability signals
to identify concrete digital service needs matching the agency's service divisions.
"""

from dataclasses import dataclass, field
from typing import Optional

from backend.app.engines.opportunity.auditor import AuditResult
from backend.app.engines.opportunity.resolver import ResolutionResult
from backend.app.models.business import Business, WebsiteStatus
from backend.app.models.opportunity import ServiceCategory


@dataclass
class DetectedNeed:
    """A specific detected digital service need."""

    service_category: ServiceCategory
    title: str
    summary: str
    evidence: dict
    pitch_angles: list[str]
    need_severity: float  # 0.0 to 1.0


# Categories that benefit immensely from dedicated mobile applications
MOBILE_APP_CANDIDATE_CATEGORIES = {
    "restaurant", "cafe", "fast_food", "food_court",
    "gym", "spa", "salon", "hairdresser", "fitness",
    "clinic", "dentist", "medical",
    "supermarket", "convenience", "clothing",
    "delivery", "transport", "hotel", "resort",
}

# Categories where online booking / reservation is standard customer expectation
BOOKING_CANDIDATE_CATEGORIES = {
    "dentist", "clinic", "doctors", "optician", "physiotherapy",
    "salon", "hairdresser", "spa",
    "restaurant", "hotel", "resort", "guest_house",
    "lawyer", "accountant", "consulting",
    "car_repair", "car_wash", "veterinary",
}

# Categories where e-commerce / online catalog is a massive revenue driver
ECOMMERCE_CANDIDATE_CATEGORIES = {
    "retail", "shop", "supermarket", "convenience", "clothes",
    "electronics", "furniture", "hardware", "jewelry", "bookshop",
    "bakery", "butcher", "florist", "gift", "pet",
}


class OpportunityDetector:
    """
    Evaluates business data and technical audit results to discover opportunities.
    """

    def detect_opportunities(
        self,
        business: Business,
        audit: Optional[AuditResult] = None,
        resolution: Optional[ResolutionResult] = None,
        business_categories: Optional[list[str]] = None,
    ) -> list[DetectedNeed]:
        """
        Identify all eligible service opportunities for a business.
        """
        needs: list[DetectedNeed] = []
        categories = [c.lower() for c in (business_categories or [])]

        # Case 1: No website or Social-only presence -> Brand New Website
        has_no_website = (
            not business.website_url
            or business.website_status in [WebsiteStatus.NOT_FOUND, WebsiteStatus.UNKNOWN]
            or (resolution and not resolution.is_reachable and resolution.http_status in [404, None])
        )
        is_social_only = business.website_status == WebsiteStatus.SOCIAL_ONLY or (
            has_no_website and bool(business.social_urls)
        )

        if has_no_website:
            evidence = {
                "missing_website": True,
                "social_presence": bool(business.social_urls),
                "business_name": business.name,
                "country": business.country_code,
            }
            if is_social_only:
                summary = (
                    f"{business.name} operates only through social media channels without an "
                    f"official business website, limiting search discovery, customer trust, and conversions."
                )
                pitch = [
                    "Convert social media followers into direct paying clients on an owned website",
                    "Establish domain authority and Google Local SEO search visibility",
                    "Stop losing high-intent search customers to competing businesses with websites",
                ]
            else:
                summary = (
                    f"{business.name} has no detectable web presence. Launching a modern, "
                    f"conversion-focused website provides an instant competitive advantage."
                )
                pitch = [
                    "Build a professional digital storefront that captures local and international customers",
                    "Establish brand credibility with professional domain-based presence",
                    "Enable 24/7 inbound customer inquiries and showcase portfolio/menu/services",
                ]

            needs.append(
                DetectedNeed(
                    service_category=ServiceCategory.NEW_WEBSITE,
                    title=f"New Custom Website for {business.name}",
                    summary=summary,
                    evidence=evidence,
                    pitch_angles=pitch,
                    need_severity=0.95,
                )
            )

        # Case 2: Website exists -> Technical Audit-driven Opportunities
        if audit and resolution and resolution.is_reachable:
            # A) Website Redesign Opportunity (Mobile responsiveness, SSL, or obsolete design)
            redesign_reasons = []
            if not audit.is_mobile_responsive:
                redesign_reasons.append("Missing mobile viewport configuration (fails mobile devices)")
            if not resolution.has_ssl:
                redesign_reasons.append("Lacks HTTPS / valid SSL certificate (browser security warning)")
            if resolution.load_time_seconds and resolution.load_time_seconds > 3.5:
                redesign_reasons.append(f"Slow page loading ({resolution.load_time_seconds}s)")
            if audit.detected_cms in ["Joomla", "Drupal"]:
                redesign_reasons.append(f"Legacy {audit.detected_cms} installation")

            if redesign_reasons:
                needs.append(
                    DetectedNeed(
                        service_category=ServiceCategory.WEBSITE_REDESIGN,
                        title=f"Modern Responsive Redesign for {business.name}",
                        summary=(
                            f"Audit of {resolution.final_url or resolution.original_url} identified critical "
                            f"deficiencies: {', '.join(redesign_reasons)}."
                        ),
                        evidence={
                            "reasons": redesign_reasons,
                            "mobile_responsive": audit.is_mobile_responsive,
                            "has_ssl": resolution.has_ssl,
                            "load_time_seconds": resolution.load_time_seconds,
                            "detected_cms": audit.detected_cms,
                        },
                        pitch_angles=[
                            "Over 65% of customer traffic is mobile — non-responsive design causes immediate dropoff",
                            "Fix browser 'Not Secure' warnings with modern SSL and security architecture",
                            "Fast, modern redesign boosts Google rankings and doubles conversion rates",
                        ],
                        need_severity=0.85 if not audit.is_mobile_responsive else 0.70,
                    )
                )

            # B) Mobile Application Opportunity
            is_mobile_app_target = any(
                any(cand in cat for cand in MOBILE_APP_CANDIDATE_CATEGORIES)
                for cat in categories
            )
            if is_mobile_app_target:
                needs.append(
                    DetectedNeed(
                        service_category=ServiceCategory.MOBILE_APP,
                        title=f"Custom iOS/Android Mobile App for {business.name}",
                        summary=(
                            f"As a customer-centric business in {business.country_code or 'the market'}, "
                            f"{business.name} can drive repeat retention and direct revenue through a dedicated mobile app."
                        ),
                        evidence={
                            "matched_category": categories,
                            "business_type": "high_frequency_repeat_interaction",
                        },
                        pitch_angles=[
                            "Direct home-screen access and zero-cost push notification promotions",
                            "One-tap customer reordering, appointments, and loyalty reward tracking",
                            "Eliminate third-party delivery/booking commissions with an owned native app",
                        ],
                        need_severity=0.75,
                    )
                )

            # C) Online Booking Opportunity
            is_booking_target = any(
                any(cand in cat for cand in BOOKING_CANDIDATE_CATEGORIES)
                for cat in categories
            )
            if is_booking_target and not audit.has_online_booking:
                needs.append(
                    DetectedNeed(
                        service_category=ServiceCategory.ONLINE_BOOKING,
                        title=f"Automated Online Booking & Scheduling for {business.name}",
                        summary=(
                            f"{business.name} provides appointment-based services but does not offer "
                            f"an interactive digital scheduling widget on its website."
                        ),
                        evidence={
                            "has_booking_widget": False,
                            "target_industry": categories,
                        },
                        pitch_angles=[
                            "Capture appointment bookings after business hours when customers browse online",
                            "Reduce phone tag and front-desk administrative overhead by 70%",
                            "Automated SMS/Email reminders to eliminate customer no-shows",
                        ],
                        need_severity=0.80,
                    )
                )

            # D) E-Commerce Expansion Opportunity
            is_ecommerce_target = any(
                any(cand in cat for cand in ECOMMERCE_CANDIDATE_CATEGORIES)
                for cat in categories
            )
            if is_ecommerce_target and not audit.has_ecommerce:
                needs.append(
                    DetectedNeed(
                        service_category=ServiceCategory.ECOMMERCE_EXPANSION,
                        title=f"E-Commerce Store & Online Ordering for {business.name}",
                        summary=(
                            f"{business.name} sells physical products or food items but currently has no "
                            f"e-commerce checkout or digital ordering system on their website."
                        ),
                        evidence={
                            "has_ecommerce": False,
                            "target_industry": categories,
                        },
                        pitch_angles=[
                            "Expand revenue beyond physical walk-ins into national and local online delivery",
                            "Seamless mobile checkout with Apple Pay, Google Pay, and credit cards",
                            "Automated inventory management and integrated shipping labels",
                        ],
                        need_severity=0.80,
                    )
                )

            # E) SEO & Performance Optimization
            seo_deficiencies = []
            if not audit.meta_title or len(audit.meta_title) < 10:
                seo_deficiencies.append("Missing or truncated meta title tag")
            if not audit.meta_description:
                seo_deficiencies.append("Missing meta description for search engine previews")
            if audit.headings_summary.get("h1_count", 0) == 0:
                seo_deficiencies.append("Missing H1 heading tag structure")
            if not audit.has_analytics:
                seo_deficiencies.append("No conversion analytics tracking detected")

            if seo_deficiencies:
                needs.append(
                    DetectedNeed(
                        service_category=ServiceCategory.SEO_PERFORMANCE,
                        title=f"Search Engine & Performance Optimization for {business.name}",
                        summary=(
                            f"Technical SEO audit discovered foundational search visibility issues: "
                            f"{', '.join(seo_deficiencies)}."
                        ),
                        evidence={
                            "deficiencies": seo_deficiencies,
                            "title": audit.meta_title,
                            "has_meta_desc": bool(audit.meta_description),
                            "headings": audit.headings_summary,
                        },
                        pitch_angles=[
                            "Fix critical search engine indexing blockers to outrank local competitors",
                            "Improve organic click-through rates from Google search results",
                            "Implement transparent ROI and traffic analytics dashboards",
                        ],
                        need_severity=0.60,
                    )
                )

        return needs

</file>

<file path="E:/tmp/Siteblitz_LeadGenerator/backend/app/engines/opportunity/scorer.py">
"""
Opportunity Scorer module.

Evaluates detected needs, business profiles, and contactability signals
to generate a weighted opportunity score (0 to 100) and priority level.
"""

from dataclasses import dataclass
from typing import Optional

from backend.app.engines.opportunity.detector import DetectedNeed
from backend.app.models.business import Business
from backend.app.models.opportunity import OpportunityPriority, ServiceCategory

# High-value commercial categories with higher budget capacity
PREMIUM_TIER_CATEGORIES = {
    "dentist", "doctor", "clinic", "hospital", "medical",
    "lawyer", "legal", "accountant", "accounting", "financial",
    "architect", "consulting", "it_services", "software",
    "estate_agent", "real_estate", "hotel", "resort",
}

# Standard commercial categories
MID_TIER_CATEGORIES = {
    "restaurant", "cafe", "bar", "pub",
    "gym", "spa", "salon", "car_repair",
    "supermarket", "retail", "shop", "jewelry",
}

# Agency service alignment weight (0.0 to 1.0)
SERVICE_FIT_WEIGHTS = {
    ServiceCategory.NEW_WEBSITE: 1.0,
    ServiceCategory.WEBSITE_REDESIGN: 1.0,
    ServiceCategory.CUSTOM_WEB_APP: 0.95,
    ServiceCategory.MOBILE_APP: 0.90,
    ServiceCategory.ECOMMERCE_EXPANSION: 0.85,
    ServiceCategory.ONLINE_BOOKING: 0.80,
    ServiceCategory.SEO_PERFORMANCE: 0.75,
}


@dataclass
class ScoredOpportunity:
    """Scored evaluation of a detected opportunity."""

    score: float  # 0.0 to 100.0
    priority: OpportunityPriority
    confidence: float
    score_breakdown: dict


class OpportunityScorer:
    """
    Computes multi-factor composite scores for detected opportunities.
    """

    def score_need(
        self,
        need: DetectedNeed,
        business: Business,
        business_categories: Optional[list[str]] = None,
    ) -> ScoredOpportunity:
        """
        Calculate weighted score (0–100) and priority for a detected need.
        """
        # Factor 1: Need Severity (Weight: 40 points)
        severity_score = min(max(need.need_severity, 0.0), 1.0) * 40.0

        # Factor 2: Agency Service Division Fit (Weight: 25 points)
        service_weight = SERVICE_FIT_WEIGHTS.get(need.service_category, 0.70)
        fit_score = service_weight * 25.0

        # Factor 3: Market Viability / Category Budget (Weight: 20 points)
        cats = [c.lower() for c in (business_categories or [])]
        if any(any(p in cat for p in PREMIUM_TIER_CATEGORIES) for cat in cats):
            market_score = 20.0
        elif any(any(m in cat for m in MID_TIER_CATEGORIES) for cat in cats):
            market_score = 15.0
        else:
            market_score = 10.0

        # Factor 4: Contactability / Reachability (Weight: 15 points)
        has_phone = bool(business.phone)
        has_email = bool(business.email)
        has_social = bool(business.social_urls)

        if has_phone and has_email:
            contact_score = 15.0
        elif has_phone or has_email:
            contact_score = 11.0
        elif has_social:
            contact_score = 8.0
        else:
            contact_score = 5.0

        total_score = round(severity_score + fit_score + market_score + contact_score, 1)
        total_score = min(max(total_score, 0.0), 100.0)

        # Priority mapping
        if total_score >= 80.0:
            priority = OpportunityPriority.CRITICAL
        elif total_score >= 65.0:
            priority = OpportunityPriority.HIGH
        elif total_score >= 45.0:
            priority = OpportunityPriority.MEDIUM
        else:
            priority = OpportunityPriority.LOW

        breakdown = {
            "need_severity": round(severity_score, 1),
            "service_fit": round(fit_score, 1),
            "market_viability": round(market_score, 1),
            "contactability": round(contact_score, 1),
            "total": total_score,
        }

        return ScoredOpportunity(
            score=total_score,
            priority=priority,
            confidence=0.92,
            score_breakdown=breakdown,
        )

</file>

<file path="E:/tmp/Siteblitz_LeadGenerator/README.md">
# SiteBlitz Lead Intelligence OS

Internal sales intelligence and customer acquisition platform for web/mobile development agencies.

## Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL 16+
- Redis 7+
- Node.js 20+ (for frontend)

### Backend Setup
```bash
# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# Install dependencies
pip install -e ".[dev]"

# Configure environment
copy .env.example .env
# Edit .env with your database credentials

# Run migrations
alembic upgrade head

# Start API server
uvicorn backend.app.main:app --reload --port 8000
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## Architecture
See [Project Blueprint](docs/architecture.md) for full architecture documentation.

## Phase Status
- **Phase 1**: Discovery Engine — 🔄 In Progress
- **Phase 2**: Opportunity Engine — ⏳ Pending Phase 1 Approval
- **Phase 3**: Enrichment Engine — ⏳ Pending Phase 2 Approval
- **Phase 4**: Qualification Engine — ⏳ Pending Phase 3 Approval
- **Phase 5**: Conversion Engine — ⏳ Pending Phase 4 Approval

</file>
</project_context>

<topic>
# Topic — SiteBlitz Lead Generator: audit findings, scraping + website-need logic, UI flow

## The founder's words (translated from Hinglish)
"This is my lead generator engine. Analyse everything word by word. It has many problems — UI logic,
output not coming properly, not reliable, not efficient, not effective. The data is not extracted /
scraped properly. It should scrape Google Maps, and Instagram, Facebook, LinkedIn, TikTok or other
social platforms of a particular country, for a particular business. The main motive is not just to
scrape businesses but to UNDERSTAND them: find out which businesses actually need a website. Only if
yes should they come into HOT. The UI is very bad — I can't understand where to start, how the flow
goes. Backend APIs may be broken. ChatGPT is my assistant who knows many things; Claude knows the real
development."

The founder runs SiteBlitz, a small web studio in India that sells websites (domestic and
international clients). The tool is internal: find small businesses that truly need a website and
contact them.

## Important difference from your system prompt
This round Claude Code HAS read every file of the repository and RAN the code (unit tests + a live
end-to-end probe against the real API on SQLite + live Overpass calls). The evidence file below is
verified, not README claims. File:line references point to the repo.

## Agenda
1. Data sources: replace the broken OSM-only discovery with Google Places API (New) as the primary "Google Maps" source, OSM as free fallback, CSV as manual import — and NO direct scraping of Google Maps HTML or logged-in social platforms (Instagram, Facebook, LinkedIn, TikTok).
2. Social presence: detect a business's Instagram / Facebook / LinkedIn / TikTok links only from lawful signals (Places websiteUri pointing to a social profile, OSM contact:* tags, links on the business's own site) — is that enough, or is there a lawful source we are missing?
3. "Does this business need a website?" — replace the current rule (no website field => CRITICAL) with a verified Website-Need verdict: verify the website is really missing (Places websiteUri, OSM tags, domain-guess DNS check, dead/parked/link-in-bio detection), exclude chains / government / religious / ATMs, require the business to be operating and active.
4. Scoring + tiers: an explainable 0–100 Website Need Score with HOT / WARM / COLD / SKIP tiers and fixed thresholds; every point traced to evidence; no fake confidence.
5. Pipeline order: no-website leads have no email, so today they can never reach "qualified". Make phone / WhatsApp a first-class outreach channel and stop fabricating info@domain contacts.
6. Reliability: long network work runs inside HTTP requests today; move discovery + evaluation to background jobs with progress polling; SQLite as zero-setup default, Postgres optional.
7. UI flow + deletions: replace the 8 engine-named pages with a 4-step workflow (Find → Review → Hot leads → Outreach); delete or hide the parts that pretend (simulated sending, fake sender identity, fabricated pitch claims, Wikidata source, auto "Mobile App" opportunities).

## What Claude Code proposes for point 3–4 (challenge it)
Website Need Score (0–100), computed only from stored evidence:
- Presence evidence (max 45): no website anywhere after verification 45; website field is a social
  profile / link-in-bio (instagram, facebook, linktr.ee, wa.me) 40; listed website dead (DNS fail /
  connection refused / 5xx / parked / "coming soon") 38; old Google "business.site" URL 40; website
  works but not mobile-friendly or no HTTPS 20; works and modern 0.
- Business is real and active (max 25): operational status confirmed 10; review count >= 10 → 10,
  >= 3 → 6; rating present 5.
- Reachable (max 15): phone 10; email 3; any social link 2.
- Category website-ROI (max 15): high (clinics, dentists, salons, restaurants, hotels, gyms, coaching,
  lawyers, CAs, real estate, interior designers, trades) 15; medium (retail shops) 9; low 4.
- SKIP (score forced to 0, never shown as a lead): chain/brand (OSM brand / brand:wikidata tag, or the
  same name in >= 3 places in the run), ATM / fuel / bank branch / place of worship / government /
  school-university-hospital, permanently closed.
- Tiers: HOT >= 75, WARM 55–74, COLD < 55, SKIP. HOT additionally REQUIRES presence evidence >= 38
  (i.e. verified no real website) AND a phone number.

Answer each agenda point by number: agree / disagree because ... / need data: ... . End with the list
of points still open.
</topic>
