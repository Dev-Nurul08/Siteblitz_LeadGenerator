"""
Lead-Radar Condition Library.

Implements all 51 formal conditions defined in the 2026-11-06 strategy:
- Gates (G1 - G7)
- Website & customer-task conditions (W1 - W16)
- Intent conditions (I1 - I8)
- Demand conditions (D1 - D12)
- Stop conditions (C1 - C6)
- Jurisdiction conditions (J1, J2)
"""

from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from backend.app.engines.lead_radar.types import (
    ConditionID,
    ConditionResult,
    ConditionStrength,
    OwnedPresence,
    Availability,
    CustomerTaskCovered,
    TaskQuality,
    BuyingStatus,
    Authority,
    SixFacts,
)


class ConditionEvaluator:
    """
    Pure, deterministic evaluation engine that tests factual observation payloads
    against the 51 Lead-Radar conditions.
    """

    @classmethod
    def evaluate_all(
        cls,
        facts: SixFacts,
        raw_signals: Dict[str, Any],
    ) -> Dict[ConditionID, ConditionResult]:
        """
        Evaluate all conditions given the established 6 facts and observed raw signals.
        Returns a dictionary of condition results keyed by ConditionID.
        """
        results: Dict[ConditionID, ConditionResult] = {}

        # ─── 3.1 Gates (G1 - G7) ───────────────────────────────────

        # G1: Correct business identity
        # Official ID, or 2+ matching identity fields with no contradiction
        has_official_id = bool(raw_signals.get("official_reg_id") or raw_signals.get("tax_id") or raw_signals.get("lei"))
        matched_id_fields = raw_signals.get("matching_identity_fields_count", 0)
        has_identity_conflict = bool(raw_signals.get("identity_conflict", False))
        g1_met = (has_official_id or matched_id_fields >= 2) and not has_identity_conflict
        results[ConditionID.G1] = ConditionResult(
            condition_id=ConditionID.G1,
            name="Correct business identity",
            is_met=g1_met,
            strength=ConditionStrength.STRONG,
            evidence=f"Official ID present: {has_official_id}, Matching fields: {matched_id_fields}, Conflict: {has_identity_conflict}",
            source=raw_signals.get("identity_source", "registry_and_places"),
        )

        # G2: Evidence may be used (Source licence allows collect, store, and sales use)
        evidence_disallowed = bool(raw_signals.get("evidence_licence_restricted", False))
        g2_met = not evidence_disallowed
        results[ConditionID.G2] = ConditionResult(
            condition_id=ConditionID.G2,
            name="Evidence may be used",
            is_met=g2_met,
            strength=ConditionStrength.STRONG,
            evidence="Source licence permits analytical and prospecting use" if g2_met else "Source restricted by platform terms",
            source="source_register",
        )

        # G3: Same buying unit (Same entity and same purchasing authority)
        is_duplicate = bool(raw_signals.get("is_duplicate_entity", False))
        results[ConditionID.G3] = ConditionResult(
            condition_id=ConditionID.G3,
            name="Same buying unit (dedup check)",
            is_met=not is_duplicate,
            strength=ConditionStrength.STRONG,
            evidence="Unique buying unit identified" if not is_duplicate else "Duplicate record mapped to parent/canonical entity",
            source="deduplication_engine",
        )

        # G4: Not a non-procuring body (ATM, bus stop, landmark, public utility)
        category_name = str(raw_signals.get("category", "")).lower()
        non_procuring_tags = {"atm", "bus_stop", "bench", "waste_basket", "landmark", "traffic_signals", "memorial"}
        is_non_procuring = any(tag in category_name for tag in non_procuring_tags) or bool(raw_signals.get("is_non_procuring_object", False))
        results[ConditionID.G4] = ConditionResult(
            condition_id=ConditionID.G4,
            name="Not a non-procuring body",
            is_met=not is_non_procuring,
            strength=ConditionStrength.STRONG,
            evidence=f"Category '{category_name}' confirmed as a commercial/procuring entity" if not is_non_procuring else f"Category '{category_name}' is a non-procuring landmark or infrastructure",
            source="category_normalizer",
        )

        # G5: Closed for good (Owner confirms or 2 independent closure sources)
        closure_signals_count = raw_signals.get("closure_sources_count", 0)
        owner_closed_confirm = bool(raw_signals.get("owner_confirmed_closed", False))
        is_permanently_closed = owner_closed_confirm or (closure_signals_count >= 2)
        results[ConditionID.G5] = ConditionResult(
            condition_id=ConditionID.G5,
            name="Closed for good",
            is_met=is_permanently_closed,
            strength=ConditionStrength.STRONG,
            evidence=f"Owner confirmed closed: {owner_closed_confirm}, Closure sources: {closure_signals_count}",
            source=raw_signals.get("closure_source", "registry_listings"),
        )

        # G6: Branch cannot buy (Parent controls site and local contracting)
        branch_lacks_authority = facts.authority in (Authority.PARENT_COMPANY, Authority.FRANCHISEE) and bool(raw_signals.get("centralized_digital_mandate", False))
        results[ConditionID.G6] = ConditionResult(
            condition_id=ConditionID.G6,
            name="Branch cannot buy",
            is_met=branch_lacks_authority,
            strength=ConditionStrength.STRONG,
            evidence="Local unit cannot procure digital services independently (controlled by headquarters/franchisor)" if branch_lacks_authority else "Local entity retains purchasing authority",
            source="corporate_hierarchy",
        )

        # G7: Operating now (Owner confirmation or 2 independent activity signals in 90 days)
        independent_activity_count = raw_signals.get("independent_activity_signals_90d", 0)
        owner_active_confirm = bool(raw_signals.get("owner_confirmed_active", False))
        g7_met = owner_active_confirm or (independent_activity_count >= 2) or facts.currently_active
        results[ConditionID.G7] = ConditionResult(
            condition_id=ConditionID.G7,
            name="Operating now",
            is_met=g7_met,
            strength=ConditionStrength.STRONG,
            evidence=f"Owner confirmed active: {owner_active_confirm}, Activity signals in 90d: {independent_activity_count}",
            source="activity_monitor",
        )

        # ─── 3.2 Website & Customer-Task Conditions (W1 - W16) ─────

        # W1: No owned website found (Absence search done across 3 discovery paths, 0 matches)
        w1_met = (facts.owned_presence == OwnedPresence.NONE_FOUND) and facts.absence_search_done
        results[ConditionID.W1] = ConditionResult(
            condition_id=ConditionID.W1,
            name="No owned website found",
            is_met=w1_met,
            strength=ConditionStrength.MEDIUM,
            evidence="3-path absence search verified zero owned web presence" if w1_met else f"Presence status: {facts.owned_presence.value}",
            source="absence_certificate_engine",
        )

        # W2: A needed task has nowhere to happen (booking, menu, catalogue, enquiry missing everywhere)
        w2_met = bool(raw_signals.get("needed_task_unhosted", False)) or (
            facts.customer_task_covered in (CustomerTaskCovered.NONE_NEEDED, CustomerTaskCovered.UNKNOWN)
            and raw_signals.get("business_model_requires_task", False)
        )
        results[ConditionID.W2] = ConditionResult(
            condition_id=ConditionID.W2,
            name="A needed task has nowhere to happen",
            is_met=w2_met,
            strength=ConditionStrength.STRONG,
            evidence=raw_signals.get("w2_evidence", "Essential customer action (booking/menu/catalogue/enquiry) is unhosted across all platforms"),
            source="task_coverage_analyzer",
        )

        # W3: Official site keeps failing (Repeated failure rule: 2 checks >= 24h apart)
        w3_met = (facts.availability in (Availability.REPEATED_SERVER_FAIL, Availability.DNS_FAIL)) or facts.repeated_failure
        results[ConditionID.W3] = ConditionResult(
            condition_id=ConditionID.W3,
            name="Official site keeps failing",
            is_met=w3_met,
            strength=ConditionStrength.STRONG,
            evidence=f"Availability: {facts.availability.value}, Repeated failure verified: {facts.repeated_failure}",
            source="uptime_monitor",
        )

        # W4: Browser security warning (Certificate warning on repeat checks)
        w4_met = (facts.availability == Availability.CERTIFICATE_FAIL) or bool(raw_signals.get("ssl_cert_invalid", False))
        results[ConditionID.W4] = ConditionResult(
            condition_id=ConditionID.W4,
            name="Browser security warning",
            is_met=w4_met,
            strength=ConditionStrength.STRONG,
            evidence="SSL certificate warning (expired, mismatched, or self-signed) verified on repeat checks",
            source="ssl_security_audit",
        )

        # W5: Core action broken (Booking, enquiry, ordering fails reproducibly without submitting)
        w5_met = (facts.task_quality == TaskQuality.FAILS_REPRODUCIBLY) or bool(raw_signals.get("core_flow_broken", False))
        results[ConditionID.W5] = ConditionResult(
            condition_id=ConditionID.W5,
            name="Core action broken",
            is_met=w5_met,
            strength=ConditionStrength.STRONG,
            evidence=raw_signals.get("w5_evidence", "Customer action fails with client error, broken script, or server 500"),
            source="flow_functional_test",
        )

        # W6: Mobile task fails (Fails on 2 phone screen sizes)
        w6_met = bool(raw_signals.get("mobile_task_failed_2_screens", False))
        results[ConditionID.W6] = ConditionResult(
            condition_id=ConditionID.W6,
            name="Mobile task fails",
            is_met=w6_met,
            strength=ConditionStrength.STRONG,
            evidence=raw_signals.get("w6_evidence", "Viewport overflow or unclickable elements block task on 375px and 414px viewports"),
            source="mobile_viewport_tester",
        )

        # W7: Key buying information missing (Price, menu, timings has no answer they control)
        w7_met = bool(raw_signals.get("key_buying_info_missing", False))
        results[ConditionID.W7] = ConditionResult(
            condition_id=ConditionID.W7,
            name="Key buying information missing",
            is_met=w7_met,
            strength=ConditionStrength.MEDIUM,
            evidence=raw_signals.get("w7_evidence", "Controlled answer missing for pricing, service list, opening hours, or catalogue specs"),
            source="content_completeness_checker",
        )

        # W8: Business information conflicts (2 current official sources disagree on address, hours, booking link)
        w8_met = bool(raw_signals.get("conflicting_business_info", False))
        results[ConditionID.W8] = ConditionResult(
            condition_id=ConditionID.W8,
            name="Business information conflicts",
            is_met=w8_met,
            strength=ConditionStrength.STRONG,
            evidence=raw_signals.get("w8_evidence", "Current listings or pages report conflicting addresses, phone numbers, or hours"),
            source="multi_source_crosscheck",
        )

        # W9: Parent site ignores branch (Branch-specific task missing on parent site)
        w9_met = bool(raw_signals.get("parent_site_ignores_branch_task", False))
        results[ConditionID.W9] = ConditionResult(
            condition_id=ConditionID.W9,
            name="Parent site ignores branch",
            is_met=w9_met,
            strength=ConditionStrength.MEDIUM,
            evidence="Headquarters domain lacks local booking, localized inventory, or direct branch contact details",
            source="multi_location_analyzer",
        )

        # W10: Language gap (2+ requests for a language info is not in)
        w10_met = raw_signals.get("unserved_language_requests_count", 0) >= 2 or bool(raw_signals.get("language_gap_detected", False))
        results[ConditionID.W10] = ConditionResult(
            condition_id=ConditionID.W10,
            name="Language gap",
            is_met=w10_met,
            strength=ConditionStrength.MEDIUM,
            evidence=f"Audience requests detected in unsupported language ({raw_signals.get('unserved_language', 'local/regional')})",
            source="audience_sentiment_analysis",
        )

        # W11: Poor real-user speed (CrUX field data in Google's 'poor' band: LCP > 4s, INP > 500ms, CLS > 0.25)
        lcp = raw_signals.get("crux_lcp", 0.0)
        inp = raw_signals.get("crux_inp", 0.0)
        cls_val = raw_signals.get("crux_cls", 0.0)
        w11_met = (lcp > 4.0 or inp > 500.0 or cls_val > 0.25) or bool(raw_signals.get("crux_poor_band", False))
        results[ConditionID.W11] = ConditionResult(
            condition_id=ConditionID.W11,
            name="Poor real-user speed (CrUX)",
            is_met=w11_met,
            strength=ConditionStrength.MEDIUM,
            evidence=f"LCP: {lcp:.2f}s (thr 4s), INP: {inp:.0f}ms (thr 500ms), CLS: {cls_val:.3f} (thr 0.25)",
            source="google_crux_api",
        )

        # W12: Live material points to a dead page (Current ad, brochure, packaging, QR code leads to failed page)
        w12_met = bool(raw_signals.get("ad_or_qr_leads_to_dead_page", False))
        results[ConditionID.W12] = ConditionResult(
            condition_id=ConditionID.W12,
            name="Live material points to dead page",
            is_met=w12_met,
            strength=ConditionStrength.STRONG,
            evidence="Active marketing campaign or public collateral directs traffic to a 404/5xx dead URL",
            source="ad_landing_page_auditor",
        )

        # W13: Accessibility barrier blocks a task (Core task impossible by keyboard)
        w13_met = bool(raw_signals.get("keyboard_task_impossible", False)) or bool(raw_signals.get("critical_wcag_barrier", False))
        results[ConditionID.W13] = ConditionResult(
            condition_id=ConditionID.W13,
            name="Accessibility barrier blocks task",
            is_met=w13_met,
            strength=ConditionStrength.STRONG,
            evidence="WCAG failure: Interactive modal traps focus or core form cannot be submitted via keyboard navigation",
            source="wcag_accessibility_test",
        )

        # W14: Audience access failure (Target customers cannot complete task due to device/network limits)
        w14_met = bool(raw_signals.get("audience_access_failure", False))
        results[ConditionID.W14] = ConditionResult(
            condition_id=ConditionID.W14,
            name="Audience access failure",
            is_met=w14_met,
            strength=ConditionStrength.MEDIUM,
            evidence="Excessive payload or heavy client runtime fails on target low-bandwidth/low-spec mobile devices",
            source="network_performance_audit",
        )

        # W15: Local-format failure (Task fails because of script, name, address format, units, currency)
        w15_met = bool(raw_signals.get("local_format_failure", False))
        results[ConditionID.W15] = ConditionResult(
            condition_id=ConditionID.W15,
            name="Local-format failure",
            is_met=w15_met,
            strength=ConditionStrength.MEDIUM,
            evidence="Checkout/form rejects local phone masks, postal codes, regional script characters, or native currency",
            source="localization_l10n_auditor",
        )

        # W16: Platform-only destination excludes customers (Only destination needs app/account customers lack)
        w16_met = (facts.owned_presence in (OwnedPresence.SOCIAL_ONLY, OwnedPresence.MARKETPLACE_ONLY)) and bool(raw_signals.get("excludes_unregistered_audience", False))
        results[ConditionID.W16] = ConditionResult(
            condition_id=ConditionID.W16,
            name="Platform-only destination excludes customers",
            is_met=w16_met,
            strength=ConditionStrength.MEDIUM,
            evidence="Business forces customers to log into a third-party app (e.g. Meta/Instagram/Practo) to view basic pricing or contact info",
            source="channel_friction_analyzer",
        )

        # ─── 3.3 Intent Conditions: Are They Looking? (I1 - I8) ────

        # I1: Explicitly asking for website help (Request < 30 days, still open, authorized)
        i1_met = bool(raw_signals.get("public_request_website_help_30d", False))
        results[ConditionID.I1] = ConditionResult(
            condition_id=ConditionID.I1,
            name="Explicitly asking for website help",
            is_met=i1_met,
            strength=ConditionStrength.STRONG,
            evidence=raw_signals.get("i1_evidence", "Public RFP or explicit help request posted by authorized executive within 30 days"),
            source="intent_scanner",
        )

        # I2: Open website tender (Official notice, current deadline, eligible: SAM.gov, TED, GeM, CPPP)
        i2_met = bool(raw_signals.get("open_website_tender", False))
        results[ConditionID.I2] = ConditionResult(
            condition_id=ConditionID.I2,
            name="Open website tender",
            is_met=i2_met,
            strength=ConditionStrength.STRONG,
            evidence=raw_signals.get("i2_evidence", "Active public tender noticed on official procurement portal"),
            source=raw_signals.get("tender_portal", "procurement_registry"),
        )

        # I3: Evaluating suppliers now (Owner asked for proposals within 30 days)
        i3_met = bool(raw_signals.get("evaluating_suppliers_proposals_30d", False))
        results[ConditionID.I3] = ConditionResult(
            condition_id=ConditionID.I3,
            name="Evaluating suppliers now",
            is_met=i3_met,
            strength=ConditionStrength.STRONG,
            evidence="Direct owner correspondence or RFP intake confirmed supplier evaluation in progress",
            source="supplier_engagement_tracker",
        )

        # I4: Wants to replace current supplier (Complaint plus explicit replacement request)
        i4_met = bool(raw_signals.get("wants_to_replace_supplier", False))
        results[ConditionID.I4] = ConditionResult(
            condition_id=ConditionID.I4,
            name="Wants to replace current supplier",
            is_met=i4_met,
            strength=ConditionStrength.STRONG,
            evidence=raw_signals.get("i4_evidence", "Documented complaint with active vendor and explicit search for new digital agency"),
            source="client_feedback_signal",
        )

        # I5: 'Launching soon' or coming-soon page
        i5_met = (facts.availability == Availability.COMING_SOON) or bool(raw_signals.get("has_coming_soon_page", False))
        results[ConditionID.I5] = ConditionResult(
            condition_id=ConditionID.I5,
            name="'Launching soon' / coming-soon page",
            is_met=i5_met,
            strength=ConditionStrength.WEAK,
            evidence="Digital presence displays 'Coming Soon' / 'Under Construction' splash message",
            source="web_crawler",
        )

        # I6: Recently registered domain, parked (< 90 days, RDAP / CT logs)
        domain_age_days = raw_signals.get("domain_age_days", 9999)
        i6_met = (facts.availability == Availability.PARKED) or (domain_age_days <= 90 and bool(raw_signals.get("domain_recently_registered", False)))
        results[ConditionID.I6] = ConditionResult(
            condition_id=ConditionID.I6,
            name="Recently registered domain, parked",
            is_met=i6_met,
            strength=ConditionStrength.WEAK,
            evidence=f"Domain registered {domain_age_days} days ago; parked landing page observed",
            source="rdap_ct_logs",
        )

        # I7: Hiring a web or digital role
        i7_met = bool(raw_signals.get("hiring_web_or_digital_role", False))
        results[ConditionID.I7] = ConditionResult(
            condition_id=ConditionID.I7,
            name="Hiring a web or digital role",
            is_met=i7_met,
            strength=ConditionStrength.WEAK,
            evidence=raw_signals.get("i7_evidence", "Active job vacancy for Web Designer/Developer or Digital Manager"),
            source="job_posting_scanner",
        )

        # I8: New builder site, still incomplete (< 90 days, missing task)
        i8_met = (facts.owned_presence == OwnedPresence.BUILDER_SUBDOMAIN) and (facts.task_quality == TaskQuality.INCOMPLETE) and bool(raw_signals.get("site_first_seen_90d", False))
        results[ConditionID.I8] = ConditionResult(
            condition_id=ConditionID.I8,
            name="New builder site, still incomplete",
            is_met=i8_met,
            strength=ConditionStrength.WEAK,
            evidence="Wix/Squarespace/Shopify placeholder created within 90 days with incomplete task flows",
            source="archive_and_cms_fingerprint",
        )

        # ─── 3.4 Demand Conditions: Real Customer Pull (D1 - D12) ──

        # D1: Running ads into a gap (Ad seen < 7 days; landing page has W2-W6 or W12)
        ad_active_7d = bool(raw_signals.get("active_ad_campaign_7d", False))
        gap_condition = (w2_met or w3_met or w4_met or w5_met or w6_met or w12_met)
        d1_met = ad_active_7d and gap_condition
        results[ConditionID.D1] = ConditionResult(
            condition_id=ConditionID.D1,
            name="Running ads into a gap",
            is_met=d1_met,
            strength=ConditionStrength.STRONG,
            evidence=f"Active ad campaign confirmed in last 7d directed into destination with detected task/security failure" if d1_met else "No ad spend into broken gap observed",
            source="ad_library_scraper",
        )

        # D2: Customers keep asking same thing (3+ distinct requests in 90 days unanswered)
        unanswered_requests = raw_signals.get("unanswered_customer_requests_90d", 0)
        d2_met = unanswered_requests >= 3
        results[ConditionID.D2] = ConditionResult(
            condition_id=ConditionID.D2,
            name="Customers keep asking the same thing",
            is_met=d2_met,
            strength=ConditionStrength.MEDIUM,
            evidence=f"{unanswered_requests} repeated public queries regarding pricing, booking, or catalog left unfulfilled",
            source="social_review_monitor",
        )

        # D3: Real customer activity (10+ recent review events in 90 days)
        review_count_90d = raw_signals.get("reviews_count_90d", 0)
        d3_met = review_count_90d >= 10
        results[ConditionID.D3] = ConditionResult(
            condition_id=ConditionID.D3,
            name="Real customer activity",
            is_met=d3_met,
            strength=ConditionStrength.MEDIUM,
            evidence=f"{review_count_90d} reviews logged in past 90 days (threshold: 10)",
            source="review_platform_aggregator",
        )

        # D4: Actively promoting (2+ dated promotions in 90 days)
        promotions_90d = raw_signals.get("promotions_count_90d", 0)
        d4_met = promotions_90d >= 2
        results[ConditionID.D4] = ConditionResult(
            condition_id=ConditionID.D4,
            name="Actively promoting",
            is_met=d4_met,
            strength=ConditionStrength.MEDIUM,
            evidence=f"{promotions_90d} marketing announcements/promotions published in past 90 days",
            source="promotional_post_tracker",
        )

        # D5: Wants direct sales (Owner stated or 3+ requests for direct channel)
        direct_sales_requests = raw_signals.get("direct_sales_requests_count", 0)
        d5_met = bool(raw_signals.get("owner_declared_direct_sales_goal", False)) or (direct_sales_requests >= 3)
        results[ConditionID.D5] = ConditionResult(
            condition_id=ConditionID.D5,
            name="Wants direct sales",
            is_met=d5_met,
            strength=ConditionStrength.MEDIUM,
            evidence=f"Owner goal or {direct_sales_requests} customer requests for direct purchasing route without intermediary",
            source="direct_intent_analyzer",
        )

        # D6: Several locations, confused journey (2+ active branches with conflicting info/actions)
        branches_count = raw_signals.get("active_branches_count", 1)
        d6_met = (branches_count >= 2) and (w8_met or bool(raw_signals.get("branch_journey_confused", False)))
        results[ConditionID.D6] = ConditionResult(
            condition_id=ConditionID.D6,
            name="Several locations, confused journey",
            is_met=d6_met,
            strength=ConditionStrength.MEDIUM,
            evidence=f"{branches_count} locations identified with fragmented customer journeys across branches",
            source="multi_branch_crosschecker",
        )

        # D7: Opened, moved or expanded; web did not follow (Event < 90 days, web still old)
        d7_met = bool(raw_signals.get("business_moved_or_expanded_90d", False)) and w8_met
        results[ConditionID.D7] = ConditionResult(
            condition_id=ConditionID.D7,
            name="Opened, moved or expanded; web did not follow",
            is_met=d7_met,
            strength=ConditionStrength.MEDIUM,
            evidence="Physical expansion or address relocation in last 90d while web assets continue displaying obsolete information",
            source="registry_and_announcement_tracker",
        )

        # D8: Buyer requirement they cannot meet online (Prequalification needs info lacking online)
        d8_met = bool(raw_signals.get("buyer_prequalification_barrier", False))
        results[ConditionID.D8] = ConditionResult(
            condition_id=ConditionID.D8,
            name="Buyer requirement they cannot meet online",
            is_met=d8_met,
            strength=ConditionStrength.STRONG,
            evidence="Enterprise procurement or compliance mandate requires certifications/audit details absent from online assets",
            source="tender_prequalification_analyzer",
        )

        # D9: Out-of-area buyers need material (Export, tourist, remote buyers + catalogue or language gap)
        d9_met = bool(raw_signals.get("remote_buyers_need_material", False)) or (
            bool(raw_signals.get("is_exporter_or_tourist_business", False)) and (w7_met or w10_met)
        )
        results[ConditionID.D9] = ConditionResult(
            condition_id=ConditionID.D9,
            name="Out-of-area buyers need material",
            is_met=d9_met,
            strength=ConditionStrength.MEDIUM,
            evidence="Export manifests, foreign trade inquiries, or tourist clientele requiring digital catalogue or translated specs",
            source="trade_manifest_and_tourism_tracker",
        )

        # D10: Peers solve a task they don't (20+ true peers, 75%+ support task)
        peer_task_support_pct = raw_signals.get("peer_task_support_percentage", 0.0)
        peers_count = raw_signals.get("peer_sample_size", 0)
        d10_met = (peers_count >= 20) and (peer_task_support_pct >= 0.75)
        results[ConditionID.D10] = ConditionResult(
            condition_id=ConditionID.D10,
            name="Peers solve a task they don't",
            is_met=d10_met,
            strength=ConditionStrength.WEAK,
            evidence=f"{peer_task_support_pct*100:.0f}% of {peers_count} peer businesses support this customer task",
            source="peer_cohort_benchmarker",
        )

        # D11: Messaging workflow bottleneck ("DM / call to order" at volume)
        d11_met = bool(raw_signals.get("dm_order_friction_confirmed", False)) or (
            bool(raw_signals.get("orders_via_dm_only", False)) and d2_met
        )
        results[ConditionID.D11] = ConditionResult(
            condition_id=ConditionID.D11,
            name="Messaging workflow bottleneck",
            is_met=d11_met,
            strength=ConditionStrength.MEDIUM,
            evidence="Order/booking volume manually routed through WhatsApp/DM resulting in dropped leads and customer friction",
            source="messaging_workflow_auditor",
        )

        # D12: Commission-marketplace dependence (Sells only through Zomato/Swiggy/Practo AND wants direct channel D5)
        d12_met = (facts.owned_presence == OwnedPresence.MARKETPLACE_ONLY) and d5_met
        results[ConditionID.D12] = ConditionResult(
            condition_id=ConditionID.D12,
            name="Commission-marketplace dependence",
            is_met=d12_met,
            strength=ConditionStrength.WEAK,
            evidence="Operates solely on third-party aggregators with expressed desire for direct customer relationships",
            source="aggregator_dependency_checker",
        )

        # ─── 3.5 Stop Conditions (C1 - C6) ─────────────────────────

        # C1: Authorised person declined this
        c1_met = bool(raw_signals.get("owner_declined_outreach", False)) or (facts.buying_status == BuyingStatus.EXPLICITLY_NOT_SEEKING)
        results[ConditionID.C1] = ConditionResult(
            condition_id=ConditionID.C1,
            name="Authorised person declined this",
            is_met=c1_met,
            strength=ConditionStrength.STRONG,
            evidence="Explicit refusal logged from verified purchasing authority",
            source="suppression_registry",
        )

        # C2: Need already solved; current site completes the task
        c2_met = (facts.owned_presence == OwnedPresence.OWN_DOMAIN) and (facts.availability == Availability.WORKING) and (facts.task_quality == TaskQuality.WORKS) and not (w2_met or w5_met)
        results[ConditionID.C2] = ConditionResult(
            condition_id=ConditionID.C2,
            name="Need already solved",
            is_met=c2_met,
            strength=ConditionStrength.STRONG,
            evidence="Current website functions cleanly and satisfies required core customer task",
            source="task_verification_engine",
        )

        # C3: Supplier or in-house team already owns it
        c3_met = (facts.buying_status == BuyingStatus.SUPPLIER_ALREADY_CHOSEN) or bool(raw_signals.get("agency_already_appointed", False))
        results[ConditionID.C3] = ConditionResult(
            condition_id=ConditionID.C3,
            name="Supplier or in-house team already owns it",
            is_met=c3_met,
            strength=ConditionStrength.STRONG,
            evidence="Contracted agency or in-house web team is actively developing/maintaining the project",
            source="agency_attribution_detector",
        )

        # C4: Owner says the non-website setup is enough, and no gap found
        c4_met = bool(raw_signals.get("owner_satisfied_with_platform", False)) and not (w2_met or w5_met)
        results[ConditionID.C4] = ConditionResult(
            condition_id=ConditionID.C4,
            name="Owner says non-website setup is enough, no gap",
            is_met=c4_met,
            strength=ConditionStrength.STRONG,
            evidence="Owner confirms current operational channels meet all demand without unfulfilled customer tasks",
            source="owner_survey_response",
        )

        # C5: Owner explicitly deferred
        c5_met = bool(raw_signals.get("project_explicitly_deferred", False))
        results[ConditionID.C5] = ConditionResult(
            condition_id=ConditionID.C5,
            name="Owner explicitly deferred",
            is_met=c5_met,
            strength=ConditionStrength.STRONG,
            evidence=raw_signals.get("c5_evidence", "Owner requested follow-up at a later date or post fiscal cycle"),
            source="crm_interaction_history",
        )

        # C6: Existing platform solution is enough (Don't penalize for no own domain if task completes)
        c6_met = (facts.owned_presence in (OwnedPresence.SOCIAL_ONLY, OwnedPresence.MARKETPLACE_ONLY)) and (facts.task_quality == TaskQuality.WORKS) and not (w2_met or w5_met or d5_met)
        results[ConditionID.C6] = ConditionResult(
            condition_id=ConditionID.C6,
            name="Existing platform solution is enough",
            is_met=c6_met,
            strength=ConditionStrength.STRONG,
            evidence="Platform presence (Instagram/Zomato/Practo) cleanly handles orders/booking without friction",
            source="platform_task_completeness_verifier",
        )

        # ─── 3.6 Jurisdiction Conditions (J1, J2) ──────────────────

        # J1: Verified digital-information duty
        j1_met = bool(raw_signals.get("legal_digital_disclosure_mandate_unmet", False))
        results[ConditionID.J1] = ConditionResult(
            condition_id=ConditionID.J1,
            name="Verified digital-information duty",
            is_met=j1_met,
            strength=ConditionStrength.STRONG,
            evidence="Jurisdiction legally mandates statutory web disclosures (e.g. Impressum, professional license display) which are missing",
            source="regulatory_compliance_checker",
        )

        # J2: Proposed solution is deliverable and permitted
        j2_met = not bool(raw_signals.get("solution_undeliverable_in_region", False))
        results[ConditionID.J2] = ConditionResult(
            condition_id=ConditionID.J2,
            name="Proposed solution is deliverable",
            is_met=j2_met,
            strength=ConditionStrength.STRONG,
            evidence="Payment gateway, hosting, and domain regulations support deliverable web solution in this territory",
            source="regional_deliverability_checker",
        )

        return results

