"""
Opportunity Snapshot creation on the website (spec row 7; docs/spec/email-engine-v2-contracts.md "Snapshot").

    POST {base}/api/outreach/snapshots   Bearer OUTREACH_API_KEY   -> {"slug", "url": "<base>/s/<slug>", "expires_at"}

Called only after a reply labelled sample_requested or interested (contract, "Lead-generator side"); the returned
URL goes into the AI-drafted reply, which waits for the founder's approval. The payload is built only from approved
facts: the business's own lead data (name, city, vertical, the dated observation and its stored evidence image),
the Launch package lines from docs/outreach/company-facts.md, and the sender mailbox. The founder's recorded overview
per vertical comes from `docs/outreach/recordings.json` (E5); a vertical without a complete https URL + transcript
there gets no recording block (the website hides it). A URL in the answer that is not `<OUTREACH_PUBLIC_BASE_URL>/s/<slug>` is refused, so a
wrong or hostile answer can never put a foreign link into a draft.
"""

import base64
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import httpx

from backend.app.engines.sending.suppression_client import valid_base_url

TIMEOUT_SECONDS = 15.0
EVIDENCE_MAX_BYTES = 400 * 1024
EXPIRES_IN_DAYS = 30
CONCEPT_DEMOS = {"salon_beauty": "salon", "coaching_tuition": "coaching", "retail_showroom": "showroom"}
VERTICALS = ("salon_beauty", "coaching_tuition", "retail_showroom", "other")
OBSERVATIONS = ("SOCIAL_ONLY", "NO_VIEWPORT", "SITE_DOWN")
_SLUG = re.compile(r"^[a-z0-9][a-z0-9-]{0,79}$")
RECORDINGS_FILE = Path(__file__).resolve().parents[4] / "docs" / "outreach" / "recordings.json"
TRANSCRIPT_MAX = 2000   # contract: transcript max 2,000 characters, required when a URL is set


class SnapshotUnavailable(RuntimeError):
    """No snapshot could be created (website down, wrong answer, missing facts)."""


@dataclass
class SnapshotResult:
    slug: str
    url: str
    expires_at: datetime


