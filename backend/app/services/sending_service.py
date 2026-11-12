"""
Email engine v2, phase E2 - sending core service: mailboxes, ramp, pause flags, capacity, sequences, schedule,
moving missed messages, and resolving UNCERTAIN submissions. The pause / stop rules that react to bounces and
complaints live in delivery_rules_service.py; the sender loop in outreach_worker.py.

Nothing here sends mail. Every method takes `now` so tests run on a fake clock.
"""

from collections import defaultdict
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from typing import Optional

from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.config import Settings
from backend.app.engines.sending import scheduler as sched
from backend.app.engines.sending.message import new_message_id, reply_subject
from backend.app.engines.sending.pause_rules import Reason
from backend.app.engines.sending.smtp import mailbox_password, password_variable
from backend.app.engines.sending.tokens import email_hash, usable_secret
from backend.app.engines.sending.suppression_client import valid_base_url
from backend.app.models.business import Business
from backend.app.models.eligibility import EmailCapture, EmailEligibility
from backend.app.models.sending import (
    CAPACITY_STATES,
    STOPPED_STATES,
    SUBMITTED_STATES,
    EmailSequence,
    Mailbox,
    PauseFlag,
    PauseLevel,
    PauseScope,
    RampSetting,
    SendKind,
    SendRecord,
    SendState,
    SequenceState,
    TlsMode,
)

aware = sched.aware
PLAN_HORIZON_DAYS = sched.STEP_LATEST_OFFSET[3] + 1   # capacity read ahead for an admission (Day 1 .. Day 21)


class ServiceError(Exception):
    status = 400


class NotFound(ServiceError):
    status = 404


class Conflict(ServiceError):
    status = 409


@dataclass
class SendingConfig:
    """What the sending core needs from settings. Tests build it directly (never from a real .env)."""

    api_key: Optional[str]
    signing_secret: Optional[str]
    base_url: Optional[str]
    sender_name: Optional[str]
    reply_email: Optional[str]
    postal_address: Optional[str]

    @classmethod
    def from_settings(cls, settings: Settings) -> "SendingConfig":
        return cls(settings.OUTREACH_API_KEY, settings.OUTREACH_SIGNING_SECRET, settings.OUTREACH_PUBLIC_BASE_URL,
                   settings.SITEBLITZ_SENDER_NAME, settings.SITEBLITZ_REPLY_EMAIL, settings.SITEBLITZ_POSTAL_ADDRESS)

    def missing_outreach(self) -> list[str]:
        """Shared-with-the-website values that are unset (a secret shorter than 32 characters counts as unset)."""
        missing = []
        if usable_secret(self.api_key) is None:
            missing.append("OUTREACH_API_KEY")
        if usable_secret(self.signing_secret) is None:
            missing.append("OUTREACH_SIGNING_SECRET")
        if valid_base_url(self.base_url) is None:
            missing.append("OUTREACH_PUBLIC_BASE_URL")
        return missing

    def missing_company_facts(self) -> list[str]:
        """The email signature facts (docs/outreach/company-facts.md): blank = HOLD COMPANY_FACTS_MISSING."""
        values = {"SITEBLITZ_SENDER_NAME": self.sender_name, "SITEBLITZ_REPLY_EMAIL": self.reply_email,
                  "SITEBLITZ_POSTAL_ADDRESS": self.postal_address}
        return [name for name, value in values.items() if not (value or "").strip()]


def iso(moment: Optional[datetime]) -> Optional[str]:
    return aware(moment).isoformat() if moment else None


def idempotency_key(sequence_id: int, step: int) -> str:
    return f"seq:{sequence_id}:step:{step}"


