ChatGPT said:
C1 Gujarati Classes Startup — Brand, Website, Advertising & Admin System

Planning review · 10 November 2026 · For Claude Code implementation

Overall decision

Agree with building a proper branded startup website and an integrated admin system. Disagree with building every advanced feature before the first paying customer.

The objective is to create a credible education brand with a reliable digital operating system—not merely a landing page. However, the earlier business research has not yet proven customer acquisition costs, willingness to pay or long-term retention.

I recommend designing the complete architecture now, then implementing it in controlled phases.

Priority

	

What must be delivered




Before the first paid family

	

Brand, public website, enquiry capture, admin login, CRM, parent records, consent, batch allocation, payment collection, basic campaign tracking and legal pages




Before the first class

	

Teacher access, secure class links, attendance, session management and speaking assessments




After initial validation

	

Automated ad reporting, detailed profitability dashboards, advanced renewals, parent portal and deeper integrations

The founder will recruit teachers independently. The application should manage their information, schedules, class records and payments, but it does not need a teacher-recruitment marketplace.

1. Brand identity

Verdict: Agree — build a distinctive, parent-focused brand rather than a generic children's tuition website.

Three name candidates
વ

1. VaatKadi — વાતકડી

Preferred candidate

A proposed name built around the ideas of conversation and connection. Short, distinctive and suitable for an education brand that may later introduce additional conversation programs.

ઘ

2. GharVaat — ઘરવાત

Emphasizes conversations at home, particularly between children, parents and grandparents. Emotionally relevant to Gujarati families living abroad.

V

3. VaatoNest

A more international, contemporary name combining Gujarati conversation with a welcoming learning environment. Easier to extend into multiple countries.

Quick conflict check: Public web searches on 10 November 2026 did not surface an obvious exact-name competitor for these three candidates. This is not confirmation that the trademarks, social handles or domains are available. I excluded VaatSetu because that name already appears as an existing social identity. 
Pictame
+1

Before committing, check exact and similar spellings using India's official trademark search in Class 41 (education), relevant international trademark registries, and the chosen domain registrar. Confirm pronunciation and intended Gujarati meaning with a fluent speaker. 
PublicSearch
+1

Positioning and messaging

Positioning line: Live, small-group Gujarati conversation classes for children growing up abroad.

Tagline: From “Kem cho?” to real conversations at home.

Primary promise: Help children practise speaking Gujarati with family through guided, age-appropriate conversations.

The tone should be warm, reassuring, culturally connected and clear. Address parents, not children, because parents are the decision-makers and payers. The language should emphasize speaking confidence and family connections without suggesting guaranteed fluency.

Visual design system

Deep teal

#163A4A

Warm cream

#FFF8EE

Marigold

#F4A340

Heritage teal

#228F83

Soft clay

#E5C7B5
Gujarati roots. Everyday conversations.

A warm editorial style, not a conventional tuition template.

Explore classes

Parent enquiry

Use Plus Jakarta Sans for English and Noto Sans Gujarati for Gujarati. Both should load through the application's font system rather than depending on fonts installed on a visitor's device.

The visual identity should use custom conversational illustrations, subtle speech-bubble motifs, warm home environments and restrained cultural details. Avoid generic graduation caps, stock photographs pretending to show actual students, exaggerated cartoons or religious symbols that could make the service appear exclusive.

Day-one requirement: Wordmark, icon, palette, typography, favicon, social profile assets and reusable UI components. A complex brand animation can wait.

2. Public website and conversion flow

Verdict: Agree — the website must convert interested parents into paying families, not simply collect traffic.

Exact public pages

Route

	

Required sections

	

Timing




/ Home

	

Hero, value proposition, class summary, pricing preview, process, safety reassurance, CTA

	

Before payment




/program

	

Ages 7–9 and 10–12, conversation topics, learning method, expected practice

	

Before payment




/schedule

	

Available UAE-local slots, batch availability, timezone explanation

	

Before payment




/pricing

	

Eight classes, 45 minutes each, price, inclusions, exclusions, payment and refund explanation

	

Before payment




/how-it-works

	

Parent enquiry, introductory call, level assessment, enrolment and class commencement

	

Before payment




/safety

	

Parent communication, teacher supervision, recording policy and safeguarding

	

Before payment




/faq

	

Levels, absence, class sizes, payments, timings, cancellations

	

Before payment




/enquire

	

Secure parent enquiry form

	

Before payment




/contact

	

Support email, business identity, WhatsApp contact and response expectations

	

