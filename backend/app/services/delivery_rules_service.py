"""
Email engine v2, phase E2 - the automatic pause / stop rules applied to the database (spec row 11; the table is in
backend/app/engines/sending/pause_rules.py). E2 calls these from the worker (SMTP refusals, unknown results,
suppression service down, integrity audit); E4 calls them for DSNs read over IMAP (record_bounce), complaints,
"stop" replies, inbox reconciliation and the interested-reply backlog.

Suppressions go to the website FIRST (POST /api/outreach/suppressions), then to the local display mirror. If the
website write fails, the global pause SUPPRESSION_WRITE_FAILED keeps every send blocked until a person clears it.
"""

from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import func, select

from backend.app.engines.sending import dsn
from backend.app.engines.sending import pause_rules as rules
from backend.app.engines.sending.pause_rules import Reason
from backend.app.engines.sending.scheduler import COUNTRY_TIMEZONES, load_zone
from backend.app.engines.sending.suppression_client import SuppressionClient, SuppressionUnavailable
from backend.app.models.sending import (
    SUBMITTED_STATES,
    DeliveryEvent,
    DeliveryEventKind,
    EmailSequence,
    Mailbox,
    PauseLevel,
    PauseScope,
    SendKind,
    SendRecord,
    SendState,
    SequenceState,
    SuppressionMirror,
)
from backend.app.services.sending_service import SendingService, aware

FOUNDER_ZONE = COUNTRY_TIMEZONES["IN"]   # the founders work in India time (reply backlog business days)
# E4 (reply_service.py): idempotency-key prefix of the optional "stop" confirmation reply.
STOP_CONFIRMATION_KEY = "reply:stop-confirmation:"


def smtp_kind(status: Optional[str], response: Optional[str], code: Optional[int]) -> str:
    """HARD / POLICY / SOFT / UNKNOWN for an SMTP refusal, with the same rules as the DSN parser."""
    kind = dsn.classify_status(status)
    if kind is None:
        kind = dsn.classify_text(response or "", code)
    return kind


