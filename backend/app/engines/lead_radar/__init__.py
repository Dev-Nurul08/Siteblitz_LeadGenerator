"""
Lead-Radar Engine Package.

Exports all core components of the 2026-11-06 Global Lead Engine strategy:
- 6 Facts & Condition Library
- 17 Sales Recipes & Pitch Generator
- 10 Category Revenue Formulas & Review Model
- 6-Tier Deterministic Ranking Engine
- 3-Path Absence Search & Absence Certificate Engine
- 45-City Baselines & 16 Indian States & 27 Country Profiles
- 8-Stage Mumbai-Style Pipeline Processor
"""

from backend.app.engines.lead_radar.types import (
    AbsenceCertificate,
    Authority,
    AuthorityLevel,
    Availability,
    BusinessCategory,
    BuyingStatus,
    ConditionID,
    ConditionResult,
    ConditionStrength,
    CustomerTaskCovered,
    DemandLevel,
    DeterministicRank,
    EvidenceQuality,
    IndianEconomicType,
    OpportunityClass,
    OwnedPresence,
    RecipeID,
    RecipeMatch,
    RegionalProfile,
    RevenueConfidence,
    RevenueEstimate,
    Segment,
    SixFacts,
    TaskQuality,
    TaskSeverity,
)
from backend.app.engines.lead_radar.conditions import ConditionEvaluator
from backend.app.engines.lead_radar.segmenter import LeadRadarSegmenter
from backend.app.engines.lead_radar.revenue import RevenueEstimationEngine
from backend.app.engines.lead_radar.ranking import LeadRadarRanker
from backend.app.engines.lead_radar.absence import AbsenceSearchEngine
from backend.app.engines.lead_radar.regions import (
    CityBaseline,
    RegionalCalibrationEngine,
    OVERTURE_45_CITY_BASELINES,
    INDIAN_STATE_PROFILES,
    GLOBAL_COUNTRY_PROFILES,
)
from backend.app.engines.lead_radar.pipeline import (
    FunnelStageCounts,
    LeadRadarPipeline,
    ProcessedLead,
)

__all__ = [
    # Types & Enums
    "AbsenceCertificate",
    "Authority",
    "AuthorityLevel",
    "Availability",
    "BusinessCategory",
    "BuyingStatus",
    "ConditionID",
    "ConditionResult",
    "ConditionStrength",
    "CustomerTaskCovered",
    "DemandLevel",
    "DeterministicRank",
    "EvidenceQuality",
    "IndianEconomicType",
    "OpportunityClass",
    "OwnedPresence",
    "RecipeID",
    "RecipeMatch",
    "RegionalProfile",
    "RevenueConfidence",
    "RevenueEstimate",
    "Segment",
    "SixFacts",
    "TaskQuality",
    "TaskSeverity",
    "CityBaseline",
    # Engines & Pipelines
    "ConditionEvaluator",
    "LeadRadarSegmenter",
    "RevenueEstimationEngine",
    "LeadRadarRanker",
    "AbsenceSearchEngine",
    "RegionalCalibrationEngine",
    "LeadRadarPipeline",
    "FunnelStageCounts",
    "ProcessedLead",
    # Constants & Profiles
    "OVERTURE_45_CITY_BASELINES",
    "INDIAN_STATE_PROFILES",
    "GLOBAL_COUNTRY_PROFILES",
]