def record_dict(record: SendRecord, business_name: Optional[str] = None, mailbox: Optional[str] = None) -> dict:
    return {
        "id": record.id, "kind": record.kind.value, "sequence_id": record.sequence_id, "step": record.step,
        "idempotency_key": record.idempotency_key, "mailbox_id": record.mailbox_id, "mailbox": mailbox,
        "business_name": business_name, "recipient_email": record.recipient_email,
        "message_id": record.message_id, "subject": record.subject, "content_version": record.content_version,
        "has_body": bool(record.body), "local_date": record.local_date.isoformat(), "window": record.window_label,
        "scheduled_for": iso(record.scheduled_for), "state": record.state.value, "hold_reason": record.hold_reason,
        "cancel_reason": record.cancel_reason, "attempts": record.attempts, "smtp_code": record.smtp_code,
        "smtp_status": record.smtp_status, "smtp_response": record.smtp_response,
        "submitted_at": iso(record.submitted_at), "accepted_at": iso(record.accepted_at),
        "approved_at": iso(record.approved_at), "approved_by": record.approved_by,
        "resolved_at": iso(record.resolved_at), "resolved_by": record.resolved_by,
        "resolution_note": record.resolution_note,
    }


def pause_dict(flag: PauseFlag) -> dict:
    return {"id": flag.id, "scope": flag.scope.value, "scope_value": flag.scope_value, "level": flag.level.value,
            "reason_code": flag.reason_code, "detail": flag.detail, "created_by": flag.created_by,
            "created_at": iso(flag.created_at), "active": flag.cleared_at is None,
            "cleared_at": iso(flag.cleared_at), "cleared_by": flag.cleared_by, "clear_note": flag.clear_note}


def mailbox_dict(box: Mailbox) -> dict:
    # Never the password: only whether MAILBOX_<SLUG>_PASSWORD is set.
    return {"id": box.id, "slug": box.slug, "address": box.address, "display_name": box.display_name,
            "from_header": f"\"{box.display_name}, SiteBlitz\" <{box.address}>", "domain": box.domain,
            "enabled": box.enabled, "disabled_reason": box.disabled_reason,
            "smtp": {"host": box.smtp_host, "port": box.smtp_port, "tls": box.smtp_tls.value},
            "imap": {"host": box.imap_host, "port": box.imap_port,
                     "tls": box.imap_tls.value if box.imap_tls else None},
            "username": box.username, "password_variable": password_variable(box.slug),
            "password_configured": mailbox_password(box.slug) is not None}


