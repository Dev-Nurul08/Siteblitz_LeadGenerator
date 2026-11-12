"""
API v1 - Email engine v2, phase E2: sending core (the E3 batch screen builds on these routes).

POST /outreach/sequences                        admit approved, eligible prospects for step 1 on a day (per-item
                                                admitted / refused with a code and a message, e.g. RAMP_LIMIT_REACHED)
POST /outreach/send-records/{id}/approve        text + approval for a reserved step 2 / 3
POST /outreach/send-records/{id}/resolve        a person decides an UNCERTAIN submission: ACCEPTED or FAILED + note
GET  /outreach/schedule?date=YYYY-MM-DD         every message of that recipient-local day
GET  /outreach/capacity?date=YYYY-MM-DD         per mailbox 30 / 25 / 5, new first contacts vs the ramp
GET  /outreach/pauses?active=true|false         pause / stop flags
POST /outreach/pauses                           clear one flag (who + a note)
GET  /outreach/settings/ramp                    current stage, limit and history
POST /outreach/settings/ramp                    change the stage (who + a note; up one stage at a time)
GET  /outreach/mailboxes                        mailboxes; never a password (only whether it is set in .env)
POST /outreach/mailboxes                        add, change or disable a mailbox (matched by slug)
Nothing here sends mail: scripts/outreach_worker.py does, in supervised windows. Invalid input returns 422.
"""

import re
from datetime import date
from typing import Annotated, Literal, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import AfterValidator, BaseModel, BeforeValidator, Field, StrictBool, StringConstraints, model_validator
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.config import get_settings
from backend.app.database import get_db_session
from backend.app.engines.eligibility.rules import FREE_MAIL
from backend.app.engines.sending.smtp import LOOPBACK_HOSTS
from backend.app.schemas.types import Email, OptionalText, Text
from backend.app.services.sending_service import SendingConfig, SendingService, ServiceError

router = APIRouter(prefix="/outreach", tags=["Outreach sending (email engine v2)"])

MAX_BATCH = 100
# Spec row 8: the cold sender is a Mailforge mailbox. Not Gmail / Workspace / Microsoft 365 / SES / SendGrid /
# Mailgun / Postmark / Brevo (host names as these providers publish them).
FORBIDDEN_SENDER_HOSTS = ("gmail.com", "googlemail.com", "google.com", "outlook.com", "office365.com", "hotmail.com",
                          "live.com", "amazonaws.com", "sendgrid.net", "mailgun.org", "postmarkapp.com",
                          "brevo.com", "sendinblue.com")
_HOST = re.compile(r"^(?=.{1,253}$)([a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?)(\.[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?)*$")


def _host(value: str) -> str:
    value = value.strip().lower()
    if value not in LOOPBACK_HOSTS and not _HOST.match(value):
        raise ValueError("must be a host name like smtp.example.com")
    if any(value == h or value.endswith("." + h) for h in FORBIDDEN_SENDER_HOSTS):
        raise ValueError("this provider is not allowed as the cold sender (spec row 8)")
    return value


def _person_name(value: str) -> str:
    if "@" in value or value.strip().lower() in ("siteblitz", "team", "sales", "info", "admin", "support"):
        raise ValueError("must be a real founder name (spec row 8)")
    return value


Host = Annotated[str, StringConstraints(max_length=255), AfterValidator(_host)]
Slug = Annotated[str, BeforeValidator(lambda v: v.strip().upper() if isinstance(v, str) else v),
                 StringConstraints(pattern=r"^[A-Z][A-Z0-9_]{0,39}$")]


def config() -> SendingConfig:
    return SendingConfig.from_settings(get_settings())


def service(session: AsyncSession = Depends(get_db_session)) -> SendingService:
    return SendingService(session, config())


def _raise(exc: ServiceError):
    raise HTTPException(status_code=exc.status, detail=str(exc))


class SequenceItem(BaseModel):
    model_config = {"extra": "forbid"}
    eligibility_id: int = Field(ge=1)
    subject: Text(300, min_length=1)
    body: Text(5000, min_length=1)
    content_version: OptionalText(50) = None
    approved_by: Text(100, min_length=1)


