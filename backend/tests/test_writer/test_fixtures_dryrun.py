"""Phase 13 acceptance criterion 1: 30 fixture leads (10 per vertical, Surat / Navsari) each end READY with a
validator-passing message or HOLD with a reason code.

No API key was available on 2026-11-10, so the answers in dryrun_outputs.json were produced by Claude Code's own model
(Claude Opus 5.5) reading the exact system prompt and user messages the writer builds. They are replayed here
through the real write() flow, including the one-rewrite rule. Re-record with the live API (`python -m
backend.app.engines.writer.writer backend/tests/test_writer/fixtures_30.json`) once ANTHROPIC_API_KEY is set.
"""

import json
from pathlib import Path
from types import SimpleNamespace

from backend.app.engines.writer.writer import OutreachWriter
from backend.tests.test_writer.test_validator import SETTINGS

HERE = Path(__file__).parent
CASES = json.loads((HERE / "fixtures_30.json").read_text(encoding="utf-8"))["cases"]
RECORDED = json.loads((HERE / "dryrun_outputs.json").read_text(encoding="utf-8"))["attempts"]


class Replay:
    """Fake client that returns the recorded attempts for one case, in order."""

    def __init__(self, attempts):
        self.attempts = list(attempts)
        self.messages = self

    @property
    def beta(self):
        return self

    def create(self, **_kwargs):
        answer = self.attempts.pop(0)
        return SimpleNamespace(stop_reason="end_turn",
                               content=[SimpleNamespace(type="text", text=json.dumps(answer))])


def run_all():
    results = {}
    for case in CASES:
        case_id = case["lead"]["lead_id"]
        writer = OutreachWriter(client=Replay(RECORDED.get(case_id, [])), settings=SETTINGS)
        results[case_id] = writer.write(case["lead"], case["task"])
    return results


def test_thirty_cases_ten_per_vertical():
    verticals = [c["lead"]["vertical"] for c in CASES]
    assert len(CASES) == 30
    assert {v: verticals.count(v) for v in set(verticals)} == {
        "salon_beauty": 10, "coaching_tuition": 10, "retail_showroom": 10}
    assert {c["lead"]["city"] for c in CASES} == {"Surat", "Navsari"}


def test_every_case_is_ready_or_held_with_a_reason():
    results = run_all()
    for case_id, result in results.items():
        assert result.status in ("READY", "HOLD"), (case_id, result.errors)
        if result.status == "HOLD":
            assert result.hold_reason, case_id
    held = {k: r.hold_reason for k, r in results.items() if r.status == "HOLD"}
    assert held == {"s09": "NO_OBSERVATION", "c10": "SUPPRESSED", "r10": "NO_OBSERVATION"}, held


def test_ready_messages_carry_signature_and_opt_out():
    for case_id, result in run_all().items():
        if result.status != "READY":
            continue
        channel = next(c["task"]["channel"] for c in CASES if c["lead"]["lead_id"] == case_id)
        if channel == "email":
            assert "SiteBlitz | hello@siteblitz.example" in result.text, case_id
        if channel in ("email", "social_dm", "letter"):
            assert result.output["opt_out_line"] and result.text.rstrip().endswith(
                (result.output["opt_out_line"].strip(), "Test Road, Navsari, Gujarat")), case_id
