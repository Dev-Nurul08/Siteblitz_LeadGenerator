"""
Email engine v2, phase E3 - the batch screen's service (spec: docs/spec/email-engine-v2.md rows 5, 6, 9, 10, 19).

  allowance   new first contacts left for a sending day: ramp limit - already scheduled - held by unapproved batch
              leads, never more than the free campaign slots of the usable mailboxes; 0 with a reason when the day
              is not a campaign day, the ramp is at stage 0, new contacts are paused or no mailbox can send
  create      refuses ids that are not eligible (or already in a sequence / an open batch) and refuses a selection
              larger than the allowance (the 11th on a 10-a-day day) - all or nothing, with the ids and a message;
              otherwise stores the batch, a frozen copy of the evidence and E2's dry-run schedule per lead
  write       T1, T2, T3 per lead with the AI writer + validator (docs/outreach/pilot-templates.md); the texts name
              the sender of the lead's planned mailbox; a lead that cannot be written is HOLD with reason codes
  approve     E2 admits the sequence on that mailbox with the step-1 text, then steps 2 and 3 get their texts and
              the approval (who + when) through E2's own service
  reject      per lead, with a reason and who

Nothing here sends mail. Every method takes `now` so tests run on a fake clock.
"""

import asyncio
from collections import defaultdict
from datetime import date, datetime, timedelta, timezone
from typing import Any, Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.app.config import Settings
from backend.app.engines.sending import scheduler as sched
from backend.app.engines.writer.writer import MODEL, OutreachWriter, build_lead, pilot_task
from backend.app.models.business import Business
from backend.app.models.eligibility import EmailEligibility, ObservationType, SocialConfirmation
from backend.app.models.outreach_batch import OPEN_LEAD_STATES, BatchLeadState, OutreachBatch, OutreachBatchLead
from backend.app.models.sending import EmailSequence, Mailbox, SendRecord, SequenceState
from backend.app.services.eligibility_service import EligibilityService
from backend.app.services.sending_service import SendingConfig, SendingService, aware, iso

TEMPLATE_VERSION = "pilot-v1"            # docs/outreach/pilot-templates.md
PILOT_ZONE = sched.COUNTRY_TIMEZONES["IN"]
MAX_BATCH = 100
MISSING_COMPANY_FACT = "MISSING_COMPANY_FACT"

# Batches whose writing task is running in this process (the screen offers "continue writing" otherwise).
RUNNING: set[int] = set()


class BatchError(Exception):
    status = 400

    def __init__(self, code: str, message: str, **extra: Any):
        super().__init__(message)
        self.code, self.message, self.extra = code, message, extra

    def detail(self) -> dict:
        return {"code": self.code, "message": self.message, **self.extra}


class BatchRefused(BatchError):
    status = 409


class BatchNotFound(BatchError):
    status = 404


def default_send_date(now: datetime) -> date:
    """Today (India time) while today's last campaign window is still open, else the next Tuesday-Thursday."""
    zone = sched.load_zone(PILOT_ZONE)
    day = sched.local_date(now, zone)
    while True:
        if sched.is_campaign_day(day) and aware(now) < sched.windows_for(day, zone)[-1].end:
            return day
        day += timedelta(days=1)


def day_text(day: date) -> str:
    return f"{day:%a} {day.day} {day:%b %Y}"


def batch_status(leads: list[OutreachBatchLead]) -> str:
    states = {lead.state for lead in leads}
    if states & {BatchLeadState.PENDING, BatchLeadState.WRITING}:
        return "WRITING"
    if BatchLeadState.READY in states:
        return "REVIEW"
    return "DONE"


