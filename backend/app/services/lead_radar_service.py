"""
Lead-Radar Business Service Layer.

Orchestrates evaluation, persistence, absence certification, revenue estimation,
and funnel execution across SQLite / PostgreSQL sessions.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
import structlog
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.engines.lead_radar import (
    AbsenceSearchEngine,
    CityBaseline,
    ConditionEvaluator,
    FunnelStageCounts,
    LeadRadarPipeline,
    LeadRadarRanker,
    LeadRadarSegmenter,
    OVERTURE_45_CITY_BASELINES,
    INDIAN_STATE_PROFILES,
    GLOBAL_COUNTRY_PROFILES,
    RegionalCalibrationEngine,
    RevenueEstimationEngine,
    BusinessCategory,
    ConditionID,
    OwnedPresence,
    RecipeID,
    Segment,
    SixFacts,
)
from backend.app.models.business import Business
from backend.app.models.lead_radar import LeadRadarEvaluation

logger = structlog.get_logger(__name__)


class LeadRadarService:
    """Service layer managing Lead-Radar strategy workflows."""

    @classmethod
    async def evaluate_business_lead(
        cls,
        session: Optional[AsyncSession],
        name: str,
        city: str = "Mumbai",
        country_code: str = "IN",
        category: str = "General",
        business_id: Optional[int] = None,
        facts: Optional[SixFacts] = None,
        raw_signals: Optional[Dict[str, Any]] = None,
        persist: bool = False,
    ) -> Dict[str, Any]:
        """
        Runs complete 6-fact, 51-condition, 17-recipe, revenue, and ranking evaluation.
        """
        f = facts or SixFacts(
            owned_presence=OwnedPresence.NONE_FOUND,
            identity_verified=True,
            currently_active=True,
            absence_search_done=True,
        )
        sig = raw_signals or {}

        # 1. Condition evaluation (51 conditions)
        conditions = ConditionEvaluator.evaluate_all(f, sig)
        conditions_met = [cid.value for cid, res in conditions.items() if res.is_met]

        # 2. Strategic Segmentation, Recipes & Pitch
        meta = {
            "name": name,
            "city": city,
            "category": category,
            "country_code": country_code,
            **sig,
        }
        segment, warm_context, recipes, pitch = LeadRadarSegmenter.evaluate_segment_and_recipes(
            f, conditions, meta
        )

        # 3. Revenue Estimation
        cat_enum = BusinessCategory.OTHER
        cat_lower = category.lower()
        if "restaurant" in cat_lower or "cafe" in cat_lower or "food" in cat_lower:
            cat_enum = BusinessCategory.RESTAURANT
        elif "clinic" in cat_lower or "dental" in cat_lower:
            cat_enum = BusinessCategory.CLINIC
        elif "salon" in cat_lower or "spa" in cat_lower:
            cat_enum = BusinessCategory.SALON
        elif "hotel" in cat_lower or "stay" in cat_lower:
            cat_enum = BusinessCategory.HOTEL
        elif "retail" in cat_lower or "store" in cat_lower:
            cat_enum = BusinessCategory.RETAIL
        elif "manufactur" in cat_lower or "export" in cat_lower:
            cat_enum = BusinessCategory.MANUFACTURER_EXPORTER
        elif "consult" in cat_lower or "legal" in cat_lower or "agency" in cat_lower:
            cat_enum = BusinessCategory.PROFESSIONAL_SERVICES
        elif "school" in cat_lower or "coach" in cat_lower or "academy" in cat_lower:
            cat_enum = BusinessCategory.EDUCATION
        elif "gym" in cat_lower or "fitness" in cat_lower:
            cat_enum = BusinessCategory.GYM

        rev_estimate = RevenueEstimationEngine.estimate_revenue(cat_enum, sig)

        # 4. 6-Tier Deterministic Ranking
        rank = LeadRadarRanker.rank_lead(f, conditions, recipes, meta)

        # 5. Absence Certificate
        is_absent, presence, cert = AbsenceSearchEngine.execute_3path_search(
            business_id=business_id or hash(name),
            business_name=name,
            country_code=country_code,
            city=city,
            aliases=sig.get("aliases"),
            local_script_names=sig.get("local_script_names"),
            social_profiles=sig.get("social_profiles"),
            email_addresses=sig.get("email_addresses"),
        )

        eval_result = {
            "business_id": business_id,
            "name": name,
            "city": city,
            "country_code": country_code,
            "category": category,
            "facts": f.to_dict(),
            "segment": segment.value,
            "warm_context": warm_context,
            "conditions_met_count": len(conditions_met),
            "conditions_met": conditions_met,
            "matched_recipes": [r.to_dict() for r in recipes],
            "primary_recipe": recipes[0].to_dict() if recipes else None,
            "pitch": pitch,
            "revenue_estimate": rev_estimate.to_dict(),
            "rank": rank.to_dict(),
            "absence_certificate": cert.to_dict(),
            "evaluated_at": datetime.utcnow().isoformat(),
        }

        # 6. Optional Persistence
        if persist and session and business_id:
            try:
                # Check for existing record
                stmt = select(LeadRadarEvaluation).where(LeadRadarEvaluation.business_id == business_id)
                db_res = await session.execute(stmt)
                eval_row = db_res.scalar_one_or_none()

                if not eval_row:
                    eval_row = LeadRadarEvaluation(business_id=business_id)
                    session.add(eval_row)

                eval_row.owned_presence = f.owned_presence
                eval_row.availability = f.availability
                eval_row.customer_task_covered = f.customer_task_covered
                eval_row.task_quality = f.task_quality
                eval_row.buying_status = f.buying_status
                eval_row.authority = f.authority
                eval_row.identity_verified = f.identity_verified
                eval_row.currently_active = f.currently_active
                eval_row.absence_search_done = f.absence_search_done
                eval_row.repeated_failure = f.repeated_failure

                eval_row.segment = segment
                eval_row.warm_context = warm_context
                eval_row.conditions_met = conditions_met
                eval_row.condition_results = {k.value: v.to_dict() for k, v in conditions.items()}
                eval_row.matched_recipes = [r.to_dict() for r in recipes]
                eval_row.primary_recipe_id = recipes[0].recipe_id.value if recipes else None

                eval_row.pitch_opening_fact = pitch.get("opening_fact")
                eval_row.pitch_angle = pitch.get("pitch_angle")
                eval_row.pitch_never_say = pitch.get("never_say")
                eval_row.pitch_recommended_solution = pitch.get("recommended_solution")

                eval_row.revenue_category = rev_estimate.category.value
                eval_row.revenue_confidence = rev_estimate.confidence.value
                eval_row.min_annual_revenue = rev_estimate.min_annual_revenue
                eval_row.max_annual_revenue = rev_estimate.max_annual_revenue
                eval_row.revenue_currency = rev_estimate.currency
                eval_row.revenue_formula = rev_estimate.formula_used

                eval_row.absence_certificate_id = cert.certificate_id
                eval_row.absence_certificate_hash = cert.signature_hash
                eval_row.absence_certificate_data = cert.to_dict()

                eval_row.rank_opportunity_class = rank.opportunity_class.name
                eval_row.rank_evidence_quality = rank.evidence_quality.name
                eval_row.rank_task_severity = rank.task_severity.name
                eval_row.rank_demand_level = rank.demand_level.name
                eval_row.rank_authority_level = rank.authority_level.name
                eval_row.why_this_business = rank.why_this_business
                eval_row.why_this_project = rank.why_this_project
                eval_row.why_now = rank.why_now
                eval_row.what_is_unknown = rank.what_is_unknown

                await session.commit()
            except Exception as e:
                await session.rollback()
                logger.warning("persist_lead_radar_failed", error=str(e))

        return eval_result

    @classmethod
    def run_mumbai_pipeline(
        cls,
        city: str = "Mumbai",
        country: str = "India",
        confidence_threshold: float = 0.7,
        places: Optional[List[Dict[str, Any]]] = None,
    ) -> Dict[str, Any]:
        """
        Executes the exact 8-stage funnel from Section 1 on places data.
        If places is not provided, synthesizes a representative sample conforming
        to the measured Overture Places Mumbai distribution.
        """
        input_places = places or cls._generate_sample_mumbai_places(city)
        counts, shortlist = LeadRadarPipeline.process_places_funnel(
            input_places,
            confidence_threshold=confidence_threshold,
            city=city,
            country=country,
        )

        total = counts.stage_0_all_places
        retention = {}
        if total > 0:
            retention["confident_pct"] = round(counts.stage_1_confident / total * 100, 2)
            retention["no_website_pct"] = round(counts.stage_2_no_website_on_file / total * 100, 2)
            retention["reachable_pct"] = round(counts.stage_3_reachable / total * 100, 2)
            retention["verified_business_pct"] = round(counts.stage_4_real_business_g1_g4 / total * 100, 2)
            retention["truly_absent_pct"] = round(counts.stage_5_truly_no_site_w1 / total * 100, 2)
            retention["active_pct"] = round(counts.stage_6_alive_and_active_g7 / total * 100, 2)
            retention["task_gap_pct"] = round(counts.stage_7_real_task_gap_w2_w13 / total * 100, 2)
            retention["qualified_shortlist_pct"] = round(len(shortlist) / total * 100, 2)

        formatted_shortlist = []
        for l in shortlist[:50]:  # return top 50
            formatted_shortlist.append({
                "record_id": l.record_id,
                "name": l.name,
                "city": l.city,
                "country": l.country,
                "category": l.category,
                "overture_confidence": l.overture_confidence,
                "is_meta_source": l.is_meta_source,
                "segment": l.segment.value,
                "warm_context": l.warm_context,
                "matched_recipes_count": len(l.matched_recipes),
                "primary_recipe_name": l.matched_recipes[0].name if l.matched_recipes else None,
                "pitch_opening_fact": l.pitch.get("opening_fact", ""),
                "pitch_angle": l.pitch.get("pitch_angle", ""),
                "revenue_min": l.revenue_min,
                "revenue_max": l.revenue_max,
                "revenue_confidence": l.revenue_confidence,
                "rank_opportunity_class": l.rank.opportunity_class.name,
            })

        return {
            "city": city,
            "country": country,
            "confidence_threshold": confidence_threshold,
            "total_input_places": total,
            "stage_counts": counts.to_dict(),
            "retention_rates_pct": retention,
            "sample_shortlist": formatted_shortlist,
        }

    @classmethod
    def _generate_sample_mumbai_places(cls, city: str) -> List[Dict[str, Any]]:
        """
        Generates realistic sample records matching the measured Mumbai Overture metrics:
        - 100 places
        - ~85% Meta-sourced
        - ~24.5% no website on file
        - ~66% phone, ~93% social (no generated email addresses)
        """
        samples = []
        categories = [
            ("Apex Dental Care Clinic", "Clinic", 18, 120.0),
            ("Spice Symphony Fine Dining", "Restaurant", 60, 35.0),
            ("Mahalaxmi Silk Mills & Exporters", "Manufacturer", 120, 250.0),
            ("Glow Studio Luxury Salon", "Salon", 10, 45.0),
            ("Bandra Boutique Suites", "Hotel", 35, 95.0),
            ("Vidyalankar IIT Coaching Academy", "Education", 250, 450.0),
            ("Iron Core Fitness Gym", "Gym", 180, 50.0),
            ("Zenith Maritime Logistics & Customs", "Professional Services", 25, 140.0),
            ("Shree Krishna Sweets & Snacks", "Retail", 80, 15.0),
            ("South Bombay Realty Advisory", "Real Estate Broker", 40, 450.0),
        ]

        for i in range(100):
            base_name, cat, vol, price = categories[i % len(categories)]
            name = f"{base_name} #{i+1}"

            # Overture confidence distribution
            conf = 0.82 if i < 70 else 0.55

            # 85% meta source
            sources = ["meta_facebook", "osm"] if (i % 100) < 85 else ["osm"]

            # ~25% no website on file
            has_web = (i % 4) != 0
            websites = [f"https://{name.lower().replace(' ', '')}.com"] if has_web else []

            # Contacts: ~66% phone, ~93% social
            phones = [f"+91 98200 {10000 + i}"] if (i % 3) != 0 else []
            # No email addresses in the generated sample: a made-up info@<name>.in address looked like a real
            # contact (email engine v2 E1 removed every generated address). The email ratio is not modelled.
            emails: list[str] = []
            socials = [f"https://facebook.com/{name.lower().replace(' ', '')}"] if (i % 10) != 0 else []

            samples.append({
                "id": f"ovtr-mb-{1000+i}",
                "name": name,
                "city": city,
                "country": "India",
                "category": cat,
                "confidence": conf,
                "sources": sources,
                "websites": websites,
                "phones": phones,
                "emails": emails,
                "socials": socials,
                "reviews_count_90d": 14 if i % 2 == 0 else 3,
                "promotions_count_90d": 3 if i % 3 == 0 else 0,
                "independent_activity_signals_90d": 2,
                "needed_task_unhosted": True,
                "seats_count": vol if cat == "Restaurant" else None,
                "doctors_count": 4 if cat == "Clinic" else None,
                "staffed_stations_count": 8 if cat == "Salon" else None,
                "rooms_count": vol if cat == "Hotel" else None,
                "new_reviews_90d": 14,
                "avg_spend_per_cover": price if cat == "Restaurant" else None,
                "realised_consultation_fee": price if cat == "Clinic" else None,
            })

        return samples

