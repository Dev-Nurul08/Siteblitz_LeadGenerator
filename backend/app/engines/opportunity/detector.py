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
