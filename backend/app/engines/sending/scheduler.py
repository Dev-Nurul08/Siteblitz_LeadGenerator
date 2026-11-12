"""
Scheduler for campaign mail (spec rows 9-10). Pure and deterministic: every function takes the time it needs as an
argument, so tests run on a fake clock. The service (backend/app/services/sending_service.py) fills a CapacityBook
from the database and stores what these functions return.

Rules (all from docs/spec/email-engine-v2.md and RESULT rows 15-16; nothing invented here except where noted):
- Campaign days Tuesday, Wednesday, Thursday; windows 09:00-11:30 and 14:00-16:30 in the RECIPIENT's local time.
- The recipient's time zone comes from the business's country (India = Asia/Kolkata). No country, a country without
  a zone in COUNTRY_TIMEZONES, or a zone the machine cannot load = HOLD. There is never a default zone.
- Day 1 / 6 / 14: step 2 is due 5 days after step 1's day, step 3 13 days after it. A due day outside the rules moves
  to the next permitted window with free capacity; caps are never exceeded to catch up.
- Per mailbox per recipient-local day: 30 messages in total (everything), 25 of them campaign mail (5 kept back for
  replies).
- New first contacts per sending day (app-wide) = the ramp stage's limit: 10 / 15 / 20 / 20.
- A new prospect is admitted only when steps 2 and 3 can be reserved too, on the same mailbox (one sender per
  sequence), within these bounds (E2 decision, docs/outreach/e2-notes.md): step 2 before step 3's due day (Day 14),
  step 3 no later than Day 21 (the day a cohort counts as mature in RESULT row 16 / 02_chatgpt.md Q5 E).
- Slot spacing inside a window: 6 minutes (150-minute window / 25 campaign messages), so a full day's mail never
  leaves in one burst. This spacing is an E2 decision.
"""

from dataclasses import dataclass, field
from datetime import date, datetime, time, timedelta, timezone
from typing import Iterable, Optional
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

CAMPAIGN_WEEKDAYS = (1, 2, 3)   # Monday = 0: Tuesday, Wednesday, Thursday
WINDOWS = ((time(9, 0), time(11, 30)), (time(14, 0), time(16, 30)))
STEP_DUE_OFFSET = {1: 0, 2: 5, 3: 13}           # Day 1 / Day 6 / Day 14
STEP_LATEST_OFFSET = {2: 12, 3: 20}             # step 2 before Day 14; step 3 by Day 21 (admission bounds)
MAILBOX_DAILY_CEILING = 30                      # everything, incl. replies and tests
REPLY_RESERVE = 5
CAMPAIGN_DAILY_LIMIT = MAILBOX_DAILY_CEILING - REPLY_RESERVE   # 25
SLOT_SPACING = timedelta(minutes=6)
RAMP_LIMITS = {0: 0, 1: 10, 2: 15, 3: 20, 4: 20}  # stage 0 = pilot not started (launch gates, spec row 17)
COUNTRY_TIMEZONES = {"IN": "Asia/Kolkata"}        # spec row 2: India only for the controlled pilot
RESCHEDULE_SEARCH_DAYS = 60                       # loop guard when moving a missed message; not a business rule


class HoldCode:
    COUNTRY_MISSING = "COUNTRY_MISSING"
    COUNTRY_UNKNOWN = "COUNTRY_UNKNOWN"          # no time zone known for this country (and not in the pilot)
    TIMEZONE_MISSING = "TIMEZONE_MISSING"        # the zone cannot be loaded / is not stored
    NOT_A_CAMPAIGN_DAY = "NOT_A_CAMPAIGN_DAY"
    DATE_IN_PAST = "DATE_IN_PAST"
    RAMP_LIMIT_REACHED = "RAMP_LIMIT_REACHED"
    NO_STEP1_CAPACITY = "NO_STEP1_CAPACITY"
    FOLLOW_UPS_DO_NOT_FIT = "FOLLOW_UPS_DO_NOT_FIT"
    NO_MAILBOX = "NO_MAILBOX"


def timezone_for_country(country: Optional[str]) -> tuple[Optional[str], Optional[str]]:
    """(IANA zone name, None) or (None, HOLD code). Never a default."""
    code = (country or "").strip().upper()
    if not code:
        return None, HoldCode.COUNTRY_MISSING
    name = COUNTRY_TIMEZONES.get(code)
    if name is None:
        return None, HoldCode.COUNTRY_UNKNOWN
    return (name, None) if load_zone(name) is not None else (None, HoldCode.TIMEZONE_MISSING)


