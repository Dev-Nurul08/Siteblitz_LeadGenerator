"""
Email engine v2, phase E2 - the sender worker (one process, supervised sending windows only).

Start-up:   refuses to run when another worker holds the lock file, when the shared outreach values are missing,
            or when no enabled mailbox has its password configured. Any record left SUBMITTING by a crash becomes
            UNCERTAIN (+ global pause SEND_RESULT_UNKNOWN): it may have been accepted, so it is never re-sent.
Each cycle: integrity audit -> move missed messages to their next window -> pause every mailbox whose inbox was not
            read completely in the last 24 h (E4) -> stop if a global pause is active ->
            for every due SendRecord, in this order:
              1. approval present (text, approver, approval time) and company facts filled
              2. FRESH suppression check against the website; no trustworthy answer = no send + global pause
                 SUPPRESSION_UNAVAILABLE (the local mirror is never asked)
              3. the sequence is still ACTIVE (no reply / stop), the previous step was accepted, no duplicate
              4. observation still true: E1's recheck_before_send (a SITE_DOWN site must still be down)
              5. no pause flag in scope (global, new contacts, domain, mailbox, source, source batch)
              6. inside the recipient-local window
              7. capacity: 30 / 25 per mailbox per local day, the ramp for step 1
              8. mark SUBMITTING with a conditional update (only one worker can win a record) and COMMIT
              9. SMTP submission (STARTTLS or SSL, 30 s timeout)
             10. ACCEPTED on 2xx, FAILED on 5xx (bounce rules), back to SCHEDULED when nothing was accepted,
                 UNCERTAIN on a lost answer after DATA (+ global pause, never retried automatically). A 4xx answer
                 is tried at most 3 times in one window, then in the next window; after 3 windows the record is
                 FAILED (soft) and the sequence HELD (E3, record_temporary_refusal)
"""

import asyncio
import os
import socket
from datetime import datetime, timezone
from pathlib import Path
from typing import Awaitable, Callable, Optional

import structlog
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from backend.app.engines.eligibility.verification import VerificationLadder
from backend.app.engines.sending import scheduler as sched
from backend.app.engines.sending import smtp as smtp_engine
from backend.app.engines.sending.message import build_message
from backend.app.engines.sending.pause_rules import Reason
from backend.app.engines.sending.suppression_client import SuppressionClient, SuppressionUnavailable
from backend.app.models.eligibility import HoldReason
from backend.app.models.sending import (
    EmailSequence,
    Mailbox,
    PauseScope,
    SendKind,
    SendRecord,
    SendState,
    SequenceState,
    SuppressionMirror,
    TlsMode,
)
from backend.app.services.delivery_rules_service import DeliveryRulesService
from backend.app.services.eligibility_service import EligibilityService
from backend.app.services.inbox_guard import check_inbox_freshness
from backend.app.services.sending_service import SendingConfig, SendingService, aware

logger = structlog.get_logger(__name__)

POLL_SECONDS = 60