class SendingService:
    def __init__(self, session: AsyncSession, config: SendingConfig):
        self.session = session
        self.config = config

    @staticmethod
    def _now(now: Optional[datetime]) -> datetime:
        return aware(now) if now else datetime.now(timezone.utc)

    # ─── mailboxes ───────────────────────────────────────────────────────

    async def list_mailboxes(self) -> list[dict]:
        rows = (await self.session.execute(select(Mailbox).order_by(Mailbox.id))).scalars().all()
        return [mailbox_dict(b) for b in rows]

    async def upsert_mailbox(self, data: dict) -> dict:
        """Add a mailbox, or change / disable an existing one (matched by slug). The password stays in .env."""
        box = (await self.session.execute(select(Mailbox).where(Mailbox.slug == data["slug"]))).scalar_one_or_none()
        clash = (await self.session.execute(select(Mailbox).where(Mailbox.address == data["address"]))
                 ).scalar_one_or_none()
        if clash is not None and (box is None or clash.id != box.id):
            raise Conflict(f"{data['address']} already belongs to mailbox {clash.slug}")
        if box is None:
            box = Mailbox(slug=data["slug"])
            self.session.add(box)
        for key in ("address", "display_name", "smtp_host", "smtp_port", "imap_host", "imap_port", "username",
                    "enabled"):
            setattr(box, key, data[key])
        box.smtp_tls = TlsMode(data["smtp_tls"])
        box.imap_tls = TlsMode(data["imap_tls"]) if data.get("imap_tls") else None
        box.domain = data["address"].rsplit("@", 1)[1]
        box.disabled_reason = None if data["enabled"] else (data.get("disabled_reason") or "disabled")
        await self.session.flush()
        return mailbox_dict(box)

    async def enabled_mailboxes(self) -> list[Mailbox]:
        return list((await self.session.execute(
            select(Mailbox).where(Mailbox.enabled.is_(True)).order_by(Mailbox.id))).scalars().all())

    # ─── ramp ────────────────────────────────────────────────────────────

    async def current_ramp(self) -> Optional[RampSetting]:
        return (await self.session.execute(
            select(RampSetting).order_by(RampSetting.changed_at.desc(), RampSetting.id.desc()).limit(1))
        ).scalar_one_or_none()

    async def daily_new_limit(self) -> int:
        row = await self.current_ramp()
        return row.daily_new_limit if row else 0

    async def ramp_info(self) -> dict:
        rows = (await self.session.execute(
            select(RampSetting).order_by(RampSetting.changed_at.desc(), RampSetting.id.desc()))).scalars().all()
        current = rows[0] if rows else None
        return {"stage": current.stage if current else 0,
                "daily_new_limit": current.daily_new_limit if current else 0,
                "started": current is not None and current.stage > 0,
                "limits_by_stage": {str(k): v for k, v in sched.RAMP_LIMITS.items()},
                "history": [{"stage": r.stage, "daily_new_limit": r.daily_new_limit, "changed_by": r.changed_by,
                             "note": r.note, "changed_at": iso(r.changed_at)} for r in rows]}

    async def set_ramp(self, stage: int, changed_by: str, note: str, now: Optional[datetime] = None) -> dict:
        """Spec row 10: each step up needs the founder's yes, so the stage moves up by at most one per call; going
        down (or back to 0 = stop new contacts) is always allowed. Limits are the locked 10 / 15 / 20 / 20."""
        now = self._now(now)
        if stage not in sched.RAMP_LIMITS:
            raise ServiceError(f"stage must be one of {sorted(sched.RAMP_LIMITS)}")
        current = await self.current_ramp()
        current_stage = current.stage if current else 0
        if stage > current_stage + 1:
            raise Conflict(f"the ramp moves up one stage at a time (now {current_stage}, asked {stage})")
        self.session.add(RampSetting(stage=stage, daily_new_limit=sched.ramp_limit(stage), changed_by=changed_by,
                                     note=note, changed_at=now))
        await self.session.flush()
        return await self.ramp_info()

    # ─── pause flags ─────────────────────────────────────────────────────

    async def raise_pause(self, scope: PauseScope, reason: str, value: str = "", level: PauseLevel = PauseLevel.PAUSE,
                          detail: Optional[str] = None, created_by: str = "system",
                          now: Optional[datetime] = None) -> PauseFlag:
        """Idempotent: an active flag with the same scope, value, level and reason is returned, not duplicated."""
        existing = (await self.session.execute(select(PauseFlag).where(
            PauseFlag.cleared_at.is_(None), PauseFlag.scope == scope, PauseFlag.scope_value == value,
            PauseFlag.level == level, PauseFlag.reason_code == reason))).scalars().first()
        if existing is not None:
            return existing
        flag = PauseFlag(scope=scope, scope_value=value, level=level, reason_code=reason,
                         detail=(detail or "")[:2000] or None, created_by=created_by, created_at=self._now(now))
        self.session.add(flag)
        await self.session.flush()
        return flag

    async def active_pauses(self) -> list[PauseFlag]:
        return list((await self.session.execute(select(PauseFlag).where(PauseFlag.cleared_at.is_(None))
                                                .order_by(PauseFlag.id))).scalars().all())

    async def list_pauses(self, active: Optional[bool] = None) -> list[dict]:
        stmt = select(PauseFlag).order_by(PauseFlag.id.desc())
        if active is True:
            stmt = stmt.where(PauseFlag.cleared_at.is_(None))
        elif active is False:
            stmt = stmt.where(PauseFlag.cleared_at.isnot(None))
        return [pause_dict(f) for f in (await self.session.execute(stmt.limit(500))).scalars().all()]

    async def unresolved_uncertain(self) -> int:
        return (await self.session.execute(select(func.count()).select_from(SendRecord).where(
            SendRecord.state == SendState.UNCERTAIN))).scalar_one()

    async def clear_pause(self, pause_id: int, cleared_by: str, note: str, now: Optional[datetime] = None) -> dict:
        flag = await self.session.get(PauseFlag, pause_id)
        if flag is None:
            raise NotFound(f"pause {pause_id} not found")
        if flag.cleared_at is not None:
            raise Conflict(f"pause {pause_id} was already cleared")
        if flag.reason_code == Reason.SEND_RESULT_UNKNOWN and await self.unresolved_uncertain():
            raise Conflict("resolve every UNCERTAIN send record first (POST /send-records/{id}/resolve)")
        flag.cleared_at, flag.cleared_by, flag.clear_note = self._now(now), cleared_by, note
        await self.session.flush()
        return pause_dict(flag)

    async def _clear_reason(self, reason: str, cleared_by: str, note: str, now: datetime,
                            scope: Optional[PauseScope] = None) -> int:
        stmt = select(PauseFlag).where(PauseFlag.cleared_at.is_(None), PauseFlag.reason_code == reason)
        if scope is not None:
            stmt = stmt.where(PauseFlag.scope == scope)
        flags = (await self.session.execute(stmt)).scalars().all()
        for flag in flags:
            flag.cleared_at, flag.cleared_by, flag.clear_note = now, cleared_by, note
        await self.session.flush()
        return len(flags)

    @staticmethod
    def blocking(flags: list[PauseFlag], *, step: Optional[int], mailbox: Optional[Mailbox],
                 sequence: Optional[EmailSequence]) -> list[PauseFlag]:
        """The active flags that apply to one message (or, with mailbox / sequence None, to new admissions)."""
        out = []
        for flag in flags:
            if flag.scope == PauseScope.GLOBAL:
                out.append(flag)
            elif flag.scope == PauseScope.NEW_CONTACTS and step == 1:
                out.append(flag)
            elif mailbox is not None and flag.scope == PauseScope.DOMAIN and flag.scope_value == mailbox.domain:
                out.append(flag)
            elif mailbox is not None and flag.scope == PauseScope.MAILBOX and flag.scope_value == str(mailbox.id):
                out.append(flag)
            elif sequence is not None and flag.scope == PauseScope.SOURCE and flag.scope_value == sequence.source:
                out.append(flag)
            elif (sequence is not None and flag.scope == PauseScope.SOURCE_BATCH
                  and flag.scope_value == sequence.source_batch):
                out.append(flag)
        return out

    # ─── capacity ────────────────────────────────────────────────────────

    async def capacity_book(self, start: date, end: date) -> sched.CapacityBook:
        """Reservations on [start, end] by (mailbox, recipient-local day): every record in a capacity state."""
        book = sched.CapacityBook()
        rows = (await self.session.execute(
            select(SendRecord.mailbox_id, SendRecord.local_date, SendRecord.window_label, SendRecord.kind,
                   SendRecord.step)
            .where(SendRecord.local_date >= start, SendRecord.local_date <= end,
                   SendRecord.state.in_(CAPACITY_STATES)))).all()
        for mailbox_id, day, label, kind, step in rows:
            book.add(mailbox_id, day, label, campaign=kind == SendKind.CAMPAIGN,
                     new_contact=kind == SendKind.CAMPAIGN and step == 1)
        return book

    async def submitted_counts(self, mailbox_id: int, day: date) -> dict:
        """Messages that already left (or may have left) a mailbox on one recipient-local day."""
        rows = (await self.session.execute(
            select(SendRecord.kind, func.count()).where(
                SendRecord.mailbox_id == mailbox_id, SendRecord.local_date == day,
                SendRecord.submitted_at.isnot(None),
                SendRecord.state.in_(SUBMITTED_STATES + (SendState.FAILED,)))
            .group_by(SendRecord.kind))).all()
        by_kind = {kind: count for kind, count in rows}
        return {"total": sum(by_kind.values()), "campaign": by_kind.get(SendKind.CAMPAIGN, 0)}

    async def submitted_new_contacts(self, day: date) -> int:
        return (await self.session.execute(select(func.count()).select_from(SendRecord).where(
            SendRecord.kind == SendKind.CAMPAIGN, SendRecord.step == 1, SendRecord.local_date == day,
            SendRecord.submitted_at.isnot(None),
            SendRecord.state.in_(SUBMITTED_STATES + (SendState.FAILED,))))).scalar_one()

    async def capacity(self, day: date) -> dict:
        book = await self.capacity_book(day, day)
        limit = await self.daily_new_limit()
        boxes = (await self.session.execute(select(Mailbox).order_by(Mailbox.id))).scalars().all()
        mailboxes = []
        for box in boxes:
            load = book.load(box.id, day)
            sent = await self.submitted_counts(box.id, day)
            mailboxes.append({
                "mailbox_id": box.id, "address": box.address, "enabled": box.enabled,
                "campaign_reserved": load.campaign, "campaign_limit": sched.CAMPAIGN_DAILY_LIMIT,
                "campaign_free": max(0, sched.CAMPAIGN_DAILY_LIMIT - load.campaign),
                "total_reserved": load.total, "daily_ceiling": sched.MAILBOX_DAILY_CEILING,
                "reply_reserve": sched.REPLY_RESERVE, "by_window": dict(sorted(load.per_window.items())),
                "submitted_total": sent["total"], "submitted_campaign": sent["campaign"]})
        new = book.new_contacts.get(day, 0)
        return {"date": day.isoformat(), "campaign_day": sched.is_campaign_day(day), "mailboxes": mailboxes,
                "new_contacts": {"scheduled": new, "daily_limit": limit, "free": max(0, limit - new)}}

    # ─── sequences ───────────────────────────────────────────────────────

    async def _source_of(self, row: EmailEligibility) -> tuple[str, str]:
        origin = None
        if row.capture_id is not None:
            origin = (await self.session.execute(select(EmailCapture.origin).where(
                EmailCapture.id == row.capture_id))).scalar_one_or_none()
        origin = (origin or "unknown")[:100]
        return origin.split(":", 1)[0], origin

    async def _already_contacted(self, business_id: int, recipient_hash: str) -> bool:
        live = (await self.session.execute(select(EmailSequence.id).where(
            (EmailSequence.business_id == business_id) | (EmailSequence.recipient_hash == recipient_hash),
            EmailSequence.state != SequenceState.CANCELLED).limit(1))).scalar_one_or_none()
        if live is not None:
            return True
        sent = (await self.session.execute(select(SendRecord.id).where(
            SendRecord.recipient_hash == recipient_hash, SendRecord.submitted_at.isnot(None)).limit(1))
        ).scalar_one_or_none()
        return sent is not None

    async def create_sequences(self, send_date: date, items: list[dict], now: Optional[datetime] = None) -> dict:
        """Admit approved, eligible prospects for step 1 on `send_date` (recipient-local). Each item:
        {eligibility_id, subject, body, content_version, approved_by}. Every refusal is returned with a code and
        a message the batch screen (E3) shows as it is."""
        now = self._now(now)
        admitted, refused = [], []

        def refuse(item, code, message):
            refused.append({"eligibility_id": item["eligibility_id"], "code": code, "message": message})

        missing_facts = self.config.missing_company_facts()
        flags = await self.active_pauses()
        admission_blocks = self.blocking(flags, step=1, mailbox=None, sequence=None)
        mailboxes = await self.enabled_mailboxes()
        book = await self.capacity_book(send_date, send_date + timedelta(days=PLAN_HORIZON_DAYS))
        limit = await self.daily_new_limit()
        seen_hashes: set[str] = set()
        for item in items:
            row = await self.session.get(EmailEligibility, item["eligibility_id"])
            if row is None:
                refuse(item, "NOT_FOUND", f"eligibility row {item['eligibility_id']} does not exist")
                continue
            if not row.eligible or row.suppressed:
                refuse(item, "NOT_ELIGIBLE", "not eligible: " + (", ".join(row.hold_reasons or []) or "HOLD"))
                continue
            if missing_facts:
                refuse(item, "COMPANY_FACTS_MISSING", "blank company facts: " + ", ".join(missing_facts))
                continue
            if admission_blocks:
                refuse(item, "PAUSED", "new first contacts are paused: "
                       + ", ".join(f"{f.reason_code} ({f.scope.value})" for f in admission_blocks))
                continue
            business = await self.session.get(Business, row.business_id)
            zone_name, hold = sched.timezone_for_country(row.country or (business.country_code if business else None))
            if hold:
                refuse(item, hold, f"no recipient time zone ({hold}); a default is never assumed")
                continue
            recipient_hash = email_hash(row.email)
            if recipient_hash in seen_hashes or await self._already_contacted(row.business_id, recipient_hash):
                refuse(item, "ALREADY_IN_SEQUENCE", "this business or address already has a sequence")
                continue
            source, batch = await self._source_of(row)
            probe = EmailSequence(source=source, source_batch=batch)
            usable = [b.id for b in mailboxes
                      if not self.blocking(flags, step=1, mailbox=b, sequence=probe)]
            source_blocks = [f for f in flags if f.scope in (PauseScope.SOURCE, PauseScope.SOURCE_BATCH)
                             and f.scope_value in (source, batch)]
            if source_blocks:
                refuse(item, "PAUSED", "this lead source is paused: "
                       + ", ".join(f"{f.reason_code} ({f.scope.value} {f.scope_value})" for f in source_blocks))
                continue
            plan = sched.plan_admission(book, usable, sched.load_zone(zone_name), send_date, now, limit)
            if isinstance(plan, sched.Refusal):
                refuse(item, plan.code, plan.message)
                continue
            seen_hashes.add(recipient_hash)
            box = next(b for b in mailboxes if b.id == plan.mailbox_id)
            sequence = EmailSequence(business_id=row.business_id, eligibility_id=row.id, mailbox_id=box.id,
                                     recipient_email=row.email, recipient_hash=recipient_hash, country=row.country
                                     or (business.country_code if business else None), timezone=zone_name,
                                     source=source, source_batch=batch, current_step=0, state=SequenceState.ACTIVE)
            self.session.add(sequence)
            await self.session.flush()
            records = []
            for step, slot in sorted(plan.slots.items()):
                first = step == 1
                record = SendRecord(
                    kind=SendKind.CAMPAIGN, sequence_id=sequence.id, step=step,
                    idempotency_key=idempotency_key(sequence.id, step), mailbox_id=box.id,
                    recipient_email=row.email, recipient_hash=recipient_hash,
                    message_id=new_message_id(box.domain),
                    subject=item["subject"] if first else reply_subject(item["subject"]),
                    body=item["body"] if first else None,
                    content_version=item.get("content_version") if first else None,
                    scheduled_for=slot.scheduled_for, local_date=slot.local_date, window_label=slot.window_label,
                    window_start=slot.window_start, window_end=slot.window_end, state=SendState.SCHEDULED,
                    approved_at=now if first else None, approved_by=item["approved_by"] if first else None,
                    attempts=0)
                self.session.add(record)
                records.append(record)
            await self.session.flush()
            admitted.append({"eligibility_id": row.id, "sequence_id": sequence.id, "business_id": row.business_id,
                             "mailbox_id": box.id, "records": [record_dict(r) for r in records]})
        return {"send_date": send_date.isoformat(), "admitted": admitted, "refused": refused,
                "daily_new_limit": limit}

    async def approve_follow_up(self, record_id: int, body: str, approved_by: str,
                                content_version: Optional[str], now: Optional[datetime] = None) -> dict:
        """Steps 2 and 3 are reserved without text; the writer's text and the founder's approval arrive later."""
        record = await self.session.get(SendRecord, record_id)
        if record is None:
            raise NotFound(f"send record {record_id} not found")
        if record.step not in (2, 3) or record.state != SendState.SCHEDULED:
            raise Conflict("only a SCHEDULED step 2 or 3 can get its text and approval here")
        record.body, record.approved_by, record.approved_at = body, approved_by, self._now(now)
        record.content_version = content_version
        record.hold_reason = None
        await self.session.flush()
        return record_dict(record)

    async def stop_sequence(self, sequence_id: int, state: SequenceState, reason: str,
                            now: Optional[datetime] = None) -> dict:
        """E4 calls this for replies (STOPPED_REPLY), out-of-office (PAUSED_OOO) and suppressions. Stopping cancels
        every message not yet submitted; PAUSED_OOO keeps them (the worker holds them while paused)."""
        now = self._now(now)
        sequence = await self.session.get(EmailSequence, sequence_id)
        if sequence is None:
            raise NotFound(f"sequence {sequence_id} not found")
        if sequence.state in STOPPED_STATES and state != sequence.state:
            return {"sequence_id": sequence_id, "state": sequence.state.value, "cancelled": 0}
        sequence.state, sequence.stop_reason = state, reason[:300]
        cancelled = 0
        if state in STOPPED_STATES:
            sequence.stopped_at = now
            cancelled = (await self.session.execute(
                update(SendRecord).where(SendRecord.sequence_id == sequence_id,
                                         SendRecord.state == SendState.SCHEDULED)
                .values(state=SendState.CANCELLED, cancel_reason=f"{state.value}: {reason}"[:300])
                .execution_options(synchronize_session="fetch"))).rowcount
        await self.session.flush()
        return {"sequence_id": sequence_id, "state": sequence.state.value, "cancelled": cancelled}

    async def schedule(self, day: date) -> dict:
        rows = (await self.session.execute(
            select(SendRecord, Business.name, Mailbox.address)
            .join(EmailSequence, EmailSequence.id == SendRecord.sequence_id, isouter=True)
            .join(Business, Business.id == EmailSequence.business_id, isouter=True)
            .join(Mailbox, Mailbox.id == SendRecord.mailbox_id)
            .where(SendRecord.local_date == day)
            .order_by(SendRecord.scheduled_for, SendRecord.id))).all()
        items = [record_dict(r, name, address) for r, name, address in rows]
        counts: dict[str, int] = defaultdict(int)
        for item in items:
            counts[item["state"]] += 1
        return {"date": day.isoformat(), "items": items, "counts": dict(sorted(counts.items()))}

    # ─── moving missed messages ──────────────────────────────────────────

    async def reschedule_overdue(self, now: Optional[datetime] = None) -> dict:
        """A SCHEDULED message whose window has passed (the worker was not running, a hold, capacity) moves to the
        next permitted window with free capacity on the SAME mailbox; caps are never exceeded to catch up. A moved
        step 1 must also fit the ramp on its new day; later steps keep their Day 6 / Day 14 distance from step 1."""
        now = self._now(now)
        overdue = (await self.session.execute(
            select(SendRecord).where(SendRecord.state == SendState.SCHEDULED, SendRecord.kind == SendKind.CAMPAIGN,
                                     SendRecord.window_end <= now)
            .order_by(SendRecord.sequence_id, SendRecord.step))).scalars().all()
        if not overdue:
            return {"moved": 0, "held": 0}
        start = min(r.local_date for r in overdue)
        book = await self.capacity_book(start - timedelta(days=1),
                                        now.date() + timedelta(days=sched.RESCHEDULE_SEARCH_DAYS + 30))
        limit = await self.daily_new_limit()
        moved = held = 0
        for record in overdue:
            if record.state != SendState.SCHEDULED or aware(record.window_end) > now:
                continue   # already moved as part of its sequence
            sequence = await self.session.get(EmailSequence, record.sequence_id)
            zone = sched.load_zone(sequence.timezone if sequence else None)
            if zone is None:
                record.hold_reason = sched.HoldCode.TIMEZONE_MISSING
                held += 1
                continue
            records = (await self.session.execute(select(SendRecord).where(
                SendRecord.sequence_id == record.sequence_id).order_by(SendRecord.step))).scalars().all()
            if not await self._move(book, record, records, zone, now, limit):
                record.hold_reason = "NO_CAPACITY"
                held += 1
                continue
            moved += 1
            for later in records:   # keep the order and the Day 6 / 14 distances
                if later.step > record.step and later.state == SendState.SCHEDULED:
                    step1 = next(r for r in records if r.step == 1)
                    earliest = max(sched.due_date(step1.local_date, later.step),
                                   max(r.local_date for r in records if r.step < later.step) + timedelta(days=1))
                    if later.local_date < earliest:
                        await self._move(book, later, records, zone, now, limit, earliest=earliest)
        await self.session.flush()
        return {"moved": moved, "held": held}

    async def _move(self, book: sched.CapacityBook, record: SendRecord, records: list[SendRecord], zone,
                    now: datetime, limit: int, earliest: Optional[date] = None) -> bool:
        today = sched.local_date(now, zone)
        if earliest is None:
            earliest = today
            if record.step and record.step > 1:
                step1 = next(r for r in records if r.step == 1)
                previous = max(r.local_date for r in records if r.step < record.step)
                earliest = max(today, sched.due_date(step1.local_date, record.step), previous + timedelta(days=1))
        earliest = max(earliest, today)
        book.remove(record.mailbox_id, record.local_date, record.window_label, new_contact=record.step == 1)
        day = earliest
        last = earliest + timedelta(days=sched.RESCHEDULE_SEARCH_DAYS)
        while day <= last:
            slot = sched.find_slot(book, record.mailbox_id, zone, day, last, not_before=now)
            if slot is None:
                break
            if record.step == 1 and book.new_contacts.get(slot.local_date, 0) >= limit:
                day = slot.local_date + timedelta(days=1)
                continue
            book.add(record.mailbox_id, slot.local_date, slot.window_label, new_contact=record.step == 1)
            record.local_date, record.window_label = slot.local_date, slot.window_label
            record.window_start, record.window_end, record.scheduled_for = (slot.window_start, slot.window_end,
                                                                            slot.scheduled_for)
            record.hold_reason = None
            return True
        book.add(record.mailbox_id, record.local_date, record.window_label, new_contact=record.step == 1)
        return False

    # ─── UNCERTAIN results ───────────────────────────────────────────────

    async def resolve_uncertain(self, record_id: int, outcome: str, resolved_by: str, note: str,
                                now: Optional[datetime] = None) -> dict:
        """A person decides what happened to an UNCERTAIN submission (e.g. after looking at the Sent folder or the
        provider's log). Never automatic. When no UNCERTAIN record is left, the SEND_RESULT_UNKNOWN pause clears."""
        now = self._now(now)
        record = await self.session.get(SendRecord, record_id)
        if record is None:
            raise NotFound(f"send record {record_id} not found")
        if record.state != SendState.UNCERTAIN:
            raise Conflict(f"send record {record_id} is {record.state.value}, not UNCERTAIN")
        record.resolved_at, record.resolved_by, record.resolution_note = now, resolved_by, note
        sequence = await self.session.get(EmailSequence, record.sequence_id) if record.sequence_id else None
        if outcome == "ACCEPTED":
            record.state = SendState.ACCEPTED
            record.accepted_at = record.submitted_at   # the exact acceptance time is unknown
            if sequence is not None:
                await self.mark_step_accepted(sequence, record, now)
        else:
            record.state = SendState.FAILED
            if sequence is not None:
                await self.stop_sequence(sequence.id, SequenceState.CANCELLED,
                                         f"step {record.step} resolved as FAILED: {note}", now)
        await self.session.flush()
        if not await self.unresolved_uncertain():
            await self._clear_reason(Reason.SEND_RESULT_UNKNOWN, resolved_by,
                                     f"every UNCERTAIN record resolved (last: {record_id})", now)
        return record_dict(record)

    async def mark_step_accepted(self, sequence: EmailSequence, record: SendRecord, now: datetime) -> None:
        sequence.current_step = max(sequence.current_step or 0, record.step or 0)
        if record.step == 3 and sequence.state == SequenceState.ACTIVE:
            sequence.state, sequence.stopped_at = SequenceState.COMPLETED, now
            sequence.stop_reason = "all three steps accepted"
