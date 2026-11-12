"""
Email engine v2 E1 - rendered phone check (Node call stubbed) and the page excerpt stored with every address.
"""

import json
import subprocess
from datetime import timedelta

import pytest
from sqlalchemy import select

from backend.app.engines.eligibility import render
from backend.app.engines.eligibility.render import (
    RenderJob,
    outcome_for,
    parse_render_output,
    run_render_jobs,
    unsafe_reason,
)
from backend.app.engines.enrichment.discovery import EXCERPT_MAX, ContactDiscoveryEngine
from backend.app.models.eligibility import HoldReason, ObservationType
from backend.app.models.intelligence import CheckType, WebsiteCheck

from .conftest import NOW, add_check, no_viewport_lead, service

# ─── render-check output parsing ─────────────────────────────────────────────

NODE_STDOUT = "\n".join([
    "some warning printed by the browser",
    json.dumps({"key": "1", "url": "https://a.in", "result": "ZOOMED_OUT", "inner_width": 980,
                "final_url": "https://a.in/", "screenshot": "E:/ev/1.png", "checked_at": "2026-11-12T05:00:00.000Z"}),
    json.dumps({"key": "2", "url": "https://b.in", "result": "FITS", "inner_width": 390, "screenshot": "E:/ev/2.png"}),
    json.dumps({"key": "3", "url": "https://c.in", "result": "ERROR", "error": "page.goto: Timeout 12000ms"}),
    json.dumps({"key": "4", "url": "https://d.in", "result": "ZOOMED_OUT", "inner_width": 899}),
    "{not json",
])


def test_parse_render_output():
    results = {r.key: r for r in parse_render_output(NODE_STDOUT)}
    assert set(results) == {"1", "2", "3", "4"}
    assert (results["1"].outcome, results["1"].inner_width, results["1"].screenshot) == ("zoomed_out", 980,
                                                                                        "E:/ev/1.png")
    assert results["1"].checked_at.isoformat() == "2026-11-12T05:00:00+00:00"
    assert results["2"].outcome == "fits"
    assert results["3"].outcome == "error" and "Timeout" in results["3"].error and results["3"].screenshot is None
    # the Python side re-applies the rule: 899 is not >= 900, whatever the script said
    assert results["4"].outcome == "fits"


@pytest.mark.parametrize("width,outcome", [(980, "zoomed_out"), (900, "zoomed_out"), (899, "fits"),
                                           (390, "fits"), (None, "error")])
def test_zoomed_out_rule(width, outcome):
    assert outcome_for(width) == outcome


def test_run_render_jobs_passes_pw_path_and_marks_missing_results_as_errors(monkeypatch, tmp_path):
    seen = {}

    def fake_run(cmd, capture_output, text, encoding, env, timeout):
        seen["cmd"], seen["pw"] = cmd, env["PW_PATH"]
        seen["jobs"] = json.loads(open(cmd[2], encoding="utf-8").read())
        line = json.dumps({"key": "7", "url": "https://a.in", "result": "ZOOMED_OUT", "inner_width": 980,
                           "screenshot": "E:/ev/7.png"})
        return subprocess.CompletedProcess(cmd, 0, stdout=line + "\n", stderr="")

    monkeypatch.setattr(render.subprocess, "run", fake_run)
    jobs = [RenderJob("7", "https://a.in", "E:/ev/7.png"), RenderJob("8", "https://b.in", "E:/ev/8.png")]
    results = {r.key: r for r in run_render_jobs(jobs, pw_path="C:/pw")}
    assert seen["cmd"][1].endswith("render_check.cjs") and seen["pw"] == "C:/pw"
    assert [j["url"] for j in seen["jobs"]] == ["https://a.in", "https://b.in"]
    assert results["7"].outcome == "zoomed_out"
    assert results["8"].outcome == "error"   # a crash never looks like "fits"


