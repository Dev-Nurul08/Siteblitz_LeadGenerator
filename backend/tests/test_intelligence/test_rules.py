"""Acceptance tests for docs/spec/website-intelligence.md (pure rules, no network)."""

from datetime import datetime, timedelta, timezone

from backend.app.engines.intelligence.rules import Check, Facts, assess, skip_reason
from backend.app.models.intelligence import (
    CheckType as T,
    EvidenceConfidence,
    LeadTier,
    WebsiteVerdict as V,
)

NOW = datetime(2026, 11, 8, 12, 0, tzinfo=timezone.utc)


def facts(**kw):
    base = dict(name="Smile Dental", categories=["Dental Clinic"], phone="+91 98290 11111",
                email=None, social_platforms=[], raw_records=[])
    base.update(kw)
    return Facts(**base)


def no_site_checks(*extra):
    return [Check(1, T.SKIP_RULE, "pass"), Check(2, T.SOURCE_TAG, "none"),
            Check(3, T.DOMAIN_GUESS, "none", "smiledental.com", observed_at=NOW),
            Check(4, T.DOMAIN_GUESS, "none", "smiledental.in", observed_at=NOW), *extra]


def test_instagram_only_is_social_only_not_own_site():
    a = assess(no_site_checks(Check(5, T.SOCIAL_LINK, "found", "https://instagram.com/smile")),
               facts(social_platforms=["instagram"]), NOW)
    assert a.verdict == V.SOCIAL_ONLY_VERIFIED


def test_brand_tag_skips_unless_franchises_included():
    raw = [{"tags": {"amenity": "dentist", "brand:wikidata": "Q123"}}]
    assert skip_reason(facts(raw_records=raw)) is not None
    assert skip_reason(facts(raw_records=raw, include_franchises=True)) is None
    assert skip_reason(facts(raw_records=[{"brand_name": "Clove Dental"}])) is not None


def test_atm_and_vacant_are_skipped():
    assert skip_reason(facts(raw_records=[{"tags": {"amenity": "atm"}}]))
    assert skip_reason(facts(raw_records=[{"tags": {"shop": "vacant"}}]))
    assert skip_reason(facts(raw_records=[{"tags": {"disused:shop": "bakery"}}]))
    assert skip_reason(facts(raw_records=[{"basic_category": "bank_or_credit_union"}]))


def test_coaching_and_preschool_are_prospects_schools_are_skipped():
    """QA-038: 'school' as a substring skipped specialty_school (coaching classes) and preschool."""
    for category in ("specialty_school", "preschool", "tutoring_service", "educational_service"):
        assert skip_reason(facts(raw_records=[{"basic_category": category}])) is None, category
    for category in ("high_school", "elementary_school", "middle_school", "college_university"):
        assert skip_reason(facts(raw_records=[{"basic_category": category}])), category


def test_403_means_site_exists_not_down():
    checks = [Check(1, T.SOURCE_TAG, "found", "https://x.in"),
              Check(2, T.SITE_FETCH, "protected", "https://x.in", {"http_status": 403})]
    assert assess(checks, facts(), NOW).verdict == V.OWN_SITE_VERIFIED


def test_one_failure_is_unknown_two_failures_six_hours_apart_is_down():
    first = Check(2, T.SITE_FETCH, "failed", "https://x.in", observed_at=NOW - timedelta(hours=7))
    one = assess([Check(1, T.SOURCE_TAG, "found", "https://x.in"), first], facts(), NOW)
    assert (one.verdict, one.tier) == (V.UNKNOWN, LeadTier.REVIEW)
    two = assess([Check(1, T.SOURCE_TAG, "found", "https://x.in"), first,
                  Check(3, T.SITE_FETCH, "failed", "https://x.in", observed_at=NOW)], facts(), NOW)
    assert two.verdict == V.SITE_DOWN_CONFIRMED


def test_without_search_no_lead_is_hot():
    a = assess(no_site_checks(Check(9, T.MANUAL_ACTIVITY, "active", observed_at=NOW)), facts(), NOW)
    assert a.verdict == V.NO_SITE_VERIFIED
    assert a.confidence == EvidenceConfidence.MEDIUM
    assert a.tier == LeadTier.WARM


def test_full_evidence_no_site_dentist_is_hot_with_80_points_and_check_ids():
    checks = no_site_checks(Check(8, T.MANUAL_SEARCH, "none", observed_at=NOW),
                            Check(9, T.MANUAL_ACTIVITY, "active", observed_at=NOW))
    a = assess(checks, facts(), NOW)
    assert a.verdict == V.NO_SITE_VERIFIED and a.confidence == EvidenceConfidence.HIGH
    assert a.breakdown == {"website_gap": 60, "business_problem": 0, "activity": 10, "service_fit": 10}
    assert a.need_score == 80 and a.tier == LeadTier.HOT
    by_part = {r["part"]: r for r in a.reasons}
    assert 8 in by_part["website_gap"]["check_ids"] and 3 in by_part["website_gap"]["check_ids"]
    assert by_part["activity"]["check_ids"] == [9]


def test_hot_needs_a_contact_route():
    checks = no_site_checks(Check(8, T.MANUAL_SEARCH, "none", observed_at=NOW),
                            Check(9, T.MANUAL_ACTIVITY, "active", observed_at=NOW))
    a = assess(checks, facts(phone=None), NOW)
    assert a.tier == LeadTier.WARM


def test_manual_search_found_site_and_closed_business():
    assert assess(no_site_checks(Check(8, T.MANUAL_SEARCH, "found", "https://smile.in")),
                  facts(), NOW).verdict == V.OWN_SITE_VERIFIED
    closed = assess(no_site_checks(Check(9, T.MANUAL_ACTIVITY, "inactive")), facts(), NOW)
    assert (closed.verdict, closed.tier) == (V.SKIP, LeadTier.SKIP)


def test_social_only_reachable_only_by_dm_scores_business_problem():
    checks = no_site_checks(Check(5, T.SOCIAL_LINK, "found", "https://instagram.com/smile"))
    a = assess(checks, facts(phone=None, email=None, social_platforms=["instagram"]), NOW)
    assert a.breakdown["business_problem"] == 10


def test_own_site_without_viewport_scores_redesign_gap():
    checks = [Check(1, T.SOURCE_TAG, "found", "http://x.in"),
              Check(2, T.SITE_FETCH, "ok", "http://x.in", {"has_viewport": False, "has_ssl": False})]
    a = assess(checks, facts(), NOW)
    assert a.breakdown["website_gap"] == 35


def test_google_short_link_and_directory_are_listings_not_websites():
    from backend.app.engines.intelligence.checks import is_listing, source_checks
    assert is_listing("https://g.co/kgs/Yxpf3j") and is_listing("https://www.justdial.com/Udaipur/x")
    assert is_listing("https://smile.business.site") and not is_listing("https://smiledental.in")
    checks = source_checks([], "https://g.co/kgs/Yxpf3j", {}, None)
    tag = [c for c in checks if c.type == T.SOURCE_TAG][0]
    assert tag.outcome == "listing"
    a = assess(no_site_checks(Check(5, T.SOURCE_TAG, "listing", "https://www.practo.com/udaipur/x")), facts(phone=None), NOW)
    assert a.verdict == V.NO_SITE_VERIFIED and a.breakdown["business_problem"] == 8
