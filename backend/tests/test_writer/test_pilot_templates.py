"""
Phase E3: pilot email templates (docs/outreach/pilot-templates.md). One test per pilot validator rule, the assembled
text (signature block, unsubscribe line = the only link), the writer's pilot path and its holds. No network: the
model is a stub, settings never come from a real .env.
"""

import json

import anthropic
import httpx
import pytest

from backend.app.config import Settings
from backend.app.engines.eligibility.rules import no_viewport_text, site_down_text, social_only_text
from backend.app.engines.sending.message import build_message
from backend.app.engines.writer.validator import (
    PILOT_PRICE_LINE,
    UNSUBSCRIBE_PLACEHOLDER,
    assembled_pilot_errors,
    validate,
    word_count,
)
from backend.app.engines.writer.writer import (
    OutreachWriter,
    assemble_pilot_email,
    build_lead,
    pilot_task,
)
from backend.tests.pilot_fakes import pilot_answer, pilot_fake_client

from datetime import datetime, timezone

SETTINGS = Settings(_env_file=None, ANTHROPIC_API_KEY=None, SITEBLITZ_SENDER_NAME="Asha",
                    SITEBLITZ_REPLY_EMAIL="asha@send-one.example", SITEBLITZ_POSTAL_ADDRESS="Test Road, Navsari, Gujarat")
WRITER = OutreachWriter(client=object(), settings=SETTINGS)
DAY = datetime(2026, 11, 12, 6, 0, tzinfo=timezone.utc)

CASES = {
    "salon": ("Kesar Leaf Salon", "salon_beauty", "SOCIAL_ONLY", social_only_text(DAY, "Kesar Leaf Salon")),
    "coaching": ("Nilgiri Classes", "coaching_tuition", "NO_VIEWPORT", no_viewport_text(DAY, "nilgiri.example")),
    "retail": ("Tapti Tiles", "retail_showroom", "SITE_DOWN", site_down_text(DAY, "taptitiles.example")),
    "other": ("Zenith", "other", "SOCIAL_ONLY", social_only_text(DAY, "Zenith")),
}


def make_lead(case="salon", **kw):
    name, vertical, kind, sentence = CASES[case]
    lead = build_lead(lead_id="e-1", business_name=name, category=None, city="Surat", country="IN",
                      observations=[{"type": kind, "evidence_value": "Instagram" if kind == "SOCIAL_ONLY" else None,
                                     "checked_at": "2026-11-12", "check_id": None}])
    lead["vertical"] = vertical
    lead.update(kw)
    return lead, kind, sentence


def make(case="salon", touch=1, **answer_kw):
    lead, kind, sentence = make_lead(case)
    task = pilot_task(touch, lead, kind, sentence, WRITER.facts)
    answer = pilot_answer(lead, task)
    answer.update(answer_kw)
    return answer, lead, task


def check(answer, lead, task):
    return validate(answer, lead, task, WRITER.rows, WRITER.facts.text, WRITER.facts.signature("email"), [])


def errors(case="salon", touch=1, **answer_kw):
    answer, lead, task = make(case, touch, **answer_kw)
    result = check(answer, lead, task)
    assert not result.ok, "expected a rejection"
    return " | ".join(result.errors)


@pytest.mark.parametrize("case", list(CASES))
@pytest.mark.parametrize("touch", [1, 2, 3])
def test_every_template_passes_for_every_pilot_observation_and_vertical(case, touch):
    answer, lead, task = make(case, touch)
    result = check(answer, lead, task)
    assert result.ok, (case, touch, result.errors, word_count(answer["body"]))


def test_touch_1_uses_the_e1_sentence_and_the_fixed_lines_word_for_word():
    answer, lead, task = make("retail")
    assert answer["body"].startswith(site_down_text(DAY, "taptitiles.example"))
    assert task["pilot"]["identity_line"] == "I'm Asha from SiteBlitz, a small web studio in Gujarat."
    assert task["pilot"]["question"] == "Shall I make a sample page for Tapti Tiles and send it here?"
    assert task["pilot"]["price_line"] == PILOT_PRICE_LINE == (
        "Website setup starts at ₹7,999, with domain and hosting charged separately.")
    assert 60 <= word_count(answer["body"]) <= 85


def test_greeting_before_the_observation_is_rejected():
    answer, _, _ = make()
    assert "observation sentence, word for word" in errors(body="Hello Kesar Leaf Salon team,\n\n" + answer["body"])


def test_reworded_observation_is_rejected():
    answer, _, _ = make()
    assert "observation sentence" in errors(body=answer["body"].replace("when we checked", "when I checked"))


def test_identity_line_must_follow_the_observation():
    answer, _, _ = make()
    assert "identity line" in errors(body=answer["body"].replace("a small web studio", "a web studio"))


def test_vertical_sentence_is_required():
    answer, lead, task = make()
    pilot = task["pilot"]
    body = f"{pilot['observation_sentence']}\n\n{pilot['identity_line']}\n\n{pilot['price_line']}\n\n{pilot['question']}"
    assert "what we build for this vertical" in " | ".join(check({**answer, "body": body}, lead, task).errors)