async def test_unsafe_urls_are_never_rendered(monkeypatch):
    async def guard(request):
        if request.url.host == "internal.test":
            raise render.UnsafeDestinationError("internal.test resolves to non-public address 10.0.0.5")

    monkeypatch.setattr(render, "ensure_public_destination", guard)
    assert await unsafe_reason("https://glowhair.in/") is None
    assert (await unsafe_reason("https://internal.test/")).startswith("blocked")
    assert await unsafe_reason("file:///c:/windows") is not None
    assert await unsafe_reason("https://instagram.com/glowhair") is not None


async def test_render_results_become_phone_checks_and_the_observation(session):
    lead = await no_viewport_lead(session, render=None)
    svc = service(session)
    assert await svc.render_candidates() == [(lead.id, "https://glowhair.in/")]
    results = parse_render_output(json.dumps({
        "key": str(lead.id), "url": "https://glowhair.in/", "result": "ZOOMED_OUT", "inner_width": 980,
        "final_url": "https://glowhair.in/", "screenshot": "E:/ev/9.png",
        "checked_at": (NOW - timedelta(hours=1)).isoformat()}))
    assert await svc.record_render_results(results) == 1
    stored = (await session.execute(select(WebsiteCheck).where(
        WebsiteCheck.check_type == CheckType.PHONE_RENDER))).scalar_one()
    assert stored.outcome == "zoomed_out" and stored.detail["screenshot"] == "E:/ev/9.png"
    assert await svc.render_candidates() == []          # rendered after the latest homepage check: not again
    await svc.evaluate(now=NOW)
    row = (await svc.business_rows(lead.id))[0]
    assert row["observation"]["type"] == ObservationType.NO_VIEWPORT.value
    assert row["observation"]["evidence_path"] == "E:/ev/9.png"
    assert row["hold_reasons"] == [HoldReason.NOT_VERIFIED.value]


async def test_render_candidates_skip_sites_with_a_viewport(session):
    lead = await no_viewport_lead(session, render=None)
    await add_check(session, lead, "ok", NOW - timedelta(hours=2), has_viewport=True)
    assert await service(session).render_candidates() == []


# ─── provenance excerpt ──────────────────────────────────────────────────────


def extract(html, url="https://glowhair.in/contact"):
    return {c.email: c for c in ContactDiscoveryEngine()._extract_from_html(html, url)}


def test_visible_text_excerpt_is_the_text_around_the_address():
    filler = "Hair cuts, colour and bridal make-up in Surat. " * 20
    found = extract(f"<html><body><p>{filler} Bookings: info@glowhair.in (Mon-Sat). {filler}</p></body></html>")
    excerpt = found["info@glowhair.in"].excerpt
    assert "Bookings: info@glowhair.in (Mon-Sat)" in excerpt
    assert len(excerpt) <= EXCERPT_MAX


def test_mailto_excerpt_names_the_link_target_when_the_page_text_does_not():
    found = extract('<html><body><div><p>Questions? <a href="mailto:hello@glowhair.in">Write to us</a></p>'
                    '</div></body></html>')
    excerpt = found["hello@glowhair.in"].excerpt
    assert "Write to us" in excerpt and "<mailto:hello@glowhair.in>" in excerpt and len(excerpt) <= EXCERPT_MAX


def test_cloudflare_and_obfuscated_addresses_get_an_excerpt():
    key, email = 0x2A, "owner@glowhair.in"
    encoded = f"{key:02x}" + "".join(f"{ord(ch) ^ key:02x}" for ch in email)
    found = extract(f'<html><body><p>Owner: <span data-cfemail="{encoded}">[email protected]</span></p>'
                    f'<p>Bookings: bookings [at] glowhair [dot] in</p></body></html>')
    assert "Owner: owner@glowhair.in" in found[email].excerpt
    assert found[email].source_method == "cloudflare_decode"
    assert "bookings [at] glowhair [dot] in" in found["bookings@glowhair.in"].excerpt