def write_three(writer: OutreachWriter, lead: dict, observation_type: str, sentence: str) -> dict:
    """T1, T2, T3 for one lead (runs in a worker thread: plain data in, plain data out). Stops at the first touch
    that is not READY: a lead goes out with all three texts or not at all."""
    thread: list[dict] = []
    out: dict = {"state": "READY", "texts": {}, "subject": None, "touches": [], "hold": [], "detail": []}
    for touch in (1, 2, 3):
        task = pilot_task(touch, lead, observation_type, sentence, writer.facts)
        result = writer.write({**lead, "thread": list(thread)}, task)
        out["touches"].append({"touch": touch, "status": result.status, "attempts": result.attempts,
                               "hold_reason": result.hold_reason})
        if result.status != "READY":
            out["state"] = "HOLD"
            out["hold"] = [result.hold_reason or "VALIDATION_FAILED"]
            out["detail"] = [f"T{touch}: {e}" for e in (result.errors or [result.hold_reason or "held"])]
            return out
        out["texts"][touch] = result.text
        if touch == 1:
            out["subject"] = result.subject
        thread.append({"direction": "out", "channel": "email", "sent_at": None, "text": result.output["body"]})
    return out


class BatchService:
    def __init__(self, session: AsyncSession, config: SendingConfig, settings: Settings, client: Any = None):
        self.session = session
        self.config = config
        self.settings = settings
        self.client = client          # the model client; None = the writer builds the real one from the API key
        self.sending = SendingService(session, config)
        self._writers: dict[tuple, OutreachWriter] = {}

    @staticmethod
    def _now(now: Optional[datetime]) -> datetime:
        return aware(now) if now else datetime.now(timezone.utc)

    # ─── allowance ───────────────────────────────────────────────────────

    async def reserved_by_batches(self, send_date: date) -> int:
        return (await self.session.execute(
            select(func.count()).select_from(OutreachBatchLead)
            .join(OutreachBatch, OutreachBatch.id == OutreachBatchLead.batch_id)
            .where(OutreachBatch.send_date == send_date, OutreachBatchLead.state.in_(OPEN_LEAD_STATES)))
        ).scalar_one()

    async def allowance(self, send_date: Optional[date] = None, now: Optional[datetime] = None) -> dict:
        now = self._now(now)
        zone = sched.load_zone(PILOT_ZONE)
        send_date = send_date or default_send_date(now)
        ramp = await self.sending.ramp_info()
        limit = ramp["daily_new_limit"]
        book = await self.sending.capacity_book(send_date, send_date)
        scheduled = book.new_contacts.get(send_date, 0)
        reserved = await self.reserved_by_batches(send_date)
        flags = await self.sending.active_pauses()
        blocks = self.sending.blocking(flags, step=1, mailbox=None, sequence=None)
        boxes = []
        for box in await self.sending.enabled_mailboxes():
            load = book.load(box.id, send_date)
            paused = [f.reason_code for f in self.sending.blocking(flags, step=1, mailbox=box, sequence=None)
                      if f.scope.value in ("DOMAIN", "MAILBOX")]
            boxes.append({"mailbox_id": box.id, "address": box.address, "display_name": box.display_name,
                          "campaign_reserved": load.campaign, "campaign_limit": sched.CAMPAIGN_DAILY_LIMIT,
                          "campaign_free": max(0, sched.CAMPAIGN_DAILY_LIMIT - load.campaign),
                          "total_reserved": load.total, "daily_ceiling": sched.MAILBOX_DAILY_CEILING,
                          "paused": paused})
        free_slots = sum(b["campaign_free"] for b in boxes if not b["paused"])
        left = max(0, limit - scheduled - reserved)
        when = day_text(send_date)
        limited_by, message = "ramp", None
        if not sched.is_campaign_day(send_date):
            left, limited_by, message = 0, "not_a_campaign_day", f"{when} is not a Tuesday, Wednesday or Thursday."
        elif send_date < sched.local_date(now, zone) or now >= sched.windows_for(send_date, zone)[-1].end:
            left, limited_by, message = 0, "day_over", f"The sending windows of {when} are over."
        elif limit <= 0:
            left, limited_by = 0, "ramp_stage_0"
            message = "New first contacts are off: the ramp is at stage 0 (the pilot has not started)."
        elif blocks:
            left, limited_by = 0, "paused"
            message = "New first contacts are paused: " + ", ".join(
                f"{f.reason_code} ({f.scope.value.lower().replace('_', ' ')})" for f in blocks) + "."
        elif not any(not b["paused"] for b in boxes):
            left, limited_by, message = 0, "no_mailbox", "No enabled, unpaused mailbox can send."
        elif free_slots < left:
            left, limited_by = free_slots, "mailbox_capacity"
            message = f"The mailboxes have {free_slots} free campaign slots on {when}."
        if message is None:
            message = (f"{left} new first contacts left for {when}: the ramp (stage {ramp['stage']}) allows "
                       f"{limit} a day, {scheduled} already scheduled, {reserved} held by unapproved batch leads.")
        return {"send_date": send_date.isoformat(), "send_date_text": when,
                "campaign_day": sched.is_campaign_day(send_date), "ramp_stage": ramp["stage"],
                "daily_limit": limit, "scheduled_new": scheduled, "reserved_by_batches": reserved, "left": left,
                "limited_by": limited_by, "message": message, "mailboxes": boxes,
                "pauses": [{"id": f.id, "scope": f.scope.value, "scope_value": f.scope_value,
                            "level": f.level.value, "reason_code": f.reason_code, "detail": f.detail,
                            "created_at": iso(f.created_at), "blocks_new_contacts": f in blocks}
                           for f in flags]}

    # ─── candidates (the eligible list with HOLD reasons) ───────────────

    async def busy_map(self) -> tuple[set[int], set[str], dict[int, int]]:
        live = (await self.session.execute(select(EmailSequence.business_id, EmailSequence.recipient_hash).where(
            EmailSequence.state != SequenceState.CANCELLED))).all()
        open_leads = (await self.session.execute(select(OutreachBatchLead.eligibility_id, OutreachBatchLead.batch_id)
                                                 .where(OutreachBatchLead.state.in_(OPEN_LEAD_STATES)))).all()
        return ({b for b, _ in live}, {h for _, h in live},
                {e: b for e, b in open_leads if e is not None})

    def _busy(self, row: EmailEligibility, maps) -> Optional[dict]:
        businesses, hashes, in_batch = maps
        if row.business_id in businesses or row.email_hash in hashes:
            return {"code": "IN_SEQUENCE", "message": "this business already has a sequence"}
        if row.id in in_batch:
            return {"code": "IN_BATCH", "message": f"in batch {in_batch[row.id]}", "batch_id": in_batch[row.id]}
        return None

    async def candidates(self, status: str = "all", reason: Optional[str] = None, limit: int = 200) -> dict:
        rows = (await self.session.execute(
            select(EmailEligibility, Business.name).join(Business, Business.id == EmailEligibility.business_id)
            .order_by(EmailEligibility.eligible.desc(), EmailEligibility.business_id, EmailEligibility.email))).all()
        maps = await self.busy_map()
        counts: dict[str, int] = defaultdict(int)
        eligible = selectable = 0
        items = []
        for row, name in rows:
            busy = self._busy(row, maps) if row.eligible else None
            if row.eligible:
                eligible += 1
                selectable += busy is None
            for code in row.hold_reasons or []:
                counts[code] += 1
            if status == "eligible" and not row.eligible or status == "hold" and row.eligible:
                continue
            if reason and reason not in (row.hold_reasons or []):
                continue
            if len(items) < limit:
                items.append({**EligibilityService.row_dict(row, name), "busy": busy})
        return {"items": items, "counts": {"rows": len(rows), "eligible": eligible, "selectable": selectable,
                                           "hold": len(rows) - eligible, "by_hold_reason": dict(sorted(counts.items()))}}

    # ─── create ──────────────────────────────────────────────────────────

    async def _evidence(self, row: EmailEligibility, business: Business) -> dict:
        evidence_url = None
        if row.observation_type == ObservationType.SOCIAL_ONLY:
            evidence_url = (business.social_urls or {}).get("instagram")
            if not evidence_url:
                evidence_url = (await self.session.execute(
                    select(SocialConfirmation.profile_url).where(SocialConfirmation.business_id == business.id)
                    .order_by(SocialConfirmation.checked_at.desc()).limit(1))).scalar_one_or_none()
        elif row.observation_type is not None:
            evidence_url = business.website_url
        location = business.locations[0] if business.locations else None
        category = next((c.category_name for c in business.categories if c.is_primary), None) or \
            (business.categories[0].category_name if business.categories else None)
        return {
            "business_name": business.name, "city": location.city if location else None,
            "region": location.state_province if location else None, "category": category,
            "country": row.country or business.country_code, "vertical": row.vertical or "other",
            "email": row.email, "recipient_type": row.recipient_type.value,
            "observation": {"type": row.observation_type.value if row.observation_type else None,
                            "text": row.observation_text, "checked_at": iso(row.observation_checked_at),
                            "evidence_path": row.observation_evidence_path, "evidence_url": evidence_url},
            "provenance": {"method": row.method.value if row.method else None, "source_url": row.source_url,
                           "captured_at": iso(row.captured_at), "excerpt": row.excerpt},
            "verification": {"status": row.verification_status.value, "provider": row.verification_provider,
                             "verified_at": iso(row.verified_at)},
        }

    async def create(self, eligibility_ids: list[int], send_date: Optional[date], created_by: str,
                     now: Optional[datetime] = None) -> OutreachBatch:
        now = self._now(now)
        ids = list(dict.fromkeys(eligibility_ids))
        if not ids:
            raise BatchError("EMPTY", "select at least one lead")
        if len(ids) > MAX_BATCH:
            raise BatchError("TOO_MANY", f"at most {MAX_BATCH} leads per batch")
        maps = await self.busy_map()
        refused, rows = [], []
        for eligibility_id in ids:
            row = await self.session.get(EmailEligibility, eligibility_id)
            if row is None:
                refused.append({"eligibility_id": eligibility_id, "code": "NOT_FOUND",
                                "message": f"eligibility row {eligibility_id} does not exist"})
            elif not row.eligible or row.suppressed:
                refused.append({"eligibility_id": eligibility_id, "code": "NOT_ELIGIBLE",
                                "message": "not eligible: " + (", ".join(row.hold_reasons or []) or "HOLD")})
            elif busy := self._busy(row, maps):
                refused.append({"eligibility_id": eligibility_id, "code": busy["code"], "message": busy["message"]})
            else:
                rows.append(row)
        if refused:
            raise BatchRefused("NOT_ELIGIBLE", f"{len(refused)} of the {len(ids)} selected leads cannot be written: "
                               + "; ".join(f"#{r['eligibility_id']} {r['message']}" for r in refused[:5]),
                               refused=refused)
        allowance = await self.allowance(send_date, now)
        send_date = date.fromisoformat(allowance["send_date"])
        if len(ids) > allowance["left"]:
            over = ids[allowance["left"]:]
            message = (f"Only {allowance['left']} new first contacts are left for {allowance['send_date_text']}, "
                       f"you selected {len(ids)}. {allowance['message']}")
            raise BatchRefused("CAP_REACHED", message, allowance=allowance,
                               refused=[{"eligibility_id": i, "code": "CAP_REACHED", "message": message} for i in over])

        missing = self.config.missing_company_facts()
        planned: dict[int, dict] = {}
        dry_refused: dict[int, dict] = {}
        if not missing:
            dry = await self.sending.create_sequences(
                send_date, [{"eligibility_id": r.id, "mailbox_id": None} for r in rows], now, dry_run=True)
            planned = {p["eligibility_id"]: p for p in dry["planned"]}
            dry_refused = {r["eligibility_id"]: r for r in dry["refused"]}
        batch = OutreachBatch(send_date=send_date, created_by=created_by, created_at=now,
                              writer_model=MODEL, template_version=TEMPLATE_VERSION)
        self.session.add(batch)
        await self.session.flush()
        for position, row in enumerate(rows):
            business = (await self.session.execute(
                select(Business).where(Business.id == row.business_id)
                .options(selectinload(Business.locations), selectinload(Business.categories)))).scalar_one()
            lead = OutreachBatchLead(batch_id=batch.id, position=position, eligibility_id=row.id,
                                     business_id=row.business_id, recipient_email=row.email,
                                     evidence=await self._evidence(row, business), hold_reasons=[], hold_detail=[])
            plan = planned.get(row.id)
            if missing:
                lead.state, lead.hold_reasons = BatchLeadState.HOLD, [MISSING_COMPANY_FACT]
                lead.hold_detail = ["blank in .env: " + ", ".join(missing)]
            elif plan is None:
                refusal = dry_refused.get(row.id, {"code": "NOT_SCHEDULED", "message": "no slot was planned"})
                lead.state, lead.hold_reasons = BatchLeadState.HOLD, [refusal["code"]]
                lead.hold_detail = [refusal["message"]]
            else:
                lead.state, lead.plan, lead.mailbox_id = BatchLeadState.PENDING, plan, plan["mailbox_id"]
                lead.sender_name = plan["display_name"]
            self.session.add(lead)
        await self.session.flush()
        return batch

    # ─── write ───────────────────────────────────────────────────────────

    def writer_for(self, mailbox: Mailbox) -> OutreachWriter:
        """The texts sign with the planned mailbox's founder name and address, so the From line, the identity
        sentence, the signature and Reply-To all name the same person (spec row 8: each mailbox under a real
        founder name). The postal address stays the company fact."""
        key = (mailbox.display_name, mailbox.address)
        if key not in self._writers:
            settings = self.settings.model_copy(update={"SITEBLITZ_SENDER_NAME": mailbox.display_name,
                                                        "SITEBLITZ_REPLY_EMAIL": mailbox.address})
            self._writers[key] = OutreachWriter(client=self.client, settings=settings)
        return self._writers[key]

    async def write(self, batch_id: int, now: Optional[datetime] = None) -> dict:
        """Write every PENDING (or interrupted WRITING) lead of a batch, committing after each lead so the screen
        shows progress. The model call runs in a thread; the session is only used between calls."""
        RUNNING.add(batch_id)
        try:
            ids = (await self.session.execute(select(OutreachBatchLead.id).where(
                OutreachBatchLead.batch_id == batch_id,
                OutreachBatchLead.state.in_((BatchLeadState.PENDING, BatchLeadState.WRITING)))
                .order_by(OutreachBatchLead.position))).scalars().all()
            written = 0
            for lead_id in ids:
                lead = await self.session.get(OutreachBatchLead, lead_id)
                await self.session.refresh(lead)
                if lead.state not in (BatchLeadState.PENDING, BatchLeadState.WRITING):
                    continue   # rejected while waiting
                mailbox = await self.session.get(Mailbox, lead.mailbox_id) if lead.mailbox_id else None
                lead.state = BatchLeadState.WRITING
                await self.session.commit()
                evidence = lead.evidence or {}
                observation = evidence.get("observation") or {}
                if mailbox is None or not observation.get("text") or not observation.get("type"):
                    lead.state, lead.hold_reasons = BatchLeadState.HOLD, ["NOT_SCHEDULED" if mailbox is None
                                                                          else "NO_OBSERVATION"]
                    lead.hold_detail = ["no planned mailbox" if mailbox is None else "no stored observation"]
                    await self.session.commit()
                    continue
                writer = self.writer_for(mailbox)
                model_lead = build_lead(lead_id=f"batch-lead-{lead.id}", business_name=evidence["business_name"],
                                        category=evidence.get("category"), city=evidence.get("city"),
                                        country=evidence.get("country"), region=evidence.get("region"),
                                        observations=[{"type": observation["type"],
                                                       "evidence_value": "Instagram"
                                                       if observation["type"] == "SOCIAL_ONLY" else None,
                                                       "checked_at": (observation.get("checked_at") or "")[:10],
                                                       "check_id": None}])
                model_lead["vertical"] = evidence.get("vertical") or "other"
                try:
                    result = await asyncio.to_thread(write_three, writer, model_lead, observation["type"],
                                                     observation["text"])
                except Exception as exc:   # a bug, not the model being down: never a text, the lead waits
                    result = {"state": "HOLD", "hold": ["WRITE_FAILED"], "texts": {}, "subject": None,
                              "touches": [], "detail": [f"{type(exc).__name__}: {exc}"[:300]]}
                lead = await self.session.get(OutreachBatchLead, lead_id)
                lead.writer_detail = {"model": MODEL, "template_version": TEMPLATE_VERSION,
                                      "touches": result["touches"]}
                lead.written_at = self._now(now)
                if result["state"] == "READY":
                    lead.state, lead.subject = BatchLeadState.READY, result["subject"]
                    lead.text_1, lead.text_2, lead.text_3 = (result["texts"][n] for n in (1, 2, 3))
                    lead.hold_reasons, lead.hold_detail = [], []
                else:
                    lead.state, lead.hold_reasons, lead.hold_detail = (BatchLeadState.HOLD, result["hold"],
                                                                       result["detail"][:20])
                await self.session.commit()
                written += 1
            return {"batch_id": batch_id, "written": written}
        finally:
            RUNNING.discard(batch_id)

    # ─── approve / reject ────────────────────────────────────────────────

    async def _batch_and_leads(self, batch_id: int) -> tuple[OutreachBatch, list[OutreachBatchLead]]:
        batch = await self.session.get(OutreachBatch, batch_id)
        if batch is None:
            raise BatchNotFound("NOT_FOUND", f"batch {batch_id} not found")
        leads = (await self.session.execute(select(OutreachBatchLead).where(OutreachBatchLead.batch_id == batch_id)
                                            .order_by(OutreachBatchLead.position))).scalars().all()
        return batch, list(leads)

    async def approve(self, batch_id: int, lead_ids: Optional[list[int]], approved_by: str,
                      now: Optional[datetime] = None) -> dict:
        """`lead_ids` None = every READY lead ("all_ready")."""
        now = self._now(now)
        batch, leads = await self._batch_and_leads(batch_id)
        wanted = set(lead_ids) if lead_ids is not None else None
        unknown = sorted(wanted - {lead.id for lead in leads}) if wanted is not None else []
        if unknown:
            raise BatchError("UNKNOWN_LEAD", f"not in batch {batch_id}: {unknown}")
        targets = [lead for lead in leads if (wanted is None or lead.id in wanted)
                   and lead.state == BatchLeadState.READY and lead.eligibility_id is not None]
        skipped = [{"lead_id": lead.id, "state": lead.state.value, "message": f"{lead.state.value}, not READY"}
                   for lead in leads if wanted is not None and lead.id in wanted and lead not in targets]
        approved, refused = [], []
        if targets:
            items = [{"eligibility_id": lead.eligibility_id, "subject": lead.subject, "body": lead.text_1,
                      "content_version": f"{TEMPLATE_VERSION}:T1", "approved_by": approved_by,
                      "mailbox_id": lead.mailbox_id} for lead in targets]
            result = await self.sending.create_sequences(batch.send_date, items, now)
            by_row = {lead.eligibility_id: lead for lead in targets}
            for admitted in result["admitted"]:
                lead = by_row[admitted["eligibility_id"]]
                texts = {2: lead.text_2, 3: lead.text_3}
                for record in admitted["records"]:
                    if record["step"] in texts:
                        await self.sending.approve_follow_up(record["id"], texts[record["step"]], approved_by,
                                                             f"{TEMPLATE_VERSION}:T{record['step']}", now)
                lead.state, lead.sequence_id = BatchLeadState.APPROVED, admitted["sequence_id"]
                lead.approved_by, lead.approved_at, lead.approval_refusal = approved_by, now, None
                approved.append({"lead_id": lead.id, "sequence_id": admitted["sequence_id"]})
            for refusal in result["refused"]:
                lead = by_row[refusal["eligibility_id"]]
                lead.approval_refusal = {"code": refusal["code"], "message": refusal["message"], "at": iso(now)}
                refused.append({"lead_id": lead.id, **refusal})
        await self.session.flush()
        return {"approved": approved, "refused": refused, "skipped": skipped}

    async def reject(self, batch_id: int, lead_ids: list[int], reason: str, rejected_by: str,
                     now: Optional[datetime] = None) -> dict:
        now = self._now(now)
        _, leads = await self._batch_and_leads(batch_id)
        by_id = {lead.id: lead for lead in leads}
        unknown = sorted(set(lead_ids) - set(by_id))
        if unknown:
            raise BatchError("UNKNOWN_LEAD", f"not in batch {batch_id}: {unknown}")
        blocked = [by_id[i] for i in lead_ids if by_id[i].state not in
                   (BatchLeadState.PENDING, BatchLeadState.READY, BatchLeadState.HOLD)]
        if blocked:
            raise BatchRefused("NOT_REJECTABLE", "only a pending, ready or held lead can be rejected: "
                               + ", ".join(f"#{lead.id} is {lead.state.value}" for lead in blocked))
        for lead_id in lead_ids:
            lead = by_id[lead_id]
            lead.state, lead.rejected_by, lead.rejected_at, lead.reject_reason = (BatchLeadState.REJECTED,
                                                                                  rejected_by, now, reason)
        await self.session.flush()
        return {"rejected": list(lead_ids)}

    # ─── read ────────────────────────────────────────────────────────────

    async def _actual_schedule(self, sequence_id: int) -> Optional[dict]:
        rows = (await self.session.execute(select(SendRecord, Mailbox).join(Mailbox, Mailbox.id == SendRecord.mailbox_id)
                                           .where(SendRecord.sequence_id == sequence_id)
                                           .order_by(SendRecord.step))).all()
        if not rows:
            return None
        box = rows[0][1]
        return {"mailbox_id": box.id, "mailbox": box.address, "display_name": box.display_name,
                "steps": [{"step": r.step, "local_date": r.local_date.isoformat(), "window": r.window_label,
                           "scheduled_for": iso(r.scheduled_for), "state": r.state.value,
                           "approved_by": r.approved_by, "approved_at": iso(r.approved_at)} for r, _ in rows]}

    async def lead_dict(self, lead: OutreachBatchLead) -> dict:
        schedule = await self._actual_schedule(lead.sequence_id) if lead.sequence_id else None
        return {
            "id": lead.id, "position": lead.position, "eligibility_id": lead.eligibility_id,
            "business_id": lead.business_id, "business_name": (lead.evidence or {}).get("business_name"),
            "recipient_email": lead.recipient_email, "state": lead.state.value,
            "hold_reasons": list(lead.hold_reasons or []), "hold_detail": list(lead.hold_detail or []),
            "subject": lead.subject, "texts": {"t1": lead.text_1, "t2": lead.text_2, "t3": lead.text_3},
            "evidence": lead.evidence, "sender_name": lead.sender_name,
            "schedule": schedule or lead.plan, "schedule_kind": "scheduled" if schedule else "proposed",
            "writer": lead.writer_detail, "written_at": iso(lead.written_at),
            "sequence_id": lead.sequence_id, "approved_by": lead.approved_by, "approved_at": iso(lead.approved_at),
            "approval_refusal": lead.approval_refusal, "rejected_by": lead.rejected_by,
            "rejected_at": iso(lead.rejected_at), "reject_reason": lead.reject_reason,
        }

    @staticmethod
    def _summary(batch: OutreachBatch, leads: list[OutreachBatchLead]) -> dict:
        counts: dict[str, int] = defaultdict(int)
        for lead in leads:
            counts[lead.state.value] += 1
        return {"id": batch.id, "send_date": batch.send_date.isoformat(), "send_date_text": day_text(batch.send_date),
                "created_by": batch.created_by, "created_at": iso(batch.created_at), "writer_model": batch.writer_model,
                "template_version": batch.template_version, "status": batch_status(leads),
                "writing_active": batch.id in RUNNING, "total": len(leads), "counts": dict(sorted(counts.items()))}

    async def detail(self, batch_id: int) -> dict:
        batch, leads = await self._batch_and_leads(batch_id)
        return {**self._summary(batch, leads), "leads": [await self.lead_dict(lead) for lead in leads]}

    async def list_batches(self, limit: int = 20) -> dict:
        batches = (await self.session.execute(select(OutreachBatch).order_by(OutreachBatch.id.desc()).limit(limit))
                   ).scalars().all()
        items = []
        for batch in batches:
            leads = (await self.session.execute(select(OutreachBatchLead).where(
                OutreachBatchLead.batch_id == batch.id))).scalars().all()
            items.append(self._summary(batch, list(leads)))
        return {"items": items}
