"""
Shared fixtures for email engine v2 E1 (eligibility) tests: a throw-away SQLite database and small builders.
No test here touches the network: DNS, the verifier API, websites and the Node render check are all stubbed.
"""

from datetime import datetime, timedelta, timezone

import pytest
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

import backend.app.models  # noqa: F401  (registers every table on Base.metadata)
from backend.app.database import Base
from backend.app.engines.eligibility.verification import MxAnswer, SyntaxMxVerifier, VerificationLadder
from backend.app.models.business import Business, BusinessLocation, BusinessStatus
from backend.app.models.eligibility import CaptureMethod, EmailCapture
from backend.app.models.intelligence import CheckType, WebsiteCheck
from backend.app.services.eligibility_service import EligibilityService, capture_key

NOW = datetime(2026, 11, 12, 6, 0, tzinfo=timezone.utc)


@pytest.fixture
async def session(tmp_path):
    engine = create_async_engine(f"sqlite+aiosqlite:///{tmp_path / 'e1.db'}")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    factory = async_sessionmaker(engine, expire_on_commit=False)
    async with factory() as db:
        yield db
    await engine.dispose()


def mx_ok():
    async def lookup(domain):
        return MxAnswer(mx_hosts=[f"mx.{domain}"])
    return lookup


def ladder(paid=None, lookup=None):
    return VerificationLadder(SyntaxMxVerifier(lookup or mx_ok()), paid)


def service(db, paid=None, lookup=None, site_check=None):
    kwargs = {"site_check": site_check} if site_check else {}
    return EligibilityService(db, ladder=ladder(paid, lookup), **kwargs)


async def add_business(db, name="Glow Hair Studio", website="https://glowhair.in", country="IN", city="Surat",
                       social_urls=None, status=BusinessStatus.DISCOVERED):
    business = Business(name=name, normalized_name=name.lower(), country_code=country, website_url=website,
                        social_urls=social_urls, status=status)
    db.add(business)
    await db.flush()
    db.add(BusinessLocation(business_id=business.id, city=city, country_code=country))
    await db.flush()
    return business


async def add_capture(db, business, email, method=CaptureMethod.MAILTO, source_url="https://glowhair.in/contact",
                      excerpt="Write to us at {email} for bookings", captured_at=NOW - timedelta(days=1),
                      origin="test"):
    db.add(EmailCapture(business_id=business.id, email=email, method=method, raw_method=method.value,
                        source_url=source_url, excerpt=excerpt.format(email=email) if excerpt else None,
                        captured_at=captured_at, origin=origin,
                        capture_key=capture_key(business.id, email, origin, source_url)))
    await db.flush()


async def add_check(db, business, outcome, when, check_type=CheckType.SITE_FETCH, **detail):
    db.add(WebsiteCheck(business_id=business.id, check_type=check_type, target=business.website_url,
                        outcome=outcome, detail=detail, observed_at=when))
    await db.flush()


async def no_viewport_lead(db, email="info@glowhair.in", render="zoomed_out", **business_kwargs):
    """A business whose homepage has no viewport tag and opened zoomed-out in the phone check."""
    business = await add_business(db, **business_kwargs)
    await add_capture(db, business, email, source_url=f"{business.website_url}/contact")
    await add_check(db, business, "ok", NOW - timedelta(days=1), has_viewport=False,
                    final_url=business.website_url + "/")
    if render:
        await add_check(db, business, render, NOW - timedelta(hours=20), CheckType.PHONE_RENDER,
                        inner_width=980 if render == "zoomed_out" else 390,
                        final_url=business.website_url + "/", screenshot="E:/evidence/x.png")
    return business
