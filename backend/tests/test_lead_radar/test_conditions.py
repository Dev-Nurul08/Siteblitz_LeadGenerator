"""
Tests for Lead-Radar Section 3: 51 Condition Library (G, W, I, D, C, J).
"""

import pytest
from backend.app.engines.lead_radar.conditions import ConditionEvaluator
from backend.app.engines.lead_radar.types import (
    Authority,
    Availability,
    ConditionID,
    CustomerTaskCovered,
    OwnedPresence,
    SixFacts,
    TaskQuality,
    BuyingStatus,
)


def test_gates_evaluation():
    facts = SixFacts(
        authority=Authority.LOCAL_OWNER,
        currently_active=True,
    )
    raw_signals = {
        "official_reg_id": "CIN-U12345MH2021PTC123456",
        "category": "Software Agency",
        "is_duplicate_entity": False,
        "is_non_procuring_object": False,
        "owner_confirmed_closed": False,
        "closure_sources_count": 0,
        "centralized_digital_mandate": False,
        "independent_activity_signals_90d": 3,
    }

    conds = ConditionEvaluator.evaluate_all(facts, raw_signals)

    # G1: identity verified via official reg id
    assert conds[ConditionID.G1].is_met is True
    # G2: evidence usable
    assert conds[ConditionID.G2].is_met is True
    # G3: not duplicate
    assert conds[ConditionID.G3].is_met is True
    # G4: not landmark or ATM
    assert conds[ConditionID.G4].is_met is True
    # G5: closed for good
    assert conds[ConditionID.G5].is_met is False
    # G6: branch cannot buy
    assert conds[ConditionID.G6].is_met is False
    # G7: operating now
    assert conds[ConditionID.G7].is_met is True


def test_non_procuring_body_disqualification():
    facts = SixFacts()
    raw_signals = {
        "category": "Automated Teller Machine (ATM)",
        "is_non_procuring_object": True,
    }
    conds = ConditionEvaluator.evaluate_all(facts, raw_signals)
    assert conds[ConditionID.G4].is_met is False


def test_website_conditions_w1_w6():
    facts = SixFacts(
        owned_presence=OwnedPresence.NONE_FOUND,
        absence_search_done=True,
        availability=Availability.REPEATED_SERVER_FAIL,
        repeated_failure=True,
        task_quality=TaskQuality.FAILS_REPRODUCIBLY,
    )
    raw_signals = {
        "needed_task_unhosted": True,
        "ssl_cert_invalid": True,
        "mobile_task_failed_2_screens": True,
    }
    conds = ConditionEvaluator.evaluate_all(facts, raw_signals)

    assert conds[ConditionID.W1].is_met is True
    assert conds[ConditionID.W2].is_met is True
    assert conds[ConditionID.W3].is_met is True
    assert conds[ConditionID.W4].is_met is True
    assert conds[ConditionID.W5].is_met is True
    assert conds[ConditionID.W6].is_met is True


def test_crux_performance_w11():
    facts = SixFacts()
    # Good performance -> not met
    conds_good = ConditionEvaluator.evaluate_all(facts, {"crux_lcp": 2.1, "crux_inp": 120, "crux_cls": 0.05})
    assert conds_good[ConditionID.W11].is_met is False

    # Poor performance in Google poor band -> met
    conds_poor = ConditionEvaluator.evaluate_all(facts, {"crux_lcp": 5.4, "crux_inp": 600, "crux_cls": 0.35})
    assert conds_poor[ConditionID.W11].is_met is True


def test_accessibility_barrier_w13():
    facts = SixFacts()
    conds = ConditionEvaluator.evaluate_all(facts, {"keyboard_task_impossible": True})
    assert conds[ConditionID.W13].is_met is True


def test_intent_conditions_i1_i4():
    facts = SixFacts(authority=Authority.LOCAL_OWNER)
    raw_signals = {
        "public_request_website_help_30d": True,
        "open_website_tender": True,
        "evaluating_suppliers_proposals_30d": True,
        "wants_to_replace_supplier": True,
    }
    conds = ConditionEvaluator.evaluate_all(facts, raw_signals)
    assert conds[ConditionID.I1].is_met is True
    assert conds[ConditionID.I2].is_met is True
    assert conds[ConditionID.I3].is_met is True
    assert conds[ConditionID.I4].is_met is True


def test_demand_conditions_d1_d5():
    facts = SixFacts(
        owned_presence=OwnedPresence.NONE_FOUND,
        absence_search_done=True,
    )
    raw_signals = {
        "active_ad_campaign_7d": True,
        "needed_task_unhosted": True,  # triggers W2, so D1 is satisfied
        "unanswered_customer_requests_90d": 4,  # D2 (>=3)
        "reviews_count_90d": 15,  # D3 (>=10)
        "promotions_count_90d": 3,  # D4 (>=2)
        "direct_sales_requests_count": 5,  # D5
    }
    conds = ConditionEvaluator.evaluate_all(facts, raw_signals)
    assert conds[ConditionID.D1].is_met is True
    assert conds[ConditionID.D2].is_met is True
    assert conds[ConditionID.D3].is_met is True
    assert conds[ConditionID.D4].is_met is True
    assert conds[ConditionID.D5].is_met is True


def test_stop_conditions_c1_c6():
    facts = SixFacts(
        buying_status=BuyingStatus.EXPLICITLY_NOT_SEEKING,
    )
    conds = ConditionEvaluator.evaluate_all(facts, {})
    assert conds[ConditionID.C1].is_met is True