Before payment




/privacy, /terms, /refunds, /service-delivery

	

Legal, privacy and service policies

	

Before payment




/cookies

	

Tracking and consent explanation, preferences control

	

Before tracking




/thank-you

	

Enquiry confirmation and next-step instructions

	

Before payment

For a compact initial website, /how-it-works, /schedule and pricing previews can be included on the home page as well as their dedicated routes. Avoid publishing empty pages.

Home page structure

The first screen should communicate the product immediately:

VaatKadi વાતકડી

How it works · Safety

Help your child speak Gujarati with family.

Live online conversation classes for children aged 7–12, in small groups of up to five.

Enquire about a batch

8 × 45-minute classes

Illustrative home-page direction, not a final production design.

Immediately below the hero, include the program overview, class format, an honest explanation of the teaching approach, available enrolment slots, the founder's contact details, safety policy, FAQs and a second enquiry CTA.

Conversion journey
Adult-targeted ad
Landing page
Parent enquiry
Introductory call
Level check
Confirm batch
Payment confirmed
Welcome + schedule

The introductory call is approximately 10 minutes in English or Hindi. The Gujarati-speaking teacher handles the level assessment. A short optional assessment before payment determines grouping; the baseline speaking assessment in class one is separately recorded for progress comparison.

Important exception: Five children need compatible levels and schedules. Do not collect full fees without clearly explaining whether the batch is confirmed or conditional. First gather suitable reservations, then invite payment. If the required group does not form by the communicated deadline, offer another slot or a full refund.

Parent enquiry fields

Before asking for a child's information, initially collect only parent_name, email, whatsapp_e164, country, iana_timezone, child_age_band, gujarati_level, preferred_slot_ids, contact_request_consent, and the campaign source.

Collect the child's preferred name and more specific learning details only after a verified parent/guardian enrolment process. Operational contact permission and optional promotional marketing consent must be separate.

Pricing and currencies

The original unit economics use ₹2,400 per child for eight classes. UAE parents should see a clear AED price before payment, not an unexplained INR figure.

My proposed pricing implementation is:

UAE: a draft offer of AED 99 per child per eight-class cycle, subject to checking that net INR settlement preserves the business model.

India accounting: store the actual charge, gateway fees, currency conversion and INR settlement.

UK and USA: configure GBP and USD, but do not publish unapproved prices before those markets open.

If Razorpay cannot charge in AED for the approved merchant account, show the actual INR charge and explicitly explain the approximate local-currency amount and any card-bank conversion uncertainty. Never describe an estimate as a guaranteed amount.

Honest marketing at launch

The website may truthfully say it offers live Gujarati conversation classes, groups of up to five, age bands 7–9 and 10–12, and eight 45-minute sessions per cycle—provided these arrangements are genuinely available.

It must not invent reviews, successful student outcomes, years of operation, teacher credentials, enrolment figures or awards. Testimonials and children's photos should be absent until there are real examples and appropriate permissions.

SEO and discoverability

Use server-rendered, indexable public pages with a single clear H1, unique metadata, sitemap, canonical URLs, robots.txt, Open Graph images, accessible headings, descriptive alt text and structured data only for truthful business and service information. Suggested early search themes include Gujarati speaking classes for kids in Dubai, online Gujarati conversation classes for children, and Gujarati lessons for kids abroad.

Track enquiry submissions rather than treating page views as commercial success. Keep /admin and sensitive payment or family pages excluded from indexing, with authentication still enforced.

Razorpay's international-card onboarding also expects a functional website with terms, privacy, refund/cancellation and service-delivery information, so those pages are operational requirements, not decoration. 
Razorpay
+1

3. Advertising, lead tracking and campaign management

Verdict: Partly agree. Build an internal advertising intelligence system now; do not attempt to replace Meta Ads Manager or Google Ads on day one.

The admin panel should be able to answer four questions:

How much did we spend?

Where did interested parents come from?

How many became paying families?

Did those customers generate a positive contribution after costs?

What the admin can realistically manage

Capability

	

Initial implementation

	

Later




Define and organize campaigns

	

Internal admin

	

—




Generate UTM tracking links

	

Internal admin

	

—




View lead sources and conversions

	

Internal admin

	

—




Record daily ad expenditure

	

Manual entry

	

CSV/API import




Calculate cost per lead and CAC

	

Internal admin

	

—




Upload ad creative references

	

Internal admin

	

—




Create and launch Meta ads

	

Meta Ads Manager

	

API if justified




