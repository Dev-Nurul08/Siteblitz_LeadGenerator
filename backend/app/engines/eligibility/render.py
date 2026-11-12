"""
Email engine v2, phase E1 - the rendered phone check behind a NO_VIEWPORT observation (spec row 4).

A missing viewport tag in the page source is a signal, not proof (RESULT row 12). The observation is used only
when a real browser, emulating a phone, opened the homepage zoomed-out:
  `scripts/render_check.cjs` (Node + Playwright 1.62 from PW_PATH) - Chromium, isMobile, 390 x 844,
  deviceScaleFactor 3, 12 s navigation timeout; ZOOMED_OUT when `window.innerWidth >= 900` after load (the
  browser fell back to a desktop-width layout viewport); one viewport screenshot per page, stored outside the repo
  under E:\\SiteBlitz-World-Business-Data\\_work\\evidence\\<date>\\.
SSRF: the browser is only given URLs this module checked with the same guard as every server-side fetch
(`ensure_public_destination`: the host must resolve to public addresses only). The Node script also aborts any
request to localhost / a private IP literal.
"""

import json
import os
import subprocess
import tempfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

import httpx

from backend.app.engines.discovery.overture import social_platform
from backend.app.engines.intelligence.checks import is_listing
from backend.app.engines.opportunity.resolver import UnsafeDestinationError, ensure_public_destination

REPO_ROOT = Path(__file__).resolve().parents[4]
RENDER_SCRIPT = REPO_ROOT / "scripts" / "render_check.cjs"
DEFAULT_PW_PATH = str(Path(os.environ.get("LOCALAPPDATA", "")) / "npm-cache" / "_npx" / "e41f203b7505f1fb"
                      / "node_modules" / "playwright")
EVIDENCE_ROOT = Path("E:/SiteBlitz-World-Business-Data/_work/evidence")
ZOOMED_OUT_MIN_INNER_WIDTH = 900   # E1 brief: innerWidth >= 900 after load = desktop layout on a phone
SECONDS_PER_PAGE = 40              # subprocess time budget per page (12 s navigation + screenshot + start-up)


@dataclass
class RenderJob:
    key: str          # who the result belongs to (the business id as text)
    url: str
    screenshot: str   # where the screenshot goes


@dataclass
class RenderResult:
    key: str
    url: str
    outcome: str                      # zoomed_out | fits | error
    inner_width: Optional[int] = None
    final_url: Optional[str] = None
    screenshot: Optional[str] = None
    error: Optional[str] = None
    load_timeout: bool = False
    checked_at: Optional[datetime] = None

    def detail(self) -> dict:
        return {"inner_width": self.inner_width, "final_url": self.final_url, "screenshot": self.screenshot,
                "error": self.error, "load_timeout": self.load_timeout, "viewport": "390x844@3",
                "rule": f"innerWidth >= {ZOOMED_OUT_MIN_INNER_WIDTH} = zoomed_out"}


async def unsafe_reason(url: str) -> Optional[str]:
    """None when the browser may open `url`; otherwise why not."""
    parsed = urlparse(url or "")
    if parsed.scheme not in ("http", "https") or not parsed.hostname:
        return "not an http(s) address"
    if social_platform(url) or is_listing(url):
        return "social profile or listing, not the business's own site"
    try:
        await ensure_public_destination(httpx.Request("GET", url))
    except UnsafeDestinationError as exc:
        return f"blocked: {str(exc)[:150]}"
    return None


def outcome_for(inner_width: Optional[int]) -> str:
    if inner_width is None:
        return "error"
    return "zoomed_out" if inner_width >= ZOOMED_OUT_MIN_INNER_WIDTH else "fits"


def _parse_time(text: Optional[str]) -> Optional[datetime]:
    if not text:
        return None
    try:
        moment = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        return None
    return moment if moment.tzinfo else moment.replace(tzinfo=timezone.utc)


def parse_render_output(stdout: str) -> list[RenderResult]:
    """One JSON object per line from render_check.cjs. Lines that are not result objects are ignored.
    The outcome is re-derived from inner_width here, so the rule lives in one place on the Python side too."""
    results = []
    for line in (stdout or "").splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            row = json.loads(line)
        except ValueError:
            continue
        if not isinstance(row, dict) or "key" not in row:
            continue
        width = row.get("inner_width")
        width = int(width) if isinstance(width, (int, float)) else None
        failed = str(row.get("result", "")).upper() == "ERROR" or width is None
        results.append(RenderResult(
            key=str(row["key"]), url=str(row.get("url") or ""),
            outcome="error" if failed else outcome_for(width), inner_width=width,
            final_url=row.get("final_url"), screenshot=None if failed else row.get("screenshot"),
            error=(str(row.get("error"))[:300] if row.get("error") else None),
            load_timeout=bool(row.get("load_timeout")), checked_at=_parse_time(row.get("checked_at"))))
    return results


def evidence_dir(day: Optional[datetime] = None) -> Path:
    return EVIDENCE_ROOT / (day or datetime.now()).strftime("%Y-%m-%d")


def run_render_jobs(jobs: list[RenderJob], node: str = "node", script: Path = RENDER_SCRIPT,
                    pw_path: Optional[str] = None) -> list[RenderResult]:
    """Run the Node script once for all jobs (validated by `unsafe_reason` first) and parse its output."""
    if not jobs:
        return []
    with tempfile.TemporaryDirectory() as tmp:
        job_file = Path(tmp) / "jobs.json"
        job_file.write_text(json.dumps([job.__dict__ for job in jobs]), encoding="utf-8")
        env = {**os.environ, "PW_PATH": pw_path or os.environ.get("PW_PATH") or DEFAULT_PW_PATH}
        proc = subprocess.run([node, str(script), str(job_file)], capture_output=True, text=True,
                              encoding="utf-8", env=env, timeout=SECONDS_PER_PAGE * len(jobs) + 60)
    results = parse_render_output(proc.stdout)
    done = {r.key for r in results}
    for job in jobs:   # a crash of the script must not look like "fits"
        if job.key not in done:
            results.append(RenderResult(job.key, job.url, "error",
                                        error=(proc.stderr or "no result line")[-300:]))
    return results
