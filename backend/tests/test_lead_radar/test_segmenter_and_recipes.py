"""
Tests for Lead-Radar Section 4 (Decision Order & Conflicts) and Section 6 (17 Recipes).
"""

import pytest
from backend.app.engines.lead_radar.conditions import ConditionEvaluator
from backend.app.engines.lead_radar.segmenter import LeadRadarSegmenter
from backend.app.engines.lead_radar.types import (
    Authority,
    Availability,
    ConditionID,
    CustomerTaskCovered,
    OwnedPresence,
    RecipeID,
    Segment,
    SixFacts,
    TaskQuality,
    BuyingStatus,
)


def test_segment_a_open_mandate():
    facts = SixFacts(
        authority=Authority.LOCAL_OWNER,
        currently_active=True,
    )
    raw_signals = {
        "official_reg_id": "REG-123",
        "public_request_website_help_30d": True,
        "requested_scope": "e-commerce ordering system",
        "request_date": "2026-11-01",
    }
    conds = ConditionEvaluator.evaluate_all(facts, raw_signals)
    segment, warm, recipes, pitch = LeadRadarSegmenter.evaluate_segment_and_recipes(
        facts, conds, raw_signals
    )

    assert segment == Segment.A
    assert len(recipes) >= 1
    assert recipes[0].recipe_id == RecipeID.R1
    assert "You need a website" in recipes[0].never_say
    assert "Your request on 2026-11-01" in pitch["opening_fact"]


def test_segment_b_founders_case_r4():
    facts = SixFacts(
        owned_presence=OwnedPresence.NONE_FOUND,
        absence_search_done=True,
        authority=Authority.LOCAL_OWNER,
        currently_active=True,
    )
    raw_signals = {
        "official_reg_id": "REG-MUMBAI-99",
        "needed_task_unhosted": True,
        "promotions_count_90d": 4,
        "independent_activity_signals_90d": 2,
        "current_destination": "Instagram Bio Link",
        "missing_task_name": "table booking",
    }
    conds = ConditionEvaluator.evaluate_all(facts, raw_signals)
    segment, warm, recipes, pitch = LeadRadarSegmenter.evaluate_segment_and_recipes(
        facts, conds, raw_signals
    )

    assert segment == Segment.B
    matched_ids = [r.recipe_id for r in recipes]
    assert RecipeID.R4 in matched_ids
    assert "Your active promotions send customers to" in pitch["opening_fact"]


def test_warm_context_something_in_motion_r17():
    facts = SixFacts(
        availability=Availability.COMING_SOON,
        authority=Authority.LOCAL_OWNER,
        currently_active=True,
    )
    raw_signals = {
        "official_reg_id": "REG-WARM-1",
        "has_coming_soon_page": True,
        "promotions_count_90d": 3,
        "independent_activity_signals_90d": 2,
        "motion_signal": "new coming-soon page",
    }
    conds = ConditionEvaluator.evaluate_all(facts, raw_signals)
    segment, warm, recipes, pitch = LeadRadarSegmenter.evaluate_segment_and_recipes(
        facts, conds, raw_signals
    )

    assert warm is True
    matched_ids = [r.recipe_id for r in recipes]
    assert RecipeID.R17 in matched_ids
    assert "We know you're looking" in pitch["never_say"]


def test_stop_segment_c_supplier_already_appointed_r16():
    facts = SixFacts(
        buying_status=BuyingStatus.SUPPLIER_ALREADY_CHOSEN,
        availability=Availability.COMING_SOON,
    )
    raw_signals = {
        "official_reg_id": "REG-STOP-01",
        "agency_already_appointed": True,
        "has_coming_soon_page": True,
    }
    conds = ConditionEvaluator.evaluate_all(facts, raw_signals)
    segment, warm, recipes, pitch = LeadRadarSegmenter.evaluate_segment_and_recipes(
        facts, conds, raw_signals
    )

    assert segment == Segment.C
    matched_ids = [r.recipe_id for r in recipes]
    assert RecipeID.R16 in matched_ids


def test_conflict_parent_controls_digital():
    facts = SixFacts(
        authority=Authority.FRANCHISEE,
    )
    raw_signals = {
        "official_reg_id": "REG-BRANCH",
        "centralized_digital_mandate": True,
    }
    conds = ConditionEvaluator.evaluate_all(facts, raw_signals)
    segment, warm, recipes, pitch = LeadRadarSegmenter.evaluate_segment_and_recipes(
        facts, conds, raw_signals
    )

    assert segment == Segment.C
    assert "parent" in pitch["opening_fact"].lower()


def test_ad_leads_to_broken_page_r6():
    facts = SixFacts(
        task_quality=TaskQuality.FAILS_REPRODUCIBLY,
        currently_active=True,
    )
    raw_signals = {
        "official_reg_id": "REG-AD-01",
        "active_ad_campaign_7d": True,
        "core_flow_broken": True,
        "ad_network": "Meta Ads",
        "ad_destination_url": "https://example.com/checkout",
        "action_error": "500 Server Error upon card entry",
    }
    conds = ConditionEvaluator.evaluate_all(facts, raw_signals)
    segment, warm, recipes, pitch = LeadRadarSegmenter.evaluate_segment_and_recipes(
        facts, conds, raw_signals
    )

    assert segment == Segment.B
    matched_ids = [r.recipe_id for r in recipes]
    assert RecipeID.R6 in matched_ids
    assert "500 Server Error" in pitch["opening_fact"]

