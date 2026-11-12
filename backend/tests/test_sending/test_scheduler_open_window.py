"""
E3 fix of E2's scheduler (found on the batch screen's dry run): prospects admitted while a window is already open got
the same slot time ("now + 1 min") on one mailbox, so they would have left in one burst. Slots now continue from the
latest reserved time in the window, 6 minutes apart (E2 decision 6), also after a reload from the database.
"""

from datetime import date, datetime, timedelta, timezone

from backend.app.engines.sending import scheduler as sched

IST = sched.load_zone("Asia/Kolkata")
THU = date(2026, 11, 12)


def ist(hh, mm=0):
    return datetime(THU.year, THU.month, THU.day, hh, mm, tzinfo=IST).astimezone(timezone.utc)


def admit(book, now, n, mailboxes=(1,)):
    plans = [sched.plan_admission(book, list(mailboxes), IST, THU, now, 20) for _ in range(n)]
    assert all(isinstance(p, sched.Admission) for p in plans), plans
    return plans


def test_admissions_inside_an_open_window_are_spaced_six_minutes_apart():
    book = sched.CapacityBook()
    plans = admit(book, ist(14, 59, ), 4)
    times = [p.slots[1].scheduled_for for p in plans]
    assert times == [ist(15, 0) + sched.SLOT_SPACING * i for i in range(4)]
    assert {p.slots[1].window_label for p in plans} == {"14:00-16:30"}


def test_slots_already_used_earlier_in_the_window_are_respected_after_a_reload():
    book = sched.CapacityBook()
    # two messages reserved this morning at 09:00 and 09:06 (as capacity_book() loads them from send_records)
    book.add(1, THU, "09:00-11:30", at=ist(9, 0))
    book.add(1, THU, "09:00-11:30", at=ist(9, 6))
    plans = admit(book, ist(9, 3), 3)
    morning = [p.slots[1].scheduled_for for p in plans if p.slots[1].window_label == "09:00-11:30"]
    afternoon = [p.slots[1].scheduled_for for p in plans if p.slots[1].window_label == "14:00-16:30"]
    # the emptier afternoon window fills first (fewest messages first); the morning one then comes after 09:06,
    # never on top of a slot already used
    assert afternoon == [ist(14, 0), ist(14, 6)]
    assert morning == [ist(9, 12)]


def test_before_the_window_opens_nothing_changes():
    book = sched.CapacityBook()
    plans = admit(book, ist(6, 0), 3)
    assert [p.slots[1].scheduled_for for p in plans] == [ist(9, 0), ist(14, 0), ist(9, 0) + timedelta(minutes=6)]
