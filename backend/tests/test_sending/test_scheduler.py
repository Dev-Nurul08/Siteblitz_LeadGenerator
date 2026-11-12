"""E2 scheduler: pure functions on a fake clock (no database, no network)."""

from datetime import date, datetime, timedelta, timezone

import pytest

from backend.app.engines.sending import scheduler as s

IST = s.load_zone("Asia/Kolkata")
MON = date(2026, 11, 16)
TUE, WED, THU = date(2026, 11, 17), date(2026, 11, 18), date(2026, 11, 19)
NOW = datetime(2026, 11, 12, 6, 0, tzinfo=timezone.utc)   # Thursday before


def ist(day: date, hh: int, mm: int, ss: int = 0) -> datetime:
    return datetime(day.year, day.month, day.day, hh, mm, ss, tzinfo=IST)


def test_only_tuesday_to_thursday_are_campaign_days():
    week = [MON + timedelta(days=i) for i in range(7)]
    assert [d for d in week if s.is_campaign_day(d)] == [TUE, WED, THU]
    for day in week:
        open_window = s.window_containing(ist(day, 10, 0), IST)
        assert (open_window is not None) == (day in (TUE, WED, THU))


@pytest.mark.parametrize("hh,mm,ss,inside", [
    (8, 59, 59, False), (9, 0, 0, True), (11, 29, 59, True), (11, 30, 0, False), (13, 59, 59, False),
    (14, 0, 0, True), (16, 29, 59, True), (16, 30, 0, False), (20, 0, 0, False),
])
def test_window_edges_in_india_time(hh, mm, ss, inside):
    assert (s.window_containing(ist(TUE, hh, mm, ss), IST) is not None) is inside


def test_windows_are_stored_in_utc():
    first, second = s.windows_for(TUE, IST)
    assert (first.label, second.label) == ("09:00-11:30", "14:00-16:30")
    assert first.start == datetime(2026, 11, 17, 3, 30, tzinfo=timezone.utc)
    assert second.end == datetime(2026, 11, 17, 11, 0, tzinfo=timezone.utc)


def test_timezone_comes_from_the_country_and_never_defaults(monkeypatch):
    assert s.timezone_for_country("IN") == ("Asia/Kolkata", None)
    assert s.timezone_for_country("in") == ("Asia/Kolkata", None)
    assert s.timezone_for_country(None) == (None, s.HoldCode.COUNTRY_MISSING)
    assert s.timezone_for_country("  ") == (None, s.HoldCode.COUNTRY_MISSING)
    assert s.timezone_for_country("US") == (None, s.HoldCode.COUNTRY_UNKNOWN)
    assert s.timezone_for_country("XX") == (None, s.HoldCode.COUNTRY_UNKNOWN)
    monkeypatch.setitem(s.COUNTRY_TIMEZONES, "IN", "Nowhere/Missing_Zone")
    assert s.timezone_for_country("IN") == (None, s.HoldCode.TIMEZONE_MISSING)


@pytest.mark.parametrize("start,step2,step3", [
    (TUE, date(2026, 11, 24), date(2026, 12, 1)),   # Day 6 = Sunday -> next Tuesday; Day 14 = Monday -> Tuesday
    (WED, date(2026, 11, 24), date(2026, 12, 1)),   # Day 6 = Monday -> Tuesday; Day 14 = Tuesday
    (THU, date(2026, 11, 24), date(2026, 12, 2)),   # Day 6 = Tuesday; Day 14 = Wednesday
])
def test_follow_ups_outside_the_days_move_to_the_next_permitted_window(start, step2, step3):
    plan = s.plan_admission(s.CapacityBook(), [1], IST, start, NOW, daily_new_limit=10)
    assert isinstance(plan, s.Admission)
    assert plan.slots[1].local_date == start
    assert plan.slots[2].local_date == step2 and plan.slots[3].local_date == step3
    assert plan.slots[2].window_label == "09:00-11:30" and plan.slots[2].scheduled_for == ist(step2, 9, 0)
    assert s.due_date(start, 2) == start + timedelta(days=5) and s.due_date(start, 3) == start + timedelta(days=13)


def test_slots_alternate_windows_and_are_spaced():
    book = s.CapacityBook()
    slots = [s.find_slot(book, 1, IST, TUE, TUE) for _ in range(1)]
    book.add(1, TUE, slots[0].window_label)
    second = s.find_slot(book, 1, IST, TUE, TUE)
    book.add(1, TUE, second.window_label)
    third = s.find_slot(book, 1, IST, TUE, TUE)
    assert slots[0].scheduled_for == ist(TUE, 9, 0)
    assert second.scheduled_for == ist(TUE, 14, 0)
    assert third.scheduled_for == ist(TUE, 9, 6)   # 6-minute spacing


