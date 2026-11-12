"""
Email engine v2, phase E1 - eligibility service (spec: docs/spec/email-engine-v2.md rows 2-4).

evaluate()               load the facts, apply engines/eligibility/rules.py, store one EmailEligibility row per
                         (business, address); with verify=True first run the verifier ladder for the candidates
recheck_before_send()    E2 calls this right before an SMTP submission to a SITE_DOWN lead: a fresh homepage check
                         and a fresh MX check, then re-evaluation
record_confirmation()    the founder's Instagram-bio check (SOCIAL_ONLY) -> Tier 1 provenance when an email was seen
pending_confirmations()  SOCIAL_ONLY candidates the founder still has to check (for the E3 batch screen)
record_render_results()  store rendered phone checks (PHONE_RENDER website checks)
"""

import asyncio
import hashlib
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from typing import Awaitable, Callable, Iterable, Optional

import structlog
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.app.config import get_settings
from backend.app.engines.eligibility import rules
from backend.app.engines.eligibility.render import RenderResult
from backend.app.engines.eligibility.verification import VerificationLadder, VerifierResult
from backend.app.engines.enrichment.site_visit import SiteVisit, visit_site
from backend.app.engines.intelligence.rules import FRESH_DAYS, Check, Facts, skip_reason
from backend.app.models.business import Business, BusinessSourceLink, BusinessStatus
from backend.app.models.compliance import OptOut
from backend.app.models.eligibility import (
    EXCERPT_MAX_CHARS,
    CaptureMethod,
    EmailCapture,
    EmailEligibility,
    EmailVerification,
    HoldReason,
    ObservationType,
    SocialConfirmation,
)
from backend.app.models.intelligence import CheckType, ContactLog, WebsiteCheck
from backend.app.models.source import SourceRecord

logger = structlog.get_logger(__name__)

CHUNK = 500                      # ids per IN (...) query; SQLite limits bound parameters
VERIFY_PARALLEL = 10             # DNS lookups / verifier calls at once
EXCLUDED_STATUSES = (BusinessStatus.DUPLICATE, BusinessStatus.INVALID)


def capture_key(business_id: int, email: str, origin: str, source_url: Optional[str]) -> str:
    raw = f"{business_id}|{email.lower()}|{origin}|{source_url or ''}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def _chunks(values: list, size: int = CHUNK) -> Iterable[list]:
    for start in range(0, len(values), size):
        yield values[start:start + size]


async def homepage_check(url: str) -> SiteVisit:
    """robots.txt + homepage only, same limits and SSRF guard as every visit (site_visit.py)."""
    return await visit_site(url, lambda html, source: [], contact_pages=False)


def visit_check_detail(visit: SiteVisit, **extra) -> dict:
    return {"http_status": visit.http_status, "final_url": visit.final_url, "has_ssl": visit.has_https,
            "has_viewport": visit.has_viewport, "note": visit.note, "robots": visit.robots, **extra}