class SequencesRequest(BaseModel):
    model_config = {"extra": "forbid"}
    send_date: date
    items: list[SequenceItem] = Field(min_length=1, max_length=MAX_BATCH)


class FollowUpApproval(BaseModel):
    model_config = {"extra": "forbid"}
    body: Text(5000, min_length=1)
    approved_by: Text(100, min_length=1)
    content_version: OptionalText(50) = None


class ResolveRequest(BaseModel):
    model_config = {"extra": "forbid"}
    outcome: Literal["ACCEPTED", "FAILED"]
    resolved_by: Text(100, min_length=1)
    note: Text(500, min_length=3)


class ClearPauseRequest(BaseModel):
    model_config = {"extra": "forbid"}
    pause_id: int = Field(ge=1)
    cleared_by: Text(100, min_length=1)
    note: Text(500, min_length=3)


class RampRequest(BaseModel):
    model_config = {"extra": "forbid"}
    stage: int = Field(ge=0, le=4)
    changed_by: Text(100, min_length=1)
    note: Text(500, min_length=3)


class MailboxRequest(BaseModel):
    """No password field: extra keys are refused, so a password can never be posted and stored."""

    model_config = {"extra": "forbid"}
    slug: Slug
    address: Email
    display_name: Annotated[Text(60, min_length=2), AfterValidator(_person_name)]
    smtp_host: Host
    smtp_port: int = Field(ge=1, le=65535)
    smtp_tls: Literal["starttls", "ssl", "none"]
    imap_host: Optional[Host] = None
    imap_port: Optional[int] = Field(None, ge=1, le=65535)
    imap_tls: Optional[Literal["starttls", "ssl"]] = None
    username: Text(320, min_length=1)
    enabled: StrictBool = True
    disabled_reason: OptionalText(300) = None

    @model_validator(mode="after")
    def _rules(self):
        if self.smtp_tls == "none" and self.smtp_host not in LOOPBACK_HOSTS:
            raise ValueError("smtp_tls 'none' is only allowed for a loopback test server")
        if self.address.rsplit("@", 1)[1] in FREE_MAIL:
            raise ValueError("a free-mail address cannot be a sending mailbox (spec row 8)")
        return self


@router.post("/sequences")
async def create_sequences(body: SequencesRequest, svc: SendingService = Depends(service)):
    return await svc.create_sequences(body.send_date, [i.model_dump() for i in body.items])


@router.post("/send-records/{record_id}/approve")
async def approve_follow_up(record_id: int, body: FollowUpApproval, svc: SendingService = Depends(service)):
    try:
        return await svc.approve_follow_up(record_id, body.body, body.approved_by, body.content_version)
    except ServiceError as exc:
        _raise(exc)


@router.post("/send-records/{record_id}/resolve")
async def resolve(record_id: int, body: ResolveRequest, svc: SendingService = Depends(service)):
    try:
        return await svc.resolve_uncertain(record_id, body.outcome, body.resolved_by, body.note)
    except ServiceError as exc:
        _raise(exc)


@router.get("/schedule")
async def schedule(day: date = Query(..., alias="date"), svc: SendingService = Depends(service)):
    return await svc.schedule(day)


@router.get("/capacity")
async def capacity(day: date = Query(..., alias="date"), svc: SendingService = Depends(service)):
    return await svc.capacity(day)


@router.get("/pauses")
async def list_pauses(active: Optional[bool] = None, svc: SendingService = Depends(service)):
    return {"items": await svc.list_pauses(active)}


@router.post("/pauses")
async def clear_pause(body: ClearPauseRequest, svc: SendingService = Depends(service)):
    try:
        return await svc.clear_pause(body.pause_id, body.cleared_by, body.note)
    except ServiceError as exc:
        _raise(exc)


@router.get("/settings/ramp")
async def get_ramp(svc: SendingService = Depends(service)):
    return await svc.ramp_info()


@router.post("/settings/ramp")
async def set_ramp(body: RampRequest, svc: SendingService = Depends(service)):
    try:
        return await svc.set_ramp(body.stage, body.changed_by, body.note)
    except ServiceError as exc:
        _raise(exc)


@router.get("/mailboxes")
async def list_mailboxes(svc: SendingService = Depends(service)):
    return {"items": await svc.list_mailboxes()}