def test_a_slot_today_is_never_in_the_past():
    late = ist(TUE, 10, 41).astimezone(timezone.utc)
    slot = s.find_slot(s.CapacityBook(), 1, IST, TUE, TUE, not_before=late)
    assert slot.window_label == "09:00-11:30" and slot.scheduled_for == ist(TUE, 10, 42)
    after_hours = ist(TUE, 16, 45).astimezone(timezone.utc)
    assert s.find_slot(s.CapacityBook(), 1, IST, TUE, TUE, not_before=after_hours) is None


def test_caps_30_total_25_campaign_5_kept_for_replies():
    assert (s.MAILBOX_DAILY_CEILING, s.CAMPAIGN_DAILY_LIMIT, s.REPLY_RESERVE) == (30, 25, 5)
    book = s.CapacityBook()
    for _ in range(24):
        book.add(1, TUE, "09:00-11:30")
    assert book.has_room(1, TUE)
    book.add(1, TUE, "14:00-16:30")
    assert not book.has_room(1, TUE)                      # 25 campaign messages
    assert s.find_slot(book, 1, IST, TUE, TUE) is None
    replies = s.CapacityBook()
    for _ in range(20):
        replies.add(2, TUE, "09:00-11:30")
    for _ in range(10):
        replies.add(2, TUE, None, campaign=False)         # replies beyond the 5 kept back
    assert replies.load(2, TUE).total == 30 and not replies.has_room(2, TUE)   # the 30 ceiling still holds


def test_full_days_push_a_follow_up_to_the_next_free_day():
    book = s.CapacityBook()
    for _ in range(25):
        book.add(1, date(2026, 11, 24), "09:00-11:30")     # next Tuesday is full
    plan = s.plan_admission(book, [1], IST, TUE, NOW, daily_new_limit=10)
    assert plan.slots[2].local_date == date(2026, 11, 25)  # Wednesday, never a 26th message on Tuesday


def test_prospect_whose_follow_ups_cannot_be_reserved_is_not_admitted():
    book = s.CapacityBook()
    for day in (date(2026, 11, 24), date(2026, 11, 25), date(2026, 11, 26)):   # every Day-6 option is full
        for _ in range(25):
            book.add(1, day, "09:00-11:30")
    refusal = s.plan_admission(book, [1], IST, TUE, NOW, daily_new_limit=10)
    assert isinstance(refusal, s.Refusal) and refusal.code == s.HoldCode.FOLLOW_UPS_DO_NOT_FIT
    assert book.new_contacts.get(TUE, 0) == 0 and book.load(1, TUE).campaign == 0   # nothing was reserved
    other = s.plan_admission(book, [1, 2], IST, TUE, NOW, daily_new_limit=10)
    assert isinstance(other, s.Admission) and other.mailbox_id == 2   # same sender for all three steps


def test_step_three_is_never_later_than_day_21():
    book = s.CapacityBook()
    for day in (date(2026, 12, 1), date(2026, 12, 2), date(2026, 12, 3)):     # Day 15-17 full
        for _ in range(25):
            book.add(1, day, "09:00-11:30")
    refusal = s.plan_admission(book, [1], IST, TUE, NOW, daily_new_limit=10)
    assert refusal.code == s.HoldCode.FOLLOW_UPS_DO_NOT_FIT   # the next Tuesday would be Day 22


def test_ramp_10_15_20_and_the_eleventh_new_contact_is_refused():
    assert [s.ramp_limit(stage) for stage in (0, 1, 2, 3, 4)] == [0, 10, 15, 20, 20]
    book = s.CapacityBook()
    plans = [s.plan_admission(book, [1, 2, 3], IST, TUE, NOW, daily_new_limit=s.ramp_limit(1)) for _ in range(11)]
    assert all(isinstance(p, s.Admission) for p in plans[:10])
    assert isinstance(plans[10], s.Refusal) and plans[10].code == s.HoldCode.RAMP_LIMIT_REACHED
    assert "10" in plans[10].message
    assert sorted(p.mailbox_id for p in plans[:10]).count(1) in (3, 4)   # spread over the three mailboxes
    for stage, expected in ((2, 15), (3, 20)):
        book = s.CapacityBook()
        admitted = [s.plan_admission(book, [1, 2, 3], IST, WED, NOW, s.ramp_limit(stage)) for _ in range(expected + 1)]
        assert sum(isinstance(p, s.Admission) for p in admitted) == expected


def test_not_a_campaign_day_or_a_past_day_is_refused():
    assert s.plan_admission(s.CapacityBook(), [1], IST, MON, NOW, 10).code == s.HoldCode.NOT_A_CAMPAIGN_DAY
    assert s.plan_admission(s.CapacityBook(), [1], IST, date(2026, 11, 11), NOW, 10).code == s.HoldCode.DATE_IN_PAST
    assert s.plan_admission(s.CapacityBook(), [1], IST, TUE, NOW, 0).code == s.HoldCode.RAMP_LIMIT_REACHED