def load_zone(name: Optional[str]) -> Optional[ZoneInfo]:
    if not name:
        return None
    try:
        return ZoneInfo(name)
    except (ZoneInfoNotFoundError, ValueError):
        return None


def aware(moment: datetime) -> datetime:
    """SQLite returns naive datetimes; everything stored is UTC."""
    return moment if moment.tzinfo else moment.replace(tzinfo=timezone.utc)


def is_campaign_day(day: date) -> bool:
    return day.weekday() in CAMPAIGN_WEEKDAYS


def local_date(moment: datetime, zone: ZoneInfo) -> date:
    return aware(moment).astimezone(zone).date()


@dataclass(frozen=True)
class Window:
    local_date: date
    label: str          # "09:00-11:30"
    start: datetime     # UTC
    end: datetime       # UTC

    def contains(self, moment: datetime) -> bool:
        return self.start <= aware(moment) < self.end


def windows_for(day: date, zone: ZoneInfo) -> list[Window]:
    out = []
    for start, end in WINDOWS:
        out.append(Window(day, f"{start:%H:%M}-{end:%H:%M}",
                          datetime.combine(day, start, zone).astimezone(timezone.utc),
                          datetime.combine(day, end, zone).astimezone(timezone.utc)))
    return out


def window_containing(moment: datetime, zone: ZoneInfo) -> Optional[Window]:
    """The campaign window open at `moment` (recipient time), or None (outside the hours or not Tue-Thu)."""
    day = local_date(moment, zone)
    if not is_campaign_day(day):
        return None
    return next((w for w in windows_for(day, zone) if w.contains(moment)), None)


def due_date(step1_day: date, step: int) -> date:
    return step1_day + timedelta(days=STEP_DUE_OFFSET[step])


def latest_date(step1_day: date, step: int) -> Optional[date]:
    offset = STEP_LATEST_OFFSET.get(step)
    return step1_day + timedelta(days=offset) if offset is not None else None


def ramp_limit(stage: int) -> int:
    return RAMP_LIMITS.get(stage, 0)


# ─── capacity ────────────────────────────────────────────────────────────────


@dataclass
class DayLoad:
    campaign: int = 0                     # campaign records using a slot (scheduled, sent, uncertain, failed)
    total: int = 0                        # every kind (campaign + replies + tests)
    per_window: dict = field(default_factory=dict)   # window label -> campaign records
    # window label -> the latest slot time (UTC) reserved in it. E3 fix: without it, every message admitted while a
    # window is already open got the same time ("now + 1 min") and a mailbox's messages left in one burst.
    last_at: dict = field(default_factory=dict)


@dataclass
class CapacityBook:
    """In-memory view of the reservations: (mailbox id, local date) -> DayLoad, and new first contacts per local
    date (app-wide). Reserving in the book is what makes several admissions in one request see each other."""

    loads: dict = field(default_factory=dict)
    new_contacts: dict = field(default_factory=dict)

    def load(self, mailbox_id: int, day: date) -> DayLoad:
        return self.loads.setdefault((mailbox_id, day), DayLoad())

    def add(self, mailbox_id: int, day: date, window_label: Optional[str], campaign: bool = True,
            new_contact: bool = False, at: Optional[datetime] = None) -> None:
        load = self.load(mailbox_id, day)
        load.total += 1
        if campaign:
            load.campaign += 1
            if window_label:
                load.per_window[window_label] = load.per_window.get(window_label, 0) + 1
                if at is not None:
                    at = aware(at)
                    load.last_at[window_label] = max(load.last_at.get(window_label, at), at)
        if new_contact:
            self.new_contacts[day] = self.new_contacts.get(day, 0) + 1

    def remove(self, mailbox_id: int, day: date, window_label: Optional[str], new_contact: bool = False) -> None:
        load = self.load(mailbox_id, day)
        load.total = max(0, load.total - 1)
        load.campaign = max(0, load.campaign - 1)
        if window_label and load.per_window.get(window_label):
            load.per_window[window_label] -= 1
        if new_contact and self.new_contacts.get(day):
            self.new_contacts[day] -= 1

    def has_room(self, mailbox_id: int, day: date) -> bool:
        load = self.load(mailbox_id, day)
        return load.campaign < CAMPAIGN_DAILY_LIMIT and load.total < MAILBOX_DAILY_CEILING


@dataclass(frozen=True)
class Slot:
    local_date: date
    window_label: str
    window_start: datetime
    window_end: datetime
    scheduled_for: datetime


