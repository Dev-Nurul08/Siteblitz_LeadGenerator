"""
Email engine v2, phase E4 - the daily brief (spec rows 15-16; RESULT row 20). Every number is counted from the
database at the moment of the request; nothing is estimated. Figures the app does not track yet (quotes, deposits,
payments, paid projects) are null with "not_tracked": true; the complaint rate the mail provider does not report is
"unknown", never 0. There is no "opened" or "read" figure (no tracking pixels exist).

Periods (India time, the founders' day): "yesterday" = the calendar day before `date`; "since_last_brief" = from
the previous brief's generation time to now (null when there was none). Each call is recorded as a brief run.
"""

from datetime import date, datetime, time, timedelta, timezone

from sqlalchemy import func, select

from backend.app.engines.replies import labels as L
from backend.app.engines.sending import scheduler as sched
from backend.app.models.replies import (
    BriefRun,
    DraftState,
    InboundKind,
    InboundMessage,
    InboundState,
    MailboxReconcile,
    OpportunitySnapshot,
    ReplyDraft,
    ReplySuppression,
    WebsiteWrite,
)
from backend.app.models.sending import (
    CAPACITY_STATES,
    DeliveryEvent,
    DeliveryEventKind,
    EmailSequence,
    Mailbox,
    PauseScope,
    SendKind,
    SendRecord,
    SequenceState,
    SuppressionMirror,
)
from backend.app.services.delivery_rules_service import FOUNDER_ZONE
from backend.app.services.inbox_guard import RECONCILE_MAX_AGE
from backend.app.services.sending_service import SendingConfig, SendingService, aware, iso, pause_dict

NOT_TRACKED = {"value": None, "not_tracked": True}
HUMAN_LABELS = (L.INTERESTED, L.QUESTION, L.PRICE, L.SAMPLE_REQUESTED, L.NOT_NOW, L.WRONG_PERSON, L.STOP,
                L.COMPLAINT_LEGAL, L.NEEDS_REVIEW)


def day_bounds(day: date) -> tuple[datetime, datetime]:
    zone = sched.load_zone(FOUNDER_ZONE)
    start = datetime.combine(day, time(0, 0), zone)
    return start.astimezone(timezone.utc), (start + timedelta(days=1)).astimezone(timezone.utc)


async def _count(session, stmt) -> int:
    return int((await session.execute(stmt)).scalar_one() or 0)


async def period_counts(session, start: datetime, end: datetime) -> dict:
    def accepted(*where):
        return select(func.count()).select_from(SendRecord).where(
            SendRecord.accepted_at >= start, SendRecord.accepted_at < end, *where)

    def events(kind: DeliveryEventKind, *where):
        return select(func.count(func.distinct(DeliveryEvent.recipient_hash))).where(
            DeliveryEvent.kind == kind, DeliveryEvent.occurred_at >= start, DeliveryEvent.occurred_at < end, *where)

    human = (InboundMessage.kind == InboundKind.HUMAN, InboundMessage.sequence_id.isnot(None),
             InboundMessage.received_at >= start, InboundMessage.received_at < end)
    rows = (await session.execute(select(InboundMessage.from_hash, InboundMessage.labels).where(*human))).all()
    by_label = {}
    for label in HUMAN_LABELS:
        by_label[label] = len({h for h, labels in rows if label in (labels or []) and h})
    return {
        "accepted": {
            "total": await _count(session, accepted()),
            "campaign": await _count(session, accepted(SendRecord.kind == SendKind.CAMPAIGN)),
            "new_contacts": await _count(session, accepted(SendRecord.kind == SendKind.CAMPAIGN,
                                                           SendRecord.step == 1)),
            "replies": await _count(session, accepted(SendRecord.kind == SendKind.REPLY)),
        },
        "hard_bounces": await _count(session, events(DeliveryEventKind.HARD_BOUNCE)),
        "soft_bounces": await _count(session, events(DeliveryEventKind.SOFT_BOUNCE)),
        "unknown_bounces": await _count(session, events(DeliveryEventKind.UNKNOWN_BOUNCE)),
        "policy_rejections": await _count(session, select(func.count()).select_from(DeliveryEvent).where(
            DeliveryEvent.kind == DeliveryEventKind.POLICY_REJECTION, DeliveryEvent.occurred_at >= start,
            DeliveryEvent.occurred_at < end)),
        "complaints_received": await _count(session, events(DeliveryEventKind.COMPLAINT)),
        "complaint_rate_from_provider": "unknown",
        "unique_human_replies": len({h for h, _ in rows if h}),
        "replies_by_label": by_label,
        "out_of_office": await _count(session, select(func.count()).select_from(InboundMessage).where(
            InboundMessage.kind == InboundKind.AUTO_REPLY, InboundMessage.received_at >= start,
            InboundMessage.received_at < end)),
        "bounce_reports_read": await _count(session, select(func.count()).select_from(InboundMessage).where(
            InboundMessage.kind == InboundKind.DSN, InboundMessage.received_at >= start,
            InboundMessage.received_at < end)),
        "stops_processed": await _count(session, select(func.count(func.distinct(ReplySuppression.email_hash))).where(
            ReplySuppression.created_at >= start, ReplySuppression.created_at < end)),
        "website_unsubscribes": await _count(session, select(func.count()).select_from(SuppressionMirror).where(
            SuppressionMirror.reason.like("unsubscribe%"), SuppressionMirror.suppressed_at >= start,
            SuppressionMirror.suppressed_at < end)),
        "samples_created": await _count(session, select(func.count()).select_from(OpportunitySnapshot).where(
            OpportunitySnapshot.created_at >= start, OpportunitySnapshot.created_at < end)),
        "replies_sent": await _count(session, select(func.count()).select_from(ReplyDraft).where(
            ReplyDraft.state == DraftState.SENT, ReplyDraft.decided_at >= start, ReplyDraft.decided_at < end)),
        "quotes": NOT_TRACKED, "deposits": NOT_TRACKED, "payments": NOT_TRACKED, "paid_projects": NOT_TRACKED,
    }


