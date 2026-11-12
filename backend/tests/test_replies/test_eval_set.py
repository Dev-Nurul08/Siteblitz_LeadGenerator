"""
E4 acceptance: the labelled reply set (backend/tests/test_replies/fixtures/reply_eval_set.json) - every label, mixed
languages, adversarial cases. The deterministic safety rules must give 0 missed stop, 0 missed complaint_legal and
(on this set) 0 false stops; every out-of-office / DSN is recognised by its kind. The full-loop checks (OOO never
answered, injection changes nothing) are in test_loop_safety.py.
"""

from collections import Counter
from datetime import date

import pytest

from backend.app.engines.replies import labels as L
from backend.app.engines.replies.parsing import ooo_return_date, parse_message

from .conftest import EVAL_SET, OUR_SUBJECT, case_raw

CASES = EVAL_SET["cases"]
RECEIVED = date(2026, 11, 17)


def evaluate(case: dict) -> tuple[str, list[str], L.SafetyResult, object]:
    parsed = parse_message(case_raw(case))
    if parsed.kind == "AUTO_REPLY":
        return parsed.kind, [L.OUT_OF_OFFICE], L.SafetyResult(), parsed
    if parsed.kind == "DSN":
        return parsed.kind, [L.BOUNCE], L.SafetyResult(), parsed
    result = L.safety_labels(parsed.new_text, parsed.subject, full_text=parsed.text, original_subject=OUR_SUBJECT)
    return parsed.kind, result.labels, result, parsed


@pytest.mark.parametrize("case", CASES, ids=[c["id"] for c in CASES])
def test_each_case(case):
    kind, labels, safety, parsed = evaluate(case)
    assert kind == case["kind"], f"{case['id']}: kind {kind}"
    assert set(labels) == set(case["safety"]), f"{case['id']}: rules gave {labels} ({safety.stop_rules})"
    if "ooo_return" in case:
        expected = date.fromisoformat(case["ooo_return"]) if case["ooo_return"] else None
        assert ooo_return_date(f"{parsed.subject}\n{parsed.new_text}", RECEIVED) == expected
    if case.get("asks_for"):
        assert L.commitment_requests(parsed.new_text) == case["asks_for"]
    elif kind == "HUMAN" and not case["safety"]:
        assert L.commitment_requests(parsed.new_text) == [], case["id"]
    for flag in case.get("flags", []):
        if flag == "DELETION_REQUEST":
            assert safety.deletion_request
        elif flag == "DATA_SOURCE_QUESTION":
            assert safety.data_source_question
        elif flag == "COMPLAINT_LEGAL:credible":
            assert safety.complaint_credible
        elif flag == "COMPLAINT_LEGAL":
            assert L.COMPLAINT_LEGAL in labels and not safety.complaint_credible


def test_set_totals_zero_missed_stop_and_complaint():
    missed_stop = false_stop = missed_complaint = false_complaint = 0
    for case in CASES:
        _, labels, _, _ = evaluate(case)
        want, got = set(case["safety"]), set(labels)
        missed_stop += L.STOP in want and L.STOP not in got
        false_stop += L.STOP in got and L.STOP not in want
        missed_complaint += L.COMPLAINT_LEGAL in want and L.COMPLAINT_LEGAL not in got
        false_complaint += L.COMPLAINT_LEGAL in got and L.COMPLAINT_LEGAL not in want
    assert (missed_stop, missed_complaint) == (0, 0)
    assert (false_stop, false_complaint) == (0, 0)


def test_set_covers_every_label_language_and_adversarial_case():
    assert len(CASES) >= 60
    covered = set()
    for case in CASES:
        covered.update(case["safety"])
        covered.update(case["model"])
    assert set(L.LABELS) <= covered, set(L.LABELS) - covered
    languages = Counter(c["language"] for c in CASES)
    assert {"en", "hi-Latn", "hi", "gu", "gu-Latn"} <= set(languages)
    ids = {c["id"] for c in CASES}
    for needed in ("n02_quoted_stop_line", "n01_dont_stop", "n03_signature_unsubscribe", "o04_hindi_ooo",
                   "d01_dsn_user_unknown", "c01_this_is_spam_report", "m19_prompt_injection_database"):
        assert needed in ids
    assert sum(1 for c in CASES if L.STOP in c["safety"]) >= 20
    assert sum(1 for c in CASES if L.COMPLAINT_LEGAL in c["safety"]) >= 10
