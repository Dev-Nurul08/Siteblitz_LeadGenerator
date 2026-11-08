"""
Tests for Lead-Radar Section 10 (Absence Certificate) and Section 11 (Regions & Baselines).
"""

import pytest

from backend.app.engines.lead_radar.absence import AbsenceSearchEngine
from backend.app.engines.lead_radar.regions import (
    OVERTURE_45_CITY_BASELINES,
    RegionalCalibrationEngine,
)
from backend.app.engines.lead_radar.types import OwnedPresence


def test_absence_certificate_generation():
    is_absent, presence, cert = AbsenceSearchEngine.execute_3path_search(
        business_id=101,
        business_name="Shivaji Sweets",
        country_code="IN",
        city="Mumbai",
        aliases=["Shivaji Mithai"],
        local_script_names=["शिवाजी मिठाई"],
        social_profiles=["https://facebook.com/shivajisweets"],
        email_addresses=["contact@gmail.com"],
    )

    assert is_absent is True
    assert presence == OwnedPresence.SOCIAL_ONLY
    assert cert.certificate_id.startswith("CERT-ABS-")
    assert cert.is_truly_absent is True
    assert len(cert.signature_hash) == 64  # SHA-256
    assert len(cert.queries_executed) >= 2


def test_45_city_baselines_lookup():
    mumbai = RegionalCalibrationEngine.get_city_baseline("mumbai")
    assert mumbai is not None
    assert mumbai.places == 148298
    assert mumbai.confident_places == 48744
    assert mumbai.confident_no_website_pct == 24.5

    dallas = RegionalCalibrationEngine.get_city_baseline("Dallas")
    assert dallas is not None
    assert dallas.confident_no_website_pct == 15.9

    london = RegionalCalibrationEngine.get_city_baseline("London")
    assert london is not None
    assert london.confident_no_website_pct == 10.6


def test_regional_profiles_priority_conditions():
    mh = RegionalCalibrationEngine.get_profile("IN", "IN-MH")
    assert mh.region_name == "Maharashtra"
    assert mh.baseline_no_website_percent == 24.5
    assert len(mh.check_first) > 0

    de = RegionalCalibrationEngine.get_profile("DE")
    assert de.region_name == "Germany"
    assert "Handelsregister" in de.local_sources


def test_empirical_sample_size_blending():
    # Sample >= 200: local rate
    rate_large = RegionalCalibrationEngine.calibrate_cohort_rate(
        local_sample_size=300,
        local_positive_count=60,
        parent_rate=0.10,
    )
    assert rate_large == pytest.approx(0.20, abs=0.001)

    # Sample 50-199: blended with parent
    rate_mid = RegionalCalibrationEngine.calibrate_cohort_rate(
        local_sample_size=100,
        local_positive_count=20,
        parent_rate=0.10,
    )
    # weight on local = 100 / (100 + 200) = 1/3; local rate = 0.20; parent = 0.10 -> 0.1333
    assert rate_mid == pytest.approx(0.1333, abs=0.01)

    # Sample < 50: parent rate
    rate_small = RegionalCalibrationEngine.calibrate_cohort_rate(
        local_sample_size=20,
        local_positive_count=5,
        parent_rate=0.15,
    )
    assert rate_small == 0.15

