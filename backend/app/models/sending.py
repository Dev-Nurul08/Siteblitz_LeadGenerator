"""
Email engine v2, phase E2 - sending core models (spec: docs/spec/email-engine-v2.md rows 5, 8-13, 16, 18, 19).

All tables are new, so an existing database gets them from `create_all` without a migration:

- `mailboxes`              the sending mailboxes (Mailforge, spec row 8). The password is NEVER stored here: the
                           worker reads it from the environment / `.env` as `MAILBOX_<SLUG>_PASSWORD`.
- `email_sequences`        one prospect's 3-touch sequence (Day 1 / 6 / 14) with ONE sender for all of it (row 9).
- `send_records`           one message: idempotency key, Message-ID, text, schedule, SMTP outcome, approval.
- `pause_flags`            automatic or manual pauses / stops (row 11); a flag blocks sends until a person clears it.
- `ramp_settings`          new first contacts per sending day (row 10); history rows, the newest one counts.
- `delivery_events`        hard / soft bounces, policy rejections, complaints: what the pause rules count.
- `suppression_mirror`     a local copy of the website's suppression list FOR DISPLAY ONLY. It never authorises a
                           send: the worker asks the website fresh before every submission (row 13).

State machines (docs/outreach/e2-notes.md):
  SendRecord: SCHEDULED -> SUBMITTING -> ACCEPTED | FAILED | UNCERTAIN;  SCHEDULED -> CANCELLED;
              SUBMITTING -> UNCERTAIN (crash / restart); UNCERTAIN -> ACCEPTED | FAILED only by a person (API).
  Sequence:   ACTIVE -> COMPLETED | STOPPED_REPLY | STOPPED_SUPPRESSED | STOPPED_BOUNCE | CANCELLED;
              ACTIVE <-> PAUSED_OOO (E4, out-of-office).
"""

import enum
from datetime import date, datetime
from typing import Optional

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    Integer,
    JSON,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.database import Base

JSON_TYPE = JSON().with_variant(JSONB, "postgresql")


class TlsMode(str, enum.Enum):
    STARTTLS = "starttls"   # port 587, upgrade with STARTTLS
    SSL = "ssl"             # port 465, TLS from the first byte
    NONE = "none"           # only for a loopback test server (127.0.0.1 / localhost); refused for any other host


class SequenceState(str, enum.Enum):
    ACTIVE = "ACTIVE"
    STOPPED_REPLY = "STOPPED_REPLY"            # any reply stops the sequence (spec row 6)
    STOPPED_SUPPRESSED = "STOPPED_SUPPRESSED"  # unsubscribe / "stop" / complaint / manual do-not-contact
    STOPPED_BOUNCE = "STOPPED_BOUNCE"          # hard bounce
    PAUSED_OOO = "PAUSED_OOO"                  # out-of-office reply (E4)
    COMPLETED = "COMPLETED"                    # step 3 accepted
    CANCELLED = "CANCELLED"                    # by a person, a failed step, or a false observation


STOPPED_STATES = {SequenceState.STOPPED_REPLY, SequenceState.STOPPED_SUPPRESSED, SequenceState.STOPPED_BOUNCE,
                  SequenceState.COMPLETED, SequenceState.CANCELLED}


class SendState(str, enum.Enum):
    SCHEDULED = "SCHEDULED"
    SUBMITTING = "SUBMITTING"   # committed BEFORE the SMTP conversation starts
    ACCEPTED = "ACCEPTED"       # the receiving (submission) server answered 250 to the message
    UNCERTAIN = "UNCERTAIN"     # timeout / connection loss after DATA: may or may not have been accepted
    FAILED = "FAILED"           # a definite refusal (5xx, or a person resolved an UNCERTAIN record as failed)
    CANCELLED = "CANCELLED"     # never submitted (suppressed, reply, stop, false observation, ...)


# States that use a slot of the mailbox's daily capacity (a cancelled record frees its slot).
CAPACITY_STATES = (SendState.SCHEDULED, SendState.SUBMITTING, SendState.ACCEPTED, SendState.UNCERTAIN,
                   SendState.FAILED)
# States in which a message may have left the laptop.
SUBMITTED_STATES = (SendState.SUBMITTING, SendState.ACCEPTED, SendState.UNCERTAIN)


class SendKind(str, enum.Enum):
    CAMPAIGN = "CAMPAIGN"   # sequence steps 1-3 (25 a day per mailbox)
    REPLY = "REPLY"         # answers to prospects (E4; the 5 a day kept back count here)
    TEST = "TEST"           # seed tests (E6); count against the 30 a day ceiling too


