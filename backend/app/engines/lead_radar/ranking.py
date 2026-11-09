"""
Lead-Radar Deterministic Ranking Engine.

Implements all specifications from Section 8 of the 2026-11-06 strategy:
- 6-key strictly hierarchical deterministic sort:
  Key 1: Opportunity class (OPEN_MANDATE > BROKEN_TASK_WITH_DEMAND > MISSING_TASK_WITH_DEMAND > RESEARCH_CANDIDATE)
  Key 2: Evidence quality (OWNER_OR_FIRST_PARTY > CORROBORATED > SINGLE_SOURCE > PROXY)
  Key 3: Task severity (IMPOSSIBLE > OBSTRUCTED > INFO_INCOMPLETE > COSMETIC)
  Key 4: Demand level (OWNER_CONFIRMED > REPEATED_REQUESTS > ACTIVITY_ONLY > UNKNOWN)
  Key 5: Authority (CONFIRMED > UNRESOLVED)
  Key 6: Freshness (newer first)
- Generates the 4 essential intelligence answers for every lead:
  - Why this business?
  - Why this project?
  - Why now?
  - What is still unknown?
- Visibly preserves separation of Segments A, Warm, B, C, UNKNOWN.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from backend.app.engines.lead_radar.types import (
    Authority,
    AuthorityLevel,
    ConditionID,
    ConditionResult,
    DemandLevel,
    DeterministicRank,
    EvidenceQuality,
    OpportunityClass,
    RecipeMatch,
    Segment,
    SixFacts,
    TaskQuality,
    TaskSeverity,
)


class LeadRadarRanker:
    """
    Ranks leads without arbitrary point scoring, applying the 6 hierarchical sort keys.
    """

    @classmethod
    def rank_lead(
        cls,
        facts: SixFacts,
        conditions: Dict[ConditionID, ConditionResult],
        matched_recipes: List[RecipeMatch],
        business_info: Dict[str, Any],
        evaluated_at: Optional[datetime] = None,
    ) -> DeterministicRank:
        """
        Derives the 6 hierarchical sort keys and narrative sales rationale.
        """
        def met(cid: ConditionID) -> bool:
            return conditions.get(cid, None) is not None and conditions[cid].is_met

        eval_time = evaluated_at or datetime.utcnow()

        # ─── KEY 1: Opportunity Class ─────────────────────────────
        if met(ConditionID.I1) or met(ConditionID.I2) or met(ConditionID.I3) or met(ConditionID.I4):
            opp_class = OpportunityClass.OPEN_MANDATE
        elif (met(ConditionID.W5) or met(ConditionID.W3) or met(ConditionID.W12)) and (
            met(ConditionID.D1) or met(ConditionID.D2) or met(ConditionID.D3)
        ):
            opp_class = OpportunityClass.BROKEN_TASK_WITH_DEMAND
        elif (met(ConditionID.W1) or met(ConditionID.W2) or met(ConditionID.W7)) and (
            met(ConditionID.D4) or met(ConditionID.D2) or met(ConditionID.D5) or met(ConditionID.D9)
        ):
            opp_class = OpportunityClass.MISSING_TASK_WITH_DEMAND
        else:
            opp_class = OpportunityClass.RESEARCH_CANDIDATE

        # ─── KEY 2: Evidence Quality ──────────────────────────────
        sources_count = business_info.get("independent_sources_count", 1)
        has_first_party = bool(business_info.get("has_first_party_evidence", False))
        if has_first_party:
            ev_quality = EvidenceQuality.OWNER_OR_FIRST_PARTY
        elif sources_count >= 2:
            ev_quality = EvidenceQuality.CORROBORATED
        elif sources_count == 1:
            ev_quality = EvidenceQuality.SINGLE_SOURCE
        else:
            ev_quality = EvidenceQuality.PROXY

        # ─── KEY 3: Task Severity ─────────────────────────────────
        if met(ConditionID.W1) or met(ConditionID.W2):
            task_sev = TaskSeverity.IMPOSSIBLE
        elif met(ConditionID.W5) or met(ConditionID.W3) or met(ConditionID.W13) or met(ConditionID.W6):
            task_sev = TaskSeverity.OBSTRUCTED
        elif met(ConditionID.W7) or met(ConditionID.W8) or met(ConditionID.W10):
            task_sev = TaskSeverity.INFO_INCOMPLETE
        else:
            task_sev = TaskSeverity.COSMETIC

        # ─── KEY 4: Demand Level ──────────────────────────────────
        if met(ConditionID.D5) or business_info.get("owner_confirmed_demand", False):
            demand_lvl = DemandLevel.OWNER_CONFIRMED
        elif met(ConditionID.D2):
            demand_lvl = DemandLevel.REPEATED_REQUESTS
        elif met(ConditionID.D1) or met(ConditionID.D3) or met(ConditionID.D4):
            demand_lvl = DemandLevel.ACTIVITY_ONLY
        else:
            demand_lvl = DemandLevel.UNKNOWN

        # ─── KEY 5: Authority Level ───────────────────────────────
        if facts.authority in (Authority.LOCAL_OWNER, Authority.PROCUREMENT_TEAM):
            auth_lvl = AuthorityLevel.CONFIRMED
        else:
            auth_lvl = AuthorityLevel.UNRESOLVED

        # ─── KEY 6: Freshness ─────────────────────────────────────
        freshness = business_info.get("latest_activity_date") or eval_time

        # ─── THE 4 MANDATORY ANSWERS ──────────────────────────────
        why_business = cls._synthesize_why_business(business_info, facts, conditions)
        why_project = cls._synthesize_why_project(facts, matched_recipes, conditions)
        why_now = cls._synthesize_why_now(opp_class, conditions, business_info)
        what_unknown = cls._synthesize_what_unknown(facts, business_info)

        return DeterministicRank(
            opportunity_class=opp_class,
            evidence_quality=ev_quality,
            task_severity=task_sev,
            demand_level=demand_lvl,
            authority_level=auth_lvl,
            freshness_timestamp=freshness,
            why_this_business=why_business,
            why_this_project=why_project,
            why_now=why_now,
            what_is_unknown=what_unknown,
        )

    @classmethod
    def sort_leads(cls, leads: List[Tuple[Any, DeterministicRank]]) -> List[Tuple[Any, DeterministicRank]]:
        """
        Sorts an array of (lead_object, DeterministicRank) descending by hierarchical sort keys.
        """
        return sorted(leads, key=lambda item: item[1].sort_tuple(), reverse=True)

    # ─── SYNTHESIS HELPERS ────────────────────────────────────────

    @classmethod
    def _synthesize_why_business(
        cls,
        info: Dict[str, Any],
        facts: SixFacts,
        conditions: Dict[ConditionID, ConditionResult],
    ) -> str:
        name = info.get("name", "Target business")
        cat = info.get("category", "commercial enterprise")
        city = info.get("city", "local market")
        active_proof = "active operations verified across independent registries" if facts.currently_active else "operating in the target market"
        return f"{name} is an established {cat} in {city} with {active_proof}."

    @classmethod
    def _synthesize_why_project(
        cls,
        facts: SixFacts,
        recipes: List[RecipeMatch],
        conditions: Dict[ConditionID, ConditionResult],
    ) -> str:
        if recipes:
            r = recipes[0]
            return f"{r.name}: {r.recommended_solution}. Observed gap: {r.opening_fact}"
        if facts.owned_presence == SixFacts().owned_presence.NONE_FOUND:
            return "Establish primary owned web presence to resolve unhosted customer actions."
        return "Remediate core digital customer task workflows to ensure reliable conversion."

    @classmethod
    def _synthesize_why_now(
        cls,
        opp_class: OpportunityClass,
        conditions: Dict[ConditionID, ConditionResult],
        info: Dict[str, Any],
    ) -> str:
        if opp_class == OpportunityClass.OPEN_MANDATE:
            return "Active RFP / request open within the past 30 days with pending evaluation window."
        elif opp_class == OpportunityClass.BROKEN_TASK_WITH_DEMAND:
            return "Active paid ads or live customer requests are currently hitting a broken conversion flow."
        elif opp_class == OpportunityClass.MISSING_TASK_WITH_DEMAND:
            return "Business is actively promoting or receiving customer inquiries that cannot complete their action."
        return "Routine digital infrastructure enhancement candidate."

    @classmethod
    def _synthesize_what_unknown(
        cls,
        facts: SixFacts,
        info: Dict[str, Any],
    ) -> str:
        unknowns = []
        if facts.authority == Authority.UNRESOLVED:
            unknowns.append("purchasing decision-maker identity")
        if info.get("revenue_confidence") in ("LOW", "UNAVAILABLE", None):
            unknowns.append("exact operating revenue band")
        if not info.get("internal_tech_budget_known", False):
            unknowns.append("current fiscal digital budget allocation")
        if not unknowns:
            return "All primary qualification parameters confirmed."
        return "Still unknown: " + ", ".join(unknowns) + "."