def _cells(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def offer_from_facts(facts_md: str) -> dict:
    """The Launch row (price, delivery, inclusions) and the first two 'Not included' items of company-facts.md."""
    launch = next((line for line in facts_md.splitlines() if line.startswith("| Launch |")), None)
    if launch is None:
        raise SnapshotUnavailable("company facts have no Launch package row")
    cells = _cells(launch)   # Package | Price | Pages | Paid as | Delivery | Includes
    digits = re.sub(r"\D", "", cells[1])
    if not digits:
        raise SnapshotUnavailable("company facts: Launch price is not a number")
    lines = [part.strip() for part in cells[5].split(";") if part.strip()]
    lines = [line[0].upper() + line[1:] for line in lines][:5]
    lines.append(f"Delivery: {cells[4]}")
    excluded = None
    marker = "## Not included in any package"
    if marker in facts_md:
        after = facts_md.split(marker, 1)[1].strip().splitlines()
        excluded = after[0] if after else None
    if not excluded:
        raise SnapshotUnavailable("company facts have no 'Not included' list")
    items = [i.strip() for i in excluded.split("·") if i.strip()][:2]
    note = f"Not included and charged separately: {items[0]}" + (f"; {items[1]}" if len(items) > 1 else "") + "."
    return {"price_inr": int(digits), "scope_lines": [line[:120] for line in lines[:6]],
            "yearly_costs_note": note[:200]}


def evidence_base64(path: Optional[str]) -> Optional[str]:
    """The stored evidence image (e.g. the 390 px phone screenshot) when it is a PNG / JPEG of at most 400 KB."""
    if not path:
        return None
    file = Path(path)
    try:
        if not file.is_file() or file.stat().st_size > EVIDENCE_MAX_BYTES:
            return None
        data = file.read_bytes()
    except OSError:
        return None
    if not (data.startswith(b"\x89PNG\r\n\x1a\n") or data.startswith(b"\xff\xd8\xff")):
        return None
    return base64.b64encode(data).decode("ascii")


def load_recording(vertical: Optional[str], path: Optional[Path] = None) -> Optional[dict]:
    """The founder's recorded overview for a vertical ({"url", "transcript"}), or None.

    Only a complete entry is used: an https URL and a non-empty transcript of at most 2,000 characters (contract,
    Snapshot "recording"). Anything else - missing file, broken JSON, http URL, no transcript - means no recording,
    never a half block."""
    import json

    file = path or RECORDINGS_FILE
    try:
        data = json.loads(file.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    entry = data.get(vertical if vertical in VERTICALS else "other") if isinstance(data, dict) else None
    if not isinstance(entry, dict):
        return None
    url, transcript = str(entry.get("url") or "").strip(), str(entry.get("transcript") or "").strip()
    if not url.startswith("https://") or not transcript or len(transcript) > TRANSCRIPT_MAX:
        return None
    return {"url": url, "transcript": transcript}


def build_payload(*, business_name: str, city: Optional[str], vertical: Optional[str], observation_type: str,
                  observation_text: str, checked_at: datetime, evidence_path: Optional[str], reply_email: str,
                  facts_md: str, recording: Optional[dict] = None) -> dict:
    if observation_type not in OBSERVATIONS:
        raise SnapshotUnavailable(f"observation {observation_type!r} is not one of the pilot observations")
    if not (observation_text or "").strip():
        raise SnapshotUnavailable("the lead has no observation text")
    vertical = vertical if vertical in VERTICALS else "other"
    payload = {
        "business_name": business_name.strip()[:120],
        "city": (city or "").strip()[:80],
        "vertical": vertical,
        "observation": {"type": observation_type, "text": observation_text.strip()[:300],
                        "checked_at": checked_at.isoformat()},
        "offer": offer_from_facts(facts_md),
        "reply_email": reply_email,
        "expires_in_days": EXPIRES_IN_DAYS,
    }
    demo = CONCEPT_DEMOS.get(vertical)
    if demo:   # "other" has no demo page (company-facts.md); the key is left out (open question in e4-notes.md)
        payload["concept_demo"] = demo
    image = evidence_base64(evidence_path)
    if image:
        payload["evidence_image_base64"] = image
    if recording:
        payload["recording"] = recording
    return payload


class SnapshotClient:
    def __init__(self, base_url: Optional[str], api_key: Optional[str],
                 transport: Optional[httpx.AsyncBaseTransport] = None, timeout: float = TIMEOUT_SECONDS):
        self.base_url = valid_base_url(base_url)
        self.api_key = (api_key or "").strip() or None
        self.transport = transport
        self.timeout = timeout

    async def create(self, payload: dict) -> SnapshotResult:
        if not (self.base_url and self.api_key):
            raise SnapshotUnavailable("OUTREACH_PUBLIC_BASE_URL or OUTREACH_API_KEY is not set")
        headers = {"Authorization": f"Bearer {self.api_key}", "Accept": "application/json"}
        try:
            async with httpx.AsyncClient(timeout=self.timeout, transport=self.transport,
                                         follow_redirects=False) as client:
                response = await client.post(f"{self.base_url}/api/outreach/snapshots", json=payload,
                                             headers=headers)
        except httpx.HTTPError as exc:
            raise SnapshotUnavailable(f"{type(exc).__name__}") from exc
        if response.status_code != 200:
            raise SnapshotUnavailable(f"HTTP {response.status_code} from /api/outreach/snapshots")
        try:
            data = response.json()
        except ValueError as exc:
            raise SnapshotUnavailable("invalid JSON from /api/outreach/snapshots") from exc
        slug = data.get("slug") if isinstance(data, dict) else None
        url = data.get("url") if isinstance(data, dict) else None
        if not isinstance(slug, str) or not _SLUG.match(slug) or url != f"{self.base_url}/s/{slug}":
            raise SnapshotUnavailable("the snapshot answer has no slug / URL on the configured website")
        try:
            expires = datetime.fromisoformat(str(data.get("expires_at")).replace("Z", "+00:00"))
        except ValueError as exc:
            raise SnapshotUnavailable("the snapshot answer has no valid expires_at") from exc
        expires = expires.astimezone(timezone.utc) if expires.tzinfo else expires.replace(tzinfo=timezone.utc)
        return SnapshotResult(slug, url, expires)
