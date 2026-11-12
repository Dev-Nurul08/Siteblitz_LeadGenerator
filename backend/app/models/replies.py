"""
Email engine v2, phase E4 - the reply loop (spec rows 11, 13-16; docs/outreach/e4-notes.md).

All tables are new, so an existing database gets them from `create_all` without a migration:

- `imap_folder_states`     per mailbox + folder: the IMAP UIDVALIDITY and the last UID already stored.
- `mailbox_reconciles`     per mailbox: when the last full read of its folders started / succeeded (24 h rule).
- `inbound_messages`       one message read over IMAP: headers, the new text (quoted history stripped), labels, state.
                           The raw message is NOT stored (only its size); a DSN is parsed when it is read.
- `reply_drafts`           AI-written answers waiting for the founder (approve / reject / regenerate), plus the
                           optional one-line "stop" confirmation that is never sent unless the founder approves it.
- `reply_suppressions`     "stop" replies: written to the website's suppression list first, then locally; a failed
                           website write stays PENDING and is retried by every reconcile.
- `opportunity_snapshots`  snapshot pages created on the website for an interested / sample-requested reply.
- `brief_runs`             when the daily brief was generated ("since the last brief").

State machines:
  InboundMessage: NEW -> PROCESSED | FLAGGED (the founder must look) | NEEDS_REVIEW (no label could be given,
                  e.g. no API key) | IGNORED (our own copy, read receipt, list mail); ERROR -> retried (max 3).
  ReplyDraft:     WAITING -> SENDING -> SENT | FAILED | UNCERTAIN;  WAITING -> REJECTED | SUPERSEDED;
                  OPTIONAL (stop confirmation) -> SENDING -> ...;  BLOCKED = the draft broke a reply rule (never
                  listed for approval).
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
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.database import Base
from backend.app.models.sending import JSON_TYPE


class InboundKind(str, enum.Enum):
    HUMAN = "HUMAN"              # a person wrote it (or nothing says otherwise)
    AUTO_REPLY = "AUTO_REPLY"    # out-of-office / auto-responder (headers or a typical subject)
    DSN = "DSN"                  # delivery status notification (bounce / delay)
    FEEDBACK = "FEEDBACK"        # ARF feedback report (a provider's spam complaint)
    AUTOMATED = "AUTOMATED"      # read receipt, mailing-list / bulk mail: not a reply, never answered
    OWN = "OWN"                  # sent by one of our own mailboxes (a copy): ignored


class InboundState(str, enum.Enum):
    NEW = "NEW"
    PROCESSED = "PROCESSED"
    FLAGGED = "FLAGGED"            # the founder must look (complaint, commitment request, unmatched, ...)
    NEEDS_REVIEW = "NEEDS_REVIEW"  # no commercial label could be given (no API key, model error)
    IGNORED = "IGNORED"
    ERROR = "ERROR"


class DraftState(str, enum.Enum):
    WAITING = "WAITING"        # ready for the founder's approval
    OPTIONAL = "OPTIONAL"      # stop confirmation: never listed or sent unless the founder picks it by id
    SENDING = "SENDING"
    SENT = "SENT"
    FAILED = "FAILED"
    UNCERTAIN = "UNCERTAIN"
    REJECTED = "REJECTED"
    SUPERSEDED = "SUPERSEDED"
    BLOCKED = "BLOCKED"        # broke a reply rule (discount, date, guarantee, refund, contract, missing link)


class DraftKind(str, enum.Enum):
    REPLY = "REPLY"
    STOP_CONFIRMATION = "STOP_CONFIRMATION"


class WebsiteWrite(str, enum.Enum):
    WRITTEN = "WRITTEN"
    PENDING = "PENDING"


class ImapFolderState(Base):
    __tablename__ = "imap_folder_states"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    mailbox_id: Mapped[int] = mapped_column(Integer, ForeignKey("mailboxes.id", ondelete="CASCADE"), nullable=False)
    folder: Mapped[str] = mapped_column(String(200), nullable=False)
    uidvalidity: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    last_uid: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    last_success_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    uidvalidity_changed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    __table_args__ = (UniqueConstraint("mailbox_id", "folder", name="uq_imap_folder_states_mailbox_folder"),)


class MailboxReconcile(Base):
    __tablename__ = "mailbox_reconciles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    mailbox_id: Mapped[int] = mapped_column(Integer, ForeignKey("mailboxes.id", ondelete="CASCADE"), nullable=False,
                                            unique=True)
    last_attempt_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    last_success_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    last_error: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    last_new_messages: Mapped[int] = mapped_column(Integer, nullable=False, default=0)


class InboundMessage(Base):
    __tablename__ = "inbound_messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    mailbox_id: Mapped[int] = mapped_column(Integer, ForeignKey("mailboxes.id", ondelete="CASCADE"), nullable=False)
    folder: Mapped[str] = mapped_column(String(200), nullable=False, default="INBOX")
    uidvalidity: Mapped[int] = mapped_column(Integer, nullable=False)
    uid: Mapped[int] = mapped_column(Integer, nullable=False)
    message_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    in_reply_to: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    references: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    from_address: Mapped[Optional[str]] = mapped_column(String(320), nullable=True)
    from_hash: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    reply_to_address: Mapped[Optional[str]] = mapped_column(String(320), nullable=True)
    subject: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    received_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    body_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)       # new text, quoted history removed
    signature_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # below a "-- " line, kept apart
    had_quote: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    raw_size: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    raw_sha256: Mapped[str] = mapped_column(String(64), nullable=False)
    kind: Mapped[InboundKind] = mapped_column(Enum(InboundKind), nullable=False, default=InboundKind.HUMAN)
    meta: Mapped[Optional[dict]] = mapped_column(JSON_TYPE, nullable=True)   # auto-reply headers, DSN / ARF result

    labels: Mapped[list] = mapped_column(JSON_TYPE, nullable=False, default=list)
    label_source: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)   # rules | rules+model | ...
    flags: Mapped[list] = mapped_column(JSON_TYPE, nullable=False, default=list)     # why the founder must look
    model_summary: Mapped[Optional[str]] = mapped_column(String(300), nullable=True)
    language: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    state: Mapped[InboundState] = mapped_column(Enum(InboundState), nullable=False, default=InboundState.NEW)
    error: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    attempts: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    sequence_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("email_sequences.id", ondelete="SET NULL"), nullable=True)
    send_record_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("send_records.id", ondelete="SET NULL"), nullable=True)
    business_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    match_method: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)   # in_reply_to | references | address

    ooo_return_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    ooo_resume_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    # When an answer stopped being owed: a draft was approved, or the founder closed the thread.
    handled_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    handled_by: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    handled_note: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    processed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint("mailbox_id", "folder", "uidvalidity", "uid", name="uq_inbound_messages_uid"),
        Index("ix_inbound_messages_state", "state"),
        Index("ix_inbound_messages_sequence", "sequence_id"),
        Index("ix_inbound_messages_message_id", "message_id"),
        Index("ix_inbound_messages_received", "received_at"),
    )


class ReplyDraft(Base):
    __tablename__ = "reply_drafts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    kind: Mapped[DraftKind] = mapped_column(Enum(DraftKind), nullable=False, default=DraftKind.REPLY)
    inbound_message_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("inbound_messages.id", ondelete="CASCADE"), nullable=False)
    sequence_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("email_sequences.id", ondelete="SET NULL"), nullable=True)
    business_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    mailbox_id: Mapped[int] = mapped_column(Integer, ForeignKey("mailboxes.id"), nullable=False)
    recipient_email: Mapped[str] = mapped_column(String(320), nullable=False)
    labels: Mapped[list] = mapped_column(JSON_TYPE, nullable=False, default=list)
    language: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    subject: Mapped[str] = mapped_column(String(300), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)   # the whole text incl. signature (no unsubscribe line)
    snapshot_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("opportunity_snapshots.id", ondelete="SET NULL"), nullable=True)
    state: Mapped[DraftState] = mapped_column(Enum(DraftState), nullable=False, default=DraftState.WAITING)
    errors: Mapped[list] = mapped_column(JSON_TYPE, nullable=False, default=list)
    send_record_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("send_records.id", ondelete="SET NULL"), nullable=True)
    regenerations: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    decided_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    decided_by: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    decision_note: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    __table_args__ = (Index("ix_reply_drafts_state", "state"),)


class ReplySuppression(Base):
    __tablename__ = "reply_suppressions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    inbound_message_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("inbound_messages.id", ondelete="SET NULL"), nullable=True)
    email_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    reason: Mapped[str] = mapped_column(String(30), nullable=False)   # reply_stop (contract reason)
    website_state: Mapped[WebsiteWrite] = mapped_column(Enum(WebsiteWrite), nullable=False)
    attempts: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    last_error: Mapped[Optional[str]] = mapped_column(String(300), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    written_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    __table_args__ = (Index("ix_reply_suppressions_state", "website_state"),)


class OpportunitySnapshot(Base):
    __tablename__ = "opportunity_snapshots"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    business_id: Mapped[int] = mapped_column(Integer, nullable=False)
    sequence_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("email_sequences.id", ondelete="SET NULL"), nullable=True)
    inbound_message_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("inbound_messages.id", ondelete="SET NULL"), nullable=True)
    slug: Mapped[str] = mapped_column(String(80), nullable=False)
    url: Mapped[str] = mapped_column(String(500), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    concept_demo: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    with_evidence_image: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class BriefRun(Base):
    __tablename__ = "brief_runs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    brief_date: Mapped[date] = mapped_column(Date, nullable=False)
    generated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


__all__ = [
    "InboundKind", "InboundState", "DraftState", "DraftKind", "WebsiteWrite", "ImapFolderState", "MailboxReconcile",
    "InboundMessage", "ReplyDraft", "ReplySuppression", "OpportunitySnapshot", "BriefRun",
]
