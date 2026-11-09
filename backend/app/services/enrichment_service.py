"""
Enrichment Service — coordinates contact discovery, verification,
classification, and database persistence (Phase 3).
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

            verification_payload = {
                **ver_res.details,
                "suggested_correction": ver_res.suggested_correction,
                "mx_records": ver_res.mx_records,
                "mail_provider": ver_res.mail_provider,
                "department": class_res.department,
                "seniority_score": class_res.seniority_score,
            }

            if existing:
                existing.email_status = ver_res.status
                existing.verification_score = ver_res.verification_score
                existing.has_valid_mx = ver_res.has_valid_mx
                existing.is_role_based = ver_res.is_role_based
                existing.is_disposable = ver_res.is_disposable
                existing.verified_at = datetime.now(timezone.utc)
                existing.role_level = class_res.role_level
                existing.verification_details = verification_payload
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
                    verification_details=verification_payload,
                    verified_at=datetime.now(timezone.utc),
                )
                self.session.add(contact_record)

            # Auto-update business primary email/phone if business is missing them
            if not business.email and ver_res.has_valid_mx:
                business.email = cand.email.lower()
            if not business.phone and cand.phone:
                business.phone = cand.phone

            persisted_contacts.append(
                {
                    "email": cand.email.lower(),
                    "name": class_res.full_name,
                    "job_title": class_res.job_title,
                    "role_level": class_res.role_level.value,
                    "department": class_res.department,
                    "status": ver_res.status.value,
                    "score": ver_res.verification_score,
                    "mail_provider": ver_res.mail_provider,
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

    async def discover_domain_contacts(self, domain_or_url: str) -> dict:
        """
        On-demand domain contact discovery and verification without saving to DB.
        """
        temp_biz = Business(
            name=domain_or_url,
            normalized_name=domain_or_url.lower(),
            website_url=domain_or_url,
        )

        candidates = await self.discovery.discover_contacts(temp_biz)
        verified = []
        for cand in candidates:
            ver = self.verifier.verify(cand.email)
            cls = self.classifier.classify_contact(cand.full_name, cand.job_title, cand.email)
            verified.append({
                "email": cand.email,
                "name": cls.full_name,
                "first_name": cls.first_name,
                "last_name": cls.last_name,
                "job_title": cls.job_title,
                "role_level": cls.role_level.value,
                "department": cls.department,
                "status": ver.status.value,
                "score": ver.verification_score,
                "has_valid_mx": ver.has_valid_mx,
                "is_role_based": ver.is_role_based,
                "is_free_email": ver.is_free_email,
                "mail_provider": ver.mail_provider,
                "suggested_correction": ver.suggested_correction,
                "source_method": cand.source_method,
            })

        return {
            "query": domain_or_url,
            "contacts_found": len(verified),
            "contacts": verified,
        }
