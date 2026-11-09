"""
Tests for Lead-Radar Section 7: Revenue Estimation Engine.
"""

import pytest
from backend.app.engines.lead_radar.revenue import RevenueEstimationEngine
from backend.app.engines.lead_radar.types import (
    BusinessCategory,
    RevenueConfidence,
)


def test_statutory_filing_high_confidence():
    signals = {
        "filed_annual_revenue": 1_250_000.0,
        "filing_currency": "USD",
        "filing_source": "UK Companies House",
    }
    rev = RevenueEstimationEngine.estimate_revenue(
        BusinessCategory.RESTAURANT, signals, currency="USD"
    )
    assert rev.confidence == RevenueConfidence.HIGH
    assert rev.min_annual_revenue == 1_250_000.0 * 0.95
    assert rev.max_annual_revenue == 1_250_000.0 * 1.05


def test_restaurant_operating_inputs():
    signals = {
        "seats_count": 80,
        "avg_spend_per_cover": 30.0,
        "open_days_per_year": 300,
        "delivery_revenue_share": 0.25,
        "calibrated_rates": True,
    }
    rev = RevenueEstimationEngine.estimate_revenue(
        BusinessCategory.RESTAURANT, signals, currency="USD"
    )
    assert rev.confidence == RevenueConfidence.MEDIUM
    assert rev.min_annual_revenue is not None
    assert rev.max_annual_revenue is not None
    assert rev.min_annual_revenue > 100_000.0
    assert rev.max_annual_revenue > rev.min_annual_revenue


def test_clinic_operating_inputs():
    signals = {
        "doctors_count": 5,
        "realised_consultation_fee": 100.0,
        "open_days_per_year": 260,
        "calibrated_rates": True,
    }
    rev = RevenueEstimationEngine.estimate_revenue(
        BusinessCategory.CLINIC, signals, currency="USD"
    )
    assert rev.confidence == RevenueConfidence.MEDIUM
    assert rev.min_annual_revenue is not None
    assert rev.max_annual_revenue > rev.min_annual_revenue


def test_salon_operating_inputs():
    signals = {
        "staffed_stations_count": 6,
        "average_service_ticket": 50.0,
        "hours_open_per_day": 8.0,
        "calibrated_rates": True,
    }
    rev = RevenueEstimationEngine.estimate_revenue(
        BusinessCategory.SALON, signals, currency="USD"
    )
    assert rev.confidence == RevenueConfidence.MEDIUM
    assert rev.min_annual_revenue > 0


def test_hotel_operating_inputs():
    signals = {
        "rooms_count": 40,
        "avg_room_rate": 150.0,
        "calibrated_rates": True,
    }
    rev = RevenueEstimationEngine.estimate_revenue(
        BusinessCategory.HOTEL, signals, currency="USD"
    )
    assert rev.confidence == RevenueConfidence.MEDIUM
    assert rev.min_annual_revenue > 500_000.0


def test_udyam_micro_small_medium_classification():
    micro_rev = RevenueEstimationEngine.estimate_revenue(
        BusinessCategory.MANUFACTURER_EXPORTER, {"udyam_classification": "MICRO"}
    )
    assert micro_rev.confidence == RevenueConfidence.MEDIUM
    assert micro_rev.max_annual_revenue == 600_000

    small_rev = RevenueEstimationEngine.estimate_revenue(
        BusinessCategory.MANUFACTURER_EXPORTER, {"udyam_classification": "SMALL"}
    )
    assert small_rev.confidence == RevenueConfidence.MEDIUM
    assert small_rev.max_annual_revenue == 6_000_000


def test_review_based_estimation_and_bounds():
    signals = {
        "new_reviews_90d": 25,
        "avg_transaction_ticket": 40.0,
    }
    rev = RevenueEstimationEngine.estimate_revenue(
        BusinessCategory.OTHER, signals, currency="USD"
    )
    assert rev.confidence == RevenueConfidence.LOW
    assert rev.min_annual_revenue is not None
    assert rev.max_annual_revenue > rev.min_annual_revenue


def test_unavailable_fallback():
    signals = {
        "new_reviews_90d": 1,  # Insufficient review velocity
    }
    rev = RevenueEstimationEngine.estimate_revenue(
        BusinessCategory.OTHER, signals, currency="USD"
    )
    assert rev.confidence == RevenueConfidence.UNAVAILABLE
    assert rev.min_annual_revenue is None
    assert rev.max_annual_revenue is None

