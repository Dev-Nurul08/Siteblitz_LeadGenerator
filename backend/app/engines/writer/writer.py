"""
AI outreach writer (phase 13, docs/spec/outreach-engine.md rows 1-8 and 18).

Builds one request per lead from the files in docs/outreach/, calls Claude, checks the answer with validator.py and
asks for one rewrite when a check fails. A lead that still fails is held for the founder. Nothing here sends a
message: the caller (phase 15 batch screen) decides what happens to a READY result.

Privacy: the model receives an allow-listed copy of the lead with no email address and no phone number, and the
reply / postal address are added to the signature by the app, never by the model.
"""

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Optional
from urllib.parse import urlparse

import anthropic

from backend.app.config import Settings, get_settings
from backend.app.engines.intelligence.rules import AGGREGATOR_HOSTS, FRESH_DAYS, Check
from backend.app.engines.writer.validator import (
    CHANNEL_FACTS,
    HOLD_REASONS,
    LANGUAGE_BASES,
    OBSERVATION_PRIORITY,
    REPLY_CLASSES,
    LanguageRow,
    ValidationResult,
    expected_hold,
    load_country_languages,
    validate,
)
from backend.app.models.intelligence import CheckType, EvidenceConfidence, WebsiteVerdict

DOCS_DIR = Path(__file__).resolve().parents[4] / "docs" / "outreach"
MODEL = "claude-sonnet-5-5"  # spec row 1, approved by the founder 2026-11-10
# Server-side fallback: a declined request is re-run on Anthropic's recommended model for that refusal category.
FALLBACK_BETA = "server-side-fallback-2026-07-01"
MAX_TOKENS = 16000

FACT_ROWS = {
    "sender_name": "Sender name used in signatures",
    "reply_email": "Reply email address",
    "postal_address": "Postal address for email and letter footers",
}

# Only these lead fields ever reach the model (spec row 2).
MODEL_LEAD_KEYS = (
    "business_name", "vertical", "category", "city", "area", "region", "country", "contact_name",
    "contact_name_source", "language_evidence", "observations", "optin", "suppressed", "thread",
)
EMAIL_ADDRESS = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")
# Indian-style 10-digit numbers with optional +91 and one space, and any other run of 8+ digits.
PHONE = re.compile(r"(?:\+\d{1,3}[\s-]?)?\d{5}[\s-]?\d{5}|\d{8,}")

PLATFORM_NAMES = {
    "instagram": "Instagram", "facebook": "Facebook", "linkedin": "LinkedIn", "tiktok": "TikTok",
    "youtube": "YouTube", "x": "X", "whatsapp": "WhatsApp", "linktree": "Linktree",
}
AGGREGATOR_NAMES = {"zomato.com": "Zomato", "swiggy.com": "Swiggy", "justdial.com": "Justdial", "practo.com": "Practo"}

VERTICALS = (
    ("salon_beauty", ("salon", "beauty", "spa", "nail", "barber", "hair")),
    ("coaching_tuition", ("tutor", "coach", "education", "school", "training", "college", "classes")),
    ("retail_showroom", ("store", "shop", "retail", "showroom", "boutique")),
)