async def build_brief(session, config: SendingConfig, day: date, now: datetime, record: bool = True) -> dict:
    sending = SendingService(session, config)
    previous = (await session.execute(select(BriefRun).where(BriefRun.generated_at < now)
                                      .order_by(BriefRun.generated_at.desc()).limit(1))).scalar_one_or_none()
    y_start, y_end = day_bounds(day - timedelta(days=1))
    yesterday = {"from": y_start.isoformat(), "to": y_end.isoformat(), **await period_counts(session, y_start, y_end)}
    since = None
    if previous is not None:
        start = aware(previous.generated_at)
        since = {"from": start.isoformat(), "to": now.isoformat(), **await period_counts(session, start, now)}

    pauses = await sending.active_pauses()
    capacity = await sending.capacity(day)
    blocked_by = [f.reason_code for f in pauses if f.scope in (PauseScope.GLOBAL, PauseScope.NEW_CONTACTS)]
    allowance = dict(capacity["new_contacts"])
    allowance["blocked_by"] = blocked_by
    allowance["left"] = 0 if blocked_by else allowance["free"]

    per_box = []
    boxes = (await session.execute(select(Mailbox).order_by(Mailbox.id))).scalars().all()
    for box in boxes:
        rows = (await session.execute(select(SendRecord.state, SendRecord.step, func.count()).where(
            SendRecord.mailbox_id == box.id, SendRecord.local_date == day, SendRecord.kind == SendKind.CAMPAIGN)
            .group_by(SendRecord.state, SendRecord.step))).all()
        by_state: dict[str, int] = {}
        steps: dict[str, int] = {}
        for state, step, count in rows:
            by_state[state.value] = by_state.get(state.value, 0) + count
            if state in CAPACITY_STATES:
                steps[f"step_{step}"] = steps.get(f"step_{step}", 0) + count
        reconcile = (await session.execute(select(MailboxReconcile).where(
            MailboxReconcile.mailbox_id == box.id))).scalar_one_or_none()
        last = aware(reconcile.last_success_at) if reconcile and reconcile.last_success_at else None
        per_box.append({"mailbox_id": box.id, "address": box.address, "enabled": box.enabled,
                        "scheduled_today": sum(steps.values()), "by_step": steps, "by_state": by_state,
                        "last_inbox_read": iso(last), "inbox_read_stale": last is None
                        or last < now - RECONCILE_MAX_AGE,
                        "last_inbox_error": reconcile.last_error if reconcile else None})

    waiting = await _count(session, select(func.count()).select_from(ReplyDraft).where(
        ReplyDraft.state == DraftState.WAITING))
    brief = {
        "date": day.isoformat(), "timezone": FOUNDER_ZONE, "generated_at": now.isoformat(),
        "yesterday": yesterday, "since_last_brief": since,
        "drafts_waiting": waiting,
        "drafts_blocked": await _count(session, select(func.count()).select_from(ReplyDraft).where(
            ReplyDraft.state == DraftState.BLOCKED)),
        "messages_for_founder": await _count(session, select(func.count()).select_from(InboundMessage).where(
            InboundMessage.state.in_([InboundState.FLAGGED, InboundState.NEEDS_REVIEW, InboundState.ERROR]),
            InboundMessage.handled_at.is_(None))),
        "stops_pending_website_write": await _count(session, select(func.count()).select_from(ReplySuppression)
                                                    .where(ReplySuppression.website_state == WebsiteWrite.PENDING)),
        "sequences_paused_out_of_office": await _count(session, select(func.count()).select_from(EmailSequence)
                                                       .where(EmailSequence.state == SequenceState.PAUSED_OOO)),
        "active_pauses": [pause_dict(f) for f in pauses],
        "today": {"campaign_day": capacity["campaign_day"], "mailboxes": per_box,
                  "new_contact_allowance": allowance},
        "not_tracked": ["quotes", "deposits", "payments", "paid_projects"],
        "complaint_rate_from_provider": "unknown",
    }
    if record:
        run = BriefRun(brief_date=day, generated_at=now)
        session.add(run)
        await session.flush()
        brief["brief_run_id"] = run.id
    return brief


def default_day(now: datetime) -> date:
    return sched.local_date(now, sched.load_zone(FOUNDER_ZONE))


__all__ = ["build_brief", "period_counts", "default_day", "day_bounds", "NOT_TRACKED"]