Edit audiences, bids and ad budgets

	

Meta Ads Manager

	

API if approved




Google Ads management

	

Google Ads

	

API later




Conversion tracking

	

First-party enquiry and payment records

	

Consent-controlled Pixel/CAPI




Automated performance synchronization

	

—

	

Approved APIs

There is an important 2026 terminology correction: Meta renamed its Ads Management Standard Access feature to Marketing API Access Tier in May 2026, with Limited and Full access levels. The ads_management permission is separate. Managing only an app owner's ad account may have different access requirements from managing third-party accounts; business verification, permissions and reviews depend on the integration. Claude Code must not assume unrestricted access. 
Meta Horizon OS Developers
+1

UTM link builder

Example generated link:

Plain text
/enquire
?utm_source=meta
&utm_medium=paid_social
&utm_campaign=uae_gujarati_parents_nov26
&utm_content=grandparents_video_a

The admin should generate the complete URL and allow one-click copying. Each enquiry should preserve its first known campaign attribution and most recent attributable campaign, when available.

Campaign management screen

Use these fields:

id: uuid, name: text, platform: enum(meta, google, organic, referral, other), external_campaign_id: text?, target_country: char(2), objective: text, budget_minor: bigint, currency: char(3), start_date: date, end_date: date?, status: enum(draft, active, paused, completed), landing_path: text, created_at: timestamptz.

A related campaign_daily_spend record should contain campaign_id, spend_date, amount_minor, currency, fx_rate_inr, impressions?, clicks?, entry_method (manual, csv, api) and source_reference.

For CSV imports, uniquely identify rows by campaign, date and source record ID so importing the same report twice cannot double-count spending.

Reporting formulas

Metric

	

Calculation




Leads

	

Unique identifiable parent enquiries




CPL

	

Campaign spend ÷ attributed leads




Lead-to-paid conversion

	

Paying families ÷ leads




CAC per paying family

	

Campaign spend ÷ first-time paying families




CAC per child

	

Campaign spend ÷ newly acquired paying children




Contribution

	

Collected fees − direct delivery and acquisition costs




Campaign ROAS

	

Attributed collected revenue ÷ campaign spend

The initial hypothesis of ₹6,000 ad spend for ten paying families means a ₹600 CAC. It is a target, not an observed result.

A WhatsApp link click is not a verified lead. The platform can record the click, but the founder must identify the parent through a form or voluntary conversation. Do not scrape WhatsApp group members or treat anonymous visits as qualified leads.

Meta Pixel, Google tracking and Conversions API

The day-one system can work with UTMs and verified internal conversions. Advertising pixels are optional for initial measurement.

For later integration, require a genuine consent choice before loading marketing trackers. The consent system must support accepting, rejecting and changing preferences. Google's documentation distinguishes basic consent mode, which blocks tags before consent, from advanced mode, which can transmit cookieless signals; I recommend the simpler basic/block-until-consent approach initially. 
Google for Developers
+1

If both Meta Pixel and Conversions API are enabled, deduplicate shared events using the same event_name and event_id. Only use appropriately consented adult-related events; never send children's identities, learning assessments or attendance to advertising platforms. 
Adobe Experience Platform

Acceptance test: An adult clicks an ad, submits an enquiry, gets marked qualified, and pays. The admin attributes the new customer to the appropriate campaign without manual counting or duplicate conversions.

4. Admin panel and database design

Verdict: Agree — a single operational admin is justified, but access must be strictly role-based.

Admin navigation

Screen

	

What the founder sees




/admin

	

Today's calls, open enquiries, pending payments, upcoming classes, test targets




/admin/leads

	

CRM pipeline, call notes, follow-up dates, source campaign




/admin/families

	

Guardians, contact information, enrolments, payment status




/admin/children

	

Enrolled learners, age band, level, consent and progress




/admin/teachers

	

Approved teachers, agreements, availability, assigned batches




/admin/batches

	

Capacity, matching levels, paid seats, teacher and status




/admin/sessions

	

Class calendar, local times, meeting-link access, substitutes




/admin/attendance

	

Attendance by class and child




/admin/assessments

	

Baseline and end-of-cycle speaking scores




/admin/payments

	

Links issued, collected amounts, failures, refunds, reconciliation




/admin/invoices

	

Invoice numbers, tax treatment, issued documents




/admin/payouts

	

Teacher classes delivered, amounts due and paid




/admin/renewals

	

Parents due for renewal, advances collected, next-cycle decisions




/admin/campaigns

	