class DeliveryRulesService:
    def __init__(self, sending: SendingService, client: Optional[SuppressionClient]):
        self.sending = sending
        self.session = sending.session
        self.client = client

    # ─── helpers ─────────────────────────────────────────────────────────

    async def _context(self, record: Optional[SendRecord]):
        sequence = await self.session.get(EmailSequence, record.sequence_id) if record and record.sequence_id else None
        mailbox = await self.session.get(Mailbox, record.mailbox_id) if record else None
        return sequence, mailbox

    async def _event(self, kind: DeliveryEventKind, record: Optional[SendRecord], now: datetime, origin: str,
                     recipient_hash: Optional[str] = None, credible: bool = True, status: Optional[str] = None,
                     detail: Optional[dict] = None) -> DeliveryEvent:
        sequence, mailbox = await self._context(record)
        event = DeliveryEvent(kind=kind, send_record_id=record.id if record else None,
                              recipient_hash=recipient_hash or (record.recipient_hash if record else None),
                              mailbox_id=mailbox.id if mailbox else None,
                              sending_domain=mailbox.domain if mailbox else None,
                              source=sequence.source if sequence else None,
                              source_batch=sequence.source_batch if sequence else None,
                              credible=credible, smtp_status=status, detail=detail, origin=origin,
                              occurred_at=now)
        self.session.add(event)
        await self.session.flush()
        return event

    async def suppress(self, recipient_hash: str, reason: str, source: str, now: datetime) -> bool:
        """Website first, then the display mirror. False (and a global pause) when the website write failed."""
        ok = True
        try:
            if self.client is None:
                raise SuppressionUnavailable("no suppression client configured")
            await self.client.add(recipient_hash, reason, source)
        except (SuppressionUnavailable, ValueError) as exc:
            ok = False
            await self.sending.raise_pause(PauseScope.GLOBAL, Reason.SUPPRESSION_WRITE_FAILED,
                                           detail=f"{reason} for {recipient_hash[:12]}...: {exc}", now=now)
        row = (await self.session.execute(select(SuppressionMirror).where(
            SuppressionMirror.email_hash == recipient_hash))).scalar_one_or_none()
        if row is None:
            self.session.add(SuppressionMirror(email_hash=recipient_hash, reason=reason, suppressed_at=now,
                                               fetched_at=now))
        await self.session.flush()
        return ok

    async def _stop(self, record: Optional[SendRecord], state: SequenceState, reason: str, now: datetime) -> None:
        if record is not None and record.sequence_id:
            await self.sending.stop_sequence(record.sequence_id, state, reason, now)

    async def find_record(self, message_id: Optional[str], recipient: Optional[str]) -> Optional[SendRecord]:
        if message_id:
            record = (await self.session.execute(select(SendRecord).where(
                SendRecord.message_id == message_id.strip()))).scalar_one_or_none()
            if record is not None:
                return record
        if recipient:
            from backend.app.engines.sending.tokens import email_hash
            return (await self.session.execute(select(SendRecord).where(
                SendRecord.recipient_hash == email_hash(recipient), SendRecord.submitted_at.isnot(None))
                .order_by(SendRecord.submitted_at.desc()).limit(1))).scalars().first()
        return None

    # ─── rules ───────────────────────────────────────────────────────────

    async def record_hard_bounce(self, record: SendRecord, origin: str, now: datetime,
                                 status: Optional[str] = None, detail: Optional[dict] = None) -> dict:
        """First hard bounce: suppress the address (website) and pause that source batch. Then: 2 bounced recipients
        within the latest 100 distinct recipients of that source = stop the source."""
        already = (await self.session.execute(select(DeliveryEvent.id).where(
            DeliveryEvent.kind == DeliveryEventKind.HARD_BOUNCE, DeliveryEvent.send_record_id == record.id))
        ).scalars().first()
        if already is not None:
            return {"duplicate": True}
        event = await self._event(DeliveryEventKind.HARD_BOUNCE, record, now, origin, status=status, detail=detail)
        await self.suppress(record.recipient_hash, "hard_bounce", f"{origin}:send_record:{record.id}", now)
        await self._stop(record, SequenceState.STOPPED_BOUNCE, f"hard bounce {status or ''}".strip(), now)
        actions = []
        if event.source_batch:
            await self.sending.raise_pause(PauseScope.SOURCE_BATCH, Reason.HARD_BOUNCE, event.source_batch,
                                           detail=f"hard bounce on send record {record.id}", now=now)
            actions.append(f"PAUSE SOURCE_BATCH {event.source_batch}")
        if event.source and await self._source_bounce_stop(event.source):
            await self.sending.raise_pause(PauseScope.SOURCE, Reason.HARD_BOUNCE_RATE, event.source,
                                           level=PauseLevel.STOP,
                                           detail="2 hard-bounced recipients within the latest 100", now=now)
            actions.append(f"STOP SOURCE {event.source}")
        return {"duplicate": False, "actions": actions}

    async def _source_bounce_stop(self, source: str) -> bool:
        recent = (await self.session.execute(
            select(SendRecord.recipient_hash)
            .join(EmailSequence, EmailSequence.id == SendRecord.sequence_id)
            .where(EmailSequence.source == source, SendRecord.submitted_at.isnot(None))
            .order_by(SendRecord.submitted_at.desc(), SendRecord.id.desc()))).scalars().all()
        latest = rules.latest_distinct(recent)
        bounced = set((await self.session.execute(select(DeliveryEvent.recipient_hash).where(
            DeliveryEvent.kind == DeliveryEventKind.HARD_BOUNCE, DeliveryEvent.source == source))).scalars().all())
        return rules.hard_bounce_stop(latest, bounced)

    async def record_policy_rejection(self, record: SendRecord, origin: str, now: datetime,
                                      status: Optional[str] = None, detail: Optional[dict] = None) -> dict:
        """1 policy / authentication rejection: pause that sending domain. 3 within 24 h: stop it. The address is
        NOT suppressed (a policy block says nothing about the mailbox)."""
        event = await self._event(DeliveryEventKind.POLICY_REJECTION, record, now, origin, status=status,
                                  detail=detail)
        domain = event.sending_domain or ""
        await self.sending.raise_pause(PauseScope.DOMAIN, Reason.POLICY_REJECTION, domain,
                                       detail=f"policy rejection {status or ''} on send record {record.id}", now=now)
        times = (await self.session.execute(select(DeliveryEvent.occurred_at).where(
            DeliveryEvent.kind == DeliveryEventKind.POLICY_REJECTION, DeliveryEvent.sending_domain == domain))
        ).scalars().all()
        actions = [f"PAUSE DOMAIN {domain}"]
        if rules.policy_stop(times, now):
            await self.sending.raise_pause(PauseScope.DOMAIN, Reason.POLICY_REJECTIONS_24H, domain,
                                           level=PauseLevel.STOP, detail="3 policy rejections within 24 h", now=now)
            actions.append(f"STOP DOMAIN {domain}")
        return {"actions": actions}

    async def record_complaint(self, record: Optional[SendRecord], recipient_hash: str, credible: bool, origin: str,
                               now: datetime, detail: Optional[dict] = None) -> dict:
        """The address is always suppressed. A credible complaint pauses everything; 2 credible complaints within
        30 days stop the campaign."""
        await self._event(DeliveryEventKind.COMPLAINT, record, now, origin, recipient_hash=recipient_hash,
                          credible=credible, detail=detail)
        await self.suppress(recipient_hash, "complaint", f"{origin}:complaint", now)
        await self._stop(record, SequenceState.STOPPED_SUPPRESSED, "complaint", now)
        actions = []
        if credible:
            await self.sending.raise_pause(PauseScope.GLOBAL, Reason.COMPLAINT, detail="credible complaint", now=now)
            actions.append("PAUSE GLOBAL")
            times = (await self.session.execute(select(DeliveryEvent.occurred_at).where(
                DeliveryEvent.kind == DeliveryEventKind.COMPLAINT, DeliveryEvent.credible.is_(True)))).scalars().all()
            if rules.complaint_stop(times, now):
                await self.sending.raise_pause(PauseScope.GLOBAL, Reason.COMPLAINTS_30D, level=PauseLevel.STOP,
                                               detail="2 credible complaints within 30 days", now=now)
                actions.append("STOP GLOBAL")
        return {"actions": actions}

    async def record_bounce(self, parsed: dsn.BounceResult, origin: str = "dsn",
                            now: Optional[datetime] = None) -> dict:
        """E4 entry point for a DSN / bounce read over IMAP."""
        now = aware(now) if now else datetime.now(timezone.utc)
        if not parsed.is_bounce:
            return {"matched": False, "kind": None}
        record = await self.find_record(parsed.original_message_id, parsed.recipient)
        if record is None:
            return {"matched": False, "kind": parsed.kind}
        detail = {"diagnostic": parsed.diagnostic, "smtp_code": parsed.smtp_code}
        if parsed.kind == dsn.HARD:
            result = await self.record_hard_bounce(record, origin, now, parsed.status, detail)
        elif parsed.kind == dsn.POLICY:
            result = await self.record_policy_rejection(record, origin, now, parsed.status, detail)
        else:
            kind = DeliveryEventKind.SOFT_BOUNCE if parsed.kind == dsn.SOFT else DeliveryEventKind.UNKNOWN_BOUNCE
            await self._event(kind, record, now, origin, status=parsed.status, detail=detail)
            result = {"actions": []}
        return {"matched": True, "send_record_id": record.id, "kind": parsed.kind, **result}

    async def record_smtp_refusal(self, record: SendRecord, now: datetime) -> dict:
        kind = smtp_kind(record.smtp_status, record.smtp_response, record.smtp_code)
        detail = {"smtp_code": record.smtp_code, "response": (record.smtp_response or "")[:500]}
        if kind == dsn.HARD:
            return await self.record_hard_bounce(record, "smtp", now, record.smtp_status, detail)
        if kind == dsn.POLICY:
            result = await self.record_policy_rejection(record, "smtp", now, record.smtp_status, detail)
        else:
            await self._event(DeliveryEventKind.UNKNOWN_BOUNCE, record, now, "smtp", status=record.smtp_status,
                              detail=detail)
            result = {"actions": []}
        await self._stop(record, SequenceState.CANCELLED, f"step {record.step} refused: {record.smtp_code}", now)
        return result

    # ─── state that blocks everything ────────────────────────────────────

    async def record_suppression_unavailable(self, detail: str, now: datetime) -> None:
        await self.sending.raise_pause(PauseScope.GLOBAL, Reason.SUPPRESSION_UNAVAILABLE, detail=detail, now=now)

    async def record_reconciliation_incomplete(self, detail: str, now: datetime) -> None:
        """E4: the inboxes were not fully read before / during a sending session."""
        await self.sending.raise_pause(PauseScope.GLOBAL, Reason.INBOX_NOT_RECONCILED, detail=detail, now=now)

    async def record_send_result_unknown(self, record: SendRecord, now: datetime) -> None:
        await self.sending.raise_pause(PauseScope.GLOBAL, Reason.SEND_RESULT_UNKNOWN,
                                       detail=f"send record {record.id} is UNCERTAIN", now=now)

    async def record_integrity_incident(self, reason: str, detail: str, now: datetime) -> None:
        if reason not in (Reason.SUPPRESSED_SEND, Reason.DUPLICATE_SEND, Reason.UNAPPROVED_SEND):
            raise ValueError(f"unknown integrity incident {reason}")
        await self.sending.raise_pause(PauseScope.GLOBAL, reason, detail=detail, now=now)

    async def integrity_audit(self, now: datetime) -> list[str]:
        """Look for sends that should never have happened: no approval, two submissions of the same step to one
        recipient, or a submission after the suppression had been observed locally. Each incident pauses
        everything once (the record is marked so a cleared pause is not raised again for the same incident)."""
        found = []
        submitted = (await self.session.execute(select(SendRecord).where(
            SendRecord.state.in_(SUBMITTED_STATES + (SendState.FAILED,)), SendRecord.submitted_at.isnot(None),
            SendRecord.integrity_flag.is_(None)))).scalars().all()
        for record in submitted:
            if record.approved_at is None or not record.approved_by:
                record.integrity_flag = Reason.UNAPPROVED_SEND
                await self.record_integrity_incident(Reason.UNAPPROVED_SEND, f"send record {record.id}", now)
                found.append(f"{Reason.UNAPPROVED_SEND}:{record.id}")
        # E4: only campaign steps can be duplicates; replies (step NULL, kind REPLY) to one person are a conversation.
        dupes = (await self.session.execute(
            select(SendRecord.recipient_hash, SendRecord.step, func.count())
            .where(SendRecord.state.in_(SUBMITTED_STATES + (SendState.FAILED,)), SendRecord.submitted_at.isnot(None),
                   SendRecord.kind == SendKind.CAMPAIGN)
            .group_by(SendRecord.recipient_hash, SendRecord.step).having(func.count() > 1))).all()
        for recipient_hash, step, _ in dupes:
            rows = [r for r in submitted if r.recipient_hash == recipient_hash and r.step == step
                    and r.kind == SendKind.CAMPAIGN]
            if rows:
                for row in rows:
                    row.integrity_flag = Reason.DUPLICATE_SEND
                await self.record_integrity_incident(
                    Reason.DUPLICATE_SEND, f"step {step} submitted {len(rows)}x to {recipient_hash[:12]}...", now)
                found.append(f"{Reason.DUPLICATE_SEND}:{recipient_hash[:12]}")
        mirror = {row.email_hash: row for row in (await self.session.execute(select(SuppressionMirror))).scalars()}
        for record in submitted:
            seen = mirror.get(record.recipient_hash)
            if record.kind == SendKind.REPLY and record.idempotency_key.startswith(STOP_CONFIRMATION_KEY):
                continue   # E4: the one-line "stop" confirmation the founder approved goes to a suppressed address
            if (seen is not None and record.integrity_flag is None
                    and aware(seen.fetched_at) < aware(record.submitted_at)):
                record.integrity_flag = Reason.SUPPRESSED_SEND
                await self.record_integrity_incident(Reason.SUPPRESSED_SEND, f"send record {record.id}", now)
                found.append(f"{Reason.SUPPRESSED_SEND}:{record.id}")
        await self.session.flush()
        return found

    # ─── reply backlog (E4 calls this) ───────────────────────────────────

    async def check_reply_backlog(self, oldest_unanswered_interested_at: Optional[datetime],
                                  now: Optional[datetime] = None) -> bool:
        """True (and no new first contacts) while an interested reply waits for more than 1 business day; the
        pause clears itself when the backlog is cleared (spec row 11: "resume only after the backlog is cleared")."""
        now = aware(now) if now else datetime.now(timezone.utc)
        breached = rules.reply_backlog_breached(oldest_unanswered_interested_at, now, load_zone(FOUNDER_ZONE))
        if breached:
            await self.sending.raise_pause(
                PauseScope.NEW_CONTACTS, Reason.REPLY_BACKLOG,
                detail=f"interested reply unanswered since {aware(oldest_unanswered_interested_at).isoformat()}",
                now=now)
        else:
            await self.sending._clear_reason(Reason.REPLY_BACKLOG, "system", "reply backlog cleared", now,
                                             PauseScope.NEW_CONTACTS)
        return breached

    # ─── display mirror ──────────────────────────────────────────────────

    async def sync_mirror(self, since: Optional[datetime], now: datetime, max_pages: int = 20) -> int:
        """Copy the website's list into the DISPLAY mirror. Never used to allow a send."""
        if self.client is None:
            return 0
        stored = 0
        cursor = since
        for _ in range(max_pages):
            page = await self.client.list_since(cursor)
            for item in page.items:
                key = item["hash"].lower()
                row = (await self.session.execute(select(SuppressionMirror).where(
                    SuppressionMirror.email_hash == key))).scalar_one_or_none()
                if row is None:   # `since` paging repeats the boundary item: the unique hash removes duplicates
                    self.session.add(SuppressionMirror(email_hash=key, reason=str(item.get("reason") or "")[:50],
                                                       suppressed_at=_parse_time(item.get("created_at")),
                                                       fetched_at=now))
                    stored += 1
            await self.session.flush()
            if not page.next or page.next == (cursor.isoformat() if cursor else None):
                break
            cursor = _parse_time(page.next)
        return stored


def _parse_time(value) -> Optional[datetime]:
    if not isinstance(value, str):
        return None
    try:
        return aware(datetime.fromisoformat(value.replace("Z", "+00:00")))
    except ValueError:
        return None
