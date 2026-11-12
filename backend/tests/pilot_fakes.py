"""
A stand-in for the Anthropic client in pilot email tests (phase E3). It never touches the network: it reads the LEAD
and TASK the writer sends and answers with a pilot text built from the TASK's fixed lines, the way a compliant model
would. `bad` business names get a banned phrase (twice) so the writer ends in HOLD VALIDATION_FAILED; `delay` slows
each call so the batch screen's "writing" state can be photographed.
"""

import json
import threading
import time
from types import SimpleNamespace

SUBJECT_FACTS = {
    "SOCIAL_ONLY": "no website link in Instagram bio",
    "NO_VIEWPORT": "small homepage text in our check",
    "SITE_DOWN": "{domain} did not load in our checks",
}
VERTICAL_CONTENT = {
    "salon_beauty": "salon services, prices, opening hours and appointment enquiries",
    "coaching_tuition": "courses, timings and enquiry details",
    "retail_showroom": "your showroom, products and enquiry details",
    "other": "your services, location and contact details",
}


def _domain(sentence: str) -> str:
    marker = "the homepage at "
    if marker not in sentence:
        return ""
    return sentence.split(marker, 1)[1].split(" ", 1)[0]


def pilot_answer(lead: dict, task: dict, *, bad: bool = False) -> dict:
    pilot = task["pilot"]
    touch = task["touch"]
    name = lead["business_name"]
    kind = pilot["observation_type"]
    subject = None
    if touch == 1:
        prefix = "If you need a replacement, we" if kind == "SITE_DOWN" else "We"
        pages = "mobile-friendly pages" if kind == "NO_VIEWPORT" else "simple pages"
        content = VERTICAL_CONTENT.get(pilot["vertical"], VERTICAL_CONTENT["other"])
        body = (f"{pilot['observation_sentence']}\n\n{pilot['identity_line']} {prefix} build {pages} showing "
                f"{content}.\n\n{pilot['price_line']}\n\n{pilot['question']}")
        subject = f"{name}: " + SUBJECT_FACTS[kind].format(domain=_domain(pilot["observation_sentence"]))
    elif touch == 2:
        page = pilot["vertical_page"]
        page = page[0].lower() + page[1:]
        body = (f"{pilot['identity_line']} The sample page for {name} would show {page}. It would include "
                f"WhatsApp and call buttons so {pilot['customer_word']} can reach you from their phone. Shall I "
                f"make it and send it here?")
    else:
        body = (f"I'll close this today so I don't keep writing. If a website becomes useful for {name} later, just "
                f"reply here and I'll send the sample page and the prices. Thank you for your time. No further "
                f"follow-ups are planned.")
    if bad:
        body = body.replace("The sample page", "Just checking in: the sample page", 1) if touch == 2 \
            else body + " I came across your page."
    return {
        "decision": "WRITE", "hold_reason": None, "declared_country": "IN", "country_name": "India",
        "declared_language": "en-IN", "language_basis": "country_default", "language_self_check": "en-IN",
        "observation_type": kind, "observation_evidence_value": "Instagram" if kind == "SOCIAL_ONLY" else None,
        "channel": "email", "touch": touch, "reply_class": None, "subject": subject, "body": body,
        "signoff": None, "opt_out_line": None, "suppress": False, "call_requested": False, "pause_until": None,
        "needs_founder": False,
    }


class PilotFakeMessages:
    def __init__(self, bad=(), delay: float = 0.0, fail_with=None):
        self.bad = set(bad)
        self.delay = delay
        self.fail_with = fail_with      # an exception instance raised on every call (writer down)
        self.calls = []
        self.lock = threading.Lock()

    def create(self, **kwargs):
        with self.lock:
            self.calls.append(kwargs)
        if self.delay:
            time.sleep(self.delay)
        if self.fail_with is not None:
            raise self.fail_with
        first = json.loads(kwargs["messages"][0]["content"])
        lead, task = first["LEAD"], first["TASK"]
        answer = pilot_answer(lead, task, bad=lead["business_name"] in self.bad)
        return SimpleNamespace(stop_reason="end_turn", content=[SimpleNamespace(type="text", text=json.dumps(answer))])


def pilot_fake_client(bad=(), delay: float = 0.0, fail_with=None):
    messages = PilotFakeMessages(bad, delay, fail_with)
    return SimpleNamespace(beta=SimpleNamespace(messages=messages)), messages
