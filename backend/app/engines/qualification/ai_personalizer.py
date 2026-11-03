"""
AI Personalization Engine (Phase 4).

Generates hyper-tailored, compliance-ready B2B sales outreach pitches
derived from verified technical signals (mobile responsiveness, booking engine,
SSL status, CMS architecture) discovered during Phase 2 website audits.
"""

from dataclasses import dataclass, field
from typing import Dict, Optional

from backend.app.models.business import Business
from backend.app.models.contact import Contact
from backend.app.models.opportunity import Opportunity, ServiceCategory


@dataclass
class PersonalizationResult:
    """Generated outreach pitch package."""

    subject_line: str
    body_text: str
    template_id: str
    signals_referenced: list = field(default_factory=list)


class AIPersonalizer:
    """
    Transforms audit evidence and business attributes into personalized sales copy.
    """

    MANDATORY_FOOTER = """

---
Sent by SiteBlitz Intelligence | Modern Web & Mobile Application Development
100 Innovation Way, Suite 400, New York, NY 10001
If you do not wish to receive communications regarding your website and digital presence, click here to opt out: {{UNSUBSCRIBE_LINK}}"""

    def generate_pitch(
        self,
        business: Business,
        contact: Contact,
        opportunity: Opportunity,
        sender_name: str = "Marcus Vance",
        sender_title: str = "Digital Architecture Lead",
    ) -> PersonalizationResult:
        """
        Synthesize customized pitch based on opportunity category and audit signals.
        """
        contact_name = contact.first_name or (contact.full_name.split()[0] if contact.full_name else "there")
        business_name = business.name
        city = business.city or "your area"
        website = business.website or "your business listing"
        category = opportunity.service_category

        signals_used = []

        if category == ServiceCategory.NEW_WEBSITE:
            template_id = "NEW_WEBSITE_DISCOVERY"
            signals_used.append("Missing dedicated domain/website")
            subject = f"Website concept & digital presence for {business_name}"
            body = f"""Hi {contact_name},

I came across {business_name} while researching top {business.category or 'local'} businesses in {city}.

I noticed {business_name} currently doesn't have a dedicated website, meaning local customers searching online for your services are likely finding competitors instead.

At SiteBlitz, we specialize in high-converting, lightning-fast websites built specifically for businesses like yours. We recently built a preview concept showing how {business_name} could look with an interactive mobile-first layout and direct customer inquiry forms.

Would you be open to seeing a 3-minute video walkthrough of the preview concept this week?

Best regards,

{sender_name}
{sender_title} | SiteBlitz
{self.MANDATORY_FOOTER}"""

        elif category == ServiceCategory.WEBSITE_REDESIGN:
            template_id = "MOBILE_RESPONSIVE_REDESIGN"
            signals_used.append("Mobile viewport optimization needed")
            subject = f"Quick observation regarding {business_name}'s mobile site"
            body = f"""Hi {contact_name},

I was browsing {business_name}'s website ({website}) from my smartphone and noticed that the layout doesn't automatically adapt to mobile screens, causing text and menus to scale awkwardly.

With over 68% of local web traffic originating from mobile devices, a responsive layout directly impacts whether visitors call or bounce to another provider.

Our agency specializes in modernizing web platforms with sleek responsive designs, fast load times, and frictionless mobile experiences. We've prepared a brief audit highlighting 3 immediate improvements for {business_name}.

Would you be open to a quick 5-minute call or a summary link of the audit?

Best regards,

{sender_name}
{sender_title} | SiteBlitz
{self.MANDATORY_FOOTER}"""

        elif category == ServiceCategory.ONLINE_BOOKING:
            template_id = "BOOKING_CONVERSION_SYSTEM"
            signals_used.append("Absence of direct online appointment scheduler")
            subject = f"Automated online booking for {business_name}"
            body = f"""Hi {contact_name},

I was looking at {business_name} and was impressed by your reviews in {city}.

While reviewing {website}, I noticed that clients currently have to call or email manually to book appointments or request service times. In 2026, over 70% of clients prefer booking instantly online 24/7 without waiting for business hours.

We build modern, automated online booking engines that integrate directly into your website and sync seamlessly with your calendar, reducing admin calls while increasing confirmed bookings.

Could I share a quick demo of how self-service booking would function for {business_name}?

Best regards,

{sender_name}
{sender_title} | SiteBlitz
{self.MANDATORY_FOOTER}"""

        elif category == ServiceCategory.MOBILE_APP:
            template_id = "MOBILE_APP_REORDERING"
            signals_used.append("High repeat-customer volume, opportunity for loyalty app")
            subject = f"Mobile app & loyalty concept for {business_name}"
            body = f"""Hi {contact_name},

I've been following {business_name}'s success in {city}. Given your strong customer base, there's a significant opportunity to drive direct repeat orders without paying 20-30% third-party marketplace commissions.

Our team develops branded iOS and Android applications with one-tap reordering, digital loyalty points, and automated push notifications that bring customers back every week.

We put together an interactive prototype showing how a branded {business_name} mobile app could look. Would you have 10 minutes next Tuesday or Wednesday to check it out?

Best regards,

{sender_name}
{sender_title} | SiteBlitz
{self.MANDATORY_FOOTER}"""

        elif category == ServiceCategory.ECOMMERCE_EXPANSION:
            template_id = "ECOMMERCE_STOREFRONT"
            signals_used.append("Catalog products without digital checkout")
            subject = f"Expanding {business_name} with digital online sales"
            body = f"""Hi {contact_name},

I was admiring {business_name}'s selection of products in {city}.

I noticed {website} showcases what you offer, but doesn't allow customers to purchase or place orders directly online with modern checkout options like Apple Pay and Google Pay.

We help physical retail and catalog businesses launch high-converting eCommerce storefronts that run smoothly on both desktop and mobile, opening up 24/7 revenue beyond local foot traffic.

Would you be interested in seeing a quick case study of how a similar business increased revenue by 40% with an integrated digital storefront?

Best regards,

{sender_name}
{sender_title} | SiteBlitz
{self.MANDATORY_FOOTER}"""

        else:
            # General Web App / SEO Optimization fallback
            template_id = "CUSTOM_WEB_PERFORMANCE"
            signals_used.append("Web modernization and performance enhancement")
            subject = f"Digital enhancement ideas for {business_name}"
            body = f"""Hi {contact_name},

I hope this note finds you well. I came across {business_name} while analyzing digital web experiences in {city}.

Our team at SiteBlitz noticed a few key opportunities to elevate {website}—particularly around modern user experience, speed, and mobile conversion.

We build high-performance web applications that help businesses stand out and capture more qualified leads from their existing web traffic.

Would you be open to reviewing a short technical audit we put together for {business_name}?

Best regards,

{sender_name}
{sender_title} | SiteBlitz
{self.MANDATORY_FOOTER}"""

        return PersonalizationResult(
            subject_line=subject,
            body_text=body,
            template_id=template_id,
            signals_referenced=signals_used,
        )
