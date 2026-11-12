"""
Email engine v2, phase E4 - read every enabled mailbox once (spec row 14: at least every 24 hours, also on
non-sending days; before and during every sending session). Windows Task Scheduler runs it
(scripts/register_outreach_tasks.ps1); /start-day calls the same work through POST /api/v1/outreach/reconcile.

    .venv/Scripts/python.exe scripts/outreach_reconcile.py

Exit codes (Task Scheduler shows them as "Last Run Result"):
    0  every enabled mailbox was read completely
    1  at least one mailbox could not be read; it keeps / gets the MAILBOX pause INBOX_NOT_RECONCILED (no sends
       from it) until a later run succeeds
    2  refused to start: another reconcile is running, or no mailbox is enabled
Prints counts and mailbox ids only - never an address, a message text or a password.
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from backend.app.config import get_settings  # noqa: E402
from backend.app.database import Base, get_async_engine, get_async_session_factory  # noqa: E402
from backend.app.services.outreach_worker import WorkerLock  # noqa: E402
from backend.app.services.reply_service import build_reply_loop, reconcile_lock_path  # noqa: E402


def report(summary: dict) -> tuple[int, list[str]]:
    """(exit code, lines to print) for one reconcile summary."""
    lines = []
    if not summary.get("mailboxes"):
        return 2, ["No enabled mailbox (POST /api/v1/outreach/mailboxes). Nothing was read."]
    for box in summary["mailboxes"]:
        status = "ok" if box["ok"] else f"FAILED: {box['error']}"
        lines.append(f"mailbox {box['mailbox_id']}: {box['new_messages']} new message(s), {status}")
    processed = ", ".join(f"{k}={v}" for k, v in sorted((summary.get("processed") or {}).items())) or "none"
    lines.append(f"processed: {processed}")
    lines.append(f"out-of-office sequences resumed: {summary.get('ooo_resumed', 0)}; "
                 f"stop writes retried OK: {summary.get('suppressions_retried', 0)}; "
                 f"sequences stopped after a website unsubscribe: {summary.get('website_unsubscribes', 0)}")
    if summary.get("stale_mailboxes"):
        lines.append(f"paused (inbox not read in 24 h): mailbox {', '.join(map(str, summary['stale_mailboxes']))}")
    if summary.get("reply_backlog_breached"):
        lines.append("an interested reply waits more than 1 business day: no new first contacts until answered")
    return (0 if summary.get("ok") else 1), lines


async def main() -> int:
    import backend.app.models  # noqa: F401  (registers every table)

    settings = get_settings()
    lock = WorkerLock(reconcile_lock_path(settings.DATABASE_URL))
    if not lock.acquire():
        print(f"Another reconcile is running ({lock.holder()}). Not starting.")
        return 2
    try:
        async with get_async_engine().begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        summary = await build_reply_loop(settings, get_async_session_factory()).reconcile()
        code, lines = report(summary)
        print("\n".join(lines))
        return code
    finally:
        await get_async_engine().dispose()
        lock.release()


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