Campaign details, UTMs, spend and conversion reports




/admin/reports

	

Enrolments, CAC, batch contribution, cash flow, break-even




/admin/privacy

	

Parental consent, access/deletion requests, restricted safety incidents




/admin/settings

	

Prices, age bands, schedules, terms, permissions and notifications

Core relational data model

I recommend PostgreSQL-style types for the following schema. All records should include created_at and updated_at where applicable; references ending in _id are foreign keys.

Table

	

Essential fields and types

	

Main statuses




admin_users

	

id uuid, auth_user_id uuid, role text, is_active boolean

	

super_admin, operations, teacher, finance_readonly




leads

	

id uuid, parent_name text, email text, phone_e164 text, country char(2), age_band text, level text, campaign_id uuid?, next_action_at timestamptz?, status text

	

new, contacted, call_booked, qualified, waitlisted, payment_pending, won, lost, do_not_contact




lead_activities

	

id uuid, lead_id uuid, activity_type text, note text, actor_id uuid, occurred_at timestamptz

	

Types: call, whatsapp, email, note, status_change




families

	

id uuid, primary_parent_name text, email text, phone_e164 text, country char(2), timezone text, lead_id uuid?, status text

	

active, paused, inactive




children

	

id uuid, family_id uuid, preferred_name text, age_years smallint, age_band text, initial_level text, status text

	

pending_consent, active, inactive




consents

	

id uuid, family_id uuid, child_id uuid?, purpose text, policy_version text, granted_at timestamptz, withdrawn_at timestamptz?, verification_method text

	

granted, withdrawn, superseded




teachers

	

id uuid, user_id uuid?, display_name text, email text, hourly_or_session_rate_minor bigint, currency char(3), agreement_version text, status text

	

candidate, verified, active, on_leave, inactive




batches

	

id uuid, code text, age_band text, level text, capacity smallint, timezone text, teacher_id uuid, backup_teacher_id uuid?, status text

	

forming, payment_open, confirmed, active, completed, cancelled




batch_cycles

	

id uuid, batch_id uuid, cycle_start date, cycle_end date, session_count smallint, price_minor bigint, currency char(3)

	

planned, open, active, completed




enrolments

	

id uuid, child_id uuid, cycle_id uuid, payment_id uuid?, status text

	

reserved, offered, payment_pending, paid, active, completed, withdrawn, refunded




sessions

	

id uuid, cycle_id uuid, teacher_id uuid, starts_at timestamptz, ends_at timestamptz, meeting_reference text, status text

	

scheduled, completed, rescheduled, cancelled




attendance

	

id uuid, session_id uuid, child_id uuid, status text, marked_by uuid, marked_at timestamptz

	

present, late, absent_notified, absent_unnotified, excused




session_notes

	

id uuid, session_id uuid, child_id uuid?, teacher_id uuid, note text, created_at timestamptz

	

No workflow status




assessments

	

id uuid, child_id uuid, cycle_id uuid, assessment_stage text, rubric_version text, scores jsonb, assessor_id uuid, assessed_at timestamptz

	

baseline, endline




payments

	

id uuid, family_id uuid, gateway_link_id text?, gateway_payment_id text?, amount_minor bigint, currency char(3), settled_inr_minor bigint?, status text

	

created, link_sent, paid, failed, expired, partially_refunded, refunded, disputed




invoices

	

id uuid, family_id uuid, payment_id uuid, invoice_number text, issued_at timestamptz?, tax_treatment text, amount_minor bigint, status text

	

draft, issued, void, credited




teacher_payouts

	

id uuid, teacher_id uuid, period_start date, period_end date, amount_minor bigint, paid_at timestamptz?, status text

	

accrued, approved, paid, disputed




renewals

	

id uuid, enrolment_id uuid, next_cycle_id uuid?, advance_payment_id uuid?, status text

	

not_due, invited, advance_paid, renewed, declined, expired




campaigns, campaign_daily_spend

	

Fields specified in point 3

	

Campaign and spend records




privacy_requests

	

id uuid, family_id uuid, request_type text, requested_at timestamptz, completed_at timestamptz?, status text

	

submitted, verified, in_progress, fulfilled, rejected_with_reason




audit_logs

	

id uuid, actor_id uuid?, action text, entity_type text, entity_id uuid?, occurred_at timestamptz

	

Append-only




webhook_events

	

provider text, provider_event_id text, received_at timestamptz, processed_at timestamptz?, status text

	

received, processed, failed

Supporting settings and restricted safeguarding_incidents tables should also exist.