class WorkerLock:
    """An OS file lock: released by the operating system when the process ends, even after a crash, so a stale
    lock never needs a time-out. The holder's pid and start time are written at the top of the file."""

    LOCK_OFFSET = 4096   # the locked byte sits past the text, so another process can still read who holds it

    def __init__(self, path: Path):
        self.path = Path(path)
        self.handle = None

    def acquire(self) -> bool:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        handle = open(self.path, "a+b")
        try:
            if os.name == "nt":
                import msvcrt
                handle.seek(self.LOCK_OFFSET)
                msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl
                fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            handle.close()
            return False
        handle.seek(0)
        handle.truncate()
        handle.write(f"pid={os.getpid()} host={socket.gethostname()} "
                     f"started={datetime.now(timezone.utc).isoformat()}\n".encode("utf-8"))
        handle.flush()
        self.handle = handle
        return True

    def holder(self) -> str:
        try:
            return self.path.read_bytes()[:200].decode("utf-8", errors="replace").strip()
        except OSError:
            return "unknown"

    def release(self) -> None:
        if self.handle is None:
            return
        try:
            if os.name == "nt":
                import msvcrt
                self.handle.seek(self.LOCK_OFFSET)
                msvcrt.locking(self.handle.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                import fcntl
                fcntl.flock(self.handle.fileno(), fcntl.LOCK_UN)
        except OSError:
            pass
        self.handle.close()
        self.handle = None


def default_eligibility(session: AsyncSession) -> EligibilityService:
    from backend.app.config import get_settings
    return EligibilityService(session, ladder=VerificationLadder.from_settings(get_settings()))


class OutreachWorker:
    def __init__(self, session_factory: async_sessionmaker, config: SendingConfig, client: SuppressionClient,
                 eligibility_factory: Callable[[AsyncSession], EligibilityService] = default_eligibility,
                 submit: Callable = smtp_engine.submit,
                 password_lookup: Callable[[str], Optional[str]] = smtp_engine.mailbox_password,
                 clock: Callable[[], datetime] = lambda: datetime.now(timezone.utc),
                 smtp_timeout: float = smtp_engine.SMTP_TIMEOUT_SECONDS,
                 inbox_guard: Optional[Callable[..., Awaitable]] = check_inbox_freshness):
        self.factory = session_factory
        self.config = config
        self.client = client
        self.eligibility_factory = eligibility_factory
        self.submit = submit
        self.password_lookup = password_lookup
        self.clock = clock
        self.smtp_timeout = smtp_timeout
        # E4: a mailbox whose inbox was not read completely in the last 24 h is paused (MAILBOX scope) each cycle.
        self.inbox_guard = inbox_guard

    # ─── start-up ────────────────────────────────────────────────────────

    async def preflight(self) -> list[str]:
        """Reasons not to start (empty = ready)."""
        problems = [f"{name} is missing (or not an http(s) origin)" if name == "OUTREACH_PUBLIC_BASE_URL"
                    else f"{name} is missing (or shorter than 32 characters)"
                    for name in self.config.missing_outreach()]
        async with self.factory() as session:
            boxes = await SendingService(session, self.config).enabled_mailboxes()
        ready = [b for b in boxes if b.smtp_tls == TlsMode.NONE or self.password_lookup(b.slug)]
        if not boxes:
            problems.append("no mailbox is configured (POST /api/v1/outreach/mailboxes)")
        elif not ready:
            problems.append("no enabled mailbox has its MAILBOX_<SLUG>_PASSWORD set in .env")
        return problems

    async def recover(self) -> int:
        """A record still SUBMITTING belongs to a run that stopped mid-conversation: its result is unknown."""
        now = aware(self.clock())
        async with self.factory() as session:
            sending = SendingService(session, self.config)
            rules = DeliveryRulesService(sending, self.client)
            stuck = (await session.execute(select(SendRecord).where(
                SendRecord.state == SendState.SUBMITTING))).scalars().all()
            for record in stuck:
                record.state = SendState.UNCERTAIN
                record.smtp_response = (record.smtp_response or "") + " [worker restarted while SUBMITTING]"
                await rules.record_send_result_unknown(record, now)
            await session.commit()
        return len(stuck)

    # ─── one cycle ───────────────────────────────────────────────────────

    async def run_once(self) -> dict:
        now = aware(self.clock())
        summary = {"at": now.isoformat(), "accepted": 0, "failed": 0, "uncertain": 0, "not_sent": 0, "held": 0,
                   "cancelled": 0, "skipped": 0, "waiting": 0, "global_pause": [], "integrity": []}
        async with self.factory() as session:
            sending = SendingService(session, self.config)
            rules = DeliveryRulesService(sending, self.client)
            summary["integrity"] = await rules.integrity_audit(now)
            summary["moved"] = (await sending.reschedule_overdue(now))["moved"]
            if self.inbox_guard is not None:
                summary["stale_inboxes"] = await self.inbox_guard(session, self.config, now)
            await session.commit()
            blocking = [f for f in await sending.active_pauses() if f.scope == PauseScope.GLOBAL]
            if blocking:
                summary["global_pause"] = [f.reason_code for f in blocking]
                return summary
            due = (await session.execute(
                select(SendRecord.id).where(SendRecord.state == SendState.SCHEDULED,
                                            SendRecord.kind == SendKind.CAMPAIGN, SendRecord.scheduled_for <= now)
                .order_by(SendRecord.scheduled_for, SendRecord.id))).scalars().all()
        for record_id in due:
            outcome = await self._process(record_id)
            if outcome == "stop_cycle":
                summary["uncertain_or_unavailable"] = True
                break
            summary[outcome] = summary.get(outcome, 0) + 1
        return summary

    async def _hold(self, session: AsyncSession, record: SendRecord, reason: str) -> str:
        record.hold_reason = reason[:100]
        await session.commit()
        return "held"

    async def _cancel(self, session: AsyncSession, record: SendRecord, reason: str) -> str:
        record.state, record.cancel_reason = SendState.CANCELLED, reason[:300]
        await session.commit()
        return "cancelled"

    async def _local_hold(self, sending: SendingService, record: SendRecord, sequence: EmailSequence,
                          mailbox: Mailbox, now: datetime) -> Optional[str]:
        """Steps 5-7 (no network): the hold reason, or None when the record may go now."""
        # 5. pause flags in scope, mailbox state
        blocks = sending.blocking(await sending.active_pauses(), step=record.step, mailbox=mailbox,
                                  sequence=sequence)
        if blocks:
            return f"PAUSED:{blocks[0].reason_code}"
        if not mailbox.enabled:
            return "MAILBOX_DISABLED"
        if mailbox.smtp_tls != TlsMode.NONE and self.password_lookup(mailbox.slug) is None:
            return "MAILBOX_PASSWORD_MISSING"
        # 6. inside the recipient-local window
        zone = sched.load_zone(sequence.timezone)
        if zone is None:
            return sched.HoldCode.TIMEZONE_MISSING
        window = sched.window_containing(now, zone)
        if (window is None or window.local_date != record.local_date
                or not (aware(record.window_start) <= now < aware(record.window_end))):
            return "OUTSIDE_WINDOW"
        # 7. capacity: what already left today; caps are never exceeded to catch up
        sent = await sending.submitted_counts(mailbox.id, record.local_date)
        if sent["total"] >= sched.MAILBOX_DAILY_CEILING or sent["campaign"] >= sched.CAMPAIGN_DAILY_LIMIT:
            return "CAPACITY_FULL"
        if record.step == 1 and (await sending.submitted_new_contacts(record.local_date)
                                 >= await sending.daily_new_limit()):
            return sched.HoldCode.RAMP_LIMIT_REACHED
        return None

    async def _process(self, record_id: int) -> str:
        async with self.factory() as session:
            sending = SendingService(session, self.config)
            rules = DeliveryRulesService(sending, self.client)
            now = aware(self.clock())
            record = await session.get(SendRecord, record_id)
            if record is None or record.state != SendState.SCHEDULED:
                return "skipped"
            sequence = await session.get(EmailSequence, record.sequence_id) if record.sequence_id else None
            mailbox = await session.get(Mailbox, record.mailbox_id)
            # Cheap local pre-filter: a record that steps 5-7 would hold anyway is held before any network call,
            # so a paused or full mailbox never makes the worker ask the website or fetch a prospect's homepage
            # every minute. Steps 1-7 still all run, in order, right before the claim.
            if sequence is not None and sequence.state == SequenceState.ACTIVE:
                reason = await self._local_hold(sending, record, sequence, mailbox, now)
                if reason:
                    return await self._hold(session, record, reason)

            # 1. approval + company facts
            if not (record.approved_at and record.approved_by and (record.body or "").strip()
                    and (record.subject or "").strip()):
                return await self._hold(session, record, "NOT_APPROVED")
            missing = self.config.missing_company_facts()
            if missing or not (mailbox.display_name or "").strip():
                return await self._hold(session, record, "COMPANY_FACTS_MISSING")

            # 2. fresh suppression check (no write transaction is open during the network call)
            await session.commit()
            try:
                suppressed = await self.client.check([record.recipient_hash])
            except SuppressionUnavailable as exc:
                await rules.record_suppression_unavailable(str(exc), now)
                record.hold_reason = Reason.SUPPRESSION_UNAVAILABLE
                await session.commit()
                return "stop_cycle"
            if record.recipient_hash in suppressed:
                record.state, record.cancel_reason = SendState.CANCELLED, "SUPPRESSED (website)"
                if sequence is not None:
                    await sending.stop_sequence(sequence.id, SequenceState.STOPPED_SUPPRESSED,
                                                "suppressed on the website", now)
                if (await session.execute(select(SuppressionMirror.id).where(
                        SuppressionMirror.email_hash == record.recipient_hash))).scalar_one_or_none() is None:
                    session.add(SuppressionMirror(email_hash=record.recipient_hash, reason=None, suppressed_at=None,
                                                  fetched_at=now))
                await session.commit()
                return "cancelled"

            # 3. sequence still active, previous step accepted, no duplicate
            if sequence is None:
                return await self._cancel(session, record, "NO_SEQUENCE")
            if sequence.state == SequenceState.PAUSED_OOO:
                return await self._hold(session, record, "SEQUENCE_PAUSED_OOO")
            if sequence.state != SequenceState.ACTIVE:
                return await self._cancel(session, record, f"SEQUENCE_{sequence.state.value}")
            steps = (await session.execute(select(SendRecord).where(
                SendRecord.sequence_id == sequence.id).order_by(SendRecord.step))).scalars().all()
            if record.step and record.step > 1:
                previous = next((r for r in steps if r.step == record.step - 1), None)
                if previous is None or previous.state in (SendState.CANCELLED, SendState.FAILED):
                    return await self._cancel(session, record, "PREVIOUS_STEP_NOT_SENT")
                if previous.state != SendState.ACCEPTED:
                    return await self._hold(session, record, "PREVIOUS_STEP_NOT_ACCEPTED")
            twin = (await session.execute(select(SendRecord.id).where(
                SendRecord.recipient_hash == record.recipient_hash, SendRecord.step == record.step,
                SendRecord.id != record.id, SendRecord.submitted_at.isnot(None)).limit(1))).scalar_one_or_none()
            if twin is not None:
                await rules.record_integrity_incident(
                    Reason.DUPLICATE_SEND, f"prevented: record {record.id} repeats record {twin}", now)
                return await self._cancel(session, record, f"DUPLICATE of send record {twin}")

            # 4. the observation is still true (E1 recheck; a SITE_DOWN homepage must still fail)
            try:
                check = await self.eligibility_factory(session).recheck_before_send(sequence.business_id, now=now)
            except Exception as exc:   # an unexpected error is never a reason to send
                await session.rollback()
                record = await session.get(SendRecord, record_id)
                record.scheduled_for = record.window_end
                return await self._hold(session, record, f"RECHECK_FAILED:{type(exc).__name__}")
            if not check["send_allowed"] or (check["send_to"] or "").lower() != record.recipient_email.lower():
                if check.get("reason") == HoldReason.SITE_RECOVERED.value:
                    record.state, record.cancel_reason = SendState.CANCELLED, HoldReason.SITE_RECOVERED.value
                    await sending.stop_sequence(sequence.id, SequenceState.CANCELLED,
                                                "the site loads again (SITE_RECOVERED)", now)
                    await session.commit()
                    return "cancelled"
                reasons = next((r["hold_reasons"] for r in check["rows"]
                                if r["email"].lower() == record.recipient_email.lower()), [])
                # At most one recheck per window: the record becomes overdue and moves to the next window.
                record.scheduled_for = record.window_end
                return await self._hold(session, record, "NOT_ELIGIBLE:" + ",".join(reasons or ["?"]))
            await session.commit()

            # 5-7. pause flags and mailbox state, the recipient-local window, capacity (again, right before claiming)
            reason = await self._local_hold(sending, record, sequence, mailbox, now)
            if reason:
                return await self._hold(session, record, reason)
            password = None if mailbox.smtp_tls == TlsMode.NONE else self.password_lookup(mailbox.slug)

            # build before claiming, so a build error can never leave a record SUBMITTING
            parents = [r.message_id for r in steps if r.step < (record.step or 0) and r.state == SendState.ACCEPTED]
            try:
                outgoing = build_message(
                    mailbox_address=mailbox.address, display_name=mailbox.display_name,
                    recipient=record.recipient_email, subject=record.subject, body=record.body,
                    message_id=record.message_id, send_record_id=str(record.id), base_url=self.config.base_url,
                    signing_secret=self.config.signing_secret, date=now, thread_parent_ids=parents)
            except Exception as exc:   # e.g. a secret that became invalid
                return await self._hold(session, record, f"MESSAGE_BUILD_FAILED:{type(exc).__name__}")

            # 8. claim: only one worker / run can move this record out of SCHEDULED
            claimed = await session.execute(
                update(SendRecord).where(SendRecord.id == record.id, SendRecord.state == SendState.SCHEDULED)
                .values(state=SendState.SUBMITTING, submitted_at=now, attempts=SendRecord.attempts + 1,
                        hold_reason=None)
                .execution_options(synchronize_session=False))
            if claimed.rowcount != 1:
                await session.rollback()
                return "skipped"
            await session.commit()

            # 9. SMTP submission (blocking smtplib in a thread)
            config = smtp_engine.SmtpConfig(mailbox.smtp_host, mailbox.smtp_port, mailbox.smtp_tls.value,
                                            mailbox.username, password, self.smtp_timeout)
            result = await asyncio.to_thread(self.submit, config, mailbox.address, record.recipient_email,
                                             outgoing.as_bytes())

            # 10. outcome
            done = aware(self.clock())
            await session.refresh(record)
            record.smtp_code, record.smtp_status = result.code, result.status
            record.smtp_response = (result.response or "")[:2000] or None
            logger.info("outreach_submit", record=record.id, step=record.step, outcome=result.outcome,
                        phase=result.phase, code=result.code)
            if result.outcome == smtp_engine.ACCEPTED:
                record.state, record.accepted_at = SendState.ACCEPTED, done
                await sending.mark_step_accepted(sequence, record, done)
                await session.commit()
                return "accepted"
            if result.outcome == smtp_engine.FAILED and result.phase != "mail":
                record.state = SendState.FAILED
                await session.commit()
                await rules.record_smtp_refusal(record, done)
                await session.commit()
                return "failed"
            if result.outcome == smtp_engine.UNCERTAIN:
                record.state = SendState.UNCERTAIN
                await rules.record_send_result_unknown(record, done)
                await session.commit()
                return "stop_cycle"
            # Nothing was accepted (4xx, connection / TLS / login trouble, our sender refused): safe to try again
            # in a later slot. A mailbox problem pauses that mailbox until a person looks at it.
            record.state, record.submitted_at = SendState.SCHEDULED, None
            record.hold_reason = f"SMTP_NOT_SENT:{result.phase}:{result.code or 'error'}"
            record.scheduled_for = done + sched.SLOT_SPACING
            if result.mailbox_problem or result.phase == "mail":
                await sending.raise_pause(PauseScope.MAILBOX, Reason.SMTP_UNAVAILABLE, str(mailbox.id),
                                          detail=f"{result.phase}: {(result.response or '')[:300]}", now=done)
            elif result.code and 400 <= result.code < 500:
                # E3 cap: 3 attempts per window, then the next window; after 3 windows FAILED (soft) + HELD.
                action = await rules.record_temporary_refusal(record, done, result.code, result.status,
                                                              result.response, result.phase)
                if action == "failed":
                    await session.commit()
                    return "failed"
            await session.commit()
            return "not_sent"

    # ─── the supervised loop ─────────────────────────────────────────────

    async def run(self, until: datetime, poll_seconds: float = POLL_SECONDS,
                  sleep: Callable[[float], Awaitable] = asyncio.sleep, echo: Callable[[str], None] = print) -> None:
        recovered = await self.recover()
        if recovered:
            echo(f"{recovered} send record(s) were SUBMITTING at start-up -> UNCERTAIN, global pause "
                 f"{Reason.SEND_RESULT_UNKNOWN}; resolve them with POST /api/v1/outreach/send-records/{{id}}/resolve")
        while self.clock() < until:
            summary = await self.run_once()
            echo(" ".join(f"{k}={v}" for k, v in summary.items() if v not in (0, [], None)))
            await sleep(poll_seconds)


def last_window_end_today(now: datetime) -> Optional[datetime]:
    """End of today's last campaign window in the pilot country's time (16:30 India time), or None when today is
    not a campaign day or the windows are over."""
    zone = sched.load_zone(sched.COUNTRY_TIMEZONES["IN"])
    day = sched.local_date(now, zone)
    if not sched.is_campaign_day(day):
        return None
    end = sched.windows_for(day, zone)[-1].end
    return end if now < end else None
