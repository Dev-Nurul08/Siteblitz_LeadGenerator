"""
Email engine v2, phase E4 - the reply loop (spec rows 11, 13-16; RESULT rows 18-20; docs/outreach/e4-notes.md).

reconcile():   for every enabled mailbox, read INBOX + the junk folder over IMAP (UIDVALIDITY-aware, read-only),
               store each new message, then process every stored message that is still NEW (or ERROR, max 3 tries):
                 own copy / read receipt / list mail  -> IGNORED
                 DSN                                  -> E2's bounce rules (suppress / pause), label bounce
                 ARF feedback report                  -> credible complaint (E2 rules), label complaint_legal
                 auto-reply (out of office)           -> sequence PAUSED_OOO, resume 2 business days after the return
                                                         date (or after 14 days); never answered
                 a person's reply                     -> FIRST the cold sequence is stopped (follow-ups cancelled),
                                                         then the safety rules (stop, complaint_legal), then the
                                                         model's commercial labels, then an AI draft that waits for
                                                         the founder (never sent without approval)
               then: resume OOO sequences that are due, retry "stop" writes the website did not take, copy the
               website's suppression list (display only) and stop sequences of addresses that unsubscribed by link,
               pause every mailbox not reconciled in the last 24 h, and apply the reply-backlog rule.
drafts:        list / approve (sends now over the E2 SMTP path, same mailbox, threading headers, counted against the
               mailbox's 30-a-day ceiling) / reject / regenerate.
"""

import asyncio
from dataclasses import asdict, dataclass, field
from datetime import date, datetime, time, timedelta, timezone
from pathlib import Path
from typing import Any, Callable, Optional

import structlog
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from backend.app.engines.replies import labels as L
from backend.app.engines.replies.classifier import ReplyClassifier
from backend.app.engines.replies.imap_client import ImapError, InboxReader, connect as imap_connect
from backend.app.engines.replies.parsing import ParsedMessage, ooo_return_date, parse_message
from backend.app.engines.replies.sanitizer import sanitize
from backend.app.engines.replies.snapshot_client import (SnapshotClient, SnapshotUnavailable, build_payload,
                                                         load_recording)
from backend.app.engines.sending import dsn
from backend.app.engines.sending import scheduler as sched
from backend.app.engines.sending import smtp as smtp_engine
from backend.app.engines.sending.message import build_message, new_message_id, reply_subject
from backend.app.engines.sending.pause_rules import BUSINESS_WEEKDAYS, Reason
from backend.app.engines.sending.smtp import password_variable
from backend.app.engines.sending.suppression_client import SuppressionClient, SuppressionUnavailable
from backend.app.engines.sending.tokens import email_hash
from backend.app.models.business import Business, BusinessLocation
from backend.app.models.compliance import OptOut
from backend.app.models.eligibility import EmailEligibility
from backend.app.models.replies import (
    DraftKind,
    DraftState,
    ImapFolderState,
    InboundKind,
    InboundMessage,
    InboundState,
    MailboxReconcile,
    OpportunitySnapshot,
    ReplyDraft,
    ReplySuppression,
    WebsiteWrite,
)
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
from backend.app.services.delivery_rules_service import (
    FOUNDER_ZONE,
    STOP_CONFIRMATION_KEY,
    DeliveryRulesService,
)
from backend.app.services.inbox_guard import check_inbox_freshness
from backend.app.services.sending_service import (
    Conflict,
    NotFound,
    SendingConfig,
    SendingService,
    ServiceError,
    aware,
    iso,
)

logger = structlog.get_logger(__name__)

OOO_REVIEW_AFTER = timedelta(days=14)         # lifecycle table: no return date -> review after 14 days
OOO_RESUME_BUSINESS_DAYS = 2                  # lifecycle table: resume 2 business days after the return date
FIRST_READ_LOOKBACK = timedelta(days=30)      # first read of a folder when this mailbox never sent anything
MAX_MESSAGES_PER_FOLDER = 300                 # per run; more left = the run is incomplete (read again next time)
MAX_PROCESS_ATTEMPTS = 3
MAX_REGENERATIONS = 5
THREAD_ENTRIES = 6
STOP_CONFIRMATION_TEXT = "Understood, thank you for letting me know."   # lifecycle table, "No / stop" row
LOCK_NAME = "outreach_reconcile.lock"
BLOCKING_FLAGS = ("ASKS_FOR", "POSSIBLE_OPT_OUT", "POSSIBLE_COMPLAINT", "DATA_SOURCE_QUESTION")


class ServiceUnavailable(ServiceError):
    status = 503


def reconcile_lock_path(database_url: str) -> Path:
    if database_url.startswith("sqlite") and ":///" in database_url:
        return Path(database_url.split(":///", 1)[1]).resolve().parent / LOCK_NAME
    return Path.cwd() / LOCK_NAME


def add_business_days(day: date, count: int) -> date:
    while count > 0:
        day += timedelta(days=1)
        if day.weekday() in BUSINESS_WEEKDAYS:
            count -= 1
    return day


def founder_zone():
    return sched.load_zone(FOUNDER_ZONE)


# ─── checks the worker and the brief also use ───────────────────────────────


async def oldest_unanswered(session: AsyncSession) -> Optional[datetime]:
    rows = (await session.execute(select(InboundMessage.received_at, InboundMessage.labels).where(
        InboundMessage.kind == InboundKind.HUMAN, InboundMessage.handled_at.is_(None),
        InboundMessage.sequence_id.isnot(None),
        InboundMessage.state.in_([InboundState.PROCESSED, InboundState.FLAGGED, InboundState.NEEDS_REVIEW])))).all()
    times = [aware(received) for received, labels in rows if set(labels or []) & set(L.BACKLOG_LABELS)]
    return min(times) if times else None


async def apply_reply_backlog(session: AsyncSession, config: SendingConfig, client: Optional[SuppressionClient],
                              now: datetime) -> bool:
    """An interested / question / price / sample reply (or one the model could not label) without an approved
    answer for more than 1 business day -> E2's NEW_CONTACTS pause REPLY_BACKLOG; it clears itself when answered."""
    rules = DeliveryRulesService(SendingService(session, config), client)
    return await rules.check_reply_backlog(await oldest_unanswered(session), now)


# ─── dicts for the API ───────────────────────────────────────────────────────


def inbound_dict(msg: InboundMessage, business_name: Optional[str] = None) -> dict:
    return {"id": msg.id, "mailbox_id": msg.mailbox_id, "folder": msg.folder, "kind": msg.kind.value,
            "state": msg.state.value, "from_address": msg.from_address, "subject": msg.subject,
            "received_at": iso(msg.received_at), "labels": list(msg.labels or []), "flags": list(msg.flags or []),
            "summary": msg.model_summary, "language": msg.language, "text": (msg.body_text or "")[:2000],
            "sequence_id": msg.sequence_id, "business_id": msg.business_id, "business_name": business_name,
            "match_method": msg.match_method, "ooo_return_date": msg.ooo_return_date.isoformat()
            if msg.ooo_return_date else None, "ooo_resume_at": iso(msg.ooo_resume_at),
            "handled_at": iso(msg.handled_at), "handled_by": msg.handled_by, "error": msg.error}