Important integrity rules

The database must enforce more than what the interface displays:

A child cannot have duplicate active enrolments in the same cycle; a batch cannot exceed five active/paid seats.

A session must last 45 minutes by default, and each cycle must explicitly have eight planned sessions. Do not assume that every calendar month automatically contains exactly eight Monday/Thursday meetings.

Money uses integer minor units, not floating-point arithmetic. Payment records have unique gateway identifiers.

All scheduled events are stored as UTC timestamps with an IANA timezone such as Asia/Dubai or Asia/Kolkata. UK and US daylight-saving changes must be handled automatically.

A payment changes to paid only after server-side verification and reconciliation, not just because a user returned from checkout.

The same webhook or CSV import must never create duplicate financial records.

Speaking assessment rubric

Each child receives a short, teacher-scored assessment at the beginning and end of the cycle.

Criterion

	

Score




Understanding a simple Gujarati prompt

	

0–3




Producing an appropriate spoken response

	

0–3




Understandability of speech

	

0–3




Confidence and conversational participation

	

0–3




Total

	

0–12

The teacher should use the same rubric at both assessments and include brief observational notes. The founder can review consistency, attendance and parent feedback, but should not pretend to independently assess Gujarati speaking proficiency.

Should teachers have their own login?

Agree — yes, but limited to assigned work.

A teacher's dashboard should show their upcoming classes, assigned learners' preferred names, relevant levels, attendance entry, notes and assessment forms.

Teachers must not see full parent contact databases, advertising results, payment information, unrelated batches, other teachers' records, or financial settings. A teacher cannot create a new account or select the teacher role themselves; an administrator must invite and authorize the account.

Full teacher access is required before live classes, but the complete teacher management portal does not need to be finished before the first parent pays.

Dashboard KPIs

The founder's main dashboard should prioritize:

Paid test target

10
Unrelated paying families

CAC ceiling

₹600
Per paying family

Attendance target

80%
Across scheduled classes

Renewal target

5
Paid month-two advances
These are pilot targets, not actual operating results.

The dashboard must also show collected revenue, outstanding fees, teacher payment liabilities, campaign spending and contribution by batch.

Using the previously agreed example, one full batch produces ₹12,000 revenue and approximately ₹2,975 first-cycle contribution after the assumed acquisition and delivery costs, before fixed overhead.

The earlier estimate of 30 children breaking even is a steady-state scenario that assumes only one-third need replacing each cycle. It is not first-month break-even when all 30 students have to be acquired.

5. Technology stack and architecture

Verdict: Agree with Next.js, TypeScript, Tailwind and Vercel. Disagree with MongoDB Atlas as the default database for a brand-new implementation.

My preferred stack is:

Next.js App Router + TypeScript + Tailwind CSS

Public website · Founder admin · Restricted teacher portal

Server Actions + Route Handlers

Validation · Authorization · Payments · Consent · Business rules

Supabase

PostgreSQL · Auth · Row-level security · Backups

Vercel Pro

Hosting · SSL · Deployment · Runtime

Razorpay

Payment links · International cards · Webhooks

Resend

Transactional emails · Notifications

Manual integrations initially

Google Meet · WhatsApp Business · Meta Ads Manager

Class delivery · Parent communication · Advertising
Why PostgreSQL rather than MongoDB?

The proposed system has relationships between families, children, enrolments, batches, sessions, assessments, invoices and payments. PostgreSQL naturally supports foreign keys, transactions, uniqueness constraints and financial reconciliation.

Supabase also provides an established authentication service, reducing the amount of custom authentication code.

MongoDB Atlas is still a valid choice. If Claude Code already has a tested MongoDB implementation, I would not insist on rewriting it. In that case, use strict schema validation, unique indexes, appropriate transactions and verified backups.

For a new project with no existing code, I prefer Supabase PostgreSQL because its structure better matches this business.

Verified third-party pricing

Official vendor information checked 10 November 2026. High confidence in published base prices; account-specific eligibility, taxes and future pricing remain unconfirmed.

Service

	

Recommended tier

	

Published price




Next.js, TypeScript, Tailwind

	

Open-source stack

	

$0 license




Vercel

	

Pro, one deploying seat

	

$20/month, plus possible usage/taxes 
Vercel




Supabase

	

Free for development; Pro preferred for production

	

Free $0; Pro from $25/month 
Supabase




MongoDB Atlas, if retained

	

Flex for low-traffic production

	

Approximately $8–30/month, usage dependent 
MongoDB Docs