@router.post("/mailboxes")
async def upsert_mailbox(body: MailboxRequest, svc: SendingService = Depends(service)):
    try:
        return await svc.upsert_mailbox(body.model_dump())
    except ServiceError as exc:
        _raise(exc)


# ─── replies that arrive outside email (pre-send review 2026-11-12) ─────────────────────────────────────────────
# Owners often answer on WhatsApp or by phone. The IMAP loop (E4) never sees those answers, so without this mark
# Day 6 / Day 14 would still go out - the most likely real complaint found by the pre-send persona review.

class RepliedElsewhere(BaseModel):
    model_config = {"extra": "forbid"}
    channel: Literal["whatsapp", "phone", "in_person", "other"]
    stop: StrictBool = Field(..., description="true = they asked not to be contacted (suppressed everywhere)")
    marked_by: Text(100, min_length=1)
    note: OptionalText(300) = None


@router.post("/sequences/{sequence_id}/replied-elsewhere")
async def replied_elsewhere(sequence_id: int, body: RepliedElsewhere, svc: SendingService = Depends(service)):
    """Stop the cold sequence because the business answered outside email. With stop=true the address goes to the
    website suppression list first (DeliveryRulesService.suppress: a failed write raises E2's global pause
    SUPPRESSION_WRITE_FAILED), then an opt-out row, then the sequence is STOPPED_SUPPRESSED; otherwise STOPPED_REPLY.
    Either way every not-yet-submitted message of the sequence is cancelled."""
    from datetime import datetime, timezone

    from sqlalchemy import select

    from backend.app.engines.sending.suppression_client import SuppressionClient
    from backend.app.models.compliance import OptOut
    from backend.app.models.sending import EmailSequence, SequenceState
    from backend.app.services.delivery_rules_service import DeliveryRulesService

    sequence = await svc.session.get(EmailSequence, sequence_id)
    if sequence is None:
        raise HTTPException(status_code=404, detail=f"sequence {sequence_id} not found")
    now = datetime.now(timezone.utc)
    reason = f"replied via {body.channel} (marked by {body.marked_by})" + (f": {body.note}" if body.note else "")
    website_written = None
    if body.stop:
        settings = get_settings()
        rules = DeliveryRulesService(svc, SuppressionClient(settings.OUTREACH_PUBLIC_BASE_URL,
                                                            settings.OUTREACH_API_KEY))
        website_written = await rules.suppress(sequence.recipient_hash, "manual",
                                               f"replied_elsewhere:{body.channel}", now)
        address = (sequence.recipient_email or "").lower()
        if address and (await svc.session.execute(select(OptOut.id).where(OptOut.email == address))
                        ).scalar_one_or_none() is None:
            svc.session.add(OptOut(email=address, domain=address.rsplit("@", 1)[-1], reason="stop_elsewhere",
                                   source=body.channel.upper(), created_at=now))
        result = await svc.stop_sequence(sequence_id, SequenceState.STOPPED_SUPPRESSED, reason[:300], now)
    else:
        result = await svc.stop_sequence(sequence_id, SequenceState.STOPPED_REPLY, reason[:300], now)
    return {**result, "suppressed": body.stop, "website_written": website_written}


@router.get("/sequences")
async def find_sequences(business: str = Query(..., min_length=2, max_length=120),
                         live_only: bool = Query(True), svc: SendingService = Depends(service)):
    """Find a business's email sequence by (part of) its name, e.g. to mark a WhatsApp answer (/start-day)."""
    from sqlalchemy import select

    from backend.app.models.business import Business
    from backend.app.models.sending import EmailSequence, SequenceState

    query = (select(EmailSequence, Business.name).join(Business, Business.id == EmailSequence.business_id)
             .where(Business.name.ilike(f"%{business.strip()}%")).order_by(EmailSequence.id.desc()).limit(20))
    if live_only:
        query = query.where(EmailSequence.state.in_([SequenceState.ACTIVE, SequenceState.PAUSED_OOO,
                                                     SequenceState.HELD]))
    rows = (await svc.session.execute(query)).all()
    return {"items": [{"sequence_id": s.id, "business_name": name, "state": s.state.value,
                       "step": getattr(s, "step", None)} for s, name in rows]}
