"""
API v1 - Email engine v2, phase E4: the reply loop, the daily brief and what `/start-day` calls.

POST /outreach/reconcile                     read every enabled mailbox over IMAP (INBOX + junk), apply stops,
                                             pauses and bounces, label, draft; 409 while another reconcile runs
GET  /outreach/inbound?needs_founder=true    messages the founder must look at (complaints, commitment requests,
                                             unmatched, no label)
POST /outreach/inbound/{id}/close            the founder handled a message himself (who + a note)
GET  /outreach/drafts?state=WAITING          AI-drafted replies waiting for approval (the optional stop
                                             confirmations only with include_optional=true)
POST /outreach/drafts/{id}/approve           send it now (E2 SMTP path, same mailbox, threaded, fresh suppression
                                             check, pauses, the mailbox's 30-a-day ceiling)
POST /outreach/drafts/{id}/reject            reject (optionally close the thread: no answer is owed any more)
POST /outreach/drafts/{id}/regenerate        a new draft for the same message
GET  /outreach/brief?date=YYYY-MM-DD         the daily brief: real counts only (default date: today, India time)
Invalid input returns 422.
"""

from datetime import date
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, StrictBool
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.config import get_settings
from backend.app.database import get_async_session_factory, get_db_session
from backend.app.schemas.types import OptionalText, Text
from backend.app.services.brief_service import build_brief, default_day
from backend.app.services.outreach_worker import WorkerLock
from backend.app.services.reply_service import ReplyLoop, build_reply_loop, reconcile_lock_path
from backend.app.services.sending_service import ServiceError

router = APIRouter(prefix="/outreach", tags=["Outreach replies (email engine v2)"])

DRAFT_STATES = ("WAITING", "OPTIONAL", "SENDING", "SENT", "FAILED", "UNCERTAIN", "REJECTED", "SUPERSEDED", "BLOCKED")


def reply_loop() -> ReplyLoop:
    """Everything from settings; tests replace this dependency (app.dependency_overrides)."""
    return build_reply_loop(get_settings(), get_async_session_factory())


def lock_file() -> Path:
    return reconcile_lock_path(get_settings().DATABASE_URL)


def _raise(exc: ServiceError):
    raise HTTPException(status_code=exc.status, detail=str(exc))


class ApproveRequest(BaseModel):
    model_config = {"extra": "forbid"}
    approved_by: Text(100, min_length=1)


class RejectRequest(BaseModel):
    model_config = {"extra": "forbid"}
    rejected_by: Text(100, min_length=1)
    note: Text(500, min_length=3)
    close_thread: StrictBool = False


class RegenerateRequest(BaseModel):
    model_config = {"extra": "forbid"}
    requested_by: Text(100, min_length=1)
    note: OptionalText(500) = None


class CloseRequest(BaseModel):
    model_config = {"extra": "forbid"}
    closed_by: Text(100, min_length=1)
    note: Text(500, min_length=3)


@router.post("/reconcile")
async def reconcile(loop: ReplyLoop = Depends(reply_loop), path: Path = Depends(lock_file)):
    lock = WorkerLock(path)
    if not lock.acquire():
        raise HTTPException(status_code=409, detail=f"a reconcile is already running ({lock.holder()})")
    try:
        return await loop.reconcile()
    finally:
        lock.release()


@router.get("/inbound")
async def list_inbound(needs_founder: bool = False, limit: int = Query(100, ge=1, le=500),
                       loop: ReplyLoop = Depends(reply_loop), session: AsyncSession = Depends(get_db_session)):
    return {"items": await loop.list_inbound(session, needs_founder=needs_founder, limit=limit)}


@router.post("/inbound/{inbound_id}/close")
async def close_inbound(inbound_id: int, body: CloseRequest, loop: ReplyLoop = Depends(reply_loop),
                        session: AsyncSession = Depends(get_db_session)):
    try:
        return await loop.close_inbound(session, inbound_id, body.closed_by, body.note)
    except ServiceError as exc:
        _raise(exc)


@router.get("/drafts")
async def list_drafts(state: Optional[str] = Query("WAITING"), include_optional: bool = False,
                      loop: ReplyLoop = Depends(reply_loop), session: AsyncSession = Depends(get_db_session)):
    if state is not None and state.upper() not in DRAFT_STATES:
        raise HTTPException(status_code=422, detail=f"state must be one of {', '.join(DRAFT_STATES)}")
    return {"items": await loop.list_drafts(session, state.upper() if state else None, include_optional)}


@router.post("/drafts/{draft_id}/approve")
async def approve_draft(draft_id: int, body: ApproveRequest, loop: ReplyLoop = Depends(reply_loop)):
    try:
        return await loop.approve(draft_id, body.approved_by)
    except ServiceError as exc:
        _raise(exc)


@router.post("/drafts/{draft_id}/reject")
async def reject_draft(draft_id: int, body: RejectRequest, loop: ReplyLoop = Depends(reply_loop),
                       session: AsyncSession = Depends(get_db_session)):
    try:
        return await loop.reject(session, draft_id, body.rejected_by, body.note, body.close_thread)
    except ServiceError as exc:
        _raise(exc)


@router.post("/drafts/{draft_id}/regenerate")
async def regenerate_draft(draft_id: int, body: RegenerateRequest, loop: ReplyLoop = Depends(reply_loop)):
    try:
        return await loop.regenerate(draft_id, body.requested_by, body.note)
    except ServiceError as exc:
        _raise(exc)


@router.get("/brief")
async def brief(day: Optional[date] = Query(None, alias="date"), loop: ReplyLoop = Depends(reply_loop),
                session: AsyncSession = Depends(get_db_session)):
    now = loop.now()
    return await build_brief(session, loop.config, day or default_day(now), now)