class PauseScope(str, enum.Enum):
    GLOBAL = "GLOBAL"               # every send
    NEW_CONTACTS = "NEW_CONTACTS"   # step-1 messages only (reply backlog rule)
    DOMAIN = "DOMAIN"               # one sending domain (scope_value = the domain)
    MAILBOX = "MAILBOX"             # one mailbox (scope_value = the mailbox id)
    SOURCE = "SOURCE"               # one lead source (scope_value = e.g. "email_finder")
    SOURCE_BATCH = "SOURCE_BATCH"   # one sourcing batch (scope_value = the capture origin, "email_finder:2026-11-10")


class PauseLevel(str, enum.Enum):
    PAUSE = "PAUSE"   # stop the affected activity pending review
    STOP = "STOP"     # retire / rebuild the affected configuration before a restart (spec row 11)


class DeliveryEventKind(str, enum.Enum):
    HARD_BOUNCE = "HARD_BOUNCE"
    SOFT_BOUNCE = "SOFT_BOUNCE"
    POLICY_REJECTION = "POLICY_REJECTION"
    UNKNOWN_BOUNCE = "UNKNOWN_BOUNCE"
    COMPLAINT = "COMPLAINT"


class Mailbox(Base):
    __tablename__ = "mailboxes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # Upper-case key for the password variable: MAILBOX_<SLUG>_PASSWORD (A-Z, 0-9, _).
    slug: Mapped[str] = mapped_column(String(40), nullable=False, unique=True)
    address: Mapped[str] = mapped_column(String(320), nullable=False, unique=True)
    display_name: Mapped[str] = mapped_column(String(60), nullable=False)   # a real founder name (spec row 8)
    domain: Mapped[str] = mapped_column(String(255), nullable=False)        # the part after @ (the sending domain)
    enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    smtp_host: Mapped[str] = mapped_column(String(255), nullable=False)
    smtp_port: Mapped[int] = mapped_column(Integer, nullable=False)
    smtp_tls: Mapped[TlsMode] = mapped_column(Enum(TlsMode), nullable=False)
    imap_host: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    imap_port: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    imap_tls: Mapped[Optional[TlsMode]] = mapped_column(Enum(TlsMode), nullable=True)
    username: Mapped[str] = mapped_column(String(320), nullable=False)
    disabled_reason: Mapped[Optional[str]] = mapped_column(String(300), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(),
                                                 onupdate=func.now())


class EmailSequence(Base):
    """One prospect's sequence. `mailbox_id` never changes (one sender for the whole sequence, spec row 9)."""

    __tablename__ = "email_sequences"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    business_id: Mapped[int] = mapped_column(Integer, ForeignKey("businesses.id", ondelete="CASCADE"),
                                             nullable=False)
    eligibility_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("email_eligibility.id", ondelete="SET NULL"), nullable=True)
    mailbox_id: Mapped[int] = mapped_column(Integer, ForeignKey("mailboxes.id"), nullable=False)
    recipient_email: Mapped[str] = mapped_column(String(320), nullable=False)
    recipient_hash: Mapped[str] = mapped_column(String(64), nullable=False)   # sha256_hex(email.strip().lower())
    country: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    timezone: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)   # IANA name, e.g. Asia/Kolkata
    # Lead source for the pause rules: source = "email_finder", batch = "email_finder:2026-11-10" (capture origin).
    source: Mapped[str] = mapped_column(String(100), nullable=False)
    source_batch: Mapped[str] = mapped_column(String(100), nullable=False)
    current_step: Mapped[int] = mapped_column(Integer, nullable=False, default=0)   # last ACCEPTED step (0 = none)
    state: Mapped[SequenceState] = mapped_column(Enum(SequenceState), nullable=False, default=SequenceState.ACTIVE)
    stop_reason: Mapped[Optional[str]] = mapped_column(String(300), nullable=True)
    stopped_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        Index("ix_email_sequences_business", "business_id"),
        Index("ix_email_sequences_hash", "recipient_hash"),
        Index("ix_email_sequences_state", "state"),
    )