def draft_dict(draft: ReplyDraft, business_name: Optional[str] = None, snapshot_url: Optional[str] = None,
               inbound_text: Optional[str] = None) -> dict:
    return {"id": draft.id, "kind": draft.kind.value, "state": draft.state.value, "business_id": draft.business_id,
            "business_name": business_name, "sequence_id": draft.sequence_id, "mailbox_id": draft.mailbox_id,
            "inbound_message_id": draft.inbound_message_id, "recipient_email": draft.recipient_email,
            "labels": list(draft.labels or []), "language": draft.language, "subject": draft.subject,
            "text": draft.body, "snapshot_url": snapshot_url, "errors": list(draft.errors or []),
            "inbound_text": (inbound_text or "")[:1000], "created_at": iso(draft.created_at),
            "decided_at": iso(draft.decided_at), "decided_by": draft.decided_by,
            "decision_note": draft.decision_note, "send_record_id": draft.send_record_id,
            "regenerations": draft.regenerations}


# ─── the loop ────────────────────────────────────────────────────────────────


@dataclass
class ReplyLoopDeps:
    config: SendingConfig
    suppression: Optional[SuppressionClient]
    snapshots: SnapshotClient
    classifier: ReplyClassifier
    writer_factory: Callable[[], Any]                     # -> OutreachWriter (lazy: it reads docs/outreach/)
    facts_md: str                                         # docs/outreach/company-facts.md (snapshot offer lines)
    imap_connector: Callable[..., Any] = imap_connect
    password_lookup: Callable[[str], Optional[str]] = smtp_engine.mailbox_password
    submit: Callable = smtp_engine.submit
    clock: Callable[[], datetime] = field(default=lambda: datetime.now(timezone.utc))
    smtp_timeout: float = smtp_engine.SMTP_TIMEOUT_SECONDS


