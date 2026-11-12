"""
Email engine v2, phase E2 - the sender worker (spec rows 9, 11-13, 18). Run it while a founder is at the laptop.

    .venv/Scripts/python.exe scripts/outreach_worker.py            loop until today's last window ends (16:30 IST)
    .venv/Scripts/python.exe scripts/outreach_worker.py --once     one cycle, then exit
    .venv/Scripts/python.exe scripts/outreach_worker.py --check    only the start-up checks, then exit

It refuses to start (exit code 2) when another worker holds the lock file, when OUTREACH_API_KEY /
OUTREACH_SIGNING_SECRET / OUTREACH_PUBLIC_BASE_URL are missing, or when no enabled mailbox has its
MAILBOX_<SLUG>_PASSWORD in .env. Each cycle sends only what is due, approved, not suppressed (asked fresh from the
website), still true (E1 recheck), unpaused, inside the recipient's window and within the caps. Every decision is
stored on the send record (state, hold_reason, SMTP code); nothing is printed about addresses or passwords.
The lock file sits next to the SQLite database (or in the current folder for another database).
"""

import argparse
import asyncio
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from backend.app.config import get_settings  # noqa: E402
from backend.app.database import Base, get_async_engine, get_async_session_factory  # noqa: E402
from backend.app.engines.sending.suppression_client import SuppressionClient  # noqa: E402
from backend.app.services.outreach_worker import OutreachWorker, WorkerLock, last_window_end_today  # noqa: E402
from backend.app.services.sending_service import SendingConfig  # noqa: E402

LOCK_NAME = "outreach_worker.lock"


def lock_path(database_url: str) -> Path:
    if database_url.startswith("sqlite") and ":///" in database_url:
        db_file = Path(database_url.split(":///", 1)[1])
        return db_file.resolve().parent / LOCK_NAME
    return Path.cwd() / LOCK_NAME


async def main(args) -> int:
    import backend.app.models  # noqa: F401  (registers every table)

    settings = get_settings()
    lock = WorkerLock(lock_path(settings.DATABASE_URL))
    if not lock.acquire():
        print(f"Another outreach worker is running ({lock.holder()}). Not starting.")
        return 2
    try:
        async with get_async_engine().begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        config = SendingConfig.from_settings(settings)
        client = SuppressionClient(settings.OUTREACH_PUBLIC_BASE_URL, settings.OUTREACH_API_KEY)
        worker = OutreachWorker(get_async_session_factory(), config, client)
        problems = await worker.preflight()
        if problems:
            print("Not starting:\n- " + "\n- ".join(problems))
            return 2
        if args.check:
            print("Start-up checks passed.")
            return 0
        if args.once:
            recovered = await worker.recover()
            if recovered:
                print(f"{recovered} record(s) were SUBMITTING at start-up and are now UNCERTAIN (global pause).")
            summary = await worker.run_once()
            print(" ".join(f"{k}={v}" for k, v in summary.items() if v not in (0, [], None)))
            return 0
        until = last_window_end_today(datetime.now(timezone.utc))
        if until is None:
            print("No campaign window is left today (Tuesday-Thursday, 09:00-11:30 and 14:00-16:30 India time).")
            return 0
        print(f"Worker running until {until.isoformat()} (Ctrl+C stops it; a message in flight finishes first).")
        await worker.run(until, poll_seconds=args.poll_seconds)
        return 0
    finally:
        await get_async_engine().dispose()
        lock.release()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SiteBlitz outreach sender worker (email engine v2, E2)")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--once", action="store_true", help="run one cycle and exit")
    mode.add_argument("--check", action="store_true", help="run the start-up checks only")
    parser.add_argument("--poll-seconds", type=float, default=60.0, help="pause between cycles (default 60)")
    sys.exit(asyncio.run(main(parser.parse_args())))