class SendRecord(Base):
    __tablename__ = "send_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    kind: Mapped[SendKind] = mapped_column(Enum(SendKind), nullable=False, default=SendKind.CAMPAIGN)
    sequence_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("email_sequences.id", ondelete="CASCADE"), nullable=True)
    step: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)   # 1, 2, 3 for campaign mail
    # "seq:<sequence id>:step:<n>" for campaign mail: the database refuses a second record for the same step.
    idempotency_key: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    mailbox_id: Mapped[int] = mapped_column(Integer, ForeignKey("mailboxes.id"), nullable=False)
    recipient_email: Mapped[str] = mapped_column(String(320), nullable=False)
    recipient_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    message_id: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)   # <uuid@sending-domain>
    subject: Mapped[Optional[str]] = mapped_column(String(300), nullable=True)
    body: Mapped[Optional[str]] = mapped_column(Text, nullable=True)   # without the unsubscribe line (app adds it)
    content_version: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    # Schedule: UTC instant + the recipient-local day and window it belongs to.
    scheduled_for: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    local_date: Mapped[date] = mapped_column(Date, nullable=False)
    window_label: Mapped[str] = mapped_column(String(20), nullable=False)        # "09:00-11:30"
    window_start: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)   # UTC
    window_end: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)     # UTC

    state: Mapped[SendState] = mapped_column(Enum(SendState), nullable=False, default=SendState.SCHEDULED)
    hold_reason: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)   # why the worker skipped it
    cancel_reason: Mapped[Optional[str]] = mapped_column(String(300), nullable=True)
    attempts: Mapped[int] = mapped_column(Integer, nullable=False, default=0)   # SMTP conversations started
    smtp_code: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    smtp_status: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)   # enhanced code, e.g. 5.1.1
    smtp_response: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    submitted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    accepted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    approved_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    approved_by: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    resolved_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    resolved_by: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    resolution_note: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(),
                                                 onupdate=func.now())

    __table_args__ = (
        Index("ix_send_records_due", "state", "scheduled_for"),
        Index("ix_send_records_mailbox_day", "mailbox_id", "local_date"),
        Index("ix_send_records_hash", "recipient_hash"),
        Index("ix_send_records_sequence", "sequence_id", "step"),
    )


class PauseFlag(Base):
    """Active while `cleared_at` is NULL. Cleared only by a person through the API (or, for the reply backlog,
    by the system once the backlog is empty), with who, when and a note."""

    __tablename__ = "pause_flags"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    scope: Mapped[PauseScope] = mapped_column(Enum(PauseScope), nullable=False)
    scope_value: Mapped[str] = mapped_column(String(320), nullable=False, default="")   # "" for GLOBAL
    level: Mapped[PauseLevel] = mapped_column(Enum(PauseLevel), nullable=False, default=PauseLevel.PAUSE)
    reason_code: Mapped[str] = mapped_column(String(50), nullable=False)
    detail: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_by: Mapped[str] = mapped_column(String(100), nullable=False, default="system")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    cleared_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    cleared_by: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    clear_note: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    __table_args__ = (Index("ix_pause_flags_active", "cleared_at", "scope"),)


class RampSetting(Base):
    """New first contacts per sending day, app-wide (spec row 10). The newest row is the current setting; rows are
    only added by POST /api/v1/outreach/settings/ramp, which records who and when. No row = pilot not started = 0."""

    __tablename__ = "ramp_settings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    stage: Mapped[int] = mapped_column(Integer, nullable=False)          # 0 = not started, 1-4 = pilot weeks
    daily_new_limit: Mapped[int] = mapped_column(Integer, nullable=False)
    changed_by: Mapped[str] = mapped_column(String(100), nullable=False)
    note: Mapped[str] = mapped_column(String(500), nullable=False)
    changed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class DeliveryEvent(Base):
    __tablename__ = "delivery_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    kind: Mapped[DeliveryEventKind] = mapped_column(Enum(DeliveryEventKind), nullable=False)
    send_record_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("send_records.id", ondelete="SET NULL"), nullable=True)
    recipient_hash: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    mailbox_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    sending_domain: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    source: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    source_batch: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    credible: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)   # complaints: a person's call
    smtp_status: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    detail: Mapped[Optional[dict]] = mapped_column(JSON_TYPE, nullable=True)
    origin: Mapped[str] = mapped_column(String(30), nullable=False)   # smtp | dsn | reply | manual
    occurred_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    __table_args__ = (
        Index("ix_delivery_events_kind_time", "kind", "occurred_at"),
        Index("ix_delivery_events_hash", "recipient_hash"),
    )


class SuppressionMirror(Base):
    """DISPLAY ONLY. A copy of the website's suppression list (GET /api/outreach/suppressions?since=). It is never
    read to decide that an address may be emailed; the worker asks the website fresh before every submission."""

    __tablename__ = "suppression_mirror"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email_hash: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    reason: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    suppressed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    fetched_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


__all__ = [
    "TlsMode", "SequenceState", "STOPPED_STATES", "SendState", "CAPACITY_STATES", "SUBMITTED_STATES", "SendKind",
    "PauseScope", "PauseLevel", "DeliveryEventKind", "Mailbox", "EmailSequence", "SendRecord", "PauseFlag",
    "RampSetting", "DeliveryEvent", "SuppressionMirror",
]
