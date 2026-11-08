"""
Opportunity Scorer module (Phase 2).

Evaluates detected needs, business profiles, and contactability signals
to generate a weighted opportunity score (0 to 100), commercial priority level,
confidence rating, and estimated deal value ranges.
"""

from dataclasses import dataclass
from typing import Optional

from backend.app.engines.opportunity.detector import DetectedNeed
from backend.app.models.business import Business
from backend.app.models.opportunity import OpportunityPriority, ServiceCategory

# ─── Commercial Tiers & Budget Capacity ─────────────────────────────────────

PREMIUM_TIER_CATEGORIES = {
    "dentist", "doctor", "clinic", "hospital", "medical", "dermatology",
    "orthodontist", "optician", "physiotherapy",
    "lawyer", "legal", "solicitor", "barrister", "notary",
    "accountant", "accounting", "financial", "wealth_management",
    "architect", "consulting", "it_services", "software", "engineering",
    "estate_agent", "real_estate", "property", "mortgage_broker",
    "hotel", "resort", "boutique_hotel",
    "insurance", "bank", "investment",
    "private_school", "university",
    "veterinary",
}

MID_TIER_CATEGORIES = {
    "restaurant", "cafe", "bar", "pub", "bistro", "wine_bar",
    "gym", "fitness", "crossfit", "yoga_studio", "pilates",
    "spa", "salon", "hairdresser", "barber", "beauty",
    "car_repair", "car_dealer", "mechanic", "car_wash",
    "supermarket", "retail", "shop", "jewelry", "fashion",
    "photography", "wedding", "event_planning",
    "pharmacy", "optical",
    "co_working", "office_rental",
}

# Regional purchasing power & agency fee multipliers
COUNTRY_VALUE_MULTIPLIERS: dict[str, float] = {
    "US": 1.30, "GB": 1.20, "CA": 1.20, "AU": 1.20, "DE": 1.15,
    "CH": 1.40, "AE": 1.45, "SG": 1.30, "FR": 1.10, "NL": 1.10,
    "SE": 1.15, "NO": 1.20, "DK": 1.15, "NZ": 1.10, "IE": 1.10,
    "AT": 1.10, "BE": 1.05, "IT": 1.00, "ES": 0.95, "PT": 0.90,
    "PL": 0.85, "CZ": 0.85, "IN": 0.70, "PH": 0.65, "NG": 0.60,
    "KE": 0.60,
}

# Agency service alignment weight (0.0 to 1.0)
SERVICE_FIT_WEIGHTS: dict[ServiceCategory, float] = {
    ServiceCategory.NEW_WEBSITE: 1.0,
    ServiceCategory.WEBSITE_REDESIGN: 1.0,
    ServiceCategory.CUSTOM_WEB_APP: 0.95,
    ServiceCategory.MOBILE_APP: 0.90,
    ServiceCategory.ECOMMERCE_EXPANSION: 0.85,
    ServiceCategory.ONLINE_BOOKING: 0.80,
    ServiceCategory.SEO_PERFORMANCE: 0.75,
}

# Baseline project engagement value ranges (USD)
SERVICE_BASE_VALUES_USD: dict[ServiceCategory, tuple[float, float]] = {
    ServiceCategory.NEW_WEBSITE: (3000.0, 12000.0),
    ServiceCategory.WEBSITE_REDESIGN: (3500.0, 15000.0),
    ServiceCategory.CUSTOM_WEB_APP: (12000.0, 45000.0),
    ServiceCategory.MOBILE_APP: (15000.0, 50000.0),
    ServiceCategory.ECOMMERCE_EXPANSION: (5000.0, 25000.0),
    ServiceCategory.ONLINE_BOOKING: (2500.0, 8000.0),
    ServiceCategory.SEO_PERFORMANCE: (1800.0, 6000.0),
}


# ─── Dataclass ──────────────────────────────────────────────────────────────

@dataclass
class ScoredOpportunity:
    """Scored evaluation of a detected agency sales opportunity."""

    score: float  # 0.0 to 100.0
    priority: OpportunityPriority
    confidence: float  # 0.0 to 1.0
    score_breakdown: dict
    estimated_value_low: float
    estimated_value_high: float
    recommended_action: str
    roi_summary: str


# ─── OpportunityScorer ──────────────────────────────────────────────────────

class OpportunityScorer:
    """
    Computes a composite multi-factor score and economic prioritization for detected opportunities.
    """

    def score_need(
        self,
        need: DetectedNeed,
        business: Business,
        business_categories: Optional[list[str]] = None,
    ) -> ScoredOpportunity:
        """
        Calculate weighted score (0–100), commercial priority, and ROI metrics for a detected need.
        """
        # Factor 1: Need Severity (Weight: 40 points)
        severity_score = min(max(need.need_severity, 0.0), 1.0) * 40.0

        # Factor 2: Agency Service Division Fit (Weight: 25 points)
        service_weight = SERVICE_FIT_WEIGHTS.get(need.service_category, 0.70)
        fit_score = service_weight * 25.0

        # Factor 3: Market Viability / Category Budget (Weight: 20 points)
        cats = [c.lower() for c in (business_categories or [])]
        is_premium = any(any(p in cat for p in PREMIUM_TIER_CATEGORIES) for cat in cats)
        is_mid = any(any(m in cat for m in MID_TIER_CATEGORIES) for cat in cats)

        if is_premium:
            market_score = 20.0
            category_multiplier = 1.5
        elif is_mid:
            market_score = 15.0
            category_multiplier = 1.0
        else:
            market_score = 10.0
            category_multiplier = 0.75

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

        # Confidence Rating
        confidence = 0.70
        if has_email:
            confidence += 0.12
        if has_phone:
            confidence += 0.08
        if has_social:
            confidence += 0.04
        confidence = min(round(confidence, 2), 0.98)

        # Valuation Calculation
        country_code = (business.country_code or "").upper()
        country_mult = COUNTRY_VALUE_MULTIPLIERS.get(country_code, 1.0)
        base_low, base_high = SERVICE_BASE_VALUES_USD.get(
            need.service_category, (3000.0, 10000.0)
        )
        val_multiplier = category_multiplier * country_mult
        est_low = round((base_low * val_multiplier) / 100.0) * 100.0
        est_high = round((base_high * val_multiplier) / 100.0) * 100.0

        # Action and ROI Summary
        if priority == OpportunityPriority.CRITICAL:
            rec_action = "Immediate custom outreach — high budget, critical need, verified contacts"
        elif priority == OpportunityPriority.HIGH:
            rec_action = "Priority outreach batch within 48h — strong service fit and clear value gap"
        elif priority == OpportunityPriority.MEDIUM:
            rec_action = "Standard outreach queue — qualified prospect with steady conversion potential"
        else:
            rec_action = "Add to automated nurture campaign — monitor for triggering digital events"

        roi_summary = (
            f"Estimated project value of ${est_low:,.0f}–${est_high:,.0f} USD. "
            f"Implementation typically delivers 35–60% increase in digital conversions."
        )

        breakdown = {
            "need_severity": round(severity_score, 1),
            "service_fit": round(fit_score, 1),
            "market_viability": round(market_score, 1),
            "contactability": round(contact_score, 1),
            "total": total_score,
            "country_multiplier": country_mult,
        }

        return ScoredOpportunity(
            score=total_score,
            priority=priority,
            confidence=confidence,
            score_breakdown=breakdown,
            estimated_value_low=est_low,
            estimated_value_high=est_high,
            recommended_action=rec_action,
            roi_summary=roi_summary,
        )
