"""
Email engine v2 E1 - every eligibility rule and HOLD code (docs/spec/email-engine-v2.md rows 2-4).
Pure functions only: no database, no network.
"""

from datetime import datetime, timedelta, timezone

import pytest

from backend.app.engines.eligibility import rules
from backend.app.engines.eligibility.rules import (
    BusinessFacts,
    Capture,
    Confirmation,
    VerificationRecord,
    decide,
    dedupe,
    find_observation,
)
from backend.app.engines.intelligence.rules import Check
from backend.app.models.eligibility import (
    CaptureMethod,
    EligibilityTier,
    HoldReason,
    ObservationType,
    RecipientType,
    VerificationStatus,
)
from backend.app.models.intelligence import CheckType

NOW = datetime(2026, 11, 12, 6, 0, tzinfo=timezone.utc)
SITE = "https://glowhair.in"
H = HoldReason


def facts(**kw) -> BusinessFacts:
    base = dict(id=1, name="Glow Hair Studio", country="IN", website_url=SITE)
    base.update(kw)
    return BusinessFacts(**base)


def page_capture(email="info@glowhair.in", **kw) -> Capture:
    base = dict(id=1, email=email, method=CaptureMethod.MAILTO, source_url=f"{SITE}/contact",
                excerpt=f"Mail {email}", captured_at=NOW - timedelta(days=1), origin="test")
    base.update(kw)
    return Capture(**base)


def fetch(outcome, hours_ago, **detail) -> Check:
    return Check(None, CheckType.SITE_FETCH, outcome, SITE, detail, NOW - timedelta(hours=hours_ago))


def render(outcome, hours_ago=2, **detail) -> Check:
    detail = {"final_url": SITE + "/", "screenshot": "E:/evidence/1.png", **detail}
    return Check(None, CheckType.PHONE_RENDER, outcome, SITE, detail, NOW - timedelta(hours=hours_ago))


VALID = [VerificationRecord("syntax_mx", VerificationStatus.UNVERIFIED, NOW - timedelta(days=1), {"mx_ok": True}),
         VerificationRecord("bouncer", VerificationStatus.VALID, NOW - timedelta(days=1))]
NO_VIEWPORT_CHECKS = [fetch("ok", 30, has_viewport=False), render("zoomed_out")]


def run(f=None, email="info@glowhair.in", captures=None, checks=None, confirmation=None, verifications=None,
        suppressed=False):
    f = f or facts()
    checks = NO_VIEWPORT_CHECKS if checks is None else checks
    observation = find_observation(f, checks, confirmation, NOW)
    return decide(f, email, captures if captures is not None else [page_capture(email)], checks, observation,
                  VALID if verifications is None else verifications, suppressed, NOW)


# ─── the happy path ──────────────────────────────────────────────────────────


def test_tier1_own_site_valid_and_observed_is_eligible():
    d = run()
    assert d.holds == [] and d.eligible and d.eligible_if_verified
    assert d.tier == EligibilityTier.TIER1
    assert d.observation.type == ObservationType.NO_VIEWPORT
    assert d.observation.text == ("On 12 November 2026, the homepage at glowhair.in opened zoomed-out on a phone "
                                  "screen in our check, so the text showed very small.")
    assert d.observation.evidence_path == "E:/evidence/1.png"


def test_free_mail_on_own_site_is_treated_like_own_domain():
    d = run(email="glowhairstudio@gmail.com")
    assert d.eligible and d.tier == EligibilityTier.TIER1


# ─── country (spec row 2) ────────────────────────────────────────────────────


@pytest.mark.parametrize("country", ["US", "GB", None, ""])
def test_only_india_is_in_the_pilot(country):
    assert H.COUNTRY_NOT_IN_PILOT in run(facts(country=country)).holds


# ─── provenance (spec row 3) ─────────────────────────────────────────────────


def test_listing_only_address_is_tier2_hold():
    d = run(captures=[page_capture(method=CaptureMethod.LISTING, source_url=None, excerpt=None)])
    assert d.tier == EligibilityTier.TIER2 and H.LISTING_ONLY in d.holds and not d.eligible