Resend

	

Free transactional email

	

$0, 3,000 emails/month, maximum 100/day 
Resend




Razorpay

	

Standard international-card payments

	

Published 3% platform fee; applicable GST additional 
Razorpay




Google Meet

	

Personal-account free meetings

	

Up to 60 minutes for groups of three or more 
Google Meet Help




WhatsApp Business

	

Manual app and click-to-chat

	

No Cloud API integration initially




Domain

	

Commercial registrar

	

Price and availability to confirm

Important hosting correction: Vercel Hobby is restricted to non-commercial personal use. A paid education business should use an appropriate commercial plan, such as Pro. 
Vercel

At full recommended tiers, Vercel Pro plus Supabase Pro has a published base cost of $45/month, before applicable taxes, extra usage or domain costs.

The earlier pilot allocated only ₹1,500 for landing-page and tools costs. This budget line is not sufficient to assume both paid services are covered. The total ₹25,000 pilot cap must be recalculated before approving paid infrastructure.

Supabase Free is an option during development, but its published limitations include project pausing after a week of inactivity. Pro includes daily backups. For a real service handling children's information, I prefer a maintained paid production database rather than relying on free-tier behavior. 
Supabase

Classroom platform decision

Use Google Meet for the pilot after verifying the host account's access controls. Forty-five-minute lessons fit within the published 60-minute group limit for eligible free Meet use.

Do not use Zoom Basic for the 45-minute sessions: its published meeting limit is generally 40 minutes. 
Zoom

Each batch should have a secure meeting reference. Keep the link in authenticated staff systems and send it only to the enrolled guardians and assigned teacher. The meeting provider should enforce joining controls.

Payment architecture

Razorpay Payment Links are suitable for the first version because the founder can collect payment without building a custom card checkout. Razorpay advertises international payment links, but foreign-card acceptance requires merchant approval, so feasibility must be established before live enrolment. 
Razorpay
+1

The payment process should be:

Founder approves an enrolment offer and creates a payment request.

Razorpay generates the payment link.

The admin stores the gateway link ID and the expected amount/currency.

A verified Razorpay webhook confirms payment.

The system marks the enrolment paid, records an invoice/receipt according to the approved accounting process, and triggers the welcome email.

Failed, expired or refunded payments remain separately identifiable.

Webhook handlers must verify authenticity, handle duplicate deliveries and avoid assuming events arrive in order. Razorpay documents at-least-once delivery and recommends idempotency based on event identifiers. 
GitHub
+1

Do not store payment card details or gateway secrets in the browser.

Maintenance and security requirements

Claude Code should implement this as one Next.js application, not microservices. Use stable libraries, database migrations, environment variables, role-based authorization, validation, rate limiting, error logging and automated tests.

Every deployment should run linting, type checks, tests and a production build. Create a staging environment without real child records. Require multi-factor authentication for the founder's administrator account, test backups and restoration, and keep an audit trail for sensitive changes.

6. Implementation phases for Claude Code

Verdict: Agree — implementation must be divided into small independently verifiable sessions.

Each phase should modify no more than approximately eight files, including tests and migrations. If the work does not fit, split it; do not omit testing to satisfy the file limit.

Proposed build schedule

Phase

	

Deliverable

	

Gate




0

	

Finalize specification, branding assumptions, project structure, hosting constraints

	

Before payment




1

	

Next.js project, UI design tokens, navigation, fonts, responsive layout

	

Before payment




2

	

Home, program and how-it-works pages, basic SEO

	

Before payment




3

	

Pricing, FAQ, safety and contact pages

	

Before payment




4

	

Legal pages, privacy preferences and consent controls

	

Before payment




5

	

Database schema, migrations, authentication and authorization tests

	

Before payment




6

	

Parent enquiry form, field validation, source attribution and confirmation emails

	

Before payment




7

	

Founder CRM pipeline, notes, follow-up dates and lead search

	

Before payment




8

	

Family/child profiles, parental consent records, privacy permissions

	

Before payment




9

	

Teacher records, batch allocation, capacity enforcement

	

Before payment




10

	

Batch cycles, scheduled sessions and timezone handling

	

Before payment




11

	

Razorpay payment-link generation and admin payment tracking

	

Before payment




12

	

Payment webhook verification, idempotency, reconciliation and invoice foundation

	

Before payment




13

	

UTM builder, campaign register, daily spend and basic CAC reporting

	

Before paid ads




14

	

Security tests, mobile QA, accessibility, staging review and production launch checklist

	