NULLABLE_STRING = {"anyOf": [{"type": "string"}, {"type": "null"}]}
OUTPUT_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "decision": {"type": "string", "enum": ["WRITE", "HOLD"]},
        "hold_reason": {"anyOf": [{"type": "string", "enum": list(HOLD_REASONS)}, {"type": "null"}]},
        "declared_country": {"type": "string"},
        "country_name": {"type": "string"},
        "declared_language": {"type": "string"},
        "language_basis": {"type": "string", "enum": list(LANGUAGE_BASES)},
        "language_self_check": {"type": "string"},
        "observation_type": {"anyOf": [{"type": "string", "enum": list(OBSERVATION_PRIORITY)}, {"type": "null"}]},
        "observation_evidence_value": NULLABLE_STRING,
        "channel": {"type": "string", "enum": ["email", "whatsapp_reply", "social_dm", "letter"]},
        "touch": {"anyOf": [{"type": "integer"}, {"type": "null"}]},
        "reply_class": {"anyOf": [{"type": "string", "enum": list(REPLY_CLASSES)}, {"type": "null"}]},
        "subject": NULLABLE_STRING,
        "body": {"type": "string"},
        "signoff": NULLABLE_STRING,
        "opt_out_line": NULLABLE_STRING,
        "suppress": {"type": "boolean"},
        "call_requested": {"type": "boolean"},
        "pause_until": NULLABLE_STRING,
        "needs_founder": {"type": "boolean"},
    },
    "required": [
        "decision", "hold_reason", "declared_country", "country_name", "declared_language", "language_basis",
        "language_self_check", "observation_type", "observation_evidence_value", "channel", "touch",
        "reply_class", "subject", "body", "signoff", "opt_out_line", "suppress", "call_requested",
        "pause_until", "needs_founder",
    ],
    "additionalProperties": False,
}


class PrivacyError(ValueError):
    """Raised when an email address or phone number would reach the model."""


@dataclass
class CompanyFacts:
    text: str                     # COMPANY_FACTS as the model sees it
    sender_name: Optional[str]
    reply_email: Optional[str]
    postal_address: Optional[str]

    def missing_for(self, channel: str) -> list[str]:
        return [key for key in CHANNEL_FACTS.get(channel, ()) if not getattr(self, key)]

    def signature(self, channel: str) -> str:
        if channel == "email":
            return f"{self.sender_name}\nSiteBlitz | {self.reply_email}\n{self.postal_address}"
        if channel == "letter":
            return f"{self.sender_name}, SiteBlitz\n{self.postal_address}"
        return ""


def load_company_facts(settings: Settings, docs_dir: Path = DOCS_DIR) -> CompanyFacts:
    """company-facts.md from "## Identity" on, with the .env values put into the three blank rows. The reply and
    postal addresses are not shown to the model (the app adds them), only whether they are set."""
    raw = (docs_dir / "company-facts.md").read_text(encoding="utf-8")
    raw = raw[raw.index("## Identity"):]
    values = {
        "sender_name": (settings.SITEBLITZ_SENDER_NAME or "").strip() or None,
        "reply_email": (settings.SITEBLITZ_REPLY_EMAIL or "").strip() or None,
        "postal_address": (settings.SITEBLITZ_POSTAL_ADDRESS or "").strip() or None,
    }
    lines = []
    for line in raw.splitlines():
        for key, label in FACT_ROWS.items():
            if line.startswith(f"| {label} |") and values[key]:
                shown = values[key] if key == "sender_name" else "set (the app adds it to the signature)"
                line = f"| {label} | {shown} |"
        lines.append(line)
    return CompanyFacts("\n".join(lines), **values)


def load_system_text(facts: CompanyFacts, docs_dir: Path = DOCS_DIR) -> str:
    prompt_doc = (docs_dir / "ai-writer-system-prompt.md").read_text(encoding="utf-8")
    prompt = prompt_doc.split("```text\n", 1)[1].split("\n```", 1)[0]
    countries = (docs_dir / "country-language.csv").read_text(encoding="utf-8")
    references = (docs_dir / "reference-messages.md").read_text(encoding="utf-8")
    return (
        f"{prompt}\n\n<COMPANY_FACTS>\n{facts.text}\n</COMPANY_FACTS>\n\n"
        f"<COUNTRY_LANGUAGE>\n{countries}</COUNTRY_LANGUAGE>\n\n"
        f"<REFERENCE_MESSAGES>\n{references}</REFERENCE_MESSAGES>"
    )


def vertical_for(category: Optional[str]) -> str:
    text = (category or "").lower()
    for vertical, fragments in VERTICALS:
        if any(fragment in text for fragment in fragments):
            return vertical
    return "other"