def test_price_line_must_be_exact_and_just_before_the_question():
    answer, _, _ = make()
    assert "price line" in errors(body=answer["body"].replace("charged separately", "extra"))
    moved = answer["body"].replace(PILOT_PRICE_LINE + "\n\n", "").replace("I'm Asha", PILOT_PRICE_LINE + " I'm Asha")
    assert "price line must come just before the question" in errors(body=moved)


def test_exactly_one_question_and_it_is_the_fixed_last_sentence():
    answer, _, _ = make()
    two = answer["body"].replace("appointment enquiries.", "appointment enquiries. Do you take bookings?")
    assert "exactly one question, found 2" in errors(body=two)
    changed = answer["body"].replace("Shall I make a sample page", "Can I make a sample page")
    assert "question, word for word" in errors(body=changed)


def test_no_link_in_touch_1_and_follow_ups():
    answer, _, _ = make()
    linked = answer["body"].replace("appointment enquiries.", "appointment enquiries, see https://siteblitz.example.")
    assert "no link is allowed" in errors(body=linked)
    t2, _, _ = make(touch=2)
    assert "no link is allowed" in errors(touch=2, body=t2["body"].replace("Shall I", "See www.siteblitz.example. Shall I"))
    t3, _, _ = make(touch=3)
    assert "no link is allowed" in errors(touch=3, body=t3["body"] + " https://siteblitz.example")


@pytest.mark.parametrize("touch,low,high", [(1, 60, 85), (2, 40, 70), (3, 30, 50)])
def test_word_limits_per_touch(touch, low, high):
    answer, _, _ = make(touch=touch)
    padded = answer["body"].replace("sample page", "sample page " + "very " * 40, 1)
    assert f"needs {low}-{high}" in errors(touch=touch, body=padded)


def test_short_touch_1_is_rejected():
    _, _, task = make()
    pilot = task["pilot"]
    short = (f"{pilot['observation_sentence']}\n\n{pilot['identity_line']} We build pages.\n\n"
             f"{pilot['price_line']}\n\n{pilot['question']}")
    assert "needs 60-85" in errors(body=short)


def test_subject_is_business_name_plus_a_short_neutral_fact():
    assert "must start with the business name" in errors(subject="A website idea for Kesar Leaf Salon")
    assert "subject fact" in errors(subject="Kesar Leaf Salon: bio")
    assert "question or exclamation" in errors(subject="Kesar Leaf Salon: no website link in your bio?")


def test_model_signoff_or_opt_out_line_is_rejected():
    assert "no sign-off line" in errors(signoff="Regards,")
    assert "no opt-out line" in errors(opt_out_line="If this isn't useful, reply \"stop\".")


def test_pressure_words_are_rejected_in_every_touch():
    answer, _, _ = make()
    assert "pressure wording" in errors(body=answer["body"].replace("Website setup", "This is a limited offer. Website setup"))
    t3, _, _ = make(touch=3)
    assert "pressure wording" in errors(touch=3, body=t3["body"].replace("Thank you", "Last chance. Thank you"))


def test_follow_ups_need_new_information_not_a_nudge():
    t2, _, _ = make(touch=2)
    assert "new information" in errors(touch=2, body="Just following up. " + t2["body"])
    t3, _, _ = make(touch=3)
    assert "new information" in errors(touch=3, body=t3["body"].replace("I'll close", "Circling back, I'll close"))


def test_touch_2_offers_the_sample_with_one_question():
    t2, _, _ = make(touch=2)
    assert "offer the sample page again" in errors(touch=2, body=t2["body"].replace("sample page", "page"))
    assert "exactly one question" in errors(touch=2, body=t2["body"].replace("phone.", "phone? Really?"))


def test_banned_phrase_em_dash_and_facts_guard_still_apply_to_pilot_emails():
    answer, _, _ = make()
    assert "banned phrase" in errors(body=answer["body"].replace("We build", "We build stunning"))
    assert "em dash" in errors(body=answer["body"].replace("We build", "We build —"))
    assert "number 499" in errors(body=answer["body"].replace("We build", "We build 499"))
    assert "domain other.example" in errors(subject="Kesar Leaf Salon: other.example is missing")


def test_language_check_still_applies():
    answer, _, _ = make(touch=3)
    hindi = ("Main aaj yeh band kar raha hoon. Agar website kabhi kaam ki ho to yahan reply kijiye, main sample page "
             "aur prices bhej dunga. Aapke samay ke liye dhanyavaad, aage koi message nahi aayega.")
    assert "language check" in errors(touch=3, body=hindi)


# ─── assembled text: signature block + unsubscribe line ─────────────────────


def test_assembled_text_carries_the_v2_signature_and_the_unsubscribe_line_last():
    answer, _, _ = make()
    text = assemble_pilot_email(answer["body"], WRITER.facts)
    assert text.endswith("Asha | SiteBlitz\nasha@send-one.example | Test Road, Navsari, Gujarat\n"
                         "WhatsApp: +91 92744 90242\n\nReply \"stop\" or unsubscribe here: "
                         + UNSUBSCRIBE_PLACEHOLDER)
    assert assembled_pilot_errors(text, WRITER.facts.pilot_signature_lines()) == []


