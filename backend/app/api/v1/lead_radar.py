"""
Lead-Radar REST API Endpoints.

Exposes endpoints for the 2026-11-06 Global Lead Engine strategy:
- Business evaluation across 6 facts, 51 conditions, 17 recipes, pitch, revenue, and ranking
- 3-path absence search & certificate generation
- Category revenue formulas & review-based estimation
- 8-stage Mumbai pipeline funnel execution
- Regional calibration profiles & 45-city baseline datasets
"""

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc

from backend.app.database import get_db_session
from backend.app.engines.lead_radar import (
    AbsenceSearchEngine,
    GLOBAL_COUNTRY_PROFILES,
    INDIAN_STATE_PROFILES,
    OVERTURE_45_CITY_BASELINES,
    RegionalCalibrationEngine,
    RevenueEstimationEngine,
    BusinessCategory,
    SixFacts,
)
from backend.app.models.lead_radar import LeadRadarEvaluation
from backend.app.schemas.lead_radar import (
    AbsenceCertificateRequest,
    CityBaselineSchema,
    EvaluateLeadRadarRequest,
    EvaluateLeadRadarResponse,
    MumbaiFunnelRequest,
    MumbaiFunnelResponse,
    RegionalProfileSchema,
    RevenueEstimateRequest,
    RevenueEstimateSchema,
)
from backend.app.services.lead_radar_service import LeadRadarService

router = APIRouter(prefix="/lead-radar", tags=["Lead Radar Engine"])


@router.post(
    "/evaluate",
    response_model=EvaluateLeadRadarResponse,
    summary="Evaluate Business via Lead-Radar Condition Strategy",
    description="Evaluates 6 facts, tests 51 conditions, resolves segments (A/B/C/Warm/Unknown), matches 17 recipes, crafts pitch, estimates revenue, and ranks lead.",
)
async def evaluate_lead_radar(
    payload: EvaluateLeadRadarRequest,
    db: AsyncSession = Depends(get_db_session),
):
    facts = None
    if payload.facts:
        facts = SixFacts(
            owned_presence=payload.facts.owned_presence,
            availability=payload.facts.availability,
            customer_task_covered=payload.facts.customer_task_covered,
            task_quality=payload.facts.task_quality,
            buying_status=payload.facts.buying_status,
            authority=payload.facts.authority,
            identity_verified=payload.facts.identity_verified,
            currently_active=payload.facts.currently_active,
            absence_search_done=payload.facts.absence_search_done,
            repeated_failure=payload.facts.repeated_failure,
        )

    result = await LeadRadarService.evaluate_business_lead(
        session=db,
        name=payload.name,
        city=payload.city,
        country_code=payload.country_code,
        category=payload.category,
        business_id=payload.business_id,
        facts=facts,
        raw_signals=payload.raw_signals,
        persist=payload.persist,
    )

    return result


@router.post(
    "/absence-certificate",
    summary="Generate 3-Path Absence Certificate",
    description="Tests canonical names, profiles, and domain clues; generates a cryptographically signed Absence Certificate.",
)
async def generate_absence_certificate(
    payload: AbsenceCertificateRequest,
):
    is_absent, presence, cert = AbsenceSearchEngine.execute_3path_search(
        business_id=payload.business_id,
        business_name=payload.business_name,
        country_code=payload.country_code,
        city=payload.city,
        aliases=payload.aliases,
        local_script_names=payload.local_script_names,
        social_profiles=payload.social_profiles,
        email_addresses=payload.email_addresses,
        historical_urls=payload.historical_urls,
    )
    return {
        "is_truly_absent": is_absent,
        "owned_presence": presence.value,
        "certificate": cert.to_dict(),
    }


