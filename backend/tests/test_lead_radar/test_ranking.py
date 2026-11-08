"""
Tests for Lead-Radar Section 8: 6-Tier Deterministic Ranking Engine.
"""

from datetime import datetime, timedelta
import pytest

from backend.app.engines.lead_radar.conditions import ConditionEvaluator
from backend.app.engines.lead_radar.ranking import LeadRadarRanker
from backend.app.engines.lead_radar.types import (
    Authority,
    AuthorityLevel,
    ConditionID,
    DemandLevel,
    EvidenceQuality,
    OpportunityClass,
    SixFacts,
    TaskSeverity,
)


def test_ranking_hierarchy_mandate_beats_broken_task():
    facts_mandate = SixFacts(authority=Authority.LOCAL_OWNER)
    signals_mandate = {
        "public_request_website_help_30d": True,
        "name": "Acme Corp",
    }
    conds_mandate = ConditionEvaluator.evaluate_all(facts_mandate, signals_mandate)
    rank_mandate = LeadRadarRanker.rank_lead(facts_mandate, conds_mandate, [], signals_mandate)

    facts_broken = SixFacts(authority=Authority.LOCAL_OWNER)
    signals_broken = {
        "core_flow_broken": True,
        "active_ad_campaign_7d": True,
        "name": "Beta LLC",
    }
    conds_broken = ConditionEvaluator.evaluate_all(facts_broken, signals_broken)
    rank_broken = LeadRadarRanker.rank_lead(facts_broken, conds_broken, [], signals_broken)

    assert rank_mandate.opportunity_class == OpportunityClass.OPEN_MANDATE
    assert rank_broken.opportunity_class == OpportunityClass.BROKEN_TASK_WITH_DEMAND

    # Mandate must sort higher than broken task regardless of other signals
    sorted_leads = LeadRadarRanker.sort_leads([
        ("beta", rank_broken),
        ("acme", rank_mandate),
    ])
    assert sorted_leads[0][0] == "acme"


def test_four_mandatory_answers():
    facts = SixFacts(
        authority=Authority.UNRESOLVED,
        currently_active=True,
    )
    signals = {
        "name": "Bandra Dental Studio",
        "category": "Clinic",
        "city": "Mumbai",
        "public_request_website_help_30d": True,
    }
    conds = ConditionEvaluator.evaluate_all(facts, signals)
    rank = LeadRadarRanker.rank_lead(facts, conds, [], signals)

    assert "Bandra Dental Studio" in rank.why_this_business
    assert "Active RFP / request open within the past 30 days" in rank.why_now
    assert "Still unknown: purchasing decision-maker identity" in rank.what_is_unknown

