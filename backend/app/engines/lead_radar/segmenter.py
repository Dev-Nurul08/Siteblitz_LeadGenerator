"""
Lead-Radar Segmenter, Decision Order, Conflict Resolver, Recipe Matcher, and Pitch Generator.

Implements:
- 8-step decision order (first match wins) from Section 4.1
- Strategic conflict resolution from Section 4.2
- Warm context flag management
- 17 Combination Recipes (R1 - R17) from Section 6
- Pitch by Segment and Recipe from Section 5
"""

from typing import Any, Dict, List, Optional, Tuple

from backend.app.engines.lead_radar.types import (
    Authority,
    ConditionID,
    ConditionResult,
    OwnedPresence,
    RecipeID,
    RecipeMatch,
    Segment,
    SixFacts,
)


class LeadRadarSegmenter:
    """
    Decides business segment (A, B, C, UNKNOWN), sets warm_context,
    resolves conflicts, matches sales recipes (R1 - R17), and crafts factual pitch angles.
    """

    @classmethod
    def evaluate_segment_and_recipes(
        cls,
        facts: SixFacts,
        conditions: Dict[ConditionID, ConditionResult],
        business_metadata: Dict[str, Any],
    ) -> Tuple[Segment, bool, List[RecipeMatch], Dict[str, str]]:
        """
        Runs the full segmentation decision order and evaluates all 17 recipes.
        Returns:
            - segment: Segment (A, B, C, UNKNOWN)
            - warm_context: bool (indicates an active change in motion)
            - matched_recipes: List[RecipeMatch]
            - pitch: Dict with opening_fact, pitch_angle, never_say, recommended_solution
        """
        # Helper to check condition
        def met(cid: ConditionID) -> bool:
            return conditions.get(cid, None) is not None and conditions[cid].is_met

        # ─── 4.2 CONFLICT RESOLUTION PRE-CHECKS ───────────────────
        # Conflict: Broken site, but owner says closed -> Resolve closure first
        if met(ConditionID.G5):
            segment = Segment.C
            warm_context = False
            recipes = cls._evaluate_recipes(facts, conditions, business_metadata, segment)
            pitch = cls._build_pitch(segment, warm_context, recipes, business_metadata)
            return segment, warm_context, recipes, pitch

        # Conflict: Old request, but newer supplier appointed -> C
        if met(ConditionID.C3):
            segment = Segment.C
            warm_context = False
            recipes = cls._evaluate_recipes(facts, conditions, business_metadata, segment)
            pitch = cls._build_pitch(segment, warm_context, recipes, business_metadata)
            return segment, warm_context, recipes, pitch

        # Conflict: Parent buys centrally, branch asks alone -> Authority unresolved
        if met(ConditionID.G6):
            segment = Segment.C  # Branch cannot buy; check parent
            warm_context = False
            recipes = cls._evaluate_recipes(facts, conditions, business_metadata, segment)
            pitch = {
                "opening_fact": "Branch operates under centralized digital procurement governed by parent entity.",
                "pitch_angle": "Direct outreach to parent company headquarters rather than local branch.",
                "never_say": "Pitching the branch manager directly.",
                "recommended_solution": "Route lead to enterprise parent procurement queue.",
            }
            return segment, warm_context, recipes, pitch

        # ─── 4.1 DECISION ORDER (FIRST MATCH WINS) ────────────────
        segment = Segment.UNKNOWN
        warm_context = False

        # Step 1: Evidence not usable (G2 fails)
        if not met(ConditionID.G2):
            segment = Segment.UNKNOWN
            return segment, False, [], {
                "opening_fact": "Data source terms do not permit direct analytical retention.",
                "pitch_angle": "Purge evidence from lead record.",
                "never_say": "Contacting based on restricted source data.",
                "recommended_solution": "Drop restricted evidence.",
            }

        # Step 2: Identity unresolved (G1 fails)
        if not met(ConditionID.G1):
            segment = Segment.UNKNOWN

        # Step 3: Not a procuring body or duplicate (G3 or G4 fails)
        elif not met(ConditionID.G3) or not met(ConditionID.G4):
            segment = Segment.C  # Disqualified

        # Step 4: Any C1-C6 applies
        elif met(ConditionID.C1) or met(ConditionID.C2) or met(ConditionID.C4) or met(ConditionID.C5) or met(ConditionID.C6):
            segment = Segment.C

        # Step 5: I1, I2, I3 or I4 current and authorised -> A (Actively looking)
        elif met(ConditionID.I1) or met(ConditionID.I2) or met(ConditionID.I3) or met(ConditionID.I4):
            segment = Segment.A

        # Step 6: I5, I6, I7 or I8 present + G7 active -> Warm: something is in motion
        elif met(ConditionID.G7) and (met(ConditionID.I5) or met(ConditionID.I6) or met(ConditionID.I7) or met(ConditionID.I8)):
            warm_context = True
            # Check if there is also an unserved task gap under demand
            has_w_gap = any(met(cid) for cid in [
                ConditionID.W1, ConditionID.W2, ConditionID.W3, ConditionID.W4,
                ConditionID.W5, ConditionID.W6, ConditionID.W7, ConditionID.W8,
                ConditionID.W9, ConditionID.W10, ConditionID.W12, ConditionID.W13
            ])
            has_demand = any(met(cid) for cid in [
                ConditionID.D1, ConditionID.D2, ConditionID.D3, ConditionID.D4,
                ConditionID.D5, ConditionID.D6, ConditionID.D7, ConditionID.D8,
                ConditionID.D9, ConditionID.D11, ConditionID.D12
            ])
            if has_w_gap and has_demand:
                segment = Segment.B
            else:
                segment = Segment.UNKNOWN

        # Step 7: G7 active + a W condition + (D demand or owner evidence) -> B (Needs it, not shown looking)
        elif met(ConditionID.G7):
            has_w_gap = any(met(cid) for cid in [
                ConditionID.W1, ConditionID.W2, ConditionID.W3, ConditionID.W4,
                ConditionID.W5, ConditionID.W6, ConditionID.W7, ConditionID.W8,
                ConditionID.W9, ConditionID.W10, ConditionID.W12, ConditionID.W13
            ])
            has_demand = any(met(cid) for cid in [
                ConditionID.D1, ConditionID.D2, ConditionID.D3, ConditionID.D4,
                ConditionID.D5, ConditionID.D6, ConditionID.D7, ConditionID.D8,
                ConditionID.D9, ConditionID.D11, ConditionID.D12
            ]) or business_metadata.get("owner_confirmed_demand", False)

            if has_w_gap and has_demand:
                segment = Segment.B
            else:
                segment = Segment.UNKNOWN

        # Step 8: Only missing fields, listing counts or looks -> Unknown
        else:
            segment = Segment.UNKNOWN

        # Also set warm_context flag if I5-I8 present regardless of segment
        if met(ConditionID.I5) or met(ConditionID.I6) or met(ConditionID.I7) or met(ConditionID.I8):
            warm_context = True

        recipes = cls._evaluate_recipes(facts, conditions, business_metadata, segment)
        pitch = cls._build_pitch(segment, warm_context, recipes, business_metadata)

        return segment, warm_context, recipes, pitch

    @classmethod
    def _evaluate_recipes(
        cls,
        facts: SixFacts,
        conditions: Dict[ConditionID, ConditionResult],
        meta: Dict[str, Any],
        current_segment: Segment,
    ) -> List[RecipeMatch]:
        """Evaluates each of the 17 combination recipes defined in Section 6."""
        def met(cid: ConditionID) -> bool:
            return conditions.get(cid, None) is not None and conditions[cid].is_met

        matches: List[RecipeMatch] = []

        # R1: Open mandate (G1 + I1 + authority + still open) -> A
        r1_req = [ConditionID.G1, ConditionID.I1]
        r1_matched = [c for c in r1_req if met(c)]
        r1_ok = (len(r1_req) == len(r1_matched)) and (facts.authority in (Authority.LOCAL_OWNER, Authority.PROCUREMENT_TEAM))
        matches.append(RecipeMatch(
            recipe_id=RecipeID.R1,
            name="Open Mandate",
            target_segment=Segment.A,
            is_matched=r1_ok,
            required_conditions=r1_req,
            matched_conditions=r1_matched,
            opening_fact=f"Your request on {meta.get('request_date', 'recent dates')} specifically outlines {meta.get('requested_scope', 'website and digital capability requirements')}.",
            pitch_angle="Address the exact declared scope with specific milestones and verified portfolio references.",
            never_say="You need a website.",
            recommended_solution="Scope proposal addressing declared mandate requirements.",
        ))

        # R2: Open tender (I2 + eligible + correct entity) -> A
        r2_req = [ConditionID.I2, ConditionID.G1]
        r2_matched = [c for c in r2_req if met(c)]
        r2_ok = (len(r2_req) == len(r2_matched))
        matches.append(RecipeMatch(
            recipe_id=RecipeID.R2,
            name="Open Tender",
            target_segment=Segment.A,
            is_matched=r2_ok,
            required_conditions=r2_req,
            matched_conditions=r2_matched,
            opening_fact=f"Tender notice #{meta.get('tender_id', 'REF')} posted on {meta.get('tender_portal', 'procurement registry')} with submission deadline {meta.get('tender_deadline', 'pending')}.",
            pitch_angle="Provide formal compliance response matching public RFP tender criteria.",
            never_say="We noticed your website is outdated.",
            recommended_solution="Formal bid submission through designated procurement portal.",
        ))

        # R3: Replacement (I4 + current problem + decision open) -> A
        r3_req = [ConditionID.I4, ConditionID.G1]
        r3_matched = [c for c in r3_req if met(c)]
        r3_ok = (len(r3_req) == len(r3_matched))
        matches.append(RecipeMatch(
            recipe_id=RecipeID.R3,
            name="Supplier Replacement",
            target_segment=Segment.A,
            is_matched=r3_ok,
            required_conditions=r3_req,
            matched_conditions=r3_matched,
            opening_fact="You recently expressed seeking a new digital partner to resolve active technical delivery bottlenecks.",
            pitch_angle="Focus on seamless handover, clean code audits, and transparent SLA delivery guarantees.",
            never_say="Your current agency is failing you completely.",
            recommended_solution="Transition audit and vendor replacement roadmap.",
        ))

        # R4: Founder's case, corrected (G7 active + 2+ sources + D4 promoting + W1 no site + W2 task gap) -> B
        r4_req = [ConditionID.G7, ConditionID.D4, ConditionID.W1, ConditionID.W2]
        r4_matched = [c for c in r4_req if met(c)]
        r4_ok = (len(r4_req) == len(r4_matched))
        matches.append(RecipeMatch(
            recipe_id=RecipeID.R4,
            name="Founder's Case (Corrected)",
            target_segment=Segment.B,
            is_matched=r4_ok,
            required_conditions=r4_req,
            matched_conditions=r4_matched,
            opening_fact=f"Your active promotions send customers to {meta.get('current_destination', 'social pages')}, but {meta.get('missing_task_name', 'online booking and catalog evaluation')} cannot be completed there.",
            pitch_angle="Implement a high-converting dedicated booking/product portal directly fulfilling your promo traffic.",
            never_say="You have no website and are invisible.",
            recommended_solution="Single-purpose customer task hub (booking or ordering portal).",
        ))

        # R5: Social attention, unanswered questions (Social-only + D2 + W7) -> B
        r5_req = [ConditionID.D2, ConditionID.W7]
        r5_matched = [c for c in r5_req if met(c)]
        r5_ok = (len(r5_req) == len(r5_matched)) and (facts.owned_presence == OwnedPresence.SOCIAL_ONLY)
        matches.append(RecipeMatch(
            recipe_id=RecipeID.R5,
            name="Social Attention, Unanswered Questions",
            target_segment=Segment.B,
            is_matched=r5_ok,
            required_conditions=r5_req,
            matched_conditions=r5_matched,
            opening_fact=f"Across your recent posts, customers frequently ask for {meta.get('unanswered_topic', 'pricing and availability details')} without a direct link to find it.",
            pitch_angle="Set up a structured self-service FAQ & pricing page to capture inbound social demand immediately.",
            never_say="Your social media strategy is bad.",
            recommended_solution="Digital price list & instant inquiry capture microsite.",
        ))

        # R6: Ad leads to a broken page (D1 + W5/W12) -> B
        r6_req = [ConditionID.D1]
        r6_matched = [c for c in r6_req if met(c)]
        r6_ok = met(ConditionID.D1) and (met(ConditionID.W5) or met(ConditionID.W12))
        matches.append(RecipeMatch(
            recipe_id=RecipeID.R6,
            name="Ad Leads to Broken Page",
            target_segment=Segment.B,
            is_matched=r6_ok,
            required_conditions=r6_req,
            matched_conditions=r6_matched,
            opening_fact=f"The ad running on {meta.get('ad_network', 'Meta/Google')} links to {meta.get('ad_destination_url', 'your landing page')}, where {meta.get('action_error', 'the checkout/booking action failed on test')}.",
            pitch_angle="Immediate fix for your live landing page conversion flow to prevent dropped paid clicks.",
            never_say="Your ad spend is being wasted completely.",
            recommended_solution="Conversion flow repair & landing page recovery.",
        ))

        # R7: Live business, dead site (G7 + W3 + W12) -> B
        r7_req = [ConditionID.G7, ConditionID.W3]
        r7_matched = [c for c in r7_req if met(c)]
        r7_ok = met(ConditionID.G7) and met(ConditionID.W3)
        matches.append(RecipeMatch(
            recipe_id=RecipeID.R7,
            name="Live Business, Dead Official Site",
            target_segment=Segment.B,
            is_matched=r7_ok,
            required_conditions=r7_req,
            matched_conditions=r7_matched,
            opening_fact=f"Your active profiles link to {meta.get('website_url', 'your official site')}; it returned server connection errors on repeat checks 24 hours apart.",
            pitch_angle="Reliable hosting migration and DNS restoration to bring your official presence back online.",
            never_say="Your company looks abandoned.",
            recommended_solution="Emergency uptime restoration & modernization hosting.",
        ))

        # R8: Booking bottleneck (Appointment business + D2 booking requests + W5 or W2) -> B
        r8_req = [ConditionID.D2]
        r8_matched = [c for c in r8_req if met(c)]
        r8_ok = met(ConditionID.D2) and (met(ConditionID.W2) or met(ConditionID.W5))
        matches.append(RecipeMatch(
            recipe_id=RecipeID.R8,
            name="Booking Bottleneck",
            target_segment=Segment.B,
            is_matched=r8_ok,
            required_conditions=r8_req,
            matched_conditions=r8_matched,
            opening_fact=f"Customers inquiring about appointments currently have no direct online scheduling option.",
            pitch_angle="Introduce automated calendar booking with instant confirmation to eliminate manual coordination.",
            never_say="You are missing hundreds of bookings every week.",
            recommended_solution="Direct scheduling & calendar integration.",
        ))

        # R9: Marketplace business wants direct (D12 + D5 + W2) -> B
        r9_req = [ConditionID.D12, ConditionID.D5, ConditionID.W2]
        r9_matched = [c for c in r9_req if met(c)]
        r9_ok = (len(r9_req) == len(r9_matched))
        matches.append(RecipeMatch(
            recipe_id=RecipeID.R9,
            name="Marketplace Wants Direct Channel",
            target_segment=Segment.B,
            is_matched=r9_ok,
            required_conditions=r9_req,
            matched_conditions=r9_matched,
            opening_fact=f"You currently take orders through third-party aggregators while indicating an objective to serve repeat customers directly.",
            pitch_angle="Launch an independent direct ordering portal with 0% commissions for loyal customer reorders.",
            never_say="Aggregators are robbing your profits.",
            recommended_solution="Commission-free direct ordering system.",
        ))

        # R10: Branches, confused journey (D6 + W8/W9 + authority) -> B
        r10_req = [ConditionID.D6]
        r10_matched = [c for c in r10_req if met(c)]
        r10_ok = met(ConditionID.D6) and (met(ConditionID.W8) or met(ConditionID.W9))
        matches.append(RecipeMatch(
            recipe_id=RecipeID.R10,
            name="Multi-Location Confused Journey",
            target_segment=Segment.B,
            is_matched=r10_ok,
            required_conditions=r10_req,
            matched_conditions=r10_matched,
            opening_fact="Across your active locations, customers encounter different addresses and contact hours depending on which directory they land on.",
            pitch_angle="Synchronized multi-location locator and unified branch booking links.",
            never_say="Your branch network is in disarray.",
            recommended_solution="Multi-location portal with store locator and branch-specific booking.",
        ))

        # R11: Moved, web didn't follow (D7 + W8) -> B
        r11_req = [ConditionID.D7, ConditionID.W8]
        r11_matched = [c for c in r11_req if met(c)]
        r11_ok = (len(r11_req) == len(r11_matched))
        matches.append(RecipeMatch(
            recipe_id=RecipeID.R11,
            name="Moved, Web Did Not Follow",
            target_segment=Segment.B,
            is_matched=r11_ok,
            required_conditions=r11_req,
            matched_conditions=r11_matched,
            opening_fact=f"Your recent announcement lists your new address at {meta.get('new_address', 'your new facility')}, while existing web listings still display {meta.get('old_address', 'the previous location')}.",
            pitch_angle="A comprehensive digital sync to update your canonical location across maps, schemas, and web assets.",
            never_say="You are losing customers because people are showing up at the wrong door.",
            recommended_solution="Location synchronization & Schema.org entity update.",
        ))

        # R12: Export buyers can't evaluate (D9 + W7/W10) -> B
        r12_req = [ConditionID.D9]
        r12_matched = [c for c in r12_req if met(c)]
        r12_ok = met(ConditionID.D9) and (met(ConditionID.W7) or met(ConditionID.W10))
        matches.append(RecipeMatch(
            recipe_id=RecipeID.R12,
            name="Export Buyers Cannot Evaluate",
            target_segment=Segment.B,
            is_matched=r12_ok,
            required_conditions=r12_req,
            matched_conditions=r12_matched,
            opening_fact="International buyer inquiries require technical specification sheets and certifications currently missing from your public digital materials.",
            pitch_angle="Multi-lingual export catalogue with downloadable CAD/spec sheets and compliance credentials.",
            never_say="Foreign buyers will refuse to do business with you.",
            recommended_solution="International B2B digital export portal.",
        ))

        # R13: Mobile failure under demand (W6 + D2/D3) -> B
        r13_req = [ConditionID.W6]
        r13_matched = [c for c in r13_req if met(c)]
        r13_ok = met(ConditionID.W6) and (met(ConditionID.D2) or met(ConditionID.D3))
        matches.append(RecipeMatch(
            recipe_id=RecipeID.R13,
            name="Mobile Failure Under Active Demand",
            target_segment=Segment.B,
            is_matched=r13_ok,
            required_conditions=r13_req,
            matched_conditions=r13_matched,
            opening_fact="On standard mobile screen sizes (375px and 414px), core navigation links and inquiry fields overlap and cannot be tapped.",
            pitch_angle="Responsive mobile viewport optimization to ensure smartphone visitors can reach you seamlessly.",
            never_say="Your mobile website is completely unusable.",
            recommended_solution="Mobile-first responsive rebuild.",
        ))

        # R14: Accessibility blocked (G7 + W13) -> B
        r14_req = [ConditionID.G7, ConditionID.W13]
        r14_matched = [c for c in r14_req if met(c)]
        r14_ok = (len(r14_req) == len(r14_matched))
        matches.append(RecipeMatch(
            recipe_id=RecipeID.R14,
            name="Accessibility Barrier Blocks Task",
            target_segment=Segment.B,
            is_matched=r14_ok,
            required_conditions=r14_req,
            matched_conditions=r14_matched,
            opening_fact="Using keyboard navigation, the primary consultation form cannot be reached or focused.",
            pitch_angle="Remediate interactive form elements to satisfy WCAG 2.1 AA keyboard accessibility criteria.",
            never_say="Your website is illegal and exposes you to lawsuits.",
            recommended_solution="WCAG accessibility remediation.",
        ))

        # R15: Self-built site, one task missing (I8 + W2 + D2) -> B
        r15_req = [ConditionID.I8, ConditionID.W2, ConditionID.D2]
        r15_matched = [c for c in r15_req if met(c)]
        r15_ok = (len(r15_req) == len(r15_matched))
        matches.append(RecipeMatch(
            recipe_id=RecipeID.R15,
            name="Self-Built Site, Core Task Missing",
            target_segment=Segment.B,
            is_matched=r15_ok,
            required_conditions=r15_req,
            matched_conditions=r15_matched,
            opening_fact="Your new builder site is live, but does not yet connect to a functional payment or booking system.",
            pitch_angle="Assist with connecting professional payment/booking integrations into your existing layout.",
            never_say="Template builders look cheap.",
            recommended_solution="Custom checkout and workflow integration.",
        ))

        # R16: Launch underway, supplier chosen (I5/I6 + C3) -> C
        r16_req = [ConditionID.C3]
        r16_matched = [c for c in r16_req if met(c)]
        r16_ok = met(ConditionID.C3) and (met(ConditionID.I5) or met(ConditionID.I6))
        matches.append(RecipeMatch(
            recipe_id=RecipeID.R16,
            name="Launch Underway, Supplier Chosen",
            target_segment=Segment.C,
            is_matched=r16_ok,
            required_conditions=r16_req,
            matched_conditions=r16_matched,
            opening_fact="An agency partner is already actively building the upcoming web launch.",
            pitch_angle="Do not outreach. Respect incumbent partner engagement.",
            never_say="Any pitch.",
            recommended_solution="Archive until next review cycle.",
        ))

        # R17: Something in motion (G7 + D4 + any of I5-I7) -> Warm
        r17_req = [ConditionID.G7, ConditionID.D4]
        r17_matched = [c for c in r17_req if met(c)]
        r17_ok = met(ConditionID.G7) and met(ConditionID.D4) and (met(ConditionID.I5) or met(ConditionID.I6) or met(ConditionID.I7))
        matches.append(RecipeMatch(
            recipe_id=RecipeID.R17,
            name="Something in Motion (Warm)",
            target_segment=Segment.B,  # Warm context
            is_matched=r17_ok,
            required_conditions=r17_req,
            matched_conditions=r17_matched,
            opening_fact=f"I noticed your recent {meta.get('motion_signal', 'new domain registration or coming-soon notice')}.",
            pitch_angle="Inquire whether the upcoming project is already staffed internally, or if an agile delivery team could accelerate rollout.",
            never_say="We know you're looking.",
            recommended_solution="Agile acceleration proposal.",
        ))

        return [m for m in matches if m.is_matched]

    @classmethod
    def _build_pitch(
        cls,
        segment: Segment,
        warm_context: bool,
        recipes: List[RecipeMatch],
        meta: Dict[str, Any],
    ) -> Dict[str, str]:
        """Constructs the tailored pitch complying with Section 5 rules."""
        if recipes:
            primary = recipes[0]
            return {
                "opening_fact": primary.opening_fact,
                "pitch_angle": primary.pitch_angle,
                "never_say": primary.never_say,
                "recommended_solution": primary.recommended_solution,
            }

        if segment == Segment.A:
            return {
                "opening_fact": f"Your request on {meta.get('request_date', 'recent dates')} mentions {meta.get('requested_scope', 'digital development')}.",
                "pitch_angle": "Answer the declared scope directly with clear milestones.",
                "never_say": "You need a website.",
                "recommended_solution": "Direct proposal addressing declared requirements.",
            }
        elif warm_context:
            return {
                "opening_fact": f"I noticed your {meta.get('motion_signal', 'new domain / coming-soon launch')}.",
                "pitch_angle": "Ask if they have help; offer speed and technical bandwidth.",
                "never_say": "We know you're looking.",
                "recommended_solution": "Speed-to-launch sprint.",
            }
        elif segment == Segment.B:
            return {
                "opening_fact": f"Your profiles link to {meta.get('current_destination', 'your links')}, where {meta.get('missing_task', 'booking/menu details')} is not accessible.",
                "pitch_angle": "Offer the smallest useful fix solving that concrete task gap.",
                "never_say": "You're losing revenue.",
                "recommended_solution": "Dedicated customer task page.",
            }
        elif segment == Segment.C:
            return {
                "opening_fact": "Current operational channels meet verified customer requirements.",
                "pitch_angle": "Respect the current operational choice; no pitch.",
                "never_say": "Your agency/setup is failing.",
                "recommended_solution": "Do not pitch. Log in suppression registry.",
            }
        else:
            return {
                "opening_fact": "Observations currently incomplete across canonical discovery paths.",
                "pitch_angle": "Conduct further absence verification before proposing digital solutions.",
                "never_say": "Assuming a website is needed.",
                "recommended_solution": "Research candidate.",
            }