def _host(url: Optional[str]) -> Optional[str]:
    if not url:
        return None
    host = urlparse(url if "//" in url else f"//{url}").hostname or ""
    return host[4:] if host.startswith("www.") else host or None


def _aware(moment: datetime) -> datetime:
    return moment if moment.tzinfo else moment.replace(tzinfo=timezone.utc)


def build_observations(
    verdict: WebsiteVerdict,
    confidence: EvidenceConfidence,
    checks: list[Check],
    social_platforms: list[str],
    now: Optional[datetime] = None,
) -> list[dict]:
    """Observations from stored checks no older than 30 days (spec row 4), highest priority first.
    BROKEN_FORM needs a form-test check type, which does not exist yet, so it is never produced here."""
    now = now or datetime.now(timezone.utc)
    if confidence == EvidenceConfidence.LOW:
        return []
    fresh = [c for c in checks if _aware(c.observed_at) >= now - timedelta(days=FRESH_DAYS)]

    def obs(kind: str, evidence: Optional[str], check: Optional[Check]) -> dict:
        return {
            "type": kind,
            "evidence_value": evidence,
            "checked_at": _aware(check.observed_at).date().isoformat() if check else None,
            "check_id": check.id if check else None,
        }

    found: list[dict] = []
    fetches = [c for c in fresh if c.type == CheckType.SITE_FETCH]
    if verdict == WebsiteVerdict.SITE_DOWN_CONFIRMED:
        failed = [c for c in fetches if c.outcome == "failed"]
        if len(failed) >= 2:
            found.append(obs("SITE_DOWN", _host(failed[-1].target), failed[-1]))
    if verdict == WebsiteVerdict.OWN_SITE_VERIFIED:
        ok = [c for c in fetches if c.outcome == "ok"]
        if ok:
            latest = max(ok, key=lambda c: _aware(c.observed_at))
            domain = _host(latest.target)
            if latest.detail.get("has_viewport") is False:
                found.append(obs("NO_VIEWPORT", domain, latest))
            if latest.detail.get("has_ssl") is False:
                found.append(obs("NO_HTTPS", domain, latest))
    if verdict in (WebsiteVerdict.SOCIAL_ONLY_VERIFIED, WebsiteVerdict.NO_SITE_VERIFIED):
        guesses = [c for c in fresh if c.type == CheckType.DOMAIN_GUESS and c.outcome == "none"]
        if guesses:
            newest = max(guesses, key=lambda c: _aware(c.observed_at))
            if verdict == WebsiteVerdict.SOCIAL_ONLY_VERIFIED and social_platforms:
                platform = PLATFORM_NAMES.get(social_platforms[0].lower(), social_platforms[0])
                found.append(obs("SOCIAL_ONLY", platform, newest))
            if verdict == WebsiteVerdict.NO_SITE_VERIFIED:
                found.append(obs("NO_SITE", None, newest))
            for check in fresh:
                host = _host(check.target) or ""
                if check.type == CheckType.SOURCE_TAG and any(host.endswith(h) for h in AGGREGATOR_HOSTS):
                    name = next(v for k, v in AGGREGATOR_NAMES.items() if host.endswith(k))
                    found.append(obs("AGGREGATOR_ONLY", name, check))
                    break
    return sorted(found, key=lambda o: OBSERVATION_PRIORITY.index(o["type"]))


def build_lead(
    *,
    lead_id: str,
    business_name: str,
    category: Optional[str],
    city: Optional[str],
    country: Optional[str],
    observations: list[dict],
    area: Optional[str] = None,
    region: Optional[str] = None,
    site_language: Optional[str] = None,
    optin: Optional[dict] = None,
    suppressed: bool = False,
    thread: Optional[list[dict]] = None,
) -> dict:
    return {
        "lead_id": lead_id,
        "business_name": business_name,
        "vertical": vertical_for(category),
        "category": category,
        "city": city,
        "area": area,
        "region": region,
        "country": (country or "").strip().upper(),
        "contact_name": None,
        "contact_name_source": None,
        "language_evidence": {"site_language": site_language,
                              "source": "html lang attribute + text detection" if site_language else None},
        "observations": observations,
        "optin": optin,
        "suppressed": suppressed,
        "thread": thread or [],
    }


