"""
Tests for Lead-Radar FastAPI REST Endpoints.
"""

import pytest
from httpx import AsyncClient, ASGITransport

from backend.app.main import app


@pytest.mark.asyncio
async def test_api_regions_baselines():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/lead-radar/regions/baselines")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 45
        cities = [b["city"].lower() for b in data]
        assert "mumbai" in cities
        assert "dallas" in cities
        assert "london" in cities


@pytest.mark.asyncio
async def test_api_city_baseline_single():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/lead-radar/regions/baselines/mumbai")
        assert response.status_code == 200
        data = response.json()
        assert data["city"] == "Mumbai"
        assert data["confident_no_website_pct"] == 24.5


@pytest.mark.asyncio
async def test_api_absence_certificate():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        payload = {
            "business_id": 999,
            "business_name": "Marine Drive Bistro",
            "country_code": "IN",
            "city": "Mumbai",
            "social_profiles": ["https://instagram.com/marinedrivebistro"],
        }
        response = await client.post("/api/v1/lead-radar/absence-certificate", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["is_truly_absent"] is True
        assert "certificate" in data
        assert data["certificate"]["signature_hash"] is not None


@pytest.mark.asyncio
async def test_api_revenue_estimate():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        payload = {
            "category": "RESTAURANT",
            "signals": {
                "seats_count": 60,
                "avg_spend_per_cover": 25.0,
                "calibrated_rates": True,
            },
            "currency": "USD",
        }
        response = await client.post("/api/v1/lead-radar/revenue-estimate", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["category"] == "RESTAURANT"
        assert data["min_annual_revenue"] is not None
        assert data["max_annual_revenue"] > data["min_annual_revenue"]


@pytest.mark.asyncio
async def test_api_mumbai_funnel():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        payload = {
            "city": "Mumbai",
            "country": "India",
            "confidence_threshold": 0.7,
        }
        response = await client.post("/api/v1/lead-radar/mumbai-funnel", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["total_input_places"] == 100
        assert "stage_counts" in data
        assert len(data["sample_shortlist"]) > 0


@pytest.mark.asyncio
async def test_api_evaluate_lead():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        payload = {
            "name": "Apollo Dental Care",
            "city": "Mumbai",
            "country_code": "IN",
            "category": "Clinic",
            "raw_signals": {
                "official_reg_id": "REG-CLINIC-01",
                "needed_task_unhosted": True,
                "promotions_count_90d": 3,
                "independent_activity_signals_90d": 2,
            },
        }
        response = await client.post("/api/v1/lead-radar/evaluate", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Apollo Dental Care"
        assert data["segment"] in ["A", "B", "C", "UNKNOWN"]
        assert "pitch" in data
        assert "revenue_estimate" in data
        assert "rank" in data

