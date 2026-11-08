"""
Opportunity Detector module (Phase 2).

Synthesizes business categories, website audit metrics, and reachability signals
to identify concrete digital service needs matching the agency's 7 service divisions:
- NEW_WEBSITE
- WEBSITE_REDESIGN
- MOBILE_APP
- ONLINE_BOOKING
- ECOMMERCE_EXPANSION
- SEO_PERFORMANCE
- CUSTOM_WEB_APP
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
    estimated_value_usd: Optional[float] = None
    urgency_level: str = "STANDARD"  # IMMEDIATE, HIGH, STANDARD
    competitive_advantage: Optional[str] = None


# ─── Target Categories ──────────────────────────────────────────────────────

# High-frequency customer interaction businesses where native/PWA mobile apps drive loyalty & repeat GMV
MOBILE_APP_CANDIDATE_CATEGORIES = {
    "restaurant", "cafe", "fast_food", "food_court", "bistro", "bakery", "bar", "pub",
    "gym", "fitness", "crossfit", "yoga_studio", "pilates", "dance_studio", "martial_arts",
    "spa", "salon", "hairdresser", "barber", "beauty", "cosmetics", "nail_salon",
    "clinic", "dentist", "medical", "pharmacy", "dermatology", "physiotherapy",
    "supermarket", "convenience", "clothing", "fashion", "boutique",
    "delivery", "transport", "hotel", "resort", "car_wash", "laundry", "dry_cleaning",
    "veterinary", "pet_grooming", "daycare", "tutoring", "coworking",
}

# Businesses where digital scheduling / reservation is standard customer expectation
BOOKING_CANDIDATE_CATEGORIES = {
    "dentist", "clinic", "doctors", "optician", "physiotherapy", "chiropractor", "therapy",
    "salon", "hairdresser", "barber", "spa", "beauty", "massage", "tattoo", "piercing",
    "restaurant", "hotel", "resort", "guest_house", "event_venue",
    "lawyer", "legal", "accountant", "accounting", "consulting", "financial_advisor",
    "car_repair", "mechanic", "car_wash", "veterinary", "photographer", "personal_trainer",
    "driving_school", "tutor",
}

# Businesses selling physical or digital products where e-commerce unlocks nationwide reach
ECOMMERCE_CANDIDATE_CATEGORIES = {
    "retail", "shop", "supermarket", "convenience", "clothes", "clothing", "fashion",
    "electronics", "furniture", "hardware", "jewelry", "bookshop", "books",
    "bakery", "butcher", "florist", "gift", "pet", "shoes", "sports", "toys",
    "stationery", "craft", "art_gallery", "wine", "delicatessen", "pharmacy", "organic_food",
}

# Complex organizations that benefit from custom workflow web apps, client portals, and multi-location systems
CUSTOM_WEB_APP_CATEGORIES = {
    "hospital", "university", "college", "school", "logistics", "freight", "warehousing",
    "real_estate", "estate_agent", "property_management", "insurance", "bank", "financial",
    "franchise", "multi_location", "wholesale", "manufacturing", "construction",
    "coworking", "membership", "association", "trade_union",
}


# ─── OpportunityDetector ────────────────────────────────────────────────────

class OpportunityDetector:
    """
    Evaluates business records and technical audit findings to discover high-value agency opportunities.
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

        # ── Case 1: No Website / Social-Only -> Brand New Website ────────────
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
                "categories": categories,
            }
            if is_social_only:
                summary = (
                    f"{business.name} operates exclusively through social media channels without an "
                    f"owned official website. This creates high vulnerability to algorithm changes, "
                    f"hurts Google local discovery, and prevents automated checkout and bookings."
                )
                pitch = [
                    "Stop losing 70% of high-intent Google search customers to competitors who have websites",
                    "Convert social followers into direct paying clients on an owned, brand-controlled domain",
                    "Establish verified Google Maps Local Business ranking and domain authority",
                    "Enable 24/7 automated inquiry capture and client lead qualification",
                ]
            else:
                summary = (
                    f"{business.name} has no detectable digital web presence. In {business.country_code or 'their market'}, "
                    f"launching a high-performance modern website provides an immediate competitive advantage."
                )
                pitch = [
                    "Build a professional digital storefront that captures local and regional customers 24/7",
                    "Establish instant brand legitimacy and trust for prospective commercial partners",
                    "Showcase services, pricing, customer testimonials, and direct booking mechanisms",
                    "Dominate local search engine rankings before competing businesses saturate the area",
                ]

            needs.append(
                DetectedNeed(
                    service_category=ServiceCategory.NEW_WEBSITE,
                    title=f"Custom High-Converting Website for {business.name}",
                    summary=summary,
                    evidence=evidence,
                    pitch_angles=pitch,
                    need_severity=0.95,
                    estimated_value_usd=4500.0,
                    urgency_level="IMMEDIATE",
                    competitive_advantage="Instant market credibility and organic local customer acquisition.",
                )
            )

        # ── Case 2: Website Exists -> Deep Audit Opportunities ────────────────
        if audit and resolution and resolution.is_reachable:
            # ─────────────────────────────────────────────────────────────
            # A) WEBSITE_REDESIGN Opportunity
            # ─────────────────────────────────────────────────────────────
            redesign_reasons = []
            if not audit.is_mobile_responsive:
                redesign_reasons.append("Missing mobile viewport configuration (fails on 65%+ of smartphone traffic)")
            if not resolution.has_ssl:
                redesign_reasons.append("Lacks HTTPS / valid SSL certificate (displays 'Not Secure' browser warnings)")
            if resolution.load_time_seconds and resolution.load_time_seconds > 3.0:
                redesign_reasons.append(f"Slow initial page response ({resolution.load_time_seconds}s load time)")
            if audit.detected_cms in ["Joomla", "Drupal", "Weebly"]:
                redesign_reasons.append(f"Outdated legacy CMS platform ({audit.detected_cms}) with security risks")
            if audit.has_mixed_content:
                redesign_reasons.append("Insecure mixed-content elements detected over HTTP")
            if audit.accessibility_issues and len(audit.accessibility_issues) >= 2:
                redesign_reasons.append(f"{len(audit.accessibility_issues)} accessibility & compliance violations")
            if audit.dom_element_count > 1500:
                redesign_reasons.append(f"Excessive DOM complexity ({audit.dom_element_count} nodes) causing rendering lag")

            if redesign_reasons:
                severity = 0.90 if (not audit.is_mobile_responsive or not resolution.has_ssl) else 0.75
                needs.append(
                    DetectedNeed(
                        service_category=ServiceCategory.WEBSITE_REDESIGN,
                        title=f"Modern Responsive Redesign & Architecture Upgrade for {business.name}",
                        summary=(
                            f"Technical inspection of {resolution.final_url or resolution.original_url} uncovered "
                            f"{len(redesign_reasons)} critical flaws: {'; '.join(redesign_reasons[:3])}."
                        ),
                        evidence={
                            "reasons": redesign_reasons,
                            "mobile_responsive": audit.is_mobile_responsive,
                            "has_ssl": resolution.has_ssl,
                            "load_time_seconds": resolution.load_time_seconds,
                            "detected_cms": audit.detected_cms,
                            "mixed_content": audit.has_mixed_content,
                            "accessibility_issue_count": len(audit.accessibility_issues),
                        },
                        pitch_angles=[
                            "Over 65% of customer traffic is mobile — non-responsive design causes immediate user bounce",
                            "Eliminate damaging browser 'Not Secure' warnings with modern SSL and HSTS encryption",
                            "Migrate from legacy clunky CMS to a blistering-fast, modern tech stack (Next.js / Webflow / Headless)",
                            "Double website visitor conversion rate by modernizing UX and eliminating load lag",
                        ],
                        need_severity=severity,
                        estimated_value_usd=6000.0,
                        urgency_level="HIGH" if not audit.is_mobile_responsive else "STANDARD",
                        competitive_advantage="Drastic performance leap, ADA accessibility compliance, and mobile conversion surge.",
                    )
                )

            # B) Mobile Application: removed (spec website-intelligence.md row 18). A category is
            # not evidence that a business needs an app; every reachable restaurant/clinic used
            # to get a CRITICAL "Mobile App" opportunity.

            # ─────────────────────────────────────────────────────────────
            # C) ONLINE_BOOKING Opportunity
            # ─────────────────────────────────────────────────────────────
            is_booking_target = any(
                any(cand in cat for cand in BOOKING_CANDIDATE_CATEGORIES)
                for cat in categories
            )
            if is_booking_target and not audit.has_online_booking:
                needs.append(
                    DetectedNeed(
                        service_category=ServiceCategory.ONLINE_BOOKING,
                        title=f"Automated 24/7 Online Booking & Scheduling System for {business.name}",
                        summary=(
                            f"{business.name} operates an appointment-driven business model, but currently lacks an "
                            f"interactive digital scheduling engine on its website, causing missed after-hours reservations."
                        ),
                        evidence={
                            "has_booking_widget": False,
                            "matched_categories": categories,
                            "has_contact_form": audit.has_contact_form,
                        },
                        pitch_angles=[
                            "Capture appointment bookings 24/7, especially after hours when 42% of online consumers schedule services",
                            "Slash front-desk phone tag and manual administrative scheduling overhead by up to 75%",
                            "Automated SMS and email reminders that virtually eliminate costly client no-shows",
                            "Seamless calendar synchronization with Google Calendar, Outlook, and CRM workflows",
                        ],
                        need_severity=0.85,
                        estimated_value_usd=3500.0,
                        urgency_level="HIGH",
                        competitive_advantage="Immediate capture of high-intent bookings around the clock.",
                    )
                )

            # ─────────────────────────────────────────────────────────────
            # D) ECOMMERCE_EXPANSION Opportunity
            # ─────────────────────────────────────────────────────────────
            is_ecommerce_target = any(
                any(cand in cat for cand in ECOMMERCE_CANDIDATE_CATEGORIES)
                for cat in categories
            )
            if is_ecommerce_target and not audit.has_ecommerce:
                needs.append(
                    DetectedNeed(
                        service_category=ServiceCategory.ECOMMERCE_EXPANSION,
                        title=f"E-Commerce Storefront & Digital Ordering Engine for {business.name}",
                        summary=(
                            f"{business.name} operates in product retail/catalog sales, but lacks a digital storefront "
                            f"or checkout cart, limiting sales exclusively to in-store physical foot traffic."
                        ),
                        evidence={
                            "has_ecommerce": False,
                            "matched_categories": categories,
                        },
                        pitch_angles=[
                            "Expand retail revenue beyond geographic walk-ins to nationwide and local home delivery",
                            "Modern friction-free checkout supporting Apple Pay, Google Pay, Klarna, and credit cards",
                            "Automated inventory management, order notifications, and digital shipping label generation",
                            "Leverage search engine product rich-snippets to display stock and pricing right inside Google results",
                        ],
                        need_severity=0.85,
                        estimated_value_usd=7500.0,
                        urgency_level="HIGH",
                        competitive_advantage="Unlocks an uncapped secondary revenue stream running 24/7.",
                    )
                )

            # ─────────────────────────────────────────────────────────────
            # E) SEO_PERFORMANCE Optimization Opportunity
            # ─────────────────────────────────────────────────────────────
            seo_deficiencies = []
            if not audit.meta_title or audit.meta_title_length < 15:
                seo_deficiencies.append("Missing or critically short HTML meta title tag")
            if not audit.meta_description or audit.meta_description_length < 30:
                seo_deficiencies.append("Missing or incomplete meta description for search engine result snippets")
            if audit.headings_summary.get("h1_count", 0) == 0:
                seo_deficiencies.append("Missing H1 heading tag structure")
            elif audit.headings_summary.get("h1_count", 0) > 1:
                seo_deficiencies.append("Multiple H1 tags confusing search crawler hierarchy")
            if not audit.has_analytics:
                seo_deficiencies.append("Zero conversion analytics tracking detected (blind to visitor behavior)")
            if not audit.has_structured_data:
                seo_deficiencies.append("Missing Schema.org structured data (no rich snippet eligibility)")
            if not audit.canonical_url:
                seo_deficiencies.append("Missing canonical link tag (risk of duplicate content penalties)")
            if audit.images_without_alt > 2:
                seo_deficiencies.append(f"{audit.images_without_alt} images missing SEO alt text descriptions")

            if seo_deficiencies:
                severity = 0.80 if len(seo_deficiencies) >= 4 else 0.65
                needs.append(
                    DetectedNeed(
                        service_category=ServiceCategory.SEO_PERFORMANCE,
                        title=f"Search Engine & Performance Optimization Program for {business.name}",
                        summary=(
                            f"Technical SEO and metadata audit revealed {len(seo_deficiencies)} critical visibility blockers "
                            f"preventing high search engine ranking: {'; '.join(seo_deficiencies[:3])}."
                        ),
                        evidence={
                            "deficiencies": seo_deficiencies,
                            "title": audit.meta_title,
                            "title_length": audit.meta_title_length,
                            "has_meta_desc": bool(audit.meta_description),
                            "headings": audit.headings_summary,
                            "has_analytics": audit.has_analytics,
                            "has_structured_data": audit.has_structured_data,
                            "canonical_url": audit.canonical_url,
                        },
                        pitch_angles=[
                            "Fix critical search engine indexing blockers to outrank nearby competitors on Google",
                            "Implement Schema.org LocalBusiness markup to capture Google Maps and Rich Result features",
                            "Optimize click-through rates (CTR) with high-converting titles and metadata snippets",
                            "Deploy transparent analytics tracking to measure real monthly leads and ROI",
                        ],
                        need_severity=severity,
                        estimated_value_usd=2500.0,
                        urgency_level="STANDARD",
                        competitive_advantage="Surpasses competitors in organic Google search without recurring ad spend.",
                    )
                )

            # ─────────────────────────────────────────────────────────────
            # F) CUSTOM_WEB_APP Opportunity (Complex workflows / Portals)
            # ─────────────────────────────────────────────────────────────
            is_custom_app_target = any(
                any(cand in cat for cand in CUSTOM_WEB_APP_CATEGORIES)
                for cat in categories
            )
            if is_custom_app_target:
                needs.append(
                    DetectedNeed(
                        service_category=ServiceCategory.CUSTOM_WEB_APP,
                        title=f"Custom Cloud Portal & Workflow Automation App for {business.name}",
                        summary=(
                            f"As a complex organization in {business.country_code or 'the industry'}, "
                            f"{business.name} can drastically cut operational costs with custom client portals, "
                            f"internal management dashboards, and automated database integrations."
                        ),
                        evidence={
                            "matched_categories": categories,
                            "organization_type": "enterprise_or_institution",
                            "has_website": True,
                        },
                        pitch_angles=[
                            "Automate repetitive operational tasks and eliminate manual spreadsheets with custom software",
                            "Provide clients or members with secure self-service cloud portals for documents, status, and billing",
                            "Integrate legacy databases into a clean, modern web application with real-time reporting",
                            "Scalable enterprise architecture designed specifically around your unique business rules",
                        ],
                        need_severity=0.75,
                        estimated_value_usd=25000.0,
                        urgency_level="STANDARD",
                        competitive_advantage="Massive operational efficiency and proprietary software equity.",
                    )
                )

        return needs