class EligibilityService:
    def __init__(self, session: AsyncSession, ladder: Optional[VerificationLadder] = None,
                 site_check: Callable[[str], Awaitable[SiteVisit]] = homepage_check):
        self.session = session
        self.ladder = ladder or VerificationLadder.from_settings(get_settings())
        self.site_check = site_check

    # ─── loading ─────────────────────────────────────────────────────────

    async def _target_business_ids(self, business_ids: Optional[list[int]]) -> list[int]:
        """Businesses with at least one captured address, plus every business that shares one of their addresses
        (dedupe across businesses needs both sides)."""
        stmt = select(EmailCapture.business_id).distinct()
        if business_ids is None:
            return sorted((await self.session.execute(stmt)).scalars().all())
        wanted = sorted(set(business_ids))
        emails: set[str] = set()
        for part in _chunks(wanted):
            emails.update((await self.session.execute(
                select(EmailCapture.email).where(EmailCapture.business_id.in_(part)))).scalars().all())
        ids = set()
        for part in _chunks(sorted(emails)):
            ids.update((await self.session.execute(
                select(EmailCapture.business_id).where(EmailCapture.email.in_(part)))).scalars().all())
        return sorted(ids)

    async def _site_share_counts(self) -> dict[str, int]:
        rows = (await self.session.execute(select(Business.website_url).where(
            Business.website_url.isnot(None), Business.status.notin_(EXCLUDED_STATUSES)))).scalars().all()
        counts: dict[str, int] = defaultdict(int)
        for url in rows:
            key = rules.site_key(url) if rules.is_own_website(url) else None
            if key:
                counts[key] += 1
        return counts

    async def _load(self, ids: list[int]) -> dict:
        data = {"businesses": {}, "raw": defaultdict(list), "captures": defaultdict(list), "checks": defaultdict(list),
                "confirmations": {}, "dnc": set()}
        for part in _chunks(ids):
            for business in (await self.session.execute(select(Business).where(Business.id.in_(part)).options(
                    selectinload(Business.categories), selectinload(Business.locations)))).scalars():
                data["businesses"][business.id] = business
            for business_id, raw in (await self.session.execute(
                    select(BusinessSourceLink.business_id, SourceRecord.raw_data)
                    .join(SourceRecord, SourceRecord.id == BusinessSourceLink.source_record_id)
                    .where(BusinessSourceLink.business_id.in_(part)))).all():
                if isinstance(raw, dict):
                    data["raw"][business_id].append(raw)
            for capture in (await self.session.execute(
                    select(EmailCapture).where(EmailCapture.business_id.in_(part)))).scalars():
                data["captures"][(capture.business_id, capture.email)].append(rules.Capture(
                    capture.id, capture.email, capture.method, capture.source_url, capture.excerpt,
                    capture.captured_at, capture.origin))
            for row in (await self.session.execute(select(WebsiteCheck).where(
                    WebsiteCheck.business_id.in_(part),
                    WebsiteCheck.check_type.in_([CheckType.SITE_FETCH, CheckType.PHONE_RENDER])))).scalars():
                data["checks"][row.business_id].append(
                    Check(row.id, row.check_type, row.outcome, row.target, row.detail or {}, row.observed_at))
            for row in (await self.session.execute(select(SocialConfirmation).where(
                    SocialConfirmation.business_id.in_(part)).order_by(SocialConfirmation.checked_at,
                                                                         SocialConfirmation.id))).scalars():
                data["confirmations"][row.business_id] = rules.Confirmation(
                    row.id, row.profile_url, row.checked_at, row.website_link_present, row.email_seen)
            data["dnc"].update((await self.session.execute(select(ContactLog.business_id).where(
                ContactLog.business_id.in_(part), ContactLog.outcome == "do_not_contact"))).scalars().all())
        return data

    async def _verifications(self, emails: Iterable[str]) -> dict[str, list[rules.VerificationRecord]]:
        found: dict[str, list[rules.VerificationRecord]] = defaultdict(list)
        for part in _chunks(sorted(set(emails))):
            for row in (await self.session.execute(
                    select(EmailVerification).where(EmailVerification.email.in_(part)))).scalars():
                found[row.email].append(rules.VerificationRecord(row.provider, row.status, row.checked_at,
                                                                 row.detail or {}))
        return found

    async def _opt_outs(self) -> tuple[set[str], set[str]]:
        rows = (await self.session.execute(select(OptOut.email, OptOut.domain))).all()
        return ({(e or "").lower() for e, _ in rows if e}, {(d or "").lower() for _, d in rows if d})

    # ─── deciding ────────────────────────────────────────────────────────

    def _facts(self, business: Business, raw: list[dict], share: dict[str, int], dnc: set[int]
               ) -> rules.BusinessFacts:
        categories = [c.category_name for c in business.categories] + [
            str(r.get("basic_category") or "") for r in raw]
        brand = next((r.get("brand_name") or r.get("brand_wikidata") for r in raw
                      if r.get("brand_name") or r.get("brand_wikidata")), None)
        # Rule 9 without the brand part (a brand is CHAIN_OR_DIRECTORY here, not NOT_A_PROSPECT).
        skip = skip_reason(Facts(name=business.name, categories=categories, phone=None, email=None,
                                 social_platforms=[], raw_records=raw, include_franchises=True))
        key = rules.site_key(business.website_url) if rules.is_own_website(business.website_url) else None
        vertical = next((r.get("vertical") for r in raw if r.get("vertical")), None) or rules.vertical_for(
            " ".join(categories))
        return rules.BusinessFacts(
            id=business.id, name=business.name, country=business.country_code, website_url=business.website_url,
            social_urls=dict(business.social_urls or {}), brand=brand, skip_reason=skip,
            site_share_count=share.get(key, 1) if key else 1, suppressed=business.id in dnc, vertical=vertical)

    async def _decide_all(self, ids: list[int], now: datetime) -> tuple[list[rules.Decision], dict]:
        data = await self._load(ids)
        share = await self._site_share_counts()
        opt_emails, opt_domains = await self._opt_outs()
        verifications = await self._verifications(email for _, email in data["captures"])
        facts_by_id, decisions = {}, []
        observations: dict[int, rules.ObservationResult] = {}
        for (business_id, email), captures in sorted(data["captures"].items()):
            business = data["businesses"].get(business_id)
            if business is None or business.status in EXCLUDED_STATUSES:
                continue
            if business_id not in facts_by_id:
                facts_by_id[business_id] = self._facts(business, data["raw"][business_id], share, data["dnc"])
                observations[business_id] = rules.find_observation(
                    facts_by_id[business_id], data["checks"][business_id],
                    data["confirmations"].get(business_id), now)
            domain = email.rsplit("@", 1)[-1]
            decisions.append(rules.decide(
                facts_by_id[business_id], email, captures, data["checks"][business_id],
                observations[business_id], verifications.get(email, []),
                email in opt_emails or domain in opt_domains, now))
        rules.dedupe(decisions)
        return decisions, facts_by_id

    async def _store(self, decisions: list[rules.Decision], facts_by_id: dict, now: datetime) -> None:
        existing: dict[tuple[int, str], EmailEligibility] = {}
        ids = sorted({d.business_id for d in decisions})
        for part in _chunks(ids):
            for row in (await self.session.execute(
                    select(EmailEligibility).where(EmailEligibility.business_id.in_(part)))).scalars():
                existing[(row.business_id, row.email)] = row
        for d in decisions:
            row = existing.get((d.business_id, d.email))
            if row is None:
                row = EmailEligibility(business_id=d.business_id, email=d.email)
                self.session.add(row)
            capture, observation = d.capture, d.observation
            row.email_hash = rules.email_hash(d.email)
            row.tier = d.tier
            row.capture_id = capture.id if capture else None
            row.method = capture.method if capture else None
            row.source_url = capture.source_url if capture else None
            row.captured_at = capture.captured_at if capture else None
            row.excerpt = capture.excerpt if capture else None
            row.recipient_type = d.recipient_type
            row.verification_status = d.verification_status
            row.verification_provider = d.verification_provider
            row.verified_at = d.verified_at
            row.country = facts_by_id[d.business_id].country
            row.vertical = facts_by_id[d.business_id].vertical
            row.observation_type = observation.type if observation else None
            row.observation_text = observation.text if observation else None
            row.observation_checked_at = observation.checked_at if observation else None
            row.observation_evidence_path = observation.evidence_path if observation else None
            row.suppressed = d.suppressed
            row.hold_reasons = [h.value for h in d.holds]
            row.eligible = d.eligible
            row.eligible_if_verified = d.eligible_if_verified
            row.evaluated_at = now
        await self.session.flush()

    # ─── verification ladder ─────────────────────────────────────────────

    async def _save_verification(self, email: str, result: VerifierResult, now: datetime) -> None:
        row = (await self.session.execute(select(EmailVerification).where(
            EmailVerification.email == email, EmailVerification.provider == result.provider))).scalar_one_or_none()
        if row is None:
            row = EmailVerification(email=email, provider=result.provider)
            self.session.add(row)
        row.status, row.detail, row.checked_at = result.status, result.detail, now

    async def verify_emails(self, emails: Iterable[str], now: Optional[datetime] = None,
                            force_mx: bool = False) -> dict:
        """Run the ladder for these addresses, skipping fresh cached results (<= 30 days).
        force_mx = always repeat the MX check (the recheck right before sending)."""
        now = now or datetime.now(timezone.utc)
        emails = sorted(set(emails))
        cached = await self._verifications(emails)
        gate = asyncio.Semaphore(VERIFY_PARALLEL)
        stats = defaultdict(int)

        async def run(verifier, email):
            async with gate:
                return email, await verifier.verify(email)

        need_mx = [e for e in emails if force_mx or rules.fresh_record(cached.get(e, []), "syntax_mx", now) is None]
        for email, result in await asyncio.gather(*(run(self.ladder.syntax_mx, e) for e in need_mx)):
            stats[f"syntax_mx_{result.status.value if result.status else 'no_answer'}"] += 1
            if result.status is not None:
                await self._save_verification(email, result, now)
                cached[email] = [r for r in cached.get(email, []) if r.provider != "syntax_mx"] + [
                    rules.VerificationRecord("syntax_mx", result.status, now, result.detail)]
        if self.ladder.paid is not None:
            need_paid = [e for e in emails
                         if rules.effective_verification(cached.get(e, []), now)[0].value != "INVALID"
                         and rules.fresh_record(cached.get(e, []), "bouncer", now) is None]
            for email, result in await asyncio.gather(*(run(self.ladder.paid, e) for e in need_paid)):
                stats[f"bouncer_{result.status.value if result.status else 'no_answer'}"] += 1
                if result.status is not None:
                    await self._save_verification(email, result, now)
        else:
            stats["paid_verifier"] = 0   # no BOUNCER_API_KEY: addresses stay UNVERIFIED
        await self.session.flush()
        return dict(stats)

    # ─── public ──────────────────────────────────────────────────────────

    async def evaluate(self, business_ids: Optional[list[int]] = None, verify: bool = False,
                       now: Optional[datetime] = None) -> dict:
        now = now or datetime.now(timezone.utc)
        ids = await self._target_business_ids(business_ids)
        decisions, facts_by_id = await self._decide_all(ids, now)
        verified = {}
        if verify:
            # Only addresses that nothing else holds back are worth a (paid) verifier call.
            waiting = {HoldReason.NOT_VERIFIED, HoldReason.MAILBOX_DOMAIN_DOWN}
            candidates = [d.email for d in decisions if set(d.holds) <= waiting]
            verified = await self.verify_emails(candidates, now)
            decisions, facts_by_id = await self._decide_all(ids, now)
        await self._store(decisions, facts_by_id, now)
        holds: dict[str, int] = defaultdict(int)
        for d in decisions:
            for h in d.holds:
                holds[h.value] += 1
        return {"businesses": len(facts_by_id), "rows": len(decisions),
                "eligible": sum(d.eligible for d in decisions),
                "eligible_if_verified": sum(d.eligible_if_verified for d in decisions),
                "hold": sum(not d.eligible for d in decisions),
                "by_hold_reason": dict(sorted(holds.items())), "verification": verified,
                "paid_verifier_configured": self.ladder.paid is not None, "evaluated_at": now.isoformat()}

    async def list_eligibility(self, status: Optional[str], limit: int) -> dict:
        all_rows = (await self.session.execute(select(
            EmailEligibility.eligible, EmailEligibility.eligible_if_verified, EmailEligibility.hold_reasons))).all()
        holds: dict[str, int] = defaultdict(int)
        for _, _, reasons in all_rows:
            for reason in reasons or []:
                holds[reason] += 1
        stmt = (select(EmailEligibility, Business.name)
                .join(Business, Business.id == EmailEligibility.business_id)
                .order_by(EmailEligibility.eligible.desc(), EmailEligibility.eligible_if_verified.desc(),
                          EmailEligibility.business_id, EmailEligibility.email))
        if status == "eligible":
            stmt = stmt.where(EmailEligibility.eligible.is_(True))
        elif status == "hold":
            stmt = stmt.where(EmailEligibility.eligible.is_(False))
        items = []
        for row, name in (await self.session.execute(stmt.limit(limit))).all():
            items.append(self.row_dict(row, name))
        eligible = sum(1 for e, _, _ in all_rows if e)
        total = {"eligible": eligible, "hold": len(all_rows) - eligible}.get(status or "", len(all_rows))
        return {"items": items, "total": total,
                "counts": {"rows": len(all_rows), "eligible": eligible, "hold": len(all_rows) - eligible,
                           "eligible_if_verified": sum(1 for _, v, _ in all_rows if v),
                           "by_hold_reason": dict(sorted(holds.items()))}}

    @staticmethod
    def row_dict(row: EmailEligibility, business_name: Optional[str] = None) -> dict:
        def iso(moment):
            return rules.aware(moment).isoformat() if moment else None

        return {
            "id": row.id, "business_id": row.business_id, "business_name": business_name,
            "email": row.email, "email_hash": row.email_hash, "tier": row.tier.value,
            "provenance": {"method": row.method.value if row.method else None, "source_url": row.source_url,
                           "captured_at": iso(row.captured_at), "excerpt": row.excerpt},
            "recipient_type": row.recipient_type.value,
            "verification_status": row.verification_status.value,
            "verification_provider": row.verification_provider, "verified_at": iso(row.verified_at),
            "country": row.country, "vertical": row.vertical,
            "observation": None if row.observation_type is None else {
                "type": row.observation_type.value, "text": row.observation_text,
                "checked_at": iso(row.observation_checked_at), "evidence_path": row.observation_evidence_path},
            "suppressed": row.suppressed, "hold_reasons": list(row.hold_reasons or []),
            "eligible": row.eligible, "eligible_if_verified": row.eligible_if_verified,
            "evaluated_at": iso(row.evaluated_at),
        }

    async def business_rows(self, business_id: int) -> list[dict]:
        rows = (await self.session.execute(select(EmailEligibility, Business.name)
                                           .join(Business, Business.id == EmailEligibility.business_id)
                                           .where(EmailEligibility.business_id == business_id)
                                           .order_by(EmailEligibility.email))).all()
        return [self.row_dict(row, name) for row, name in rows]

    async def recheck_before_send(self, business_id: int, now: Optional[datetime] = None) -> dict:
        """
        Spec row 4: a SITE_DOWN lead is "rechecked right before sending". E2 calls this immediately before the SMTP
        submission and sends only when `send_allowed` is true:
          1. a fresh homepage check (robots.txt + homepage, same limits and SSRF guard); stored as a SITE_FETCH check
          2. a fresh MX check of the business's addresses (an address on the down domain must still accept mail)
          3. re-evaluation; for a SITE_DOWN lead the fresh check itself must have failed
        For a lead with another observation it re-evaluates only (send_allowed = an eligible address exists).
        """
        now = now or datetime.now(timezone.utc)
        business = (await self.session.execute(select(Business).where(Business.id == business_id))
                    ).scalar_one_or_none()
        if business is None:
            raise LookupError(f"Business {business_id} not found")
        before = {r["email"]: r for r in await self.business_rows(business_id)}
        site_down = any((r.get("observation") or {}).get("type") == ObservationType.SITE_DOWN.value
                        for r in before.values())
        check = None
        if site_down and rules.is_own_website(business.website_url):
            visit = await self.site_check(business.website_url)
            self.session.add(WebsiteCheck(business_id=business_id, check_type=CheckType.SITE_FETCH,
                                          target=business.website_url[:1000], outcome=visit.outcome,
                                          detail=visit_check_detail(visit, recheck_before_send=True),
                                          observed_at=now))
            check = {"outcome": visit.outcome, "note": visit.note, "observed_at": now.isoformat()}
            emails = (await self.session.execute(select(EmailCapture.email).where(
                EmailCapture.business_id == business_id).distinct())).scalars().all()
            await self.verify_emails(emails, now, force_mx=True)
            await self.session.flush()
        await self.evaluate([business_id], now=now)
        after = await self.business_rows(business_id)
        allowed = [r for r in after if r["eligible"]]
        if site_down and (check is None or check["outcome"] != "failed"):
            allowed = []
        reason = None
        if site_down and check and check["outcome"] in rules.SITE_EXISTS:
            reason = HoldReason.SITE_RECOVERED.value
        elif not allowed:
            reason = "NOT_ELIGIBLE"
        return {"business_id": business_id, "site_down_lead": site_down, "site_check": check,
                "send_allowed": bool(allowed), "reason": reason,
                "send_to": allowed[0]["email"] if allowed else None,
                "observation_text": (allowed[0]["observation"] or {}).get("text") if allowed else None,
                "rows": after}

    # ─── founder confirmations (SOCIAL_ONLY) ─────────────────────────────

    async def record_confirmation(self, business_id: int, profile_url: str, checked_at: datetime,
                                  website_link_present: bool, email_seen: Optional[str]) -> dict:
        business = (await self.session.execute(select(Business).where(Business.id == business_id))
                    ).scalar_one_or_none()
        if business is None:
            raise LookupError(f"Business {business_id} not found")
        checked_at = rules.aware(checked_at)
        row = SocialConfirmation(business_id=business_id, profile_url=profile_url, checked_at=checked_at,
                                 website_link_present=website_link_present, email_seen=email_seen)
        self.session.add(row)
        await self.session.flush()
        socials = dict(business.social_urls or {})
        if "instagram" not in socials:
            socials["instagram"] = profile_url
            business.social_urls = socials   # a new dict: JSON columns do not track in-place edits
        if email_seen:
            origin = f"confirmation:{row.id}"
            excerpt = (f"Founder check of the Instagram bio on {rules.date_text(checked_at)}: "
                       f"the profile showed {email_seen}.")[:EXCERPT_MAX_CHARS]
            self.session.add(EmailCapture(
                business_id=business_id, email=email_seen, method=CaptureMethod.FOUNDER_CONFIRMED,
                raw_method="founder_confirmed", source_url=profile_url, excerpt=excerpt, captured_at=checked_at,
                origin=origin, capture_key=capture_key(business_id, email_seen, origin, profile_url)))
            await self.session.flush()
        await self.evaluate([business_id])
        return {"confirmation": {"id": row.id, "business_id": business_id, "profile_url": profile_url,
                                 "checked_at": checked_at.isoformat(),
                                 "website_link_present": website_link_present, "email_seen": email_seen},
                "eligibility": await self.business_rows(business_id)}

    async def pending_confirmations(self, limit: int, now: Optional[datetime] = None) -> dict:
        """India, live, an Instagram profile, no own website, and no founder check in the last 30 days."""
        now = now or datetime.now(timezone.utc)
        cutoff = now - timedelta(days=FRESH_DAYS)
        recent = select(SocialConfirmation.business_id).where(SocialConfirmation.checked_at >= cutoff)
        stmt = (select(Business).where(Business.country_code == "IN", Business.status.notin_(EXCLUDED_STATUSES),
                                       Business.social_urls.isnot(None), Business.id.notin_(recent))
                .options(selectinload(Business.locations), selectinload(Business.categories))
                .order_by(Business.id))
        items = []
        for business in (await self.session.execute(stmt)).scalars():
            profile = (business.social_urls or {}).get("instagram")
            if not profile or rules.is_own_website(business.website_url):
                continue
            items.append({"business_id": business.id, "business_name": business.name, "profile_url": profile,
                          "city": business.locations[0].city if business.locations else None,
                          "vertical": rules.vertical_for(" ".join(c.category_name for c in business.categories))})
        return {"items": items[:limit], "total": len(items)}

    # ─── rendered phone checks ───────────────────────────────────────────

    async def render_candidates(self, business_ids: Optional[list[int]] = None) -> list[tuple[int, str]]:
        """Businesses whose latest homepage check found no viewport tag and that have an address read on their
        own pages (only those can become Tier 1 + NO_VIEWPORT). A page already rendered (zoomed_out / fits) after
        that homepage check is not rendered again. Returns (business id, URL to render)."""
        page_methods = [CaptureMethod.MAILTO, CaptureMethod.VISIBLE_TEXT, CaptureMethod.CLOUDFLARE_DECODE]
        stmt = select(EmailCapture.business_id).where(EmailCapture.method.in_(page_methods)).distinct()
        ids = sorted(set((await self.session.execute(stmt)).scalars().all()))
        if business_ids is not None:
            ids = sorted(set(ids) & set(business_ids))
        out = []
        for part in _chunks(ids):
            checks: dict[int, list[WebsiteCheck]] = defaultdict(list)
            renders: dict[int, list[WebsiteCheck]] = defaultdict(list)
            for row in (await self.session.execute(select(WebsiteCheck).where(
                    WebsiteCheck.business_id.in_(part),
                    WebsiteCheck.check_type.in_([CheckType.SITE_FETCH, CheckType.PHONE_RENDER])))).scalars():
                (checks if row.check_type == CheckType.SITE_FETCH else renders)[row.business_id].append(row)
            for business_id in part:
                fetches = sorted(checks.get(business_id, []), key=lambda c: (rules.aware(c.observed_at), c.id))
                fetches = [c for c in fetches if c.outcome in rules.SITE_EXISTS | rules.SITE_FAILED]
                no_viewport = (fetches[-1].detail or {}).get("has_viewport") is False if fetches else False
                if not fetches or fetches[-1].outcome != "ok" or not no_viewport:
                    continue
                latest = fetches[-1]
                if any(r.outcome in ("zoomed_out", "fits")
                       and rules.aware(r.observed_at) >= rules.aware(latest.observed_at)
                       for r in renders.get(business_id, [])):
                    continue
                out.append((business_id, (latest.detail or {}).get("final_url") or latest.target))
        return out

    async def record_render_results(self, results: list[RenderResult]) -> int:
        stored = 0
        for result in results:
            try:
                business_id = int(result.key)
            except ValueError:
                continue
            self.session.add(WebsiteCheck(
                business_id=business_id, check_type=CheckType.PHONE_RENDER, target=(result.url or "")[:1000],
                outcome=result.outcome, detail=result.detail(),
                observed_at=result.checked_at or datetime.now(timezone.utc)))
            stored += 1
        await self.session.flush()
        return stored