class ReplyLoop:
    def __init__(self, session_factory: async_sessionmaker, deps: ReplyLoopDeps):
        self.factory = session_factory
        self.deps = deps
        self.config = deps.config

    def now(self) -> datetime:
        return aware(self.deps.clock())

    def _services(self, session: AsyncSession) -> tuple[SendingService, DeliveryRulesService]:
        sending = SendingService(session, self.config)
        return sending, DeliveryRulesService(sending, self.deps.suppression)

    # ─── reconcile ───────────────────────────────────────────────────────

    async def reconcile(self) -> dict:
        started = self.now()
        summary: dict[str, Any] = {"started_at": started.isoformat(), "mailboxes": []}
        async with self.factory() as session:
            boxes = await SendingService(session, self.config).enabled_mailboxes()
            own = {b.address.lower() for b in (await session.execute(select(Mailbox))).scalars().all()}
        for box in boxes:
            summary["mailboxes"].append(await self._read_mailbox(box, own))
        summary["processed"] = await self.process_pending()
        now = self.now()
        summary["ooo_resumed"] = await self.resume_ooo(now)
        summary["suppressions_retried"] = await self.retry_pending_suppressions(now)
        summary["website_unsubscribes"] = await self.sync_website_unsubscribes(now)
        async with self.factory() as session:
            summary["stale_mailboxes"] = await check_inbox_freshness(session, self.config, now)
            summary["reply_backlog_breached"] = await apply_reply_backlog(session, self.config,
                                                                          self.deps.suppression, now)
            await session.commit()
        summary["finished_at"] = self.now().isoformat()
        summary["ok"] = all(m["ok"] for m in summary["mailboxes"]) and bool(summary["mailboxes"])
        return summary

    async def _since_date(self, session: AsyncSession, box: Mailbox, now: datetime) -> date:
        first = (await session.execute(select(SendRecord.submitted_at).where(
            SendRecord.mailbox_id == box.id, SendRecord.submitted_at.isnot(None))
            .order_by(SendRecord.submitted_at).limit(1))).scalar_one_or_none()
        start = aware(first) - timedelta(days=1) if first else now - FIRST_READ_LOOKBACK
        return start.date()

    async def _read_mailbox(self, box: Mailbox, own: set[str]) -> dict:
        now = self.now()
        result = {"mailbox_id": box.id, "address": box.address, "ok": False, "new_messages": 0, "folders": [],
                  "error": None}
        async with self.factory() as session:
            row = (await session.execute(select(MailboxReconcile).where(
                MailboxReconcile.mailbox_id == box.id))).scalar_one_or_none()
            if row is None:
                row = MailboxReconcile(mailbox_id=box.id, last_new_messages=0)
                session.add(row)
            row.last_attempt_at = now
            await session.commit()
        reader = None
        try:
            if not (box.imap_host and box.imap_port and box.imap_tls):
                raise ImapError("IMAP host / port / TLS are not set for this mailbox")
            password = None if box.imap_tls == TlsMode.NONE else self.deps.password_lookup(box.slug)
            if box.imap_tls != TlsMode.NONE and password is None:
                raise ImapError(f"{password_variable(box.slug)} is not set in .env")
            reader = await asyncio.to_thread(InboxReader.open_session, box.imap_host, box.imap_port,
                                             box.imap_tls.value, box.username, password or "",
                                             self.deps.imap_connector)
            complete = True
            for folder in await asyncio.to_thread(reader.folders):
                stored, finished = await self._read_folder(reader, box, folder, own, now)
                result["new_messages"] += stored
                result["folders"].append({"folder": folder, "new_messages": stored, "complete": finished})
                complete = complete and finished
            if not complete:
                raise ImapError(f"more than {MAX_MESSAGES_PER_FOLDER} new messages in a folder; read again")
            result["ok"] = True
        except ImapError as exc:
            result["error"] = str(exc)[:300]
        except Exception as exc:   # a parser or database surprise must not look like a complete read
            result["error"] = f"{type(exc).__name__}: {exc}"[:300]
            logger.warning("reconcile_mailbox_failed", mailbox=box.id, error=type(exc).__name__)
        finally:
            if reader is not None:
                await asyncio.to_thread(reader.close)
        async with self.factory() as session:
            row = (await session.execute(select(MailboxReconcile).where(
                MailboxReconcile.mailbox_id == box.id))).scalar_one()
            row.last_new_messages = result["new_messages"]
            row.last_error = result["error"]
            if result["ok"]:
                row.last_success_at = now
            await session.commit()
        return result

    async def _read_folder(self, reader: InboxReader, box: Mailbox, folder: str, own: set[str], now: datetime
                           ) -> tuple[int, bool]:
        uidvalidity = await asyncio.to_thread(reader.open, folder)
        async with self.factory() as session:
            state = (await session.execute(select(ImapFolderState).where(
                ImapFolderState.mailbox_id == box.id, ImapFolderState.folder == folder))).scalar_one_or_none()
            if state is None:
                state = ImapFolderState(mailbox_id=box.id, folder=folder, uidvalidity=None, last_uid=0)
                session.add(state)
            if state.uidvalidity != uidvalidity:
                # A new UIDVALIDITY means every UID changed: read again from the first send of this mailbox (or 30
                # days back); messages already stored are recognised by Message-ID / content hash, not by UID.
                if state.uidvalidity is not None:
                    state.uidvalidity_changed_at = now
                state.uidvalidity, state.last_uid = uidvalidity, 0
                since = await self._since_date(session, box, now)
                uids = await asyncio.to_thread(reader.uids_since, since)
            else:
                uids = await asyncio.to_thread(reader.uids_after, state.last_uid)
            await session.commit()
        finished = len(uids) <= MAX_MESSAGES_PER_FOLDER
        stored = 0
        for uid in uids[:MAX_MESSAGES_PER_FOLDER]:
            fetched = await asyncio.to_thread(reader.fetch, folder, uidvalidity, uid)
            parsed = parse_message(fetched.raw)
            async with self.factory() as session:
                if await self._store(session, box, folder, uidvalidity, uid, fetched.size, parsed, own, now):
                    stored += 1
                state = (await session.execute(select(ImapFolderState).where(
                    ImapFolderState.mailbox_id == box.id, ImapFolderState.folder == folder))).scalar_one()
                state.last_uid = max(state.last_uid or 0, uid)
                await session.commit()
            del fetched, parsed
        async with self.factory() as session:
            state = (await session.execute(select(ImapFolderState).where(
                ImapFolderState.mailbox_id == box.id, ImapFolderState.folder == folder))).scalar_one()
            if finished:
                state.last_success_at = now
            await session.commit()
        return stored, finished

    async def _store(self, session: AsyncSession, box: Mailbox, folder: str, uidvalidity: int, uid: int,
                     size: int, parsed: ParsedMessage, own: set[str], now: datetime) -> bool:
        if parsed.message_id:
            dup = select(InboundMessage.id).where(InboundMessage.mailbox_id == box.id,
                                                  InboundMessage.message_id == parsed.message_id[:255])
        else:
            dup = select(InboundMessage.id).where(InboundMessage.mailbox_id == box.id,
                                                  InboundMessage.raw_sha256 == parsed.raw_sha256)
        if (await session.execute(dup.limit(1))).scalar_one_or_none() is not None:
            return False
        kind = InboundKind(parsed.kind)
        if parsed.from_address and parsed.from_address in own:
            kind = InboundKind.OWN
        received = parsed.date
        if received is None or received > now + timedelta(days=1) or received.year < 2000:
            received = now
        # SQLite keeps no UTC offset: everything stored is UTC (E2 convention), so a "+0530" Date header is converted.
        received = received.astimezone(timezone.utc)
        meta: dict[str, Any] = {"auto_signals": parsed.auto_signals, "report_type": parsed.report_type,
                                "to": parsed.to_addresses[:5]}
        if parsed.bounce is not None:
            meta["bounce"] = asdict(parsed.bounce)
        if parsed.feedback is not None:
            meta["feedback"] = parsed.feedback
        if not parsed.new_text.strip():
            meta["fallback_text"] = L.fallback_text(parsed.text)[:5000]
        session.add(InboundMessage(
            mailbox_id=box.id, folder=folder, uidvalidity=uidvalidity, uid=uid,
            message_id=parsed.message_id[:255] if parsed.message_id else None,
            in_reply_to=parsed.in_reply_to[:255] if parsed.in_reply_to else None,
            references=" ".join(parsed.references)[-4000:] or None, from_address=parsed.from_address,
            from_hash=email_hash(parsed.from_address) if parsed.from_address else None,
            reply_to_address=parsed.reply_to, subject=parsed.subject or None, received_at=received,
            body_text=parsed.new_text[:20000] or None, signature_text=parsed.signature[:2000] or None,
            had_quote=bool(parsed.quoted), raw_size=size, raw_sha256=parsed.raw_sha256, kind=kind, meta=meta,
            labels=[], flags=[], state=InboundState.NEW, attempts=0))
        await session.flush()
        return True

    # ─── processing ──────────────────────────────────────────────────────

    async def process_pending(self) -> dict:
        async with self.factory() as session:
            ids = (await session.execute(select(InboundMessage.id).where(
                (InboundMessage.state == InboundState.NEW)
                | ((InboundMessage.state == InboundState.ERROR)
                   & (InboundMessage.attempts < MAX_PROCESS_ATTEMPTS)))
                .order_by(InboundMessage.received_at, InboundMessage.id))).scalars().all()
        counts: dict[str, int] = {}
        for inbound_id in ids:
            state = await self.process(inbound_id)
            counts[state] = counts.get(state, 0) + 1
        return counts

    async def process(self, inbound_id: int) -> str:
        now = self.now()
        async with self.factory() as session:
            msg = await session.get(InboundMessage, inbound_id)
            if msg is None:
                return "missing"
            msg.attempts = (msg.attempts or 0) + 1
            msg.error = None
            await session.commit()
            try:
                box = await session.get(Mailbox, msg.mailbox_id)
                if msg.kind in (InboundKind.OWN, InboundKind.AUTOMATED):
                    msg.state = InboundState.IGNORED
                elif msg.kind == InboundKind.DSN:
                    await self._process_dsn(session, msg, now)
                elif msg.kind == InboundKind.FEEDBACK:
                    await self._process_feedback(session, msg, now)
                else:
                    sequence, record = await self._match(session, msg, box)
                    if msg.kind == InboundKind.AUTO_REPLY:
                        await self._process_ooo(session, msg, sequence, now)
                    else:
                        await self._process_human(session, msg, sequence, record, now)
                msg.processed_at = now
                await session.commit()
            except Exception as exc:
                logger.warning("reply_process_failed", inbound=inbound_id, error=type(exc).__name__)
                await session.rollback()
                msg = await session.get(InboundMessage, inbound_id)
                msg.state, msg.error = InboundState.ERROR, f"{type(exc).__name__}: {exc}"[:500]
                await session.commit()
            return msg.state.value

    async def _match(self, session: AsyncSession, msg: InboundMessage, box: Mailbox
                     ) -> tuple[Optional[EmailSequence], Optional[SendRecord]]:
        """In-Reply-To, then References (newest first) against our Message-IDs; else sender address + mailbox."""
        candidates = ([(msg.in_reply_to, "in_reply_to")] if msg.in_reply_to else []) + [
            (ref, "references") for ref in reversed((msg.references or "").split()) if ref != msg.in_reply_to]
        for message_id, method in candidates:
            record = (await session.execute(select(SendRecord).where(
                SendRecord.message_id == message_id))).scalar_one_or_none()
            if record is not None and record.sequence_id:
                sequence = await session.get(EmailSequence, record.sequence_id)
                msg.sequence_id, msg.send_record_id, msg.match_method = sequence.id, record.id, method
                msg.business_id = sequence.business_id
                return sequence, record
        for address in (msg.from_address, msg.reply_to_address):
            if not address:
                continue
            sequence = (await session.execute(select(EmailSequence).where(
                EmailSequence.recipient_hash == email_hash(address), EmailSequence.mailbox_id == box.id)
                .order_by(EmailSequence.id.desc()).limit(1))).scalar_one_or_none()
            if sequence is not None:
                record = (await session.execute(select(SendRecord).where(
                    SendRecord.sequence_id == sequence.id, SendRecord.submitted_at.isnot(None))
                    .order_by(SendRecord.submitted_at.desc()).limit(1))).scalar_one_or_none()
                msg.sequence_id, msg.send_record_id, msg.match_method = (
                    sequence.id, record.id if record else None, "address")
                msg.business_id = sequence.business_id
                return sequence, record
        return None, None

    async def _process_dsn(self, session: AsyncSession, msg: InboundMessage, now: datetime) -> None:
        _, rules = self._services(session)
        data = dict((msg.meta or {}).get("bounce") or {})
        parsed = dsn.BounceResult(**data) if data else dsn.BounceResult(is_bounce=False, kind=dsn.UNKNOWN)
        result = await rules.record_bounce(parsed, origin="imap_dsn", now=now)
        msg.labels, msg.label_source = [L.BOUNCE], "rules"
        if result.get("matched"):
            record = await session.get(SendRecord, result["send_record_id"])
            msg.send_record_id = record.id
            msg.sequence_id = record.sequence_id
            if record.sequence_id:
                sequence = await session.get(EmailSequence, record.sequence_id)
                msg.business_id = sequence.business_id if sequence else None
            msg.state = InboundState.PROCESSED
            msg.flags = [f"BOUNCE_{parsed.kind}"] if parsed.kind not in (dsn.HARD, dsn.POLICY, dsn.SOFT) else []
        else:
            msg.state, msg.flags = InboundState.FLAGGED, ["BOUNCE_UNMATCHED"]

    async def _process_feedback(self, session: AsyncSession, msg: InboundMessage, now: datetime) -> None:
        _, rules = self._services(session)
        info = (msg.meta or {}).get("feedback") or {}
        record = await rules.find_record(info.get("original_message_id"), info.get("original_recipient"))
        msg.labels, msg.label_source = [L.COMPLAINT_LEGAL], "rules"
        if record is None:
            msg.state, msg.flags = InboundState.FLAGGED, ["COMPLAINT_LEGAL", "FEEDBACK_UNMATCHED"]
            return
        msg.send_record_id, msg.sequence_id = record.id, record.sequence_id
        await rules.record_complaint(record, record.recipient_hash, True, "arf", now,
                                     detail={"inbound_message_id": msg.id})
        msg.state, msg.flags = InboundState.FLAGGED, ["COMPLAINT_LEGAL:credible", "PROVIDER_FEEDBACK"]

    async def _process_ooo(self, session: AsyncSession, msg: InboundMessage, sequence: Optional[EmailSequence],
                           now: datetime) -> None:
        """Out of office: pause the sequence, never answer. Resume 2 business days after the return date, or after
        14 days when no date can be read (follow-ups still need the founder's approval before they go)."""
        sending, _ = self._services(session)
        zone = founder_zone()
        received = aware(msg.received_at)
        back = ooo_return_date(f"{msg.subject or ''}\n{msg.body_text or ''}", received.astimezone(zone).date())
        if back is not None:
            resume_day = add_business_days(back, OOO_RESUME_BUSINESS_DAYS)
            msg.ooo_return_date = back
            msg.ooo_resume_at = datetime.combine(resume_day, time(0, 0), zone).astimezone(timezone.utc)
        else:
            msg.ooo_resume_at = received + OOO_REVIEW_AFTER
        msg.labels, msg.label_source = [L.OUT_OF_OFFICE], "rules"
        msg.state = InboundState.PROCESSED
        if sequence is not None:
            await sending.stop_sequence(sequence.id, SequenceState.PAUSED_OOO,
                                        f"out of office (inbound {msg.id}), resume {msg.ooo_resume_at.isoformat()}",
                                        now)

    async def _process_human(self, session: AsyncSession, msg: InboundMessage, sequence: Optional[EmailSequence],
                             record: Optional[SendRecord], now: datetime) -> None:
        sending, rules = self._services(session)
        # 1. FIRST: any reply stops the cold sequence (spec row 6; 01_chatgpt.md section 6) and is committed at once.
        if sequence is not None:
            await sending.stop_sequence(sequence.id, SequenceState.STOPPED_REPLY, f"reply received (inbound {msg.id})",
                                        now)
            await session.commit()
        full_text = msg.body_text or (msg.meta or {}).get("fallback_text") or ""
        original_subject = record.subject if record is not None else None
        safety = L.safety_labels(msg.body_text or "", msg.subject or "", full_text=full_text,
                                 original_subject=original_subject)
        labels, flags = list(safety.labels), []

        # 2. Safety labels are rules, never the model: stop -> suppress (website first), complaint -> E2 rules.
        if L.STOP in labels:
            await self._apply_stop(session, msg, sequence, now)
            if safety.deletion_request:
                flags.append("DELETION_REQUEST")
        if L.COMPLAINT_LEGAL in labels:
            credible = safety.complaint_credible and sequence is not None
            target = sequence.recipient_hash if sequence is not None else msg.from_hash
            if target:
                await rules.record_complaint(record, target, credible, "reply", now,
                                             detail={"inbound_message_id": msg.id,
                                                     "rules": safety.complaint_rules[:5]})
            if msg.from_hash and msg.from_hash != target:
                await rules.suppress(msg.from_hash, "complaint", f"reply:inbound:{msg.id}", now)
            flags.append("COMPLAINT_LEGAL:credible" if credible else "COMPLAINT_LEGAL")
        if labels:
            if L.STOP in labels and L.COMPLAINT_LEGAL not in labels and sequence is not None:
                await self._stop_confirmation(session, msg, sequence, now)
            if sequence is not None:
                # After a stop or a complaint no answer is owed in this thread any more (backlog rule), and a draft
                # that still waits is withdrawn so it can never be approved by mistake.
                for row in (await session.execute(select(InboundMessage).where(
                        InboundMessage.sequence_id == sequence.id, InboundMessage.handled_at.is_(None),
                        InboundMessage.id != msg.id))).scalars().all():
                    row.handled_at, row.handled_by = now, "system"
                    row.handled_note = f"{' / '.join(labels)} received later (inbound {msg.id})"
                for old in (await session.execute(select(ReplyDraft).where(
                        ReplyDraft.sequence_id == sequence.id, ReplyDraft.kind == DraftKind.REPLY,
                        ReplyDraft.state.in_([DraftState.WAITING, DraftState.BLOCKED])))).scalars().all():
                    old.state, old.decided_at, old.decided_by = DraftState.REJECTED, now, "system"
                    old.decision_note = f"{' / '.join(labels)} received (inbound {msg.id})"
            msg.labels, msg.label_source, msg.flags = labels, "rules", flags
            msg.state = InboundState.FLAGGED if flags else InboundState.PROCESSED
            return

        # 3. Topics only the founder may answer: no draft.
        if safety.data_source_question:
            flags.append("DATA_SOURCE_QUESTION")
        requests = L.commitment_requests(full_text)
        if requests:
            flags.append("ASKS_FOR:" + ",".join(requests))
        if sequence is None:
            msg.labels, msg.label_source = [], "rules"
            msg.flags, msg.state = flags + ["UNMATCHED"], InboundState.FLAGGED
            return

        # 4. Commercial labels from the model (sanitized text, strict schema). No key / no answer = needs_review.
        result = await asyncio.to_thread(self.deps.classifier.classify, msg.subject or "", full_text)
        if not result.ok:
            msg.labels, msg.label_source, msg.flags = [L.NEEDS_REVIEW], "rules", flags
            msg.error = result.error
            msg.state = InboundState.NEEDS_REVIEW
            return
        msg.labels, msg.label_source = list(result.labels), "rules+model"
        msg.language, msg.model_summary = result.language, result.summary
        if result.possible_opt_out:
            flags.append("POSSIBLE_OPT_OUT")
        if result.possible_complaint:
            flags.append("POSSIBLE_COMPLAINT")
        if result.asks_for_commitment and not requests:
            flags.append("ASKS_FOR:model")
        if not msg.labels:
            flags.append("NO_COMMERCIAL_LABEL")
        msg.flags = flags
        if any(f.startswith(BLOCKING_FLAGS) for f in flags) or not set(msg.labels) & set(L.DRAFT_LABELS):
            msg.state = InboundState.FLAGGED if flags else InboundState.PROCESSED
            return
        msg.state = InboundState.PROCESSED
        await self._draft(session, msg, sequence, record, now)

    async def _apply_stop(self, session: AsyncSession, msg: InboundMessage, sequence: Optional[EmailSequence],
                          now: datetime) -> None:
        """Website suppression list FIRST (reason reply_stop), then locally: the display mirror, an opt-out row (E1
        reads it), every live sequence of the address stopped. A failed website write is stored PENDING (retried by
        every reconcile) and E2's global pause SUPPRESSION_WRITE_FAILED blocks every send until a person clears it."""
        sending, rules = self._services(session)
        targets: list[tuple[str, Optional[str]]] = []
        if sequence is not None:
            targets.append((sequence.recipient_hash, sequence.recipient_email))
        for address in (msg.from_address, msg.reply_to_address):
            if address and email_hash(address) not in [t[0] for t in targets]:
                targets.append((email_hash(address), address))
        for target_hash, address in targets:
            ok = await rules.suppress(target_hash, "reply_stop", f"reply:inbound:{msg.id}", now)
            session.add(ReplySuppression(
                inbound_message_id=msg.id, email_hash=target_hash, reason="reply_stop",
                website_state=WebsiteWrite.WRITTEN if ok else WebsiteWrite.PENDING, attempts=1,
                last_error=None if ok else "the website did not confirm the write", created_at=now,
                written_at=now if ok else None))
            if address and (await session.execute(select(OptOut.id).where(
                    OptOut.email == address.lower()))).scalar_one_or_none() is None:
                session.add(OptOut(email=address.lower(), domain=address.lower().rsplit("@", 1)[-1],
                                   reason="reply_stop", source="EMAIL_REPLY", created_at=now))
            live = (await session.execute(select(EmailSequence).where(
                EmailSequence.recipient_hash == target_hash))).scalars().all()
            for row in live:
                if row.state in (SequenceState.ACTIVE, SequenceState.PAUSED_OOO):
                    await sending.stop_sequence(row.id, SequenceState.STOPPED_SUPPRESSED, "stop reply", now)
                elif row.state == SequenceState.STOPPED_REPLY:
                    # The reply already cancelled the follow-ups; the more exact reason is recorded.
                    row.state, row.stop_reason = SequenceState.STOPPED_SUPPRESSED, "stop reply"
        await session.flush()

    async def _stop_confirmation(self, session: AsyncSession, msg: InboundMessage, sequence: EmailSequence,
                                 now: datetime) -> None:
        """ONE optional "Understood, thank you" line. Default: never sent. Only the founder can send it, by its id."""
        recipient = msg.reply_to_address or msg.from_address
        if not recipient:
            return
        existing = (await session.execute(select(ReplyDraft.id).where(
            ReplyDraft.kind == DraftKind.STOP_CONFIRMATION, ReplyDraft.sequence_id == sequence.id))).first()
        if existing is not None:
            return
        name = (self.config.sender_name or "").strip()
        body = STOP_CONFIRMATION_TEXT + (f"\n\n{name}\nSiteBlitz" if name else "")
        session.add(ReplyDraft(kind=DraftKind.STOP_CONFIRMATION, inbound_message_id=msg.id, sequence_id=sequence.id,
                               business_id=sequence.business_id, mailbox_id=sequence.mailbox_id,
                               recipient_email=recipient, labels=[L.STOP], language="en",
                               subject=reply_subject(msg.subject or "SiteBlitz")[:300], body=body,
                               state=DraftState.OPTIONAL, errors=[], created_at=now))
        await session.flush()

    # ─── drafts ──────────────────────────────────────────────────────────

    async def _thread(self, session: AsyncSession, sequence: EmailSequence, upto: InboundMessage) -> list[dict]:
        entries = []
        sent = (await session.execute(select(SendRecord).where(
            SendRecord.sequence_id == sequence.id, SendRecord.state == SendState.ACCEPTED))).scalars().all()
        for record in sent:
            entries.append((aware(record.accepted_at or record.submitted_at or record.created_at),
                            {"direction": "out", "channel": "email",
                             "sent_at": iso(record.accepted_at or record.submitted_at),
                             "text": sanitize(record.body or "")[:1500]}))
        inbound = (await session.execute(select(InboundMessage).where(
            InboundMessage.sequence_id == sequence.id, InboundMessage.kind == InboundKind.HUMAN,
            InboundMessage.received_at <= upto.received_at, InboundMessage.id != upto.id))).scalars().all()
        for row in inbound:
            entries.append((aware(row.received_at), {"direction": "in", "channel": "email",
                                                     "sent_at": iso(row.received_at),
                                                     "text": sanitize(row.body_text or "")[:1500]}))
        entries.sort(key=lambda e: e[0])
        return [e[1] for e in entries[-THREAD_ENTRIES:]]

    async def _snapshot(self, session: AsyncSession, msg: InboundMessage, sequence: EmailSequence,
                        business: Business, city: Optional[str], now: datetime) -> OpportunitySnapshot:
        existing = (await session.execute(select(OpportunitySnapshot).where(
            OpportunitySnapshot.sequence_id == sequence.id).order_by(OpportunitySnapshot.id.desc()).limit(1))
        ).scalar_one_or_none()
        if existing is not None and aware(existing.expires_at) > now + timedelta(days=1):
            return existing
        row = await session.get(EmailEligibility, sequence.eligibility_id) if sequence.eligibility_id else None
        if row is None or row.observation_type is None or row.observation_checked_at is None:
            raise SnapshotUnavailable("the lead has no stored observation")
        mailbox = await session.get(Mailbox, sequence.mailbox_id)
        payload = build_payload(
            business_name=business.name, city=city, vertical=row.vertical, observation_type=row.observation_type.value,
            observation_text=row.observation_text or "", checked_at=aware(row.observation_checked_at),
            evidence_path=row.observation_evidence_path, reply_email=mailbox.address, facts_md=self.deps.facts_md,
            recording=load_recording(row.vertical))
        result = await self.deps.snapshots.create(payload)
        snapshot = OpportunitySnapshot(business_id=business.id, sequence_id=sequence.id, inbound_message_id=msg.id,
                                       slug=result.slug, url=result.url, expires_at=result.expires_at,
                                       concept_demo=payload.get("concept_demo"),
                                       with_evidence_image="evidence_image_base64" in payload, created_at=now)
        session.add(snapshot)
        await session.flush()
        return snapshot

    async def _draft(self, session: AsyncSession, msg: InboundMessage, sequence: EmailSequence,
                     record: Optional[SendRecord], now: datetime, regenerations: int = 0) -> Optional[ReplyDraft]:
        """The AI writer drafts from approved facts only; the draft waits for the founder."""
        from backend.app.engines.writer.writer import build_lead

        recipient = msg.reply_to_address or msg.from_address
        if not recipient:
            msg.flags, msg.state = list(msg.flags or []) + ["NO_REPLY_ADDRESS"], InboundState.FLAGGED
            return None
        writer = self.deps.writer_factory()
        business = await session.get(Business, sequence.business_id)
        city = (await session.execute(select(BusinessLocation.city).where(
            BusinessLocation.business_id == business.id).limit(1))).scalar_one_or_none()
        eligibility = (await session.get(EmailEligibility, sequence.eligibility_id)
                       if sequence.eligibility_id else None)
        snapshot = None
        if set(msg.labels or []) & set(L.SNAPSHOT_LABELS):
            try:
                snapshot = await self._snapshot(session, msg, sequence, business, city, now)
            except SnapshotUnavailable as exc:
                msg.flags = list(msg.flags or []) + [f"SNAPSHOT_FAILED: {exc}"[:120]]
                msg.state = InboundState.FLAGGED
                return None
        observations = []
        if eligibility is not None and eligibility.observation_type is not None:
            observations.append({"type": eligibility.observation_type.value, "evidence_value": None,
                                 "checked_at": aware(eligibility.observation_checked_at).date().isoformat()
                                 if eligibility.observation_checked_at else None, "check_id": None})
        lead = build_lead(lead_id=f"b{business.id}", business_name=business.name, category=None, city=city,
                          country=sequence.country or business.country_code, observations=observations,
                          thread=await self._thread(session, sequence, msg))
        if eligibility is not None and eligibility.vertical:
            lead["vertical"] = eligibility.vertical
        full_text = msg.body_text or (msg.meta or {}).get("fallback_text") or ""
        task = {"channel": "email", "touch": None, "inbound_message": sanitize(full_text)[:4000],
                "attachments_allowed": [snapshot.url] if snapshot else [], "reply_labels": list(msg.labels),
                "sample_page_url": snapshot.url if snapshot else None}
        try:
            result = await asyncio.to_thread(writer.write, lead, task)
        except Exception as exc:   # model down / unexpected answer: no draft, the founder sees why (launch gate e)
            msg.flags = list(msg.flags or []) + [f"WRITER_ERROR: {type(exc).__name__}"]
            msg.state = InboundState.FLAGGED
            return None
        if result.status != "READY":
            reason = result.hold_reason or "; ".join(result.errors) or result.status
            msg.flags = list(msg.flags or []) + [f"WRITER_{result.status}: {reason}"[:120]]
            msg.state = InboundState.FLAGGED
            return None
        output = result.output or {}
        model_text = "\n".join(x for x in ((output.get("body") or ""), (output.get("signoff") or "")) if x)
        violations = L.draft_violations(model_text, writer.facts.text)
        if snapshot is not None and snapshot.url not in (result.text or ""):
            violations.append("the sample page link is missing")
        for old in (await session.execute(select(ReplyDraft).where(
                ReplyDraft.sequence_id == sequence.id, ReplyDraft.kind == DraftKind.REPLY,
                ReplyDraft.state == DraftState.WAITING))).scalars().all():
            if violations and old.inbound_message_id == msg.id:
                continue   # a blocked regeneration never replaces a usable draft for the same message
            old.state, old.decided_at, old.decided_by = DraftState.SUPERSEDED, now, "system"
            old.decision_note = f"a newer draft (inbound {msg.id})"
        subject = reply_subject(msg.subject or (record.subject if record else "") or business.name)
        draft = ReplyDraft(kind=DraftKind.REPLY, inbound_message_id=msg.id, sequence_id=sequence.id,
                           business_id=business.id, mailbox_id=sequence.mailbox_id,
                           recipient_email=recipient, labels=list(msg.labels),
                           language=output.get("declared_language"), subject=subject[:300], body=result.text,
                           snapshot_id=snapshot.id if snapshot else None,
                           state=DraftState.BLOCKED if violations else DraftState.WAITING, errors=violations,
                           regenerations=regenerations, created_at=now)
        session.add(draft)
        if violations:
            msg.flags = list(msg.flags or []) + ["DRAFT_BLOCKED"]
            msg.state = InboundState.FLAGGED
        await session.flush()
        return draft

    # ─── later steps of a reconcile ──────────────────────────────────────

    async def resume_ooo(self, now: datetime) -> int:
        resumed = 0
        async with self.factory() as session:
            sending, _ = self._services(session)
            paused = (await session.execute(select(EmailSequence).where(
                EmailSequence.state == SequenceState.PAUSED_OOO))).scalars().all()
            for sequence in paused:
                latest = (await session.execute(select(InboundMessage).where(
                    InboundMessage.sequence_id == sequence.id, InboundMessage.kind == InboundKind.AUTO_REPLY)
                    .order_by(InboundMessage.received_at.desc(), InboundMessage.id.desc()).limit(1))
                ).scalar_one_or_none()
                if latest is not None and latest.ooo_resume_at is not None and aware(latest.ooo_resume_at) <= now:
                    await sending.stop_sequence(sequence.id, SequenceState.ACTIVE,
                                                f"resumed after out of office (inbound {latest.id})", now)
                    resumed += 1
            await session.commit()
        return resumed

    async def retry_pending_suppressions(self, now: datetime) -> int:
        written = 0
        async with self.factory() as session:
            pending = (await session.execute(select(ReplySuppression).where(
                ReplySuppression.website_state == WebsiteWrite.PENDING))).scalars().all()
            for row in pending:
                row.attempts += 1
                try:
                    if self.deps.suppression is None:
                        raise SuppressionUnavailable("no suppression client")
                    await self.deps.suppression.add(row.email_hash, row.reason, f"reply:retry:{row.id}")
                except (SuppressionUnavailable, ValueError) as exc:
                    row.last_error = str(exc)[:300]
                    continue
                row.website_state, row.written_at, row.last_error = WebsiteWrite.WRITTEN, now, None
                written += 1
            await session.commit()
        return written

    async def sync_website_unsubscribes(self, now: datetime) -> int:
        """Copy the website's list into the DISPLAY mirror and stop local sequences of addresses that unsubscribed
        by link (the worker would refuse them anyway; this keeps the schedule and the brief honest)."""
        if self.deps.suppression is None:
            return 0
        stopped = 0
        async with self.factory() as session:
            sending, rules = self._services(session)
            # The whole list every time (small in the pilot): the mirror also holds rows this app wrote itself, so
            # its newest row is no safe cursor for what the website stored earlier.
            try:
                await rules.sync_mirror(None, now)
            except SuppressionUnavailable as exc:
                logger.info("suppression_mirror_sync_failed", error=str(exc)[:100])
                await session.rollback()
                return 0
            mirrored = set((await session.execute(select(SuppressionMirror.email_hash))).scalars().all())
            live = (await session.execute(select(EmailSequence).where(
                EmailSequence.state.in_([SequenceState.ACTIVE, SequenceState.PAUSED_OOO])))).scalars().all()
            for sequence in live:
                if sequence.recipient_hash in mirrored:
                    await sending.stop_sequence(sequence.id, SequenceState.STOPPED_SUPPRESSED,
                                                "suppressed on the website", now)
                    stopped += 1
            await session.commit()
        return stopped

    # ─── inbound list / close ────────────────────────────────────────────

    async def list_inbound(self, session: AsyncSession, needs_founder: bool = False, limit: int = 100) -> list[dict]:
        stmt = (select(InboundMessage, Business.name)
                .join(Business, Business.id == InboundMessage.business_id, isouter=True)
                .order_by(InboundMessage.received_at.desc(), InboundMessage.id.desc()))
        if needs_founder:
            stmt = stmt.where(InboundMessage.state.in_([InboundState.FLAGGED, InboundState.NEEDS_REVIEW,
                                                        InboundState.ERROR]), InboundMessage.handled_at.is_(None))
        rows = (await session.execute(stmt.limit(limit))).all()
        return [inbound_dict(msg, name) for msg, name in rows]

    async def close_inbound(self, session: AsyncSession, inbound_id: int, closed_by: str, note: str) -> dict:
        msg = await session.get(InboundMessage, inbound_id)
        if msg is None:
            raise NotFound(f"inbound message {inbound_id} not found")
        if msg.handled_at is not None:
            raise Conflict(f"inbound message {inbound_id} was already handled")
        now = self.now()
        msg.handled_at, msg.handled_by, msg.handled_note = now, closed_by, note
        await session.flush()
        await apply_reply_backlog(session, self.config, self.deps.suppression, now)
        return inbound_dict(msg)

    # ─── draft list / approve / reject / regenerate ──────────────────────

    async def list_drafts(self, session: AsyncSession, state: Optional[str] = "WAITING",
                          include_optional: bool = False) -> list[dict]:
        stmt = (select(ReplyDraft, Business.name, OpportunitySnapshot.url, InboundMessage.body_text)
                .join(Business, Business.id == ReplyDraft.business_id, isouter=True)
                .join(OpportunitySnapshot, OpportunitySnapshot.id == ReplyDraft.snapshot_id, isouter=True)
                .join(InboundMessage, InboundMessage.id == ReplyDraft.inbound_message_id)
                .order_by(ReplyDraft.created_at, ReplyDraft.id))
        if state:
            states = [DraftState(state)] + ([DraftState.OPTIONAL] if include_optional else [])
            stmt = stmt.where(ReplyDraft.state.in_(states))
        elif not include_optional:
            stmt = stmt.where(ReplyDraft.state != DraftState.OPTIONAL)
        await self._sync_uncertain(session)
        rows = (await session.execute(stmt)).all()
        return [draft_dict(d, name, url, text) for d, name, url, text in rows]

    async def _sync_uncertain(self, session: AsyncSession) -> None:
        """A draft whose UNCERTAIN send a person resolved (E2 /send-records/{id}/resolve) takes that outcome; a draft
        left SENDING by a crash takes its record's state (the worker's start-up turns SUBMITTING into UNCERTAIN)."""
        rows = (await session.execute(select(ReplyDraft, SendRecord.state)
                                      .join(SendRecord, SendRecord.id == ReplyDraft.send_record_id)
                                      .where(ReplyDraft.state.in_([DraftState.UNCERTAIN, DraftState.SENDING])))
                ).all()
        for draft, state in rows:
            if state == SendState.ACCEPTED:
                draft.state = DraftState.SENT
            elif state == SendState.FAILED:
                draft.state = DraftState.FAILED
            elif state == SendState.UNCERTAIN:
                draft.state = DraftState.UNCERTAIN
        await session.flush()

    async def reject(self, session: AsyncSession, draft_id: int, rejected_by: str, note: str,
                     close_thread: bool = False) -> dict:
        draft = await session.get(ReplyDraft, draft_id)
        if draft is None:
            raise NotFound(f"draft {draft_id} not found")
        if draft.state not in (DraftState.WAITING, DraftState.OPTIONAL, DraftState.BLOCKED, DraftState.FAILED):
            raise Conflict(f"draft {draft_id} is {draft.state.value}")
        now = self.now()
        draft.state, draft.decided_at, draft.decided_by, draft.decision_note = (DraftState.REJECTED, now,
                                                                                rejected_by, note)
        if close_thread:
            msg = await session.get(InboundMessage, draft.inbound_message_id)
            if msg.handled_at is None:
                msg.handled_at, msg.handled_by, msg.handled_note = now, rejected_by, f"draft {draft_id} rejected: {note}"
        await session.flush()
        await apply_reply_backlog(session, self.config, self.deps.suppression, now)
        return draft_dict(draft)

    async def regenerate(self, draft_id: int, requested_by: str, note: Optional[str]) -> dict:
        now = self.now()
        async with self.factory() as session:
            draft = await session.get(ReplyDraft, draft_id)
            if draft is None:
                raise NotFound(f"draft {draft_id} not found")
            if draft.kind != DraftKind.REPLY or draft.state not in (DraftState.WAITING, DraftState.REJECTED,
                                                                     DraftState.BLOCKED, DraftState.FAILED):
                raise Conflict(f"draft {draft_id} ({draft.kind.value}, {draft.state.value}) cannot be regenerated")
            if draft.regenerations >= MAX_REGENERATIONS:
                raise Conflict(f"draft {draft_id} was regenerated {MAX_REGENERATIONS} times; write to the founder")
            msg = await session.get(InboundMessage, draft.inbound_message_id)
            sequence = await session.get(EmailSequence, draft.sequence_id)
            record = await session.get(SendRecord, msg.send_record_id) if msg.send_record_id else None
            before = (draft.state, draft.decided_at, draft.decided_by, draft.decision_note)
            if draft.state == DraftState.WAITING:
                draft.state = DraftState.SUPERSEDED
            draft.decided_at, draft.decided_by = now, requested_by
            draft.decision_note = f"regenerate requested: {note or ''}"[:500]
            await session.flush()
            new = await self._draft(session, msg, sequence, record, now, regenerations=draft.regenerations + 1)
            if new is None or new.state == DraftState.BLOCKED:
                # No usable new draft (writer hold, snapshot failure, a broken reply rule): the old one stays.
                draft.state, draft.decided_at, draft.decided_by, draft.decision_note = before
            await session.commit()
            if new is None:
                raise Conflict("no new draft: " + "; ".join(msg.flags or []))
            return draft_dict(new)

    async def approve(self, draft_id: int, approved_by: str) -> dict:
        """Send one approved reply now: same mailbox as the sequence, threaded under the prospect's message, fresh
        suppression check, pauses, and the mailbox's 30-a-day ceiling (5 of which campaign mail never takes)."""
        now = self.now()
        async with self.factory() as session:
            sending, rules = self._services(session)
            draft = await session.get(ReplyDraft, draft_id)
            if draft is None:
                raise NotFound(f"draft {draft_id} not found")
            if draft.state not in (DraftState.WAITING, DraftState.OPTIONAL):
                raise Conflict(f"draft {draft_id} is {draft.state.value}, not WAITING")
            box = await session.get(Mailbox, draft.mailbox_id)
            msg = await session.get(InboundMessage, draft.inbound_message_id)
            sequence = await session.get(EmailSequence, draft.sequence_id) if draft.sequence_id else None
            missing = self.config.missing_company_facts() + self.config.missing_outreach()
            if missing:
                raise Conflict("not configured: " + ", ".join(missing))
            blocks = sending.blocking(await sending.active_pauses(), step=None, mailbox=box, sequence=None)
            if blocks:
                raise Conflict("sending is paused: " + ", ".join(f"{f.reason_code} ({f.scope.value})" for f in blocks))
            if not box.enabled:
                raise Conflict(f"mailbox {box.id} is disabled")
            password = None if box.smtp_tls == TlsMode.NONE else self.deps.password_lookup(box.slug)
            if box.smtp_tls != TlsMode.NONE and password is None:
                raise Conflict(f"{password_variable(box.slug)} is not set in .env")
            stop_confirmation = draft.kind == DraftKind.STOP_CONFIRMATION
            recipient_hash = email_hash(draft.recipient_email)
            key = (f"{STOP_CONFIRMATION_KEY}{recipient_hash}" if stop_confirmation else f"reply:draft:{draft.id}")
            zone = sched.load_zone(sequence.timezone if sequence and sequence.timezone else FOUNDER_ZONE)
            day = sched.local_date(now, zone)
            record = (await session.execute(select(SendRecord).where(
                SendRecord.idempotency_key == key))).scalar_one_or_none()
            if record is not None and record.state != SendState.SCHEDULED:
                raise Conflict(f"this reply was already submitted (send record {record.id})")
            if record is None:
                load = (await sending.capacity_book(day, day)).load(box.id, day)
                if load.total >= sched.MAILBOX_DAILY_CEILING:
                    raise Conflict(f"REPLY_CAPACITY_FULL: mailbox {box.id} already has {load.total} of "
                                   f"{sched.MAILBOX_DAILY_CEILING} messages on {day.isoformat()}")
            claimed = await session.execute(
                update(ReplyDraft).where(ReplyDraft.id == draft.id,
                                         ReplyDraft.state.in_([DraftState.WAITING, DraftState.OPTIONAL]))
                .values(state=DraftState.SENDING).execution_options(synchronize_session=False))
            if claimed.rowcount != 1:
                await session.rollback()
                raise Conflict(f"draft {draft_id} is being sent by another request")
            await session.commit()
            await session.refresh(draft)

            # Fresh suppression check (the website is the only authority). A stop confirmation goes to an address
            # that is suppressed by design: it is the one reply that skips this check, and only by its own id.
            if not stop_confirmation:
                hashes = {recipient_hash} | ({sequence.recipient_hash} if sequence else set())
                try:
                    suppressed = await self.deps.suppression.check(sorted(hashes)) if self.deps.suppression else None
                    if suppressed is None:
                        raise SuppressionUnavailable("no suppression client configured")
                except SuppressionUnavailable as exc:
                    await rules.record_suppression_unavailable(str(exc), now)
                    draft.state = DraftState.WAITING
                    await session.commit()
                    raise ServiceUnavailable(f"suppression check unavailable: {exc}")
                if suppressed & hashes:
                    draft.state, draft.decided_at, draft.decided_by = DraftState.REJECTED, now, "system"
                    draft.decision_note = "the address is on the website's suppression list"
                    await session.commit()
                    raise Conflict("the recipient is suppressed; nothing was sent")

            parents = (msg.references or "").split()
            if msg.message_id:
                parents = [p for p in parents if p != msg.message_id] + [msg.message_id]
            parents = parents[-10:]
            if record is None:
                record = SendRecord(
                    kind=SendKind.REPLY, sequence_id=sequence.id if sequence else None, step=None,
                    idempotency_key=key, mailbox_id=box.id, recipient_email=draft.recipient_email,
                    recipient_hash=recipient_hash, message_id=new_message_id(box.domain), subject=draft.subject,
                    body=draft.body, content_version="stop-confirmation-v1" if stop_confirmation else "reply-v1",
                    scheduled_for=now, local_date=day, window_label="reply", window_start=now, window_end=now,
                    state=SendState.SCHEDULED, attempts=0)
                session.add(record)
                await session.flush()
            record.approved_at, record.approved_by = now, approved_by
            try:
                outgoing = build_message(
                    mailbox_address=box.address, display_name=box.display_name, recipient=draft.recipient_email,
                    subject=draft.subject, body=draft.body, message_id=record.message_id,
                    send_record_id=str(record.id), base_url=self.config.base_url,
                    signing_secret=self.config.signing_secret, date=now, thread_parent_ids=parents)
            except Exception as exc:
                draft.state = DraftState.WAITING
                await session.commit()
                raise Conflict(f"the message could not be built: {type(exc).__name__}")
            record.state, record.submitted_at = SendState.SUBMITTING, now
            record.attempts = (record.attempts or 0) + 1
            record.hold_reason = None
            draft.send_record_id = record.id
            await session.commit()

            config = smtp_engine.SmtpConfig(box.smtp_host, box.smtp_port, box.smtp_tls.value, box.username, password,
                                            self.deps.smtp_timeout)
            result = await asyncio.to_thread(self.deps.submit, config, box.address, draft.recipient_email,
                                             outgoing.as_bytes())
            done = self.now()
            await session.refresh(record)
            record.smtp_code, record.smtp_status = result.code, result.status
            record.smtp_response = (result.response or "")[:2000] or None
            logger.info("reply_submit", draft=draft.id, record=record.id, outcome=result.outcome, code=result.code)
            if result.outcome == smtp_engine.ACCEPTED:
                record.state, record.accepted_at = SendState.ACCEPTED, done
                draft.state = DraftState.SENT
                await self._mark_answered(session, msg, draft, approved_by, done)
            elif result.outcome == smtp_engine.UNCERTAIN:
                record.state = SendState.UNCERTAIN
                draft.state = DraftState.UNCERTAIN
                await rules.record_send_result_unknown(record, done)
                await self._mark_answered(session, msg, draft, approved_by, done)
            elif result.outcome == smtp_engine.FAILED and result.phase != "mail":
                record.state = SendState.FAILED
                draft.state = DraftState.FAILED
                draft.errors = list(draft.errors or []) + [f"SMTP {result.code}: {(result.response or '')[:200]}"]
                await session.commit()
                await rules.record_smtp_refusal(record, done)
            else:
                record.state, record.submitted_at = SendState.SCHEDULED, None
                record.hold_reason = f"SMTP_NOT_SENT:{result.phase}:{result.code or 'error'}"
                draft.state = DraftState.OPTIONAL if stop_confirmation else DraftState.WAITING
                draft.errors = list(draft.errors or []) + [record.hold_reason]
                if result.mailbox_problem or result.phase == "mail":
                    await sending.raise_pause(PauseScope.MAILBOX, Reason.SMTP_UNAVAILABLE, str(box.id),
                                              detail=f"{result.phase}: {(result.response or '')[:300]}", now=done)
            draft.decided_at, draft.decided_by = done, approved_by
            await session.flush()
            await apply_reply_backlog(session, self.config, self.deps.suppression, done)
            await session.commit()
            out = draft_dict(draft)
            out["smtp"] = {"outcome": result.outcome, "code": result.code, "status": result.status}
            out["message_id"] = record.message_id
            return out

    async def _mark_answered(self, session: AsyncSession, msg: InboundMessage, draft: ReplyDraft, by: str,
                             now: datetime) -> None:
        """The approved answer covers this message and every earlier unanswered one in the same thread."""
        if draft.kind != DraftKind.REPLY:
            return
        rows = [msg]
        if msg.sequence_id:
            rows = (await session.execute(select(InboundMessage).where(
                InboundMessage.sequence_id == msg.sequence_id, InboundMessage.handled_at.is_(None),
                InboundMessage.received_at <= msg.received_at))).scalars().all()
        for row in rows:
            row.handled_at, row.handled_by = now, by
            row.handled_note = f"answered by draft {draft.id}"
        await session.flush()


FACTS_FILE = Path(__file__).resolve().parents[3] / "docs" / "outreach" / "company-facts.md"


def build_reply_loop(settings, session_factory: async_sessionmaker) -> ReplyLoop:
    """The loop with everything from settings (API and scripts/outreach_reconcile.py). The AI writer is created
    only when a draft is needed (it reads docs/outreach/ and imports the model client)."""
    config = SendingConfig.from_settings(settings)
    writer_box: dict = {}

    def writer():
        if "w" not in writer_box:
            from backend.app.engines.writer.writer import OutreachWriter
            writer_box["w"] = OutreachWriter(settings=settings)
        return writer_box["w"]

    deps = ReplyLoopDeps(
        config=config,
        suppression=SuppressionClient(settings.OUTREACH_PUBLIC_BASE_URL, settings.OUTREACH_API_KEY),
        snapshots=SnapshotClient(settings.OUTREACH_PUBLIC_BASE_URL, settings.OUTREACH_API_KEY),
        classifier=ReplyClassifier(lambda: writer().client(), api_key_set=bool(settings.ANTHROPIC_API_KEY)),
        writer_factory=writer, facts_md=FACTS_FILE.read_text(encoding="utf-8"))
    return ReplyLoop(session_factory, deps)