def test_own_site_beats_listing_for_the_same_address():
    d = run(captures=[page_capture(method=CaptureMethod.LISTING, source_url=None, excerpt=None), page_capture()])
    assert d.tier == EligibilityTier.TIER1 and H.LISTING_ONLY not in d.holds


@pytest.mark.parametrize("missing", ["excerpt", "captured_at", "source_url"])
def test_own_site_address_without_url_date_or_excerpt_is_incomplete(missing):
    d = run(captures=[page_capture(**{missing: None})])
    assert d.tier == EligibilityTier.HOLD and H.PROVENANCE_INCOMPLETE in d.holds


def test_address_read_on_another_host_is_not_own_site():
    d = run(captures=[page_capture(source_url="https://directory-site.in/glow")])
    assert d.tier == EligibilityTier.HOLD and H.SOURCE_NOT_OWN_SITE in d.holds


def test_redirect_target_host_counts_as_own_site():
    checks = [fetch("ok", 30, has_viewport=False, final_url="https://glowhairstudio.com/"), render("zoomed_out")]
    d = run(captures=[page_capture(source_url="https://glowhairstudio.com/contact")], checks=checks)
    assert d.tier == EligibilityTier.TIER1


def test_founder_confirmed_address_is_tier1():
    confirmation = Confirmation(1, "https://instagram.com/glowhair", NOW - timedelta(days=1), False, "glow@gmail.com")
    capture = Capture(2, "glow@gmail.com", CaptureMethod.FOUNDER_CONFIRMED, confirmation.profile_url,
                      "Founder check ...", confirmation.checked_at, "confirmation:1")
    d = run(facts(website_url=None, social_urls={"instagram": confirmation.profile_url}), email="glow@gmail.com",
            captures=[capture], checks=[], confirmation=confirmation)
    assert d.tier == EligibilityTier.TIER1 and d.eligible
    assert d.observation.type == ObservationType.SOCIAL_ONLY
    assert d.observation.text == ("On 11 November 2026, the Instagram profile for Glow Hair Studio showed no "
                                  "website link when we checked its bio.")


# ─── recipient (RESULT row 10) ───────────────────────────────────────────────


@pytest.mark.parametrize("email,expected", [
    ("info@glowhair.in", RecipientType.BUSINESS),
    ("bookings.surat@glowhair.in", RecipientType.BUSINESS),
    ("glowhair@gmail.com", RecipientType.BUSINESS),           # names the business
    ("priya.shah@glowhair.in", RecipientType.EMPLOYEE_LIKE),  # first.last at the company domain
    ("r.patel@glowhair.in", RecipientType.EMPLOYEE_LIKE),
    ("priya.shah@gmail.com", RecipientType.UNKNOWN),           # free-mail: cannot tell
    ("ps1990@gmail.com", RecipientType.UNKNOWN),
])
def test_recipient_type(email, expected):
    assert rules.recipient_type(email, "Glow Hair Studio", {"glowhair.in"}) == expected


def test_employee_like_address_is_held_unknown_is_not():
    assert H.EMPLOYEE_LIKE_ADDRESS in run(email="priya.shah@glowhair.in").holds
    assert run(email="ps1990@gmail.com").eligible


@pytest.mark.parametrize("email", ["noreply@glowhair.in", "no-reply@glowhair.in", "postmaster@glowhair.in",
                                   "privacy@glowhair.in", "grievance@glowhair.in"])
def test_system_mailboxes_are_held(email):
    assert H.SYSTEM_ADDRESS in run(email=email).holds


# ─── chains and duplicates (spec row 3) ──────────────────────────────────────


def test_overture_brand_or_shared_host_is_chain():
    assert H.CHAIN_OR_DIRECTORY in run(facts(brand="Lakme Salon")).holds
    assert H.CHAIN_OR_DIRECTORY in run(facts(site_share_count=3)).holds
    assert H.CHAIN_OR_DIRECTORY not in run(facts(site_share_count=2)).holds