Before payment




15

	

Restricted teacher login and assigned-session screen

	

Before first class




16

	

Attendance, absence reporting and teacher notes

	

Before first class




17

	

Baseline/endline rubric and progress summaries

	

Before first class




18

	

Teacher payouts, renewal advances and finance reconciliation

	

During pilot




19

	

Contribution per batch, break-even and cohort reporting

	

During pilot




20

	

CSV ad imports, consent-based Pixel/CAPI events and extended analytics

	

After validation




21

	

Optional Meta/Google API integrations, improved automations and parent portal

	

After validation

These are deliverable boundaries rather than promises that an entire phase can always be completed in a single attempt. Some phases, especially the database and payment work, may need subdivision to maintain the eight-file constraint.

Required verification gates

Before accepting the first payment, demonstrate a complete test journey with sample data:

An ad-tagged enquiry creates exactly one CRM lead, retaining campaign attribution.

A founder can qualify the lead and assign a compatible batch without exceeding its capacity.

Family information is inaccessible to unauthenticated users and unrelated staff.

A simulated successful payment updates the enrolment once, even if the webhook is delivered twice.

Failed payments and refunds do not appear as collected revenue.

Child data cannot be submitted without the required guardian-consent workflow.

No marketing Pixel fires when marketing consent has been rejected.

Dubai and India schedule displays agree on the same actual class time.

The public site works on mobile, publishes accurate fees and policies, and passes basic accessibility checks.

Before the first class, verify the teacher can log in, access only their assigned batch, mark attendance and record an assessment. Test meeting admission controls and backup-teacher reassignment.

Every completed phase should produce: a short change summary, modified-file list, migration record where relevant, test results, screenshots of applicable screens and any unresolved risks. Claude Code should not mark a phase complete while relevant tests fail.

Production release policy

Use a protected main branch and separate staging deployment. Keep credentials out of Git. Production changes should require passing tests, and database migrations must have a documented rollback or recovery procedure.

This creates a repeatable workflow the founder can manage without debugging complex infrastructure.

7. Compliance, child safeguarding and financial policies

Verdict: Agree — these requirements must be built into the first release. Several are launch blockers, not later enhancements.

India: DPDP Act 2023 and Rules 2025

India's Digital Personal Data Protection Act, 2023 and the notified DPDP Rules, 2025 are relevant because the business operates from India.

The rules were notified in November 2025 with phased commencement. Several substantive obligations, including children's verifiable parental-consent requirements, are scheduled for the later commencement period around May 2027. Design for them now rather than relying on the transition window. 
MeitY
+1

The application should keep a versioned record of the privacy notice, consent purpose, guardian verification method and withdrawal status. A simple unchecked/checked consent field alone must not be assumed to satisfy every legal requirement for verifiable parental consent.

UAE: launch-market requirements

UAE Federal Decree-Law No. 45 of 2021 (Personal Data Protection Law) is relevant to handling customer information from the UAE.

There is also an important additional rule: UAE Federal Decree-Law No. 26 of 2025 on Child Digital Safety. Official UAE guidance states that collecting or using personal data from children under 13 requires the applicable safeguards, including clear parental consent, withdrawal capability, a stated purpose and restrictions on targeted advertising involving children's data. Educational-service exemptions may exist under specific legal conditions, but they must not be assumed automatically. 
U.AE
+2

For this UAE-first service, use parent-controlled enrolment and obtain appropriate verified consent before creating operational child profiles.

UK expansion

When actively serving UK families, assess UK GDPR, the Data Protection Act 2018 and the Information Commissioner's Children's Code. The ICO explains that the code can apply to education-related online services likely to be accessed by children, including providers outside the UK. 
ico.org.uk
+1

Conduct an appropriate privacy-impact assessment before launching direct UK child-facing functionality.

United States expansion

For American families with children under 13, assess the Children's Online Privacy Protection Act and Rule (COPPA). Requirements can include parental notice, verifiable consent, access/deletion rights, security and data minimization. 
Federal Trade Commission

Do not enable a US-targeted enrolment campaign solely by adding USD pricing. Complete the market-specific legal review first.

Safeguarding rules to implement

Requirement

	

Implementation




Parent-controlled enrolment

	

Guardian authorization before collecting child learning details




No child direct messaging

	

All logistical communication goes through the parent




No private teacher-child contact

	

No private WhatsApp, email or unsupervised messaging




Safe video classes

	

Controlled admission, approved participants and restricted meeting links




No recording by default

	