def _slot_on(book: CapacityBook, mailbox_id: int, day: date, zone: ZoneInfo,
             not_before: Optional[datetime]) -> Optional[Slot]:
    if not is_campaign_day(day) or not book.has_room(mailbox_id, day):
        return None
    load = book.load(mailbox_id, day)
    options = []
    for index, window in enumerate(windows_for(day, zone)):
        at = window.start + SLOT_SPACING * load.per_window.get(window.label, 0)
        last = load.last_at.get(window.label)
        if last is not None and at < last + SLOT_SPACING:
            at = last + SLOT_SPACING
        if not_before is not None and at < not_before:
            at = aware(not_before).replace(second=0, microsecond=0) + timedelta(minutes=1)
        if at < window.end:
            # Fewest messages first (spreads the day over both windows); the earlier window wins a tie.
            options.append((load.per_window.get(window.label, 0), index,
                            Slot(day, window.label, window.start, window.end, at)))
    return min(options, key=lambda o: (o[0], o[1]))[2] if options else None


def find_slot(book: CapacityBook, mailbox_id: int, zone: ZoneInfo, earliest: date, latest: Optional[date],
              not_before: Optional[datetime] = None) -> Optional[Slot]:
    """The first permitted window with free capacity on a day in [earliest, latest] (latest None = search
    RESCHEDULE_SEARCH_DAYS ahead). `not_before` (UTC) skips windows / slot times already in the past."""
    last = latest if latest is not None else earliest + timedelta(days=RESCHEDULE_SEARCH_DAYS)
    day = earliest
    while day <= last:
        slot = _slot_on(book, mailbox_id, day, zone, not_before)
        if slot is not None:
            return slot
        day += timedelta(days=1)
    return None


@dataclass(frozen=True)
class Admission:
    mailbox_id: int
    slots: dict   # step -> Slot


@dataclass(frozen=True)
class Refusal:
    code: str
    message: str


def plan_admission(book: CapacityBook, mailbox_ids: Iterable[int], zone: ZoneInfo, send_day: date,
                   now: datetime, daily_new_limit: int):
    """Admit one new prospect on `send_day` (recipient-local) or refuse it. On success the three slots are reserved
    in `book`. Mailboxes are tried with the least-loaded first (then the lowest id), so a batch spreads evenly."""
    if not is_campaign_day(send_day):
        return Refusal(HoldCode.NOT_A_CAMPAIGN_DAY, f"{send_day.isoformat()} is not a Tuesday, Wednesday or Thursday")
    if send_day < local_date(now, zone):
        return Refusal(HoldCode.DATE_IN_PAST, f"{send_day.isoformat()} is in the past")
    already = book.new_contacts.get(send_day, 0)
    if daily_new_limit <= 0:
        return Refusal(HoldCode.RAMP_LIMIT_REACHED,
                       "new first contacts are off: the ramp is at stage 0 (pilot not started, or stopped)")
    if already >= daily_new_limit:
        return Refusal(HoldCode.RAMP_LIMIT_REACHED,
                       f"{already} new first contacts are already scheduled for {send_day.isoformat()}; "
                       f"the current ramp allows {daily_new_limit} a day")
    ids = sorted(set(mailbox_ids), key=lambda m: (book.load(m, send_day).campaign, m))
    if not ids:
        return Refusal(HoldCode.NO_MAILBOX, "no enabled, unpaused mailbox")
    step1_fitted = False
    for mailbox_id in ids:
        first = find_slot(book, mailbox_id, zone, send_day, send_day, not_before=now)
        if first is None:
            continue
        step1_fitted = True
        # Reserve step 1 tentatively so step 2 / 3 on the same day-load see it (they never share a day anyway).
        second = find_slot(book, mailbox_id, zone, due_date(send_day, 2), latest_date(send_day, 2))
        third = None
        if second is not None:
            third = find_slot(book, mailbox_id, zone,
                              max(due_date(send_day, 3), second.local_date + timedelta(days=1)),
                              latest_date(send_day, 3))
        if second is None or third is None:
            continue
        book.add(mailbox_id, first.local_date, first.window_label, new_contact=True, at=first.scheduled_for)
        book.add(mailbox_id, second.local_date, second.window_label, at=second.scheduled_for)
        book.add(mailbox_id, third.local_date, third.window_label, at=third.scheduled_for)
        return Admission(mailbox_id, {1: first, 2: second, 3: third})
    if not step1_fitted:
        return Refusal(HoldCode.NO_STEP1_CAPACITY,
                       f"no mailbox has a free campaign slot left on {send_day.isoformat()}")
    return Refusal(HoldCode.FOLLOW_UPS_DO_NOT_FIT,
                   "the Day 6 and Day 14 follow-ups cannot be reserved within their windows on any mailbox, "
                   "so this prospect is not admitted")
