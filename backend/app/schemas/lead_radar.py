"""
Lead-Radar Pydantic Schemas.

Defines API payload request and response schemas for all Lead-Radar strategy endpoints.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from backend.app.engines.lead_radar.types import (
    Authority,
    Availability,
    BusinessCategory,
    BuyingStatus,
    CustomerTaskCovered,
    IndianEconomicType,
    OwnedPresence,
    RecipeID,
    RevenueConfidence,
    Segment,
    TaskQuality,
)


class SixFactsSchema(BaseModel):
    owned_presence: OwnedPresence = OwnedPresence.UNRESOLVED
    availability: Availability = Availability.UNKNOWN
    customer_task_covered: CustomerTaskCovered = CustomerTaskCovered.UNKNOWN
    task_quality: TaskQuality = TaskQuality.NOT_TESTED
    buying_status: BuyingStatus = BuyingStatus.UNKNOWN
    authority: Authority = Authority.UNRESOLVED
    identity_verified: bool = False
    currently_active: bool = False
    absence_search_done: bool = False
    repeated_failure: bool = False


class RecipeMatchSchema(BaseModel):
    recipe_id: RecipeID
    name: str
    target_segment: Segment
    is_matched: bool
    required_conditions: List[str]
    matched_conditions: List[str]
    opening_fact: str
    pitch_angle: str
    never_say: str
    recommended_solution: str


class PitchSchema(BaseModel):
    opening_fact: str
    pitch_angle: str
    never_say: str
    recommended_solution: str


class RevenueEstimateSchema(BaseModel):
    category: str
    confidence: str
    min_annual_revenue: Optional[float] = None
    max_annual_revenue: Optional[float] = None
    currency: str = "USD"
    formula_used: str = ""
    notes: str = ""


class DeterministicRankSchema(BaseModel):
    opportunity_class: str
    evidence_quality: str
    task_severity: str
    demand_level: str
    authority_level: str
    freshness: str
    why_this_business: str
    why_this_project: str
    why_now: str
    what_is_unknown: str


class EvaluateLeadRadarRequest(BaseModel):
    business_id: Optional[int] = None
    name: str
    city: str = "Mumbai"
    country_code: str = "IN"
    category: str = "General"
    facts: Optional[SixFactsSchema] = None
    raw_signals: Dict[str, Any] = Field(default_factory=dict)
    persist: bool = False


class EvaluateLeadRadarResponse(BaseModel):
    business_id: Optional[int] = None
    name: str
    city: str
    country_code: str
    category: str
    facts: SixFactsSchema
    segment: Segment
    warm_context: bool
    conditions_met_count: int
    conditions_met: List[str]
    matched_recipes: List[RecipeMatchSchema]
    primary_recipe: Optional[RecipeMatchSchema] = None
    pitch: PitchSchema
    revenue_estimate: RevenueEstimateSchema
    rank: DeterministicRankSchema
    absence_certificate: Optional[Dict[str, Any]] = None
    evaluated_at: str


class AbsenceCertificateRequest(BaseModel):
    business_id: Optional[int] = None
    business_name: str
    country_code: str = "IN"
    city: str = "Mumbai"
    aliases: Optional[List[str]] = None
    local_script_names: Optional[List[str]] = None
    social_profiles: Optional[List[str]] = None
    email_addresses: Optional[List[str]] = None
    historical_urls: Optional[List[str]] = None


class RevenueEstimateRequest(BaseModel):
    category: BusinessCategory = BusinessCategory.RESTAURANT
    signals: Dict[str, Any] = Field(default_factory=dict)
    currency: str = "USD"


class MumbaiFunnelRequest(BaseModel):
    city: str = "Mumbai"
    country: str = "India"
    confidence_threshold: float = 0.7
    places: Optional[List[Dict[str, Any]]] = None  # If omitted, generates synthetic sample based on Overture distributions


class ProcessedLeadItem(BaseModel):
    record_id: str
    name: str
    city: str
    country: str
    category: str
    overture_confidence: float
    is_meta_source: bool
    segment: str
    warm_context: bool
    matched_recipes_count: int
    primary_recipe_name: Optional[str]
    pitch_opening_fact: str
    pitch_angle: str
    revenue_min: Optional[float]
    revenue_max: Optional[float]
    revenue_confidence: str
    rank_opportunity_class: str


class MumbaiFunnelResponse(BaseModel):
    city: str
    country: str
    confidence_threshold: float
    total_input_places: int
    stage_counts: Dict[str, int]
    retention_rates_pct: Dict[str, float]
    sample_shortlist: List[ProcessedLeadItem]


class CityBaselineSchema(BaseModel):
    city: str
    country: str
    places: int
    confident_places: int
    meta_first_pct: float
    confident_no_website_pct: float
    phone_pct: float
    email_pct: float
    social_pct: float


class RegionalProfileSchema(BaseModel):
    region_code: str
    region_name: str
    country_code: str
    economic_type: Optional[str] = None
    baseline_no_website_percent: float
    check_first: List[str]
    trust_less: List[str]
    local_sources: List[str]
    local_languages: List[str]
    target_categories: List[str]