Disable recording and screenshots as part of teacher operating rules




Class supervision

	

Parent present for initial setup; documented safeguards for one-to-one situations




Teacher verification

	

Founder confirms identity, references and suitability before activation




Substitutes

	

Only pre-approved backup teachers may access classes




Restricted learning notes

	

Teacher can view only assigned learners' necessary information




Incident handling

	

Restricted report, escalation procedure, responsible adult and audit trail




Privacy requests

	

Guardian can request access, correction, withdrawal or deletion as applicable

Do not collect a child's full date of birth, home address, school details, ID documents or photograph unless a defined operational or legal need is established. For this pilot, age in years and age band should be enough.

The retention policy should distinguish educational records from invoices and statutory financial records. Delete or anonymize unnecessary learning information when it is no longer required, while retaining records that must legally be kept.

Refund and cancellation policy

Proposed policy for legal review, not yet an agreed commercial term:

Scenario

	

Proposed treatment




Required batch does not form by the promised deadline

	

Full refund or guardian-approved alternative




Parent cancels sufficiently before the first class

	

Full refund under a clearly disclosed cutoff




Business cancels a class

	

Reschedule with agreement or refund the undelivered lesson




Child misses a class

	

Offer a makeup opportunity when feasible under the disclosed policy




Parent withdraws mid-cycle

	

Clearly stated treatment of undelivered classes, consistent with applicable consumer law




Month-two ₹500 advance

	

Credited toward the next fee; refund conditions disclosed before collection

I suggest an initial 48-hour pre-class cancellation cutoff, subject to legal review and parent feedback. Do not use vague statements such as "all payments non-refundable."

Also publish a complaint-response process, a delivery-of-services policy, and support contact details.

GST, invoices and payments from abroad

This item requires a chartered accountant before launch.

Indian GST law provides a zero-rated framework for qualifying exports of services, but whether this specific tutoring arrangement qualifies requires confirmation of the statutory conditions, including location of supplier and recipient, place of supply, payment realization and the relationship between the parties. Export status must not be assumed merely because a parent lives abroad. 
taxinformation.cbic.gov.in
+1

The system should therefore support configurable tax treatment rather than hardcoding zero GST.

Invoices should record seller identity, invoice number and date, recipient information where required, service description, amount, currency, applicable tax treatment and the relevant payment reference. Actual foreign-currency settlement and gateway charges must be reconcilable.

The founder must also confirm which legal form and KYC documentation the chosen payment provider will accept. A private limited company may not be necessary for a small test, but that does not mean an unverified individual automatically qualifies for international-card processing.

Final implementation recommendation

I would approve the VaatKadi-style branded website with a single founder admin and restricted teacher portal, built around the full data architecture described above.

I would not approve building the advanced ad-management API integration, a student-facing app, or a large parent portal during the first paid test. Those add cost and risk without addressing the primary uncertainty: whether unrelated Gujarati families abroad will pay and renew.

The first production release is successful when a parent can discover the service, enquire, speak to the founder, be matched into a suitable group, pay safely, and receive the correct class schedule—and when the founder can account for every lead, payment and class.

Points still open

1. Final brand and domain: Select one of the proposed names, confirm native Gujarati pronunciation, complete trademark checks and purchase an available domain.

2. Legal seller and payment approval: Confirm the merchant's legal identity, bank account, Razorpay KYC, international-card approval, accepted currencies and settlement terms.

3. Pilot pricing: Decide whether the UAE price will be a fixed AED amount or an INR charge with a displayed AED estimate. Recalculate margins using actual expected settlement.

4. Production budget: Confirm whether the ₹25,000 overall test cap remains strict. It must cover the chosen hosting/database tiers, payment charges, contingency and any external development costs.

5. Batch policy: Decide whether a group requires five paid children or may begin with four, the reservation deadline, refund cutoff and make-up lesson rules.

6. Safeguarding and consent: Obtain review of the parental verification method, teacher safeguards and privacy policies for the UAE-first model.

7. Teacher and classroom readiness: Founder to provide verified teacher details, confirmed per-session quotes, available time slots, backup arrangements and the approved meeting-host setup.

8. Unproven business assumptions: Real cost to acquire paying families, willingness to pay versus lower-cost community classes, attendance, and renewal conversion remain unknown until the pilot runs.

Final position: Agree with the startup direction and core system, with the modifications and conditions above. The plan is suitable as an implementation specification for Claude Code; it is not evidence that the business is validated or that payment and regulatory approvals have already been obtained.
