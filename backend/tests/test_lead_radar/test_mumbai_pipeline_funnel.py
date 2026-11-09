"""
Tests for Lead-Radar Section 1: 8-Stage Mumbai Pipeline Funnel.
"""

import pytest

from backend.app.engines.lead_radar.pipeline import LeadRadarPipeline
from backend.app.services.lead_radar_service import LeadRadarService


def test_mumbai_funnel_execution():
    result = LeadRadarService.run_mumbai_pipeline(
        city="Mumbai",
        country="India",
        confidence_threshold=0.7,
    )

    assert result["total_input_places"] == 100
    counts = result["stage_counts"]
    assert counts["stage_0_all_places"] == 100
    assert counts["stage_1_confident"] > 0
    assert counts["stage_2_no_website_on_file"] > 0
    assert counts["stage_3_reachable"] > 0
    assert counts["stage_4_real_business_g1_g4"] > 0
    assert counts["stage_5_truly_no_site_w1"] > 0
    assert counts["stage_6_alive_and_active_g7"] > 0

    assert len(result["sample_shortlist"]) > 0
    top_lead = result["sample_shortlist"][0]
    assert "name" in top_lead
    assert "pitch_opening_fact" in top_lead
    assert top_lead["rank_opportunity_class"] in [
        "OPEN_MANDATE", "BROKEN_TASK_WITH_DEMAND", "MISSING_TASK_WITH_DEMAND", "RESEARCH_CANDIDATE"
    ]