def _redact(value: Any) -> Any:
    if isinstance(value, str):
        return PHONE.sub("(phone removed)", EMAIL_ADDRESS.sub("(email removed)", value))
    if isinstance(value, list):
        return [_redact(v) for v in value]
    if isinstance(value, dict):
        return {k: _redact(v) for k, v in value.items()}
    return value


def model_payload(lead: dict) -> dict:
    """The allow-listed, redacted lead sent to the model. Raises PrivacyError if anything still looks like an
    email address or a phone number."""
    payload = _redact({key: lead.get(key) for key in MODEL_LEAD_KEYS})
    dumped = json.dumps(payload, ensure_ascii=False)
    if EMAIL_ADDRESS.search(dumped) or PHONE.search(dumped):
        raise PrivacyError("an email address or phone number would be sent to the model")
    return payload


def model_task(task: dict) -> dict:
    """The TASK as sent to the model: the owner's reply (inbound_message) can carry their number or address,
    so it gets the same redaction and check as the lead (spec row 2). The validator still sees the original."""
    payload = _redact(dict(task))
    dumped = json.dumps(payload, ensure_ascii=False)
    if EMAIL_ADDRESS.search(dumped) or PHONE.search(dumped):
        raise PrivacyError("an email address or phone number would be sent to the model")
    return payload


def assemble_message(output: dict, facts: CompanyFacts, channel: str) -> str:
    """The text the recipient sees: the model's body + sign-off, the app's signature, the model's opt-out line."""
    body = (output.get("body") or "").strip()
    signoff = (output.get("signoff") or "").strip()
    opt_out = (output.get("opt_out_line") or "").strip()
    if channel == "email":
        sign = "\n".join(x for x in (signoff, facts.signature("email")) if x)
        return f"{body}\n\n{sign}" + (f"\n{opt_out}" if opt_out else "")
    if channel == "letter":
        return "\n\n".join(p for p in (body, opt_out, facts.signature("letter")) if p)
    if channel == "social_dm":
        return "\n".join(p for p in (body, opt_out) if p)
    return body


@dataclass
class WriterResult:
    status: str                    # READY | HOLD | ERROR
    lead_id: Optional[str]
    hold_reason: Optional[str] = None
    output: Optional[dict] = None
    text: Optional[str] = None
    subject: Optional[str] = None
    errors: list[str] = field(default_factory=list)
    attempts: int = 0