def test_site_key_separates_sites_on_shared_platforms():
    assert rules.site_key("https://www.GlowHair.in/branch/surat") == "glowhair.in"
    assert rules.site_key("https://sites.google.com/view/glow-hair/home") == "sites.google.com/view/glow-hair"
    assert rules.site_key("https://sites.google.com/view/other") != rules.site_key(
        "https://sites.google.com/view/glow-hair")


def test_rule9_skip_is_not_a_prospect():
    assert H.NOT_A_PROSPECT in run(facts(skip_reason="Not a website prospect (category=college)")).holds


def test_one_recipient_per_business():
    f = facts()
    observation = find_observation(f, NO_VIEWPORT_CHECKS, None, NOW)
    first = decide(f, "info@glowhair.in", [page_capture("info@glowhair.in")], NO_VIEWPORT_CHECKS, observation,
                   VALID, False, NOW)
    second = decide(f, "priya.shah@glowhair.in", [page_capture("priya.shah@glowhair.in")], NO_VIEWPORT_CHECKS,
                    observation, VALID, False, NOW)
    dedupe([second, first])
    assert first.eligible
    assert H.NOT_PRIMARY_RECIPIENT in second.holds


def test_same_address_on_two_businesses_goes_to_one_and_on_three_is_a_chain():
    def for_business(business_id):
        f = facts(id=business_id)
        observation = find_observation(f, NO_VIEWPORT_CHECKS, None, NOW)
        return decide(f, "info@glowhair.in", [page_capture()], NO_VIEWPORT_CHECKS, observation, VALID, False, NOW)

    a, b = for_business(1), for_business(2)
    dedupe([a, b])
    assert a.eligible and H.DUPLICATE_RECIPIENT in b.holds

    group = [for_business(i) for i in (1, 2, 3)]
    dedupe(group)
    assert all(H.CHAIN_OR_DIRECTORY in d.holds for d in group)


# ─── suppression ─────────────────────────────────────────────────────────────


def test_suppressed_address_or_business_is_held():
    assert H.SUPPRESSED in run(suppressed=True).holds
    assert H.SUPPRESSED in run(facts(suppressed=True)).holds


# ─── verification (spec row 3: only VALID) ───────────────────────────────────


@pytest.mark.parametrize("status,code", [
    (VerificationStatus.RISKY, H.VERIFIER_RISKY),
    (VerificationStatus.CATCH_ALL, H.VERIFIER_CATCH_ALL),
    (VerificationStatus.UNKNOWN, H.VERIFIER_UNKNOWN),
    (VerificationStatus.INVALID, H.VERIFIER_INVALID),
])
def test_only_valid_passes_the_verifier(status, code):
    d = run(verifications=[VerificationRecord("bouncer", status, NOW - timedelta(days=1))])
    assert d.holds == [code] and not d.eligible_if_verified


def test_unverified_is_held_but_eligible_once_verified():
    d = run(verifications=[])
    assert d.holds == [H.NOT_VERIFIED]
    assert not d.eligible and d.eligible_if_verified
    assert d.verification_status == VerificationStatus.UNVERIFIED


def test_verifier_result_expires_after_30_days():
    old = [VerificationRecord("bouncer", VerificationStatus.VALID, NOW - timedelta(days=31))]
    assert run(verifications=old).holds == [H.NOT_VERIFIED]


def test_failed_mx_check_beats_an_older_valid_result():
    records = VALID[1:] + [VerificationRecord("syntax_mx", VerificationStatus.INVALID, NOW, {"mx_ok": False})]
    assert H.VERIFIER_INVALID in run(verifications=records).holds


# ─── observations (spec row 4) ───────────────────────────────────────────────


def test_no_viewport_needs_the_rendered_phone_check():
    assert run(checks=[fetch("ok", 30, has_viewport=False)]).holds == [H.PHONE_CHECK_PENDING]
    assert run(checks=[fetch("ok", 30, has_viewport=False), render("error")]).holds == [H.PHONE_CHECK_PENDING]
    # source said "no viewport" but the phone check found the page fits: no observation
    assert run(checks=[fetch("ok", 30, has_viewport=False), render("fits")]).holds == [H.NO_PILOT_OBSERVATION]


