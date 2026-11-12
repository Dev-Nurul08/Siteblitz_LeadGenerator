"""
API v1 - Email engine v2, phase E3: the batch screen (select, write, validate, review, approve, schedule).

GET  /outreach/batches/allowance?date=YYYY-MM-DD   new first contacts left for a sending day (default: the next
                                                   day with an open campaign window), mailbox capacity, pauses
GET  /outreach/batches/candidates?status=&reason=  E1 eligibility rows + whether each is already in a sequence or
                                                   an open batch, counts by HOLD reason
GET  /outreach/batches?limit=                      recent batches with counts
POST /outreach/batches                             {eligibility_ids, send_date?, created_by} -> 202; refuses ids that
                                                   are not eligible and a selection above the allowance (409, with
                                                   a message and the refused ids), then writes T1-T3 in the background
GET  /outreach/batches/{id}                        each lead READY / HOLD (+ codes) with subject, the three texts,
                                                   evidence, provenance, verification, proposed or real schedule
POST /outreach/batches/{id}/write                  continue writing after a restart (PENDING / WRITING leads)
POST /outreach/batches/{id}/approve                {lead_ids | "all_ready", approved_by}: E2 sequences, steps 2 + 3
                                                   approved with their texts
POST /outreach/batches/{id}/reject                 {lead_ids, reason, rejected_by}
Nothing here sends mail. Invalid input returns 422.
"""

from datetime import date
from typing import Annotated, Any, Literal, Optional, Union

import structlog
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.config import get_settings
from backend.app.database import get_async_session_factory, get_db_session
from backend.app.schemas.types import Text
from backend.app.services.batch_service import MAX_BATCH, RUNNING, BatchError, BatchService
from backend.app.services.sending_service import SendingConfig

logger = structlog.get_logger(__name__)
router = APIRouter(prefix="/outreach/batches", tags=["Outreach batches (email engine v2)"])

Id = Annotated[int, Field(ge=1)]


def get_writer_client() -> Any:
    """The model client for the writer. None = the writer builds the real Anthropic client from ANTHROPIC_API_KEY
    (no key = every lead HOLD WRITER_UNAVAILABLE). Tests override this dependency with a stub."""
    return None


def _service(session: AsyncSession, client: Any = None) -> BatchService:
    settings = get_settings()
    return BatchService(session, SendingConfig.from_settings(settings), settings, client)


def _raise(exc: BatchError):
    raise HTTPException(status_code=exc.status, detail=exc.detail())


async def write_in_background(batch_id: int, client: Any) -> None:
    """Runs after the response: its own session, a commit after each lead (the screen polls the progress)."""
    factory = get_async_session_factory()
    try:
        async with factory() as session:
            await _service(session, client).write(batch_id)
    except Exception as exc:   # the batch stays WRITING; the screen offers "continue writing"
        logger.error("batch_writing_failed", batch_id=batch_id, error=f"{type(exc).__name__}: {exc}")
    finally:
        RUNNING.discard(batch_id)


class CreateRequest(BaseModel):
    model_config = {"extra": "forbid"}
    eligibility_ids: list[Id] = Field(min_length=1, max_length=MAX_BATCH)
    send_date: Optional[date] = None
    created_by: Text(100, min_length=1)


class ApproveRequest(BaseModel):
    model_config = {"extra": "forbid"}
    lead_ids: Union[Literal["all_ready"], list[Id]] = Field(...)
    approved_by: Text(100, min_length=1)


class RejectRequest(BaseModel):
    model_config = {"extra": "forbid"}
    lead_ids: list[Id] = Field(min_length=1, max_length=MAX_BATCH)
    reason: Text(500, min_length=3)
    rejected_by: Text(100, min_length=1)


@router.get("/allowance")
async def allowance(day: Optional[date] = Query(None, alias="date"), session: AsyncSession = Depends(get_db_session)):
    return await _service(session).allowance(day)


@router.get("/candidates")
async def candidates(status: Literal["all", "eligible", "hold"] = "all",
                     reason: Optional[str] = Query(None, max_length=50), limit: int = Query(200, ge=1, le=500),
                     session: AsyncSession = Depends(get_db_session)):
    return await _service(session).candidates(status, reason, limit)


@router.get("")
async def list_batches(limit: int = Query(20, ge=1, le=100), session: AsyncSession = Depends(get_db_session)):
    return await _service(session).list_batches(limit)


@router.post("", status_code=202)
async def create_batch(body: CreateRequest, background: BackgroundTasks,
                       session: AsyncSession = Depends(get_db_session), client: Any = Depends(get_writer_client)):
    svc = _service(session, client)
    try:
        batch = await svc.create(body.eligibility_ids, body.send_date, body.created_by)
    except BatchError as exc:
        _raise(exc)
    await session.commit()
    RUNNING.add(batch.id)   # the screen shows "writing" at once; write() keeps it until it ends
    detail = await svc.detail(batch.id)
    # End this request's (read) transaction before the background writer starts: an open SQLite read lock would
    # make the writer's first commit wait and fail with "database is locked".
    await session.commit()
    background.add_task(write_in_background, batch.id, client)
    return detail


@router.get("/{batch_id}")
async def batch_detail(batch_id: int, session: AsyncSession = Depends(get_db_session)):
    try:
        return await _service(session).detail(batch_id)
    except BatchError as exc:
        _raise(exc)


@router.post("/{batch_id}/write", status_code=202)
async def continue_writing(batch_id: int, background: BackgroundTasks,
                           session: AsyncSession = Depends(get_db_session), client: Any = Depends(get_writer_client)):
    svc = _service(session, client)
    try:
        detail = await svc.detail(batch_id)
    except BatchError as exc:
        _raise(exc)
    if batch_id in RUNNING:
        raise HTTPException(status_code=409, detail={"code": "ALREADY_WRITING",
                                                     "message": f"batch {batch_id} is being written now"})
    if detail["status"] != "WRITING":
        raise HTTPException(status_code=409, detail={"code": "NOTHING_TO_WRITE",
                                                     "message": f"batch {batch_id} has no lead waiting to be written"})
    await session.commit()   # no open read transaction while the background writer runs (SQLite locks)
    background.add_task(write_in_background, batch_id, client)
    RUNNING.add(batch_id)
    return {**detail, "writing_active": True}


@router.post("/{batch_id}/approve")
async def approve(batch_id: int, body: ApproveRequest, session: AsyncSession = Depends(get_db_session)):
    svc = _service(session)
    try:
        result = await svc.approve(batch_id, None if body.lead_ids == "all_ready" else body.lead_ids,
                                   body.approved_by)
    except BatchError as exc:
        _raise(exc)
    return {**result, "batch": await svc.detail(batch_id)}


@router.post("/{batch_id}/reject")
async def reject(batch_id: int, body: RejectRequest, session: AsyncSession = Depends(get_db_session)):
    svc = _service(session)
    try:
        result = await svc.reject(batch_id, body.lead_ids, body.reason, body.rejected_by)
    except BatchError as exc:
        _raise(exc)
    return {**result, "batch": await svc.detail(batch_id)}
