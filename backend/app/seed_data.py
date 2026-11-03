"""
Comprehensive database seeder for SiteBlitz Lead Intelligence OS.
Populates realistic sample data across all 5 architectural phases.
"""

import asyncio
from datetime import datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.database import Base, get_async_engine, get_async_session_factory
from backend.app.models.business import (
    Business,
    BusinessCategory,
    BusinessLocation,
    BusinessStatus,
    BusinessType,
    WebsiteStatus,
)
from backend.app.models.campaign import (
    AnalyticsEvent,
    Campaign,
    CampaignStatus,
    CRMDeal,
    DealStage,
    EventType,
    MessageStatus,
    OutreachMessage,
)
from backend.app.models.compliance import (
    ComplianceEvaluation,
    LeadStatus,
    LegalBasis,
    LegalFramework,
    OptOut,
    OutreachChannel,
    OutreachMode,
    QualifiedLead,
)
from backend.app.models.contact import (
    Contact,
    EmailVerificationStatus,
    RoleLevel,
)
from backend.app.models.opportunity import (
    Opportunity,
    OpportunityPriority,
    OpportunityStatus,
    ServiceCategory,
    WebsiteAudit,
)
from backend.app.models.source import Source, SourceLicense, SourceStatus


async def seed_all():
    engine = get_async_engine()

    # 1. Ensure all tables are created
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session_factory = get_async_session_factory()
    async with session_factory() as session:
        # Check if already seeded with campaigns
        camp_check = await session.execute(select(Campaign))
        if camp_check.scalars().first():
            print("Database already has campaigns data. Seeding complete.")
            return

        now = datetime.now(timezone.utc)

        # ─── Sources ────────────────────────────────────────────────
        # Delete any existing sources to cleanly recreate or avoid duplicates
        existing_sources = (await session.execute(select(Source))).scalars().all()
        if not existing_sources:
            osm_source = Source(
                name="OpenStreetMap Overpass API",
                slug="openstreetmap",
                license_type=SourceLicense.OPEN_LICENSE,
                status=SourceStatus.ACTIVE,
                attribution_required=True,
                attribution_text="© OpenStreetMap contributors (ODbL)",
            )
            wikidata_source = Source(
                name="Wikidata SPARQL Endpoint",
                slug="wikidata",
                license_type=SourceLicense.OPEN_LICENSE,
                status=SourceStatus.ACTIVE,
                attribution_required=True,
                attribution_text="Wikidata (CC0)",
            )
            session.add_all([osm_source, wikidata_source])
            await session.flush()

        # ─── Businesses & Locations & Categories ─────────────────────
        businesses_data = [
            {
                "name": "Apex Dental & Orthodontics",
                "country_code": "US",
                "country_name": "United States",
                "city": "Chicago",
                "state": "IL",
                "website_url": "https://apexdentalcare.com",
                "website_status": WebsiteStatus.FOUND,
                "category": "Dental Clinic",
                "phone": "+1 312 555 0192",
                "email": "office@apexdentalcare.com",
                "contact_name": "Dr. Sarah Jenkins",
                "contact_title": "Founder & Lead Orthodontist",
                "contact_email": "sjenkins@apexdentalcare.com",
                "contact_role": RoleLevel.EXECUTIVE,
                "service_category": ServiceCategory.ONLINE_BOOKING,
                "opp_title": "Automated Online Patient Scheduling Engine",
                "opp_summary": "High-volume dental practice currently forces patients to call during office hours. Direct 24/7 calendar booking increases new patient intake by 45%.",
                "opp_score": 88.0,
                "opp_priority": OpportunityPriority.HIGH,
                "deal_stage": DealStage.MEETING_SCHEDULED,
                "deal_val": 8500.0,
            },
            {
                "name": "Trattoria Da Bella",
                "country_code": "US",
                "country_name": "United States",
                "city": "Boston",
                "state": "MA",
                "website_url": "https://bellaboston.com",
                "website_status": WebsiteStatus.FOUND,
                "category": "Italian Restaurant",
                "phone": "+1 617 555 0144",
                "email": "ciao@bellaboston.com",
                "contact_name": "Marco Rossi",
                "contact_title": "Co-Owner & Managing Director",
                "contact_email": "marco@bellaboston.com",
                "contact_role": RoleLevel.EXECUTIVE,
                "service_category": ServiceCategory.MOBILE_APP,
                "opp_title": "Direct Digital Ordering & Customer Loyalty App",
                "opp_summary": "High repeat dine-in and takeout volume paying 25% third-party marketplace fees. Branded iOS/Android ordering app recovers margins.",
                "opp_score": 92.0,
                "opp_priority": OpportunityPriority.CRITICAL,
                "deal_stage": DealStage.PROPOSAL_SENT,
                "deal_val": 14000.0,
            },
            {
                "name": "Kensington Luxury Interiors",
                "country_code": "GB",
                "country_name": "United Kingdom",
                "city": "London",
                "state": "Greater London",
                "website_url": "https://kensingtoninteriors.co.uk",
                "website_status": WebsiteStatus.FOUND,
                "category": "Interior Architecture",
                "phone": "+44 20 7946 0912",
                "email": "enquiries@kensingtoninteriors.co.uk",
                "contact_name": "Alistair Sterling",
                "contact_title": "Managing Director",
                "contact_email": "a.sterling@kensingtoninteriors.co.uk",
                "contact_role": RoleLevel.EXECUTIVE,
                "service_category": ServiceCategory.WEBSITE_REDESIGN,
                "opp_title": "Mobile Responsive Redesign & 3D Project Portfolio",
                "opp_summary": "Outdated non-responsive viewport layout built in 2017. Luxury high-net-worth clientele expect flawless mobile and interactive project galleries.",
                "opp_score": 84.0,
                "opp_priority": OpportunityPriority.HIGH,
                "deal_stage": DealStage.NEGOTIATION,
                "deal_val": 18500.0,
            },
            {
                "name": "München Craft Roasters",
                "country_code": "DE",
                "country_name": "Germany",
                "city": "Munich",
                "state": "Bavaria",
                "website_url": "https://muenchen-craftcoffee.de",
                "website_status": WebsiteStatus.FOUND,
                "category": "Specialty Coffee Roastery",
                "phone": "+49 89 2018 4591",
                "email": "kontakt@muenchen-craftcoffee.de",
                "contact_name": "Felix Weber",
                "contact_title": "Operations & Growth Director",
                "contact_email": "felix@muenchen-craftcoffee.de",
                "contact_role": RoleLevel.MANAGEMENT,
                "service_category": ServiceCategory.ECOMMERCE_EXPANSION,
                "opp_title": "Full Direct-to-Consumer E-Commerce Storefront",
                "opp_summary": "Retail roast beans showcased only as static catalog with no digital checkout or subscription model.",
                "opp_score": 79.0,
                "opp_priority": OpportunityPriority.HIGH,
                "deal_stage": DealStage.CONTACTED,
                "deal_val": 9500.0,
            },
            {
                "name": "Vance & Sterling Legal Associates",
                "country_code": "CA",
                "country_name": "Canada",
                "city": "Toronto",
                "state": "ON",
                "website_url": "https://vancestoronto.ca",
                "website_status": WebsiteStatus.FOUND,
                "category": "Commercial Law Firm",
                "phone": "+1 416 555 0831",
                "email": "info@vancestoronto.ca",
                "contact_name": "Claire Vance",
                "contact_title": "Senior Partner",
                "contact_email": "cvance@vancestoronto.ca",
                "contact_role": RoleLevel.EXECUTIVE,
                "service_category": ServiceCategory.CUSTOM_WEB_APP,
                "opp_title": "Secure Client Intake Portal & Document Exchange",
                "opp_summary": "Corporate law firm relying on unencrypted email attachments for onboarding corporate clients.",
                "opp_score": 86.0,
                "opp_priority": OpportunityPriority.HIGH,
                "deal_stage": DealStage.WON,
                "deal_val": 22000.0,
            },
            {
                "name": "Harborview Artisan Bakery",
                "country_code": "AU",
                "country_name": "Australia",
                "city": "Sydney",
                "state": "NSW",
                "website_url": None,
                "website_status": WebsiteStatus.NOT_FOUND,
                "category": "Bakery & Patisserie",
                "phone": "+61 2 9555 0188",
                "email": "orders@harborviewbakery.com.au",
                "contact_name": "Liam Hemsworth",
                "contact_title": "Proprietor & Master Baker",
                "contact_email": "liam@harborviewbakery.com.au",
                "contact_role": RoleLevel.EXECUTIVE,
                "service_category": ServiceCategory.NEW_WEBSITE,
                "opp_title": "Complete Brand Identity & Modern Responsive Website",
                "opp_summary": "Top-rated bakery operating solely on social media without an official website or catering request portal.",
                "opp_score": 95.0,
                "opp_priority": OpportunityPriority.CRITICAL,
                "deal_stage": DealStage.PROSPECT,
                "deal_val": 6000.0,
            },
            {
                "name": "Atelier Mode Parisienne",
                "country_code": "FR",
                "country_name": "France",
                "city": "Paris",
                "state": "Île-de-France",
                "website_url": "https://ateliermodeparis.fr",
                "website_status": WebsiteStatus.FOUND,
                "category": "Designer Boutique",
                "phone": "+33 1 42 68 55 00",
                "email": "contact@ateliermodeparis.fr",
                "contact_name": "Camille Laurent",
                "contact_title": "Creative & Commercial Director",
                "contact_email": "camille@ateliermodeparis.fr",
                "contact_role": RoleLevel.EXECUTIVE,
                "service_category": ServiceCategory.ECOMMERCE_EXPANSION,
                "opp_title": "Global Multi-Currency Luxury Fashion Storefront",
                "opp_summary": "High-end Parisian fashion label with strong international demand but no Shopify/e-commerce checkout.",
                "opp_score": 91.0,
                "opp_priority": OpportunityPriority.CRITICAL,
                "deal_stage": DealStage.WON,
                "deal_val": 28000.0,
            },
        ]

        # ─── Create Campaign ────────────────────────────────────────
        campaign = Campaign(
            name="Q4 Enterprise Modernization & Digital Apps",
            description="Multi-market outbound campaign targeting high-growth businesses with verified digital service needs.",
            status=CampaignStatus.RUNNING,
            target_service_category="ALL_SERVICES",
            daily_send_limit=50,
            delay_seconds_between_sends=120,
            send_window_start_hour=9,
            send_window_end_hour=17,
            total_leads_count=len(businesses_data),
            sent_count=5,
            opened_count=4,
            replied_count=3,
            converted_count=2,
            started_at=now - timedelta(days=5),
        )
        session.add(campaign)
        await session.flush()

        # Seed global suppression entry
        opt_out = OptOut(
            email="blocked-user@spamsuppression.org",
            domain="spamsuppression.org",
            reason="Global test suppression check",
            source="REGISTRY_INIT",
        )
        session.add(opt_out)

        for b_dict in businesses_data:
            # 1. Business
            b = Business(
                name=b_dict["name"],
                country_code=b_dict["country_code"],
                country_name=b_dict["country_name"],
                website_url=b_dict["website_url"],
                website_status=b_dict["website_status"],
                business_type=BusinessType.COMPANY,
                phone=b_dict["phone"],
                email=b_dict["email"],
                status=BusinessStatus.ACTIVE,
                normalized_name=b_dict["name"].lower().replace("&", "and"),
            )
            session.add(b)
            await session.flush()

            # Location & Category
            loc = BusinessLocation(
                business_id=b.id,
                city=b_dict["city"],
                state_province=b_dict["state"],
                country_code=b_dict["country_code"],
                is_primary=True,
            )
            cat = BusinessCategory(
                business_id=b.id,
                category_name=b_dict["category"],
                normalized_category=b_dict["category"].lower().replace(" ", "_"),
                source_category=b_dict["category"].lower(),
                is_primary=True,
            )
            session.add_all([loc, cat])

            # 2. Opportunity
            opp = Opportunity(
                business_id=b.id,
                service_category=b_dict["service_category"],
                title=b_dict["opp_title"],
                summary=b_dict["opp_summary"],
                score=b_dict["opp_score"],
                priority=b_dict["opp_priority"],
                status=OpportunityStatus.QUALIFIED,
                confidence=0.95,
            )
            session.add(opp)
            await session.flush()

            # 3. Contact
            first_name = b_dict["contact_name"].split()[0]
            if first_name.startswith("Dr.") or first_name.startswith("Mr."):
                first_name = b_dict["contact_name"].split()[1]

            contact = Contact(
                business_id=b.id,
                full_name=b_dict["contact_name"],
                first_name=first_name,
                job_title=b_dict["contact_title"],
                email=b_dict["contact_email"],
                role_level=b_dict["contact_role"],
                email_status=EmailVerificationStatus.VERIFIED,
                verification_score=0.96,
                has_valid_mx=True,
                is_role_based=False,
                is_disposable=False,
                source_method="HTML_CONTACT_CRAWL",
                verified_at=now,
            )
            session.add(contact)
            await session.flush()

            # 4. Compliance Evaluation
            fw_map = {
                "US": LegalFramework.CAN_SPAM,
                "GB": LegalFramework.GDPR_UK,
                "DE": LegalFramework.GDPR_EU,
                "FR": LegalFramework.GDPR_EU,
                "CA": LegalFramework.CASL,
                "AU": LegalFramework.AUSTRALIA_SPAM_ACT,
            }
            fw = fw_map.get(b_dict["country_code"], LegalFramework.GENERAL_B2B)
            mode = OutreachMode.MANUAL_REVIEW_ONLY if b_dict["country_code"] in ("DE", "CA") else OutreachMode.AUTOMATED

            comp_eval = ComplianceEvaluation(
                business_id=b.id,
                contact_id=contact.id,
                opportunity_id=opp.id,
                country_code=b_dict["country_code"],
                legal_framework=fw,
                is_outreach_permitted=True,
                outreach_mode=mode,
                legal_basis=LegalBasis.LEGITIMATE_INTEREST if "GDPR" in fw.value else LegalBasis.OPT_OUT_REGIME,
                risk_score=0.20 if mode == OutreachMode.AUTOMATED else 0.55,
                requirements_checklist={"valid_postal_address": True, "clear_opt_out_link": True},
                evaluation_notes=f"Compliant under {fw.value} regulations.",
            )
            session.add(comp_eval)
            await session.flush()

            # 5. Qualified Lead & AI Personalized Pitch
            subject = f"Digital enhancement concept for {b.name}"
            pitch = f"""Hi {first_name},

I was researching top businesses in {b_dict['city']} and came across {b.name}.

{b_dict['opp_summary']}

At SiteBlitz, we engineer lightning-fast modern web applications and mobile solutions designed to maximize client conversion. We put together a brief preview illustrating how {b.name} could look with direct mobile ordering and instant response times.

Would you be open to a 5-minute preview this week?

Best regards,

Marcus Vance
Solutions Director | SiteBlitz
---
100 Innovation Way, Suite 400, New York, NY 10001
To unsubscribe from future updates: http://localhost:8000/api/v1/qualification/unsubscribe?email={b_dict['contact_email']}"""

            lead_status = LeadStatus.READY_FOR_OUTREACH if mode == OutreachMode.AUTOMATED else LeadStatus.NEEDS_REVIEW
            ql = QualifiedLead(
                business_id=b.id,
                contact_id=contact.id,
                opportunity_id=opp.id,
                compliance_evaluation_id=comp_eval.id,
                composite_score=b_dict["opp_score"],
                lead_status=lead_status,
                outreach_channel=OutreachChannel.EMAIL,
                personalized_subject=subject,
                personalized_pitch=pitch,
                pitch_template_used="ENTERPRISE_PREVIEW",
                validation_passed=True,
                validation_flags=[],
            )
            session.add(ql)
            await session.flush()

            # 6. Outreach Message
            msg = OutreachMessage(
                campaign_id=campaign.id,
                lead_id=ql.id,
                contact_id=contact.id,
                business_id=b.id,
                sender_mailbox="marcus.vance@siteblitz.agency",
                recipient_email=contact.email,
                subject=subject,
                body_text=pitch,
                status=MessageStatus.SENT if b_dict["deal_stage"] != DealStage.PROSPECT else MessageStatus.QUEUED,
                scheduled_at=now - timedelta(hours=4),
                sent_at=now - timedelta(hours=3) if b_dict["deal_stage"] != DealStage.PROSPECT else None,
            )
            session.add(msg)
            await session.flush()

            # 7. CRM Deal
            deal = CRMDeal(
                lead_id=ql.id,
                business_id=b.id,
                title=f"{b_dict['opp_title'][:40]} ({b.name})",
                stage=b_dict["deal_stage"],
                estimated_value=b_dict["deal_val"],
                notes=f"Active prospect from {b_dict['city']}. Identified opportunity: {b_dict['service_category'].value}",
                last_activity_at=now - timedelta(hours=2),
            )
            session.add(deal)

            # 8. Analytics Event
            event = AnalyticsEvent(
                event_type=EventType.MESSAGE_SENT,
                campaign_id=campaign.id,
                message_id=msg.id,
                lead_id=ql.id,
                metadata_payload={"recipient": contact.email, "city": b_dict["city"]},
            )
            session.add(event)

        await session.commit()
        print("Successfully seeded all 5 phases with realistic enterprise lead data!")


if __name__ == "__main__":
    asyncio.run(seed_all())