def test_working_mobile_site_has_no_pilot_observation():
    assert run(checks=[fetch("ok", 30, has_viewport=True)]).holds == [H.NO_PILOT_OBSERVATION]
    assert run(checks=[]).holds == [H.NO_PILOT_OBSERVATION]


def test_observation_older_than_30_days_does_not_count():
    old = [fetch("ok", 24 * 40, has_viewport=False), render("zoomed_out", hours_ago=24 * 31)]
    assert run(checks=old).holds == [H.OBSERVATION_STALE]


def test_site_down_needs_two_failures_six_hours_apart():
    assert run(checks=[fetch("failed", 1)]).holds == [H.SITE_DOWN_NEEDS_RECHECK]
    assert run(checks=[fetch("failed", 5), fetch("failed", 1)]).holds == [H.SITE_DOWN_NEEDS_RECHECK]
    d = run(checks=[fetch("failed", 8), fetch("failed", 1)])
    assert d.eligible and d.observation.type == ObservationType.SITE_DOWN
    assert d.observation.text == ("On 12 November 2026, the homepage at glowhair.in did not load in our checks, "
                                  "the last one shortly before this email. The interruption may be temporary.")


def test_block_or_challenge_page_is_never_down():
    # visit_site records a challenge / 403 page as "protected": it breaks a run of failures
    assert run(checks=[fetch("failed", 20), fetch("protected", 10), fetch("failed", 1)]).holds == [
        H.SITE_DOWN_NEEDS_RECHECK]
    assert run(checks=[fetch("failed", 20), fetch("failed", 10), fetch("protected", 1)]).holds == [
        H.SITE_RECOVERED]


def test_site_down_address_on_the_down_domain_must_pass_mx():
    checks = [fetch("failed", 8), fetch("failed", 1)]
    no_mx = [VerificationRecord("bouncer", VerificationStatus.VALID, NOW - timedelta(days=1))]
    assert run(checks=checks, verifications=no_mx).holds == [H.MAILBOX_DOMAIN_DOWN]
    assert run(checks=checks).eligible                                    # MX passed
    other_domain = run(email="glowhair@gmail.com", checks=checks, verifications=no_mx)
    assert H.MAILBOX_DOMAIN_DOWN not in other_domain.holds              # free-mail is not on the down domain


def test_social_only_needs_the_founder_check():
    f = facts(website_url=None, social_urls={"instagram": "https://instagram.com/glowhair"})
    assert run(f, checks=[], captures=[page_capture(method=CaptureMethod.LISTING, source_url=None)]).holds == [
        H.LISTING_ONLY, H.NEEDS_FOUNDER_CHECK]
    with_link = Confirmation(1, "https://instagram.com/glowhair", NOW - timedelta(days=1), True)
    assert H.NO_PILOT_OBSERVATION in run(f, checks=[], confirmation=with_link).holds
    stale = Confirmation(1, "https://instagram.com/glowhair", NOW - timedelta(days=31), False)
    assert H.OBSERVATION_STALE in run(f, checks=[], confirmation=stale).holds


def test_every_hold_has_a_reason_and_every_code_is_documented():
    doc = rules.__doc__ + (HoldReason.__doc__ or "")
    for code in HoldReason:
        assert code.value in doc, code
    assert not run(facts(country="US")).eligible and run(facts(country="US")).holds


def test_email_hash_matches_the_contract():
    # docs/spec/email-engine-v2-contracts.md: sha256_hex(email.strip().lower())
    import hashlib
    assert rules.email_hash("  Info@GlowHair.in ") == hashlib.sha256(b"info@glowhair.in").hexdigest()


def test_dates_are_written_in_india_time():
    late_utc = datetime(2026, 11, 11, 20, 0, tzinfo=timezone.utc)   # 01:30 IST on 12 November
    assert rules.date_text(late_utc) == "12 November 2026"
