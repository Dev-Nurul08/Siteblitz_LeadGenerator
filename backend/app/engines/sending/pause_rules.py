"""
Automatic pause / stop rules (spec row 11; 02_chatgpt.md Q5 D). Pure helpers; the service applies them to the
database (SendingService.record_* methods) and every flag they raise blocks sends until a person clears it.

| Signal                                   | Pause                                  | Stop                                       |
|------------------------------------------|----------------------------------------|--------------------------------------------|
| hard bounce (invalid recipient)          | 1st: suppress address (website) +      | 2 bounced recipients in the latest 100     |
|                                          | pause that source batch                | distinct recipients of that source         |
| credible complaint                       | 1: pause everything                    | 2 in 30 days: stop the campaign            |
| policy / authentication rejection        | 1: pause that sending domain           | 3 in 24 h: stop that sending domain        |
| send to a suppressed address, duplicate, | 1: pause everything until fixed        |                                            |
| unapproved send                          |                                        |                                            |
| suppression service down, inbox not      | no further sends (pause everything)    | no time-based automatic restart            |
| reconciled, unknown SMTP result          |                                        |                                            |
| interested reply unanswered > 1          | no new first contacts                  | resumes when the backlog is cleared        |
| business day                             |                                        |                                            |

The hard-bounce rate counts each recipient once: follow-ups never inflate the denominator.
"""

from datetime import date, datetime, time, timedelta
from typing import Iterable, Optional
from zoneinfo import ZoneInfo

from backend.app.engines.sending.scheduler import aware

HARD_BOUNCE_LOOKBACK_RECIPIENTS = 100
HARD_BOUNCE_STOP_COUNT = 2
COMPLAINT_STOP_COUNT = 2
COMPLAINT_STOP_WINDOW = timedelta(days=30)
POLICY_STOP_COUNT = 3
POLICY_STOP_WINDOW = timedelta(hours=24)
REPLY_BACKLOG_BUSINESS_DAYS = 1
BUSINESS_WEEKDAYS = (0, 1, 2, 3, 4)   # Monday-Friday (E2 decision, docs/outreach/e2-notes.md)


class Reason:
    HARD_BOUNCE = "HARD_BOUNCE"                          # SOURCE_BATCH pause
    HARD_BOUNCE_RATE = "HARD_BOUNCE_RATE"                # SOURCE stop
    COMPLAINT = "COMPLAINT"                              # GLOBAL pause
    COMPLAINTS_30D = "COMPLAINTS_30D"                    # GLOBAL stop
    POLICY_REJECTION = "POLICY_REJECTION"                # DOMAIN pause
    POLICY_REJECTIONS_24H = "POLICY_REJECTIONS_24H"      # DOMAIN stop
    SUPPRESSED_SEND = "SUPPRESSED_SEND"                  # GLOBAL pause (integrity)
    DUPLICATE_SEND = "DUPLICATE_SEND"                    # GLOBAL pause (integrity)
    UNAPPROVED_SEND = "UNAPPROVED_SEND"                  # GLOBAL pause (integrity)
    SUPPRESSION_UNAVAILABLE = "SUPPRESSION_UNAVAILABLE"  # GLOBAL pause
    SUPPRESSION_WRITE_FAILED = "SUPPRESSION_WRITE_FAILED"  # GLOBAL pause: a bounce / complaint is not on the list
    INBOX_NOT_RECONCILED = "INBOX_NOT_RECONCILED"        # GLOBAL pause (E4 raises it)
    SEND_RESULT_UNKNOWN = "SEND_RESULT_UNKNOWN"          # GLOBAL pause until every UNCERTAIN record is resolved
    REPLY_BACKLOG = "REPLY_BACKLOG"                      # NEW_CONTACTS pause
    SMTP_UNAVAILABLE = "SMTP_UNAVAILABLE"                # MAILBOX pause: connect / TLS / login refused
    SOFT_BOUNCE_LIMIT = "SOFT_BOUNCE_LIMIT"              # E3: record FAILED (soft) + sequence HELD, no pause
    MANUAL = "MANUAL"


def latest_distinct(recipients_newest_first: Iterable[str], limit: int = HARD_BOUNCE_LOOKBACK_RECIPIENTS
                    ) -> list[str]:
    """The latest `limit` DISTINCT recipients (each counted once, by their most recent message)."""
    seen: list[str] = []
    for value in recipients_newest_first:
        if value not in seen:
            seen.append(value)
            if len(seen) == limit:
                break
    return seen


def hard_bounce_stop(latest_recipients: list[str], bounced: set[str]) -> bool:
    """2 hard-bounced recipients within the latest 100 distinct recipients attempted (a window smaller than 100
    counts too)."""
    return len(set(latest_recipients) & bounced) >= HARD_BOUNCE_STOP_COUNT


def count_since(moments: Iterable[datetime], now: datetime, window: timedelta) -> int:
    start = aware(now) - window
    return sum(1 for m in moments if aware(m) > start)


def complaint_stop(complaint_times: Iterable[datetime], now: datetime) -> bool:
    return count_since(complaint_times, now, COMPLAINT_STOP_WINDOW) >= COMPLAINT_STOP_COUNT


def policy_stop(rejection_times: Iterable[datetime], now: datetime) -> bool:
    return count_since(rejection_times, now, POLICY_STOP_WINDOW) >= POLICY_STOP_COUNT


def _is_business_day(day: date) -> bool:
    return day.weekday() in BUSINESS_WEEKDAYS


def reply_deadline(received_at: datetime, zone: ZoneInfo, business_days: int = REPLY_BACKLOG_BUSINESS_DAYS
                   ) -> datetime:
    """When an interested reply received at `received_at` becomes overdue: `business_days` business days later in
    the founders' time (India). A reply that arrives on a weekend starts counting on Monday 00:00."""
    local = aware(received_at).astimezone(zone)
    while not _is_business_day(local.date()):
        local = datetime.combine(local.date() + timedelta(days=1), time(0, 0), zone)
    remaining = business_days
    while remaining > 0:
        local = local + timedelta(days=1)
        if _is_business_day(local.date()):
            remaining -= 1
    return local


def reply_backlog_breached(oldest_unanswered_interested_at: Optional[datetime], now: datetime,
                           zone: ZoneInfo) -> bool:
    if oldest_unanswered_interested_at is None:
        return False
    return aware(now) > reply_deadline(oldest_unanswered_interested_at, zone)
