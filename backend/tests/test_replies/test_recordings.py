"""E5: the founder's recorded overview reaches the snapshot payload only when complete (contract "recording")."""
import json
from datetime import datetime, timezone
from pathlib import Path

from backend.app.engines.replies.snapshot_client import RECORDINGS_FILE, build_payload, load_recording

FACTS = Path(__file__).resolve().parents[3] / "docs" / "outreach" / "company-facts.md"


def _write(tmp_path, data) -> Path:
    file = tmp_path / "recordings.json"
    file.write_text(json.dumps(data), encoding="utf-8")
    return file


def test_complete_entry_is_used(tmp_path):
    f = _write(tmp_path, {"coaching_tuition": {"url": "https://example.com/r/coaching.mp3", "transcript": "Hello."}})
    assert load_recording("coaching_tuition", f) == {"url": "https://example.com/r/coaching.mp3", "transcript": "Hello."}


def test_incomplete_or_unsafe_entries_give_no_recording(tmp_path):
    cases = [{"coaching_tuition": {"url": "http://example.com/a.mp3", "transcript": "x"}},
             {"coaching_tuition": {"url": "https://example.com/a.mp3", "transcript": ""}},
             {"coaching_tuition": {"url": "", "transcript": "x"}},
             {"coaching_tuition": {"url": "https://example.com/a.mp3", "transcript": "x" * 2001}},
             {"other": {"url": "https://example.com/a.mp3", "transcript": "x"}}]
    for data in cases:
        assert load_recording("coaching_tuition", _write(tmp_path, data)) is None
    bad = tmp_path / "broken.json"
    bad.write_text("{not json", encoding="utf-8")
    assert load_recording("coaching_tuition", bad) is None
    assert load_recording("coaching_tuition", tmp_path / "missing.json") is None


def test_unknown_vertical_uses_other(tmp_path):
    f = _write(tmp_path, {"other": {"url": "https://example.com/o.mp3", "transcript": "General overview."}})
    assert load_recording("bakery", f)["url"] == "https://example.com/o.mp3"


def test_shipped_file_has_no_recording_yet():
    for vertical in ("salon_beauty", "coaching_tuition", "retail_showroom", "other"):
        assert load_recording(vertical, RECORDINGS_FILE) is None


def test_payload_carries_recording_only_when_given():
    kwargs = dict(business_name="Fixture Coaching", city="Surat", vertical="coaching_tuition",
                  observation_type="NO_VIEWPORT", observation_text="On 12 November 2026, the homepage ...",
                  checked_at=datetime(2026, 11, 12, tzinfo=timezone.utc), evidence_path=None,
                  reply_email="asha@send-one.example", facts_md=FACTS.read_text(encoding="utf-8"))
    assert "recording" not in build_payload(**kwargs)
    rec = {"url": "https://example.com/r.mp3", "transcript": "Hello."}
    assert build_payload(**kwargs, recording=rec)["recording"] == rec
