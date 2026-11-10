"""Phase 13 acceptance: one test per validator rejection (docs/spec/outreach-engine.md, criterion 2)."""

import pytest

from backend.app.config import Settings
from backend.app.engines.writer.validator import is_roman_hindi, numbers_in, validate
from backend.app.engines.writer.writer import OutreachWriter

SETTINGS = Settings(SITEBLITZ_SENDER_NAME="Asha", SITEBLITZ_REPLY_EMAIL="hello@siteblitz.example",
                    SITEBLITZ_POSTAL_ADDRESS="Test Road, Navsari, Gujarat")
WRITER = OutreachWriter(client=object(), settings=SETTINGS)

T1_BODY = (
    "Hello Glow Studio team,\n\n"
    "I found Glow Studio on Instagram, but I couldn't find a website for it anywhere. A simple page of your own "
    "would show clients your services and prices without scrolling through posts.\n\n"
    "I'm Asha from SiteBlitz, a small web studio in Gujarat. We build websites for local businesses, starting at "
    "₹7,999 (domain and hosting are separate).\n\n"
    "Would you like me to send a short outline for Glow Studio?"
)


def lead(**kw):
    base = {
        "lead_id": "t-1", "business_name": "Glow Studio", "vertical": "salon_beauty", "category": "beauty_salon",
        "city": "Surat", "area": "Adajan", "region": "Gujarat", "country": "IN",
        "contact_name": None, "contact_name_source": None,
        "language_evidence": {"site_language": None, "source": None},
        "observations": [{"type": "SOCIAL_ONLY", "evidence_value": "Instagram", "checked_at": "2026-11-10",
                          "check_id": 7}],
        "optin": None, "suppressed": False, "thread": [],
    }
    base.update(kw)
    return base


def task(**kw):
    base = {"channel": "email", "touch": 1, "inbound_message": None, "attachments_allowed": []}
    base.update(kw)
    return base


def answer(**kw):
    base = {
        "decision": "WRITE", "hold_reason": None, "declared_country": "IN", "country_name": "India",
        "declared_language": "en-IN", "language_basis": "country_default", "language_self_check": "en-IN",
        "observation_type": "SOCIAL_ONLY", "observation_evidence_value": "Instagram", "channel": "email",
        "touch": 1, "reply_class": None, "subject": "A website idea for Glow Studio", "body": T1_BODY,
        "signoff": "Regards,", "opt_out_line": "If this isn't useful, reply \"stop\" and I won't write again.",
        "suppress": False, "call_requested": False, "pause_until": None, "needs_founder": False,
    }
    base.update(kw)
    return base


def check(out, the_lead=None, the_task=None, missing=None):
    the_task = the_task or task()
    return validate(out, the_lead or lead(), the_task, WRITER.rows, WRITER.facts.text,
                    WRITER.facts.signature(the_task["channel"]), missing or [])


def errors_of(out, **kw):
    result = check(out, **kw)
    assert not result.ok
    return " | ".join(result.errors)


def test_reference_touch_1_passes():
    result = check(answer())
    assert result.ok, result.errors


def test_country_mismatch_rejected():
    assert "declared_country" in errors_of(answer(declared_country="US"))


def test_language_not_allowed_for_country_rejected():
    assert "not allowed for IN" in errors_of(answer(declared_language="fr-FR", language_self_check="fr-FR"))


def test_language_detector_disagrees_rejected():
    french = ("Bonjour l'équipe Glow Studio,\n\nJ'ai trouvé Glow Studio sur Instagram, mais je n'ai trouvé aucun site "
              "web. Une page simple montrerait vos services et vos prix à vos clientes sans parcourir les "
              "publications. Je suis Asha de SiteBlitz, un petit studio web au Gujarat. Nos sites commencent à "
              "₹7,999, domaine et hébergement en plus. Voulez-vous que je vous envoie un court plan pour Glow Studio?")
    assert "language check" in errors_of(answer(body=french))


def test_self_check_must_match_declared_language():
    assert "language_self_check" in errors_of(answer(language_self_check="en-US"))


def test_too_short_and_too_long_rejected():
    assert "words" in errors_of(answer(body="Hello Glow Studio team,\n\nInstagram only. Want a website?"))
    long_body = T1_BODY.replace("Would you like", "We also write the page text with you and set up the "
                                "WhatsApp button so clients can ask about a slot. Would you like")
    assert "words" in errors_of(answer(body=long_body))


def test_zero_or_two_questions_rejected():
    assert "exactly one question" in errors_of(answer(body=T1_BODY.replace("Glow Studio?", "Glow Studio.")))
    two = T1_BODY.replace("anywhere.", "anywhere. Is that right?")
    assert "exactly one question" in errors_of(answer(body=two))