def test_the_unsubscribe_url_is_allowed_and_required_and_is_the_only_link():
    answer, _, _ = make()
    lines = WRITER.facts.pilot_signature_lines()
    with_url = assemble_pilot_email(answer["body"], WRITER.facts, unsubscribe="https://siteblitz.example/u/abc.def")
    assert assembled_pilot_errors(with_url, lines) == []
    without = with_url.rsplit("\n", 1)[0]
    assert any("last line" in e for e in assembled_pilot_errors(without, lines))
    extra = with_url.replace("WhatsApp:", "See https://siteblitz.example/demo\nWhatsApp:")
    assert any("only link" in e for e in assembled_pilot_errors(extra, lines))
    twice = with_url + "\nReply \"stop\" or unsubscribe here: https://siteblitz.example/u/x"
    assert any("exactly once" in e for e in assembled_pilot_errors(twice, lines))
    unsigned = with_url.replace("WhatsApp: +91 92744 90242\n", "")
    assert any("signature line missing" in e for e in assembled_pilot_errors(unsigned, lines))


def test_e2_message_builder_replaces_the_placeholder_with_the_real_link():
    answer, _, _ = make()
    stored = assemble_pilot_email(answer["body"], WRITER.facts)
    outgoing = build_message(mailbox_address="asha@send-one.example", display_name="Asha", recipient="info@k.example",
                             subject="Kesar Leaf Salon: no website link in Instagram bio", body=stored,
                             message_id="<m1@send-one.example>", send_record_id="1",
                             base_url="https://siteblitz.example", signing_secret="s" * 40, date=DAY)
    sent = outgoing.message.get_content()
    assert UNSUBSCRIBE_PLACEHOLDER not in sent
    assert sent.rstrip().endswith(f'Reply "stop" or unsubscribe here: {outgoing.unsubscribe_url}')
    assert sent.count("unsubscribe here:") == 1 and "WhatsApp: +91 92744 90242" in sent


# ─── the writer's pilot path ─────────────────────────────────────────────────


def test_writer_returns_ready_pilot_text_with_signature_and_placeholder():
    client, messages = pilot_fake_client()
    writer = OutreachWriter(client=client, settings=SETTINGS)
    lead, kind, sentence = make_lead("coaching")
    result = writer.write(lead, pilot_task(1, lead, kind, sentence, writer.facts))
    assert result.status == "READY", result.errors
    assert result.subject == "Nilgiri Classes: small homepage text in our check"
    assert result.text.startswith(sentence) and result.text.endswith(UNSUBSCRIBE_PLACEHOLDER)
    system = messages.calls[0]["system"][0]["text"]
    assert "<PILOT_EMAIL_TEMPLATES>" in system and "Website setup starts at ₹7,999" in system
    sent = json.loads(messages.calls[0]["messages"][0]["content"])
    assert sent["TASK"]["pilot"]["observation_sentence"] == sentence


def test_writer_holds_after_two_failed_pilot_answers():
    client, messages = pilot_fake_client(bad={"Kesar Leaf Salon"})
    writer = OutreachWriter(client=client, settings=SETTINGS)
    lead, kind, sentence = make_lead("salon")
    result = writer.write(lead, pilot_task(1, lead, kind, sentence, writer.facts))
    assert result.status == "HOLD" and result.hold_reason == "VALIDATION_FAILED" and len(messages.calls) == 2


def test_missing_company_fact_holds_before_any_call():
    for blank in ("SITEBLITZ_SENDER_NAME", "SITEBLITZ_REPLY_EMAIL", "SITEBLITZ_POSTAL_ADDRESS"):
        client, messages = pilot_fake_client()
        writer = OutreachWriter(client=client, settings=SETTINGS.model_copy(update={blank: None}))
        lead, kind, sentence = make_lead()
        result = writer.write(lead, pilot_task(1, lead, kind, sentence, writer.facts))
        assert result.hold_reason == "MISSING_COMPANY_FACT" and messages.calls == [], blank


def test_missing_api_key_holds_writer_unavailable_without_text():
    writer = OutreachWriter(settings=SETTINGS)
    lead, kind, sentence = make_lead()
    result = writer.write(lead, pilot_task(1, lead, kind, sentence, writer.facts))
    assert result.status == "HOLD" and result.hold_reason == "WRITER_UNAVAILABLE" and result.text is None


def test_model_down_holds_writer_unavailable_without_text():
    request = httpx.Request("POST", "https://api.anthropic.com/v1/messages")
    client, _ = pilot_fake_client(fail_with=anthropic.APIConnectionError(request=request))
    writer = OutreachWriter(client=client, settings=SETTINGS)
    lead, kind, sentence = make_lead()
    result = writer.write(lead, pilot_task(1, lead, kind, sentence, writer.facts))
    assert result.hold_reason == "WRITER_UNAVAILABLE" and result.text is None
