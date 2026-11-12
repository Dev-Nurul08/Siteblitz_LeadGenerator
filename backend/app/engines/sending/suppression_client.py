"""
Client for the website's suppression API (docs/spec/email-engine-v2-contracts.md, "Website endpoints").

    POST {base}/api/outreach/suppressions/check   {"hashes": [...]} (max 500) -> {"suppressed": [...], "checked_at"}
    POST {base}/api/outreach/suppressions         {"hash", "reason", "source"} -> {"ok": true}
    GET  {base}/api/outreach/suppressions?since=  -> {"items": [{"hash", "reason", "created_at"}], "next"}

Every call sends `Authorization: Bearer <OUTREACH_API_KEY>`. ANY answer other than a well-formed 200 - a 401, a
503, a timeout, a refused connection, invalid JSON, `ok: false`, a missing key or base URL - raises
SuppressionUnavailable. The worker then sends nothing and raises the global pause SUPPRESSION_UNAVAILABLE.
The website is the only authority: the local mirror (SuppressionMirror) is for display and never authorises a send.
"""

import re
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from urllib.parse import urlparse

import httpx

CHECK_MAX_HASHES = 500
TIMEOUT_SECONDS = 10.0
REASONS = ("reply_stop", "hard_bounce", "complaint", "manual")
SOURCE_MAX = 200
_HEX64 = re.compile(r"^[0-9a-f]{64}$")


class SuppressionUnavailable(RuntimeError):
    """The suppression service could not give a trustworthy answer. Never treat this as 'not suppressed'."""


@dataclass
class SuppressionPage:
    items: list[dict]
    next: Optional[str]


def valid_base_url(value: Optional[str]) -> Optional[str]:
    text = (value or "").strip().rstrip("/")
    parsed = urlparse(text)
    if parsed.scheme not in ("http", "https") or not parsed.hostname:
        return None
    return text


class SuppressionClient:
    def __init__(self, base_url: Optional[str], api_key: Optional[str],
                 transport: Optional[httpx.AsyncBaseTransport] = None, timeout: float = TIMEOUT_SECONDS):
        self.base_url = valid_base_url(base_url)
        self.api_key = (api_key or "").strip() or None
        self.transport = transport
        self.timeout = timeout

    @property
    def configured(self) -> bool:
        return bool(self.base_url and self.api_key)

    async def _request(self, method: str, path: str, **kwargs) -> dict:
        if not self.configured:
            raise SuppressionUnavailable("OUTREACH_PUBLIC_BASE_URL or OUTREACH_API_KEY is not set")
        headers = {"Authorization": f"Bearer {self.api_key}", "Accept": "application/json"}
        try:
            async with httpx.AsyncClient(timeout=self.timeout, transport=self.transport,
                                         follow_redirects=False) as client:
                response = await client.request(method, f"{self.base_url}{path}", headers=headers, **kwargs)
        except httpx.HTTPError as exc:
            raise SuppressionUnavailable(f"{type(exc).__name__}: {exc}"[:300]) from exc
        if response.status_code != 200:
            raise SuppressionUnavailable(f"HTTP {response.status_code} from {path}")
        try:
            data = response.json()
        except ValueError as exc:
            raise SuppressionUnavailable(f"invalid JSON from {path}") from exc
        if not isinstance(data, dict) or data.get("ok") is False:
            raise SuppressionUnavailable(f"unexpected answer from {path}")
        return data

    async def check(self, hashes: list[str]) -> set[str]:
        """The subset of `hashes` the website lists as suppressed. Raises SuppressionUnavailable otherwise."""
        wanted = sorted({h.lower() for h in hashes})
        if not wanted:
            return set()
        if len(wanted) > CHECK_MAX_HASHES or not all(_HEX64.match(h) for h in wanted):
            raise ValueError("check takes 1-500 sha256 hex hashes")
        data = await self._request("POST", "/api/outreach/suppressions/check", json={"hashes": wanted})
        suppressed = data.get("suppressed")
        if not isinstance(suppressed, list) or not all(isinstance(h, str) for h in suppressed):
            raise SuppressionUnavailable("check answer has no 'suppressed' list")
        found = {h.lower() for h in suppressed}
        if not found <= set(wanted):
            raise SuppressionUnavailable("check answer lists hashes that were not asked about")
        return found

    async def add(self, email_hash: str, reason: str, source: str) -> None:
        if not _HEX64.match(email_hash) or reason not in REASONS:
            raise ValueError("add takes a sha256 hex hash and one of " + ", ".join(REASONS))
        data = await self._request("POST", "/api/outreach/suppressions",
                                   json={"hash": email_hash, "reason": reason, "source": source[:SOURCE_MAX]})
        if data.get("ok") is not True:
            raise SuppressionUnavailable("add was not confirmed with ok: true")

    async def list_since(self, since: Optional[datetime]) -> SuppressionPage:
        params = {"since": since.isoformat()} if since else {}
        data = await self._request("GET", "/api/outreach/suppressions", params=params)
        items = data.get("items")
        if not isinstance(items, list):
            raise SuppressionUnavailable("list answer has no 'items' list")
        clean = [i for i in items if isinstance(i, dict) and isinstance(i.get("hash"), str)
                 and _HEX64.match(i["hash"].lower())]
        return SuppressionPage(clean, data.get("next") if isinstance(data.get("next"), str) else None)
