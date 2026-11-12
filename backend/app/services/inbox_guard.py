"""
Email engine v2, phase E4 - the inbox reconciliation guard (spec row 11 "inbox not reconciled: no further sends";
row 14 "at least every 24 hours"). Kept apart from reply_service.py so the sender worker can use it without loading
the model client.

A mailbox whose inbox was not read completely in the last 24 h (or never) gets the MAILBOX pause
INBOX_NOT_RECONCILED: the worker holds its messages and reply approvals are refused. A complete read clears it again
(the condition itself is resolved, so no person needs to clear it; see docs/outreach/e4-notes.md).
"""

from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.engines.sending.pause_rules import Reason
from backend.app.models.replies import MailboxReconcile
from backend.app.models.sending import PauseFlag, PauseScope
from backend.app.services.sending_service import SendingConfig, SendingService, aware

RECONCILE_MAX_AGE = timedelta(hours=24)


async def check_inbox_freshness(session: AsyncSession, config: SendingConfig, now: datetime) -> list[int]:
    """Raise / clear the per-mailbox pause. Returns the ids of the mailboxes that are stale."""
    sending = SendingService(session, config)
    stale = []
    for box in await sending.enabled_mailboxes():
        row = (await session.execute(select(MailboxReconcile).where(
            MailboxReconcile.mailbox_id == box.id))).scalar_one_or_none()
        last = aware(row.last_success_at) if row and row.last_success_at else None
        if last is None or last < now - RECONCILE_MAX_AGE:
            detail = (f"mailbox {box.id}: last complete inbox read "
                      + (last.isoformat() if last else "never")
                      + (f"; last error: {row.last_error}" if row and row.last_error else ""))
            await sending.raise_pause(PauseScope.MAILBOX, Reason.INBOX_NOT_RECONCILED, str(box.id), detail=detail,
                                      now=now)
            stale.append(box.id)
        else:
            flags = (await session.execute(select(PauseFlag).where(
                PauseFlag.cleared_at.is_(None), PauseFlag.scope == PauseScope.MAILBOX,
                PauseFlag.scope_value == str(box.id), PauseFlag.reason_code == Reason.INBOX_NOT_RECONCILED))
            ).scalars().all()
            for flag in flags:
                flag.cleared_at, flag.cleared_by = now, "system"
                flag.clear_note = f"inbox read completely at {last.isoformat()}"
    await session.flush()
    return stale
