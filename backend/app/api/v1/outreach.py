"""
API v1 - Email engine v2, phase E1: eligibility and the founder's social-profile confirmations.

GET  /outreach/eligibility?status=eligible|hold&limit=     rows + counts by HOLD reason
POST /outreach/eligibility/evaluate                       re-run the rules (optionally the verifier ladder first)
POST /outreach/confirmations                              founder checked an Instagram bio by hand (SOCIAL_ONLY)
GET  /outreach/confirmations/pending?limit=               SOCIAL_ONLY candidates still to check
Nothing here sends anything. Invalid input returns 422 (same validated types as every other route).
"""

from datetime import datetime, timedelta, timezone
from typing import Annotated, Literal, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import AfterValidator, BaseModel, Field, StrictBool
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.database import get_db_session
from backend.app.engines.discovery.overture import social_platform
from backend.app.schemas.types import Email, HttpUrl, Opt
from backend.app.services.eligibility_service import EligibilityService

router = APIRouter(prefix="/outreach", tags=["Outreach eligibility (email engine v2)"])

MAX_EVALUATE_IDS = 1000
CLOCK_SKEW = timedelta(minutes=5)


def _instagram_profile(value: str) -> str:
    # Spec row 4: SOCIAL_ONLY is about the business's Instagram bio; the observation text names Instagram.
    if social_platform(value) != "instagram":
        raise ValueError("must be an instagram.com profile address")
    return value


InstagramUrl = Annotated[HttpUrl, AfterValidator(_instagram_profile)]


class EvaluateRequest(BaseModel):
    model_config = {"extra": "forbid"}
    business_ids: Optional[list[Annotated[int, Field(ge=1)]]] = Field(None, max_length=MAX_EVALUATE_IDS)
    # True = run the verifier ladder (MX lookup; Bouncer only with BOUNCER_API_KEY) for the addresses that
    # nothing else holds back, before deciding. False = use cached verifier results only.
    verify: bool = False


class ConfirmationRequest(BaseModel):
    model_config = {"extra": "forbid"}
    business_id: int = Field(ge=1)
    profile_url: InstagramUrl
    checked_at: datetime
    website_link_present: StrictBool   # the one fact this record proves: a real true / false only
    email_seen: Opt(Email) = None


@router.get("/eligibility")
async def list_eligibility(
    status: Optional[Literal["eligible", "hold"]] = None,
    limit: int = Query(100, ge=1, le=500),
    session: AsyncSession = Depends(get_db_session),
):
    """Eligibility rows (eligible first) with counts by HOLD reason over all rows."""
    return await EligibilityService(session).list_eligibility(status, limit)


@router.post("/eligibility/evaluate")
async def evaluate(body: Optional[EvaluateRequest] = None, session: AsyncSession = Depends(get_db_session)):
    body = body or EvaluateRequest()
    return await EligibilityService(session).evaluate(body.business_ids, verify=body.verify)


@router.post("/confirmations")
async def record_confirmation(body: ConfirmationRequest, session: AsyncSession = Depends(get_db_session)):
    """The founder looked at the business's Instagram bio. No website link -> SOCIAL_ONLY observation; an email
    shown in the bio -> Tier 1 provenance (method founder_confirmed)."""
    checked_at = body.checked_at if body.checked_at.tzinfo else body.checked_at.replace(tzinfo=timezone.utc)
    if checked_at > datetime.now(timezone.utc) + CLOCK_SKEW:
        raise HTTPException(status_code=422, detail=[{"loc": ["body", "checked_at"],
                                                      "msg": "checked_at cannot be in the future",
                                                      "type": "value_error"}])
    try:
        return await EligibilityService(session).record_confirmation(
            body.business_id, body.profile_url, checked_at, body.website_link_present, body.email_seen)
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@router.get("/confirmations/pending")
async def pending_confirmations(limit: int = Query(100, ge=1, le=500),
                                session: AsyncSession = Depends(get_db_session)):
    """SOCIAL_ONLY candidates (India, Instagram profile, no own website) without a founder check in 30 days."""
    return await EligibilityService(session).pending_confirmations(limit)