class OutreachWriter:
    def __init__(
        self,
        client: Optional[Any] = None,
        settings: Optional[Settings] = None,
        docs_dir: Path = DOCS_DIR,
    ):
        self.settings = settings or get_settings()
        self.facts = load_company_facts(self.settings, docs_dir)
        self.rows: dict[str, LanguageRow] = load_country_languages(docs_dir / "country-language.csv")
        self.system_text = load_system_text(self.facts, docs_dir)
        self._client = client

    def client(self) -> Any:
        if self._client is None:
            self._client = anthropic.Anthropic(api_key=self.settings.ANTHROPIC_API_KEY)
        return self._client

    def request(self, messages: list[dict]) -> dict:
        return {
            "model": MODEL,
            "max_tokens": MAX_TOKENS,
            "betas": [FALLBACK_BETA],
            "fallbacks": "default",
            "system": [{"type": "text", "text": self.system_text, "cache_control": {"type": "ephemeral"}}],
            "messages": messages,
            "output_config": {"format": {"type": "json_schema", "schema": OUTPUT_SCHEMA}},
        }

    def check(self, output: dict, lead: dict, task: dict) -> ValidationResult:
        return validate(output, lead, task, self.rows, self.facts.text,
                        self.facts.signature(task.get("channel", "")), self.facts.missing_for(task.get("channel", "")))

    def write(self, lead: dict, task: dict) -> WriterResult:
        lead_id = lead.get("lead_id")
        channel = task.get("channel", "")
        hold = expected_hold(lead, task, self.rows, self.facts.missing_for(channel))
        if hold:
            # Decided by the rules alone; the model is not called and no data leaves the machine.
            return WriterResult("HOLD", lead_id, hold_reason=hold)
        if not self.settings.ANTHROPIC_API_KEY and self._client is None:
            return WriterResult("ERROR", lead_id, errors=["ANTHROPIC_API_KEY is not set in .env"])
        try:
            user = json.dumps({"LEAD": model_payload(lead), "TASK": model_task(task)}, ensure_ascii=False)
        except PrivacyError as exc:
            return WriterResult("ERROR", lead_id, errors=[str(exc)])

        messages: list[dict] = [{"role": "user", "content": user}]
        errors: list[str] = []
        for attempt in (1, 2):
            try:
                response = self.client().beta.messages.create(**self.request(messages))
            except (anthropic.AuthenticationError, anthropic.PermissionDeniedError):
                return WriterResult("ERROR", lead_id, errors=["API key missing or not allowed"], attempts=attempt)
            except anthropic.RateLimitError:
                return WriterResult("ERROR", lead_id, errors=["rate limited; try the batch again later"],
                                    attempts=attempt)
            except anthropic.APIStatusError as exc:
                return WriterResult("ERROR", lead_id, errors=[f"API error {exc.status_code}"], attempts=attempt)
            except anthropic.APIConnectionError:
                return WriterResult("ERROR", lead_id, errors=["network error"], attempts=attempt)

            if response.stop_reason == "refusal":
                return WriterResult("HOLD", lead_id, hold_reason="MODEL_REFUSED", attempts=attempt)
            text = next((b.text for b in response.content if b.type == "text"), "")
            try:
                output = json.loads(text)
            except json.JSONDecodeError:
                output = {}
                result = ValidationResult(False, ["the answer was not valid JSON"])
            else:
                result = self.check(output, lead, task)
            if result.ok:
                if output["decision"] == "HOLD":
                    return WriterResult("HOLD", lead_id, hold_reason=output.get("hold_reason"), output=output,
                                        attempts=attempt)
                return WriterResult("READY", lead_id, output=output, attempts=attempt,
                                    text=assemble_message(output, self.facts, channel),
                                    subject=output.get("subject"))
            errors = result.errors
            # Append-only retry: the earlier answer stays in the conversation, unchanged.
            messages += [
                {"role": "assistant", "content": response.content},
                {"role": "user", "content": "Your answer failed these checks:\n- " + "\n- ".join(errors)
                 + "\nWrite it again so every check passes. Answer with the JSON object only."},
            ]
        return WriterResult("HOLD", lead_id, hold_reason="VALIDATION_FAILED", errors=errors, attempts=2)


def _main(argv: list[str]) -> int:
    """Run the writer over a fixtures file: python -m backend.app.engines.writer.writer <fixtures.json>
    Needs ANTHROPIC_API_KEY and the three SITEBLITZ_* values in .env. Prints one line per lead."""
    parser = argparse.ArgumentParser(description=_main.__doc__)
    parser.add_argument("fixtures", type=Path)
    args = parser.parse_args(argv)
    cases = json.loads(args.fixtures.read_text(encoding="utf-8"))["cases"]
    writer = OutreachWriter()
    for case in cases:
        result = writer.write(case["lead"], case["task"])
        detail = result.hold_reason or "; ".join(result.errors) or (result.subject or "")
        print(f"{result.status:6} {case['lead']['lead_id']:10} attempts={result.attempts} {detail}")
    return 0


if __name__ == "__main__":
    sys.exit(_main(sys.argv[1:]))
