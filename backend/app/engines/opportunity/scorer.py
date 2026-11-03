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