def test_link_in_first_touch_rejected():
    body = T1_BODY.replace("(domain and hosting are separate)", "(see https://siteblitz.vercel.app)")
    assert "no link" in errors_of(answer(body=body))


def test_banned_phrase_rejected():
    body = T1_BODY.replace("I found Glow Studio", "I came across Glow Studio")
    assert "banned phrase" in errors_of(answer(body=body))


@pytest.mark.parametrize("char,name", [("—", "em dash"), ("!", "exclamation"), (";", "semicolon")])
def test_banned_characters_rejected(char, name):
    body = T1_BODY.replace("anywhere.", f"anywhere{char} really.")
    assert name in errors_of(answer(body=body))


@pytest.mark.parametrize("token", ["[Business Name]", "{{SENDER}}", "TO FILL"])
def test_unresolved_placeholder_rejected(token):
    body = T1_BODY.replace("I'm Asha", f"I'm {token}")
    assert "unresolved placeholder" in errors_of(answer(body=body))


def test_missing_opt_out_rejected():
    assert "opt-out" in errors_of(answer(opt_out_line=None))


def test_missing_signoff_rejected():
    assert "sign-off" in errors_of(answer(signoff=None))


def test_missing_signature_facts_means_hold():
    msg = errors_of(answer(), missing=["postal_address"])
    assert "MISSING_COMPANY_FACT" in msg


def test_hold_country_must_not_produce_text():
    msg = errors_of(answer(declared_country="DE", declared_language="de-DE"), the_lead=lead(country="DE"))
    assert "COUNTRY_ON_HOLD" in msg


def test_hold_answer_for_hold_country_passes():
    out = answer(decision="HOLD", hold_reason="COUNTRY_ON_HOLD", body="")
    assert check(out, the_lead=lead(country="DE")).ok


def test_unexpected_hold_rejected():
    assert "nothing requires a hold" in errors_of(answer(decision="HOLD", hold_reason="NO_OBSERVATION", body=""))


def test_invented_number_rejected():
    body = T1_BODY.replace("anywhere.", "anywhere, and 68 people searched for it.")
    assert "number 68" in errors_of(answer(body=body))


def test_invented_domain_rejected():
    body = T1_BODY.replace("anywhere.", "anywhere, only glowstudio-surat.in.")
    assert "domain glowstudio-surat.in" in errors_of(answer(body=body))


def test_lower_priority_observation_rejected():
    the_lead = lead(observations=[
        {"type": "NO_SITE", "evidence_value": None, "checked_at": "2026-11-10", "check_id": 1},
        {"type": "SITE_DOWN", "evidence_value": "glow.example", "checked_at": "2026-11-10", "check_id": 2},
    ])
    msg = errors_of(answer(observation_type="NO_SITE"), the_lead=the_lead)
    assert "highest-priority one is SITE_DOWN" in msg
    assert "evidence 'glow.example'" in msg


def test_ai_mention_rejected():
    body = T1_BODY.replace("We build websites", "Our AI builds websites")
    assert "must not mention AI" in errors_of(answer(body=body))


def test_roman_hindi_only_after_owner_wrote_roman_hindi():
    body = ("Namaste, message karne ke liye thank you. Main Asha, SiteBlitz se.\n"
            "1 page ki website ₹7,999 aur 3 pages ki ₹17,999 hai. Domain aur hosting alag se.\n"
            "Yeh nayi website ke liye hai, ya abhi wali website badalni hai?")
    optin = {"source": "qr_whatsapp", "at": "2026-11-10", "message": "Hello SiteBlitz, I received your website idea."}
    out = answer(channel="whatsapp_reply", touch=None, subject=None, signoff=None, opt_out_line=None,
                 declared_language="hi-Latn", language_self_check="hi-Latn", language_basis="owner_message",
                 observation_type=None, observation_evidence_value=None, body=body, reply_class="PRICE_QUESTION")
    english_owner = task(channel="whatsapp_reply", touch=None, inbound_message="How much does a website cost?")
    assert "Roman Hindi" in errors_of(out, the_lead=lead(optin=optin), the_task=english_owner)
    hindi_owner = task(channel="whatsapp_reply", touch=None,
                       inbound_message="Bhai website ka kitna lagega? 1 page wali chahiye")
    result = check(out, the_lead=lead(optin=optin), the_task=hindi_owner)
    assert result.ok, result.errors


def test_stop_reply_must_suppress():
    out = answer(touch=None, subject=None, reply_class="STOP", body="Understood, thank you for letting me know.",
                 opt_out_line=None, suppress=False)
    msg = errors_of(out, the_task=task(touch=None, inbound_message="Please stop emailing me"))
    assert "suppress" in msg


def test_helpers():
    assert numbers_in("₹7,999 and ₹17,999.") == {"7999", "17999"}
    assert is_roman_hindi("Kya aap website banate hai?")
    assert not is_roman_hindi("Please send the price")