@router.post(
    "/revenue-estimate",
    response_model=RevenueEstimateSchema,
    summary="Calculate Calibrated Category Revenue Band",
    description="Estimates annual revenue ranges for 10 industries or via review velocity under Section 7 rules.",
)
async def calculate_revenue_estimate(
    payload: RevenueEstimateRequest,
):
    rev = RevenueEstimationEngine.estimate_revenue(
        category=payload.category,
        signals=payload.signals,
        currency=payload.currency,
    )
    return rev.to_dict()


@router.post(
    "/mumbai-funnel",
    response_model=MumbaiFunnelResponse,
    summary="Run 8-Stage Pipeline Funnel (Section 1)",
    description="Processes raw place records through stages 0 to 8: Confident -> No site -> Reachable -> Real business -> Truly absent -> Alive -> Task gap -> Segment.",
)
async def run_mumbai_pipeline_funnel(
    payload: MumbaiFunnelRequest,
):
    res = LeadRadarService.run_mumbai_pipeline(
        city=payload.city,
        country=payload.country,
        confidence_threshold=payload.confidence_threshold,
        places=payload.places,
    )
    return res


@router.get(
    "/regions/baselines",
    response_model=List[CityBaselineSchema],
    summary="Get 45-City Overture Baseline Metrics (Section 11.9)",
    description="Returns empirical Places, Confidence, Meta-first share, No-website %, and contact field rates across 45 surveyed global cities.",
)
async def list_city_baselines():
    baselines = list(OVERTURE_45_CITY_BASELINES.values())
    return [b.__dict__ for b in baselines]


@router.get(
    "/regions/baselines/{city}",
    response_model=CityBaselineSchema,
    summary="Get City Baseline by Name",
)
async def get_city_baseline(city: str):
    baseline = RegionalCalibrationEngine.get_city_baseline(city)
    if not baseline:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Baseline not found for city '{city}'. Available cities include: {', '.join(OVERTURE_45_CITY_BASELINES.keys())}",
        )
    return baseline.__dict__


@router.get(
    "/regions/profiles",
    summary="Get Regional Priority Profiles",
    description="Returns Indian state profiles (Section 11.5) and Global country profiles (Section 11.6) with priority (↑) and discount (↓) checks.",
)
async def list_regional_profiles():
    return {
        "indian_states": {k: v.to_dict() for k, v in INDIAN_STATE_PROFILES.items()},
        "global_countries": {k: v.to_dict() for k, v in GLOBAL_COUNTRY_PROFILES.items()},
    }


@router.get(
    "/evaluations",
    summary="List Stored Lead Radar Evaluations",
)
async def list_evaluations(
    segment: Optional[str] = Query(None, description="Filter by segment: A, B, C, UNKNOWN"),
    recipe: Optional[str] = Query(None, description="Filter by recipe: R1 - R17"),
    limit: int = Query(50, ge=1, le=200),
    db: AsyncSession = Depends(get_db_session),
):
    stmt = select(LeadRadarEvaluation).order_by(desc(LeadRadarEvaluation.created_at)).limit(limit)
    if segment:
        stmt = stmt.where(LeadRadarEvaluation.segment == segment.upper())
    if recipe:
        stmt = stmt.where(LeadRadarEvaluation.primary_recipe_id == recipe.upper())

    result = await db.execute(stmt)
    records = result.scalars().all()

    return [
        {
            "id": r.id,
            "business_id": r.business_id,
            "segment": r.segment.value if r.segment else None,
            "warm_context": r.warm_context,
            "primary_recipe_id": r.primary_recipe_id,
            "pitch_opening_fact": r.pitch_opening_fact,
            "pitch_angle": r.pitch_angle,
            "min_annual_revenue": r.min_annual_revenue,
            "max_annual_revenue": r.max_annual_revenue,
            "revenue_confidence": r.revenue_confidence,
            "rank_opportunity_class": r.rank_opportunity_class,
            "why_this_business": r.why_this_business,
            "why_this_project": r.why_this_project,
            "why_now": r.why_now,
            "what_is_unknown": r.what_is_unknown,
            "created_at": r.created_at.isoformat() if r.created_at else None,
        }
        for r in records
    ]
