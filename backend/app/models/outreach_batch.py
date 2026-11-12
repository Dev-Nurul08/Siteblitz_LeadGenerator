"""
Email engine v2, phase E3 - the batch screen: select eligible leads, write T1-T3 with the AI writer + validator,
review, approve into E2 sequences, or reject (spec: docs/spec/email-engine-v2.md rows 5, 6, 9, 10, 19).

Two new tables, so an existing database gets them from `create_all` without a migration:

- `outreach_batches`       one "Write" press: who, when, the recipient-local sending day it was written for.
- `outreach_batch_leads`   one eligibility row in a batch: state, the three texts, HOLD reason codes, a snapshot of
                           the evidence the texts were written from (observation, provenance, verification), the
                           dry-run schedule from E2's scheduler, and who approved or rejected it and when.

Lead states: PENDING -> WRITING -> READY | HOLD;  READY -> APPROVED (E2 sequence created) | REJECTED;
             HOLD -> REJECTED. A READY lead whose approval E2 refuses stays READY with `approval_refusal` set.
The batch's own status (WRITING / REVIEW / DONE) is derived from its leads, never stored.
"""

import enum
from datetime import date, datetime
from typing import Optional

from sqlalchemy import (
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    Integer,
    JSON,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.database import Base

JSON_TYPE = JSON().with_variant(JSONB, "postgresql")


class BatchLeadState(str, enum.Enum):
    PENDING = "PENDING"      # selected, not written yet
    WRITING = "WRITING"      # the writer is working on it now
    READY = "READY"          # T1, T2 and T3 passed the validator; waits for the founder
    HOLD = "HOLD"            # not written or not valid: `hold_reasons` says why (no text is ever faked)
    APPROVED = "APPROVED"    # an E2 sequence exists (step 1 approved, steps 2 and 3 approved with their texts)
    REJECTED = "REJECTED"    # the founder said no, with a reason


OPEN_LEAD_STATES = (BatchLeadState.PENDING, BatchLeadState.WRITING, BatchLeadState.READY)


class OutreachBatch(Base):
    __tablename__ = "outreach_batches"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    send_date: Mapped[date] = mapped_column(Date, nullable=False)          # recipient-local day for touch 1
    created_by: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    writer_model: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    template_version: Mapped[str] = mapped_column(String(30), nullable=False)


class OutreachBatchLead(Base):
    __tablename__ = "outreach_batch_leads"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    batch_id: Mapped[int] = mapped_column(Integer, ForeignKey("outreach_batches.id", ondelete="CASCADE"),
                                          nullable=False)
    position: Mapped[int] = mapped_column(Integer, nullable=False)        # order of selection
    eligibility_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("email_eligibility.id", ondelete="SET NULL"), nullable=True)
    business_id: Mapped[int] = mapped_column(Integer, ForeignKey("businesses.id", ondelete="CASCADE"),
                                             nullable=False)
    recipient_email: Mapped[str] = mapped_column(String(320), nullable=False)
    state: Mapped[BatchLeadState] = mapped_column(Enum(BatchLeadState), nullable=False,
                                                  default=BatchLeadState.PENDING)
    hold_reasons: Mapped[list] = mapped_column(JSON_TYPE, nullable=False, default=list)   # codes
    hold_detail: Mapped[list] = mapped_column(JSON_TYPE, nullable=False, default=list)    # validator messages

    # What the texts were written from, frozen at selection (E1 rows are recomputed later).
    evidence: Mapped[dict] = mapped_column(JSON_TYPE, nullable=False, default=dict)
    # E2 scheduler dry run: {"mailbox_id", "mailbox", "display_name", "steps": [{step, local_date, window, ...}]}
    plan: Mapped[Optional[dict]] = mapped_column(JSON_TYPE, nullable=True)
    mailbox_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("mailboxes.id"), nullable=True)
    sender_name: Mapped[Optional[str]] = mapped_column(String(60), nullable=True)

    subject: Mapped[Optional[str]] = mapped_column(String(300), nullable=True)
    text_1: Mapped[Optional[str]] = mapped_column(Text, nullable=True)    # body + signature + unsubscribe line
    text_2: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    text_3: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    writer_detail: Mapped[Optional[dict]] = mapped_column(JSON_TYPE, nullable=True)   # attempts per touch
    written_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    sequence_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("email_sequences.id", ondelete="SET NULL"), nullable=True)
    approved_by: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    approved_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    approval_refusal: Mapped[Optional[dict]] = mapped_column(JSON_TYPE, nullable=True)   # {code, message, at}
    rejected_by: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    rejected_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    reject_reason: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint("batch_id", "eligibility_id", name="uq_batch_lead_eligibility"),
        Index("ix_batch_leads_state", "state"),
        Index("ix_batch_leads_eligibility", "eligibility_id"),
    )


__all__ = ["BatchLeadState", "OPEN_LEAD_STATES", "OutreachBatch", "OutreachBatchLead"]
