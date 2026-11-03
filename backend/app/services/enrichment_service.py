"""
Enrichment Service — coordinates contact discovery, verification,
classification, and database persistence.
"""

from datetime import datetime, timezone
from typing import Optional
import structlog
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.app.engines.enrichment.classifier import ContactClassifier
from backend.app.engines.enrichment.discovery import ContactDiscoveryEngine
from backend.app.engines.enrichment.verifier import EmailVerifier
from backend.app.models.business import Business
from backend.app.models.contact import Contact
from backend.app.models.opportunity import WebsiteAudit

logger = structlog.get_logger(__name__)


class EnrichmentService:
    """
    Coordinates Phase 3 contact enrichment pipeline:
    1. Discover raw candidate contacts
    2. Verify email deliverability & MX
    3. Classify job title & role hierarchy
    4. Persist validated contacts
    """

    def __init__(self, session: AsyncSession):
        self.session = session
        self.discovery = ContactDiscoveryEngine()
        self.verifier = EmailVerifier()
        self.classifier = ContactClassifier()

    async def enrich_business(self, business_id: int) -> dict:
        """
        Discover, verify, and store contacts for a business.
        """
        # Load business with audits
        stmt = (
            select(Business)
            .where(Business.id == business_id)
            .options(selectinload(Business.audits))
        )
        business = (await self.session.execute(stmt)).scalar_one_or_none()

        if not business:
            return {"error": f"Business {business_id} not found"}

        latest_audit = business.audits[-1] if business.audits else None

        # 1. Discover raw candidate contacts
        discovered_candidates = await self.discovery.discover_contacts(
            business=business,
            audit=latest_audit,
        )

        persisted_contacts = []
        for cand in discovered_candidates:
            # 2. Verify deliverability
            ver_res = self.verifier.verify(cand.email)

            # 3. Classify role & identity
            class_res = self.classifier.classify_contact(
                full_name=cand.full_name,
                job_title=cand.job_title,
                email=cand.email,
            )

            # 4. Check for existing contact
            existing_stmt = select(Contact).where(
                Contact.business_id == business.id,
                Contact.email == cand.email.lower(),
            )
            existing = (await self.session.execute(existing_stmt)).scalar_one_or_none()

            if existing:
                existing.email_status = ver_res.status
                existing.verification_score = ver_res.verification_score
                existing.has_valid_mx = ver_res.has_valid_mx
                existing.is_role_based = ver_res.is_role_based
                existing.is_disposable = ver_res.is_disposable
                existing.verified_at = datetime.now(timezone.utc)
                existing.role_level = class_res.role_level
                if class_res.first_name and not existing.first_name:
                    existing.first_name = class_res.first_name
                    existing.last_name = class_res.last_name
                    existing.full_name = class_res.full_name
                contact_record = existing
            else:
                contact_record = Contact(
                    business_id=business.id,
                    email=cand.email.lower(),
                    full_name=class_res.full_name,
                    first_name=class_res.first_name,
                    last_name=class_res.last_name,
                    job_title=class_res.job_title,
                    role_level=class_res.role_level,
                    email_status=ver_res.status,
                    verification_score=ver_res.verification_score,
                    has_valid_mx=ver_res.has_valid_mx,
                    is_role_based=ver_res.is_role_based,
                    is_disposable=ver_res.is_disposable,
                    phone=cand.phone or business.phone,
                    linkedin_url=cand.linkedin_url,
                    source_method=cand.source_method,
                    source_url=cand.source_url,
                    verification_details=ver_res.details,
                    verified_at=datetime.now(timezone.utc),
                )
                self.session.add(contact_record)

            persisted_contacts.append(
                {
                    "email": cand.email.lower(),
                    "name": class_res.full_name,
                    "role_level": class_res.role_level.value,
                    "status": ver_res.status.value,
                    "score": ver_res.verification_score,
                }
            )

        await self.session.flush()

        logger.info(
            "business_enriched",
            business_id=business.id,
            contacts_found=len(persisted_contacts),
        )

        return {
            "business_id": business.id,
            "business_name": business.name,
            "contacts_count": len(persisted_contacts),
            "contacts": persisted_contacts,
        }

    async def batch_enrich_businesses(self, limit: int = 25) -> dict:
        """
        Enrich businesses that currently have 0 contacts registered.
        """
        stmt = (
            select(Business.id)
            .outerjoin(Contact, Business.id == Contact.business_id)
            .where(Contact.id.is_(None))
            .limit(limit)
        )
        biz_ids = (await self.session.execute(stmt)).scalars().all()

        results = []
        for bid in biz_ids:
            res = await self.enrich_business(bid)
            results.append(res)

        return {
            "enriched_count": len(results),
            "results": results,
        }
