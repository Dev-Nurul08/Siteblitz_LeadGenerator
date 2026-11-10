ChatGPT said:
C1 Startup — Round 2 Final Planning Response

10 November 2026 · Technical decisions for Claude Code

Overall verdict: Agree with the founder's decisions, with implementation safeguards and several important corrections.

This response is intended to become the implementation specification for the Gujarati children's online conversation-class startup.

The accepted technology direction is:

Brand: VaatKadi, with VaatoNest as backup.

Hosting: Netlify Personal for production.

Application: Next.js App Router, TypeScript and Tailwind CSS.

Database: MongoDB Atlas, initially Free (M0).

Authentication: Better Auth with restricted teacher access.

Payments: PayPal first, Razorpay after merchant approval, with manual bank transfer available.

Classes: Google Meet, eight 45-minute sessions per cycle.

Communications: Resend for email; manual WhatsApp Business initially.

No teacher-recruitment marketplace, student mobile app, advanced ad-management API or general-purpose LMS is required.

The founder should manage all routine operations through the admin panel without editing source code, database records or deployment settings.

1. Brand — Agree, with a naming qualification
Final name: VaatKadi — વાતકડી

Decision: Select VaatKadi. Backup: VaatoNest.

The intended Gujarati word construction is:

Part

	

Gujarati

	

Meaning




Vaat

	

વાત

	

Conversation, talk or something being said




Kadi

	

કડી

	

Link, connection or a link in a chain




VaatKadi

	

વાતકડી

	

An invented compound intended to mean a link through conversation

The full name is a coined brand word, not an established dictionary word that I can verify.

It should be understood as connecting families through conversation, not as the literal translation of a familiar Gujarati phrase.

My concern is that some native speakers could find it slightly unusual. The pronunciation is roughly Vaat-ka-di, with the last part corresponding to કડી, not કઢી (the Gujarati dish).

I have not found a clearly established offensive meaning, but a web search cannot confirm how the name feels to Gujarati speakers. Ask at least three native speakers, preferably including teachers and parents, whether the meaning is intuitive and pleasant.

The backup, VaatoNest, combines vaato (conversations) with nest (a warm place of belonging). It is more immediately international but less distinctly Gujarati.

Brand approval rule: Proceed with VaatKadi as the working name. Before buying the domain or finalizing printed assets, complete the native-speaker, trademark and domain checks. The absence of an obvious exact-match business online is not trademark clearance.

Locked identity direction

Positioning: Live Gujarati conversation classes for children growing up abroad.

Tagline: From “Kem cho?” to real conversations at home.

Primary color: Deep teal #163A4A.

Secondary colors: Marigold #F4A340, heritage teal #228F83, warm cream #FFF8EE, soft clay #E5C7B5.

Fonts: Plus Jakarta Sans for English and Noto Sans Gujarati for Gujarati.

Voice: Warm, credible, respectful, parent-focused and never exaggerated.

No fabricated testimonials, guaranteed fluency claims, artificial enrolment counters or invented teacher credentials.

Status: Agreed for implementation; native-language and legal clearance remain open.

2. Website — Agree with all three changes
2.1 Additional public pages

Add the requested pages to the previously agreed website structure.

Route

	

Exact purpose




/imprint

	

Legal seller name, operating address, business status, applicable registration/licence details, phone, support email and website




/complaints

	

Complaint form, acknowledgement, ticket number and follow-up instructions




/complaints/track

	

Complaint status lookup using ticket number plus verified parent email/one-time verification




/feedback

	

Genuine experience ratings and feedback, with privacy controls

The complaint tracking page must not reveal information based on a ticket number alone.

Use an unguessable public tracking token or ticket ID together with a verified email/one-time code. Rate-limit attempts. Never display children's names, private teacher notes or other personal details publicly.

2.2 Public rating box

Agree to implement an authentic rating feature.

Use the following data fields:

feedbackId, familyId, parentVerified, overallRating (integer 1–5), feedbackText, publicationConsent, moderationStatus, submittedAt, publishedAt.

Moderation statuses:

pending, approved, rejected_privacy, rejected_abuse, withdrawn.

Only genuine customers should be described as verified customers. Publishing is optional and separate from submitting feedback.

The public page may initially say “No customer reviews yet” and allow feedback. Never pre-populate five-star ratings, suppress genuine negative feedback simply because it is negative, or publish identifiable child information.

The UAE's e-commerce legislation includes provisions concerning an experience-rating mechanism, complaint channels, merchant identification and detailed electronic invoices. These features are therefore appropriate for the UAE-first website. 
Ministry of Economy and Tourism UAE

2.3 Reservation before payment

Agree with the sequence:

Parent enquiry → introductory call → level check → matching batch → conditional reservation → payment → confirmed place → welcome.

The platform should distinguish:

reserved: A temporary offer has been made.

payment_pending: Parent has received checkout instructions.

paid: Payment was verified.

active: Enrolment has entered a running class cycle.

Set reservationExpiresAt when offering a place. If a reservation expires, release the held seat automatically.

Do not charge for an unconfirmed group without displaying the batch-formation deadline and the applicable refund rule.

2.4 Stage-A USD price — modified proposal

Decision: Charge USD 29.00 per child for the eight-class cycle during PayPal Stage A.

Do not advertise AED 99 while actually charging USD 29. That would be misleading because USD 29 is approximately AED 106.50, not AED 99.

STAGE A — PAYPAL PRICE

$29.00

USD / child / 8 classes

Approximately AED 106.50

Actual card charge is USD 29. The AED figure is an estimate; the payer's bank may apply its own exchange rate or fees.
🇺🇸
US Dollar
$
🇦🇪
UAE Dirham
AED

The UAE dirham is pegged to the US dollar at approximately 3.6725 AED per USD. The Central Bank of the UAE publishes official intervention rates around this parity. 
Domestic Market Operations

PayPal unit economics

PayPal India's published international receiving fee is 4.40% plus USD 0.30 per transaction, with a 3% conversion spread for converting received balances into another currency in the applicable case. 
PayPal IN

Using the illustrative USD/INR reference of ₹93.3767 on 10 November 2026:

Item

	

Approximate value




Parent pays

	

$29.00




Gross INR equivalent

	

₹2,708




PayPal transaction fee

	

$1.58




Assumed conversion spread

	

$0.82




Approximate net receipt

	

₹2,484




Total effective payment cost

	

₹224

This is a modelling estimate, not a guaranteed settlement quote. Applicable taxes, provider-specific adjustments and actual PayPal exchange rates must be checked using the merchant's own transactions.

Why $29 rather than $27? USD 27 is approximately AED 99, but at the reference exchange rate and fee assumptions it nets only about ₹2,311. USD 29 leaves a modest buffer above ₹2,400 net.

Stage-B pricing

After Razorpay approves international-card payments:

Charge AED 99 if direct AED charging is supported and approved.

Disclose the actual currency on the payment screen.

Preserve the original price agreement for an already-paid cycle.

Notify parents before applying a changed price on renewal.

Keep each price in pricePlans with provider, currency, amountMinor, effectiveFrom, effectiveTo and version.

There should be no automatic price switch during a live billing cycle.

Payment-provider warning

PayPal officially supports a Business Individual classification for unregistered Indian service providers and offers PayPal-hosted guest card checkout, but actual onboarding, verification and guest-checkout presentation depend on account approval and other conditions. 
PayPal IN
+2

Stage A is an implementation path, not a guarantee that a live merchant account will be approved within seven days. International payment acceptance must be tested successfully before advertising enrolment as payable.

Status: Agreed, with USD 29 for Stage A and AED 99 as the proposed Stage-B rate.

3. Advertising system — Agree

Decision: Keep advertising execution in Meta Ads Manager and Google Ads, with performance tracking and operational control in the VaatKadi admin panel.

The first version should contain /admin/campaigns, /admin/campaigns/new, /admin/campaigns/[id], /admin/ad-spend, and /admin/reports/acquisition.

Campaign and tracking model

campaigns should contain:

_id, name, platform, externalAccountId?, externalCampaignId?, targetCountry, objective, budgetMinor, currency, landingPath, status, startDate, endDate?, utmConfig, createdAt.

Statuses: draft, active, paused, completed, archived.

The UTM builder must create URLs with source, medium, campaign and content parameters. Store first-touch and last-touch attribution on the lead without storing child information in advertising records.

The founder can enter daily spend manually or import platform CSV reports. Use one canonical spend record per campaign per day; later imports replace or reconcile that record, rather than adding it again.

Report CPL, CAC_per_family, CAC_per_child, lead_to_paid_rate, collected_revenue, ROAS, and contribution_after_acquisition.

Keep CAC_per_family and CAC_per_child separate because one family may enrol more than one child. The pilot's ₹600 target concerns acquiring one paying family.

For later Meta Pixel or Conversions API usage, track only appropriately consented adult-side conversions. Never transmit child names, levels, assessments, attendance, dates of birth or classroom identifiers.

Claude's statement about own-account ads_read access may be sufficient for an eventual integration, but that should be rechecked against the Meta application configuration when the feature is actually built. No API access is required for v1.

Status: Agreed. Manual and CSV campaign tracking are in scope; direct ad purchasing and automated API management are deferred.

4. Admin panel — Agree, with the complete extensions

Decision: The founder should control the operating workflow from one admin panel, including scheduling, payments, communications, teacher assignments, reporting and complaints.

4.1 MongoDB document model

I accept MongoDB Atlas as the project database because the founder's implementation environment is already TypeScript/MongoDB-oriented.

Use MongoDB ObjectId for application document references, Date for UTC timestamps, integer minor units for money, IANA timezone strings, and runtime validation with Zod. Better Auth manages its own user/session identifiers, which application staff records will reference using their actual adapter-compatible type.

Embed small bounded information used with its parent document. Reference growing histories and independently managed entities.

Collection

	

Required fields and relationship

	

Status values




leads

	

parentName:string, emailNormalized:string, phoneE164:string, country:string, timezone:string, ageBand:string, initialLevel:string, firstTouch:object, lastTouch:object, campaignId:ObjectId?, nextActionAt:Date?, status:string

	

new, contacted, call_booked, qualified, waitlisted, payment_pending, won, lost, do_not_contact




leadActivities

	

leadId:ObjectId, type:string, note:string, actorId:string, occurredAt:Date, channel:string

	

Types: call, email, whatsapp_draft_opened, whatsapp_sent_confirmed, note, status_change




families

	

primaryGuardian:object, additionalGuardians:object[], country:string, timezone:string, leadId:ObjectId?, status:string

	

active, paused, inactive




children

	

familyId:ObjectId, preferredName:string, ageYears:number, ageBand:string, level:string, status:string

	

active, paused, inactive




teachers

	

authUserId:string?, name:string, email:string, availability:object[], agreement:object, rateMinor:number, currency:string, status:string

	

pending, verified, active, unavailable, inactive




batches

	

name:string, ageBand:string, level:string, timezone:string, weeklyPattern:object[], primaryTeacherId:ObjectId, backupTeacherId:ObjectId?, capacity:5, meetLinkEncrypted:string, status:string

	

forming, confirmed, active, paused, closed




batchCycles

	

batchId:ObjectId, cycleNumber:number, plannedSessionCount:8, allocatedSeats:number, capacity:5, priceSnapshot:object, startsAt:Date, endsAt:Date, status:string

	

draft, booking_open, confirmed, active, completed, cancelled




enrolments

	

childId:ObjectId, cycleId:ObjectId, familyId:ObjectId, status:string, reservationExpiresAt:Date?, paymentRequestId:ObjectId?

	

reserved, payment_pending, paid, active, completed, cancelled, refunded




sessions

	

cycleId:ObjectId, ordinal:number, startsAtUtc:Date, endsAtUtc:Date, teacherId:ObjectId, status:string, rescheduleHistory:object[]

	

scheduled, completed, cancelled




teacherSlotLocks

	

teacherId:ObjectId, sessionId:ObjectId, slotStartUtc:Date

	

Active locks only




attendance

	

sessionId:ObjectId, childId:ObjectId, status:string, markedBy:string, markedAt:Date

	

present, late, absent_notified, absent_unnotified, excused




sessionNotes

	

sessionId:ObjectId, teacherId:ObjectId, childId:ObjectId?, note:string

	

No status




assessments

	

childId:ObjectId, cycleId:ObjectId, stage:string, rubricVersion:string, scores:object, assessorId:ObjectId, assessedAt:Date

	

baseline, endline




paymentRequests

	

enrolmentId:ObjectId, provider:string, providerOrderId:string?, amountMinor:number, currency:string, checkoutUrl:string?, expiresAt:Date?, status:string

	

created, sent, pending, paid, expired, cancelled




payments

	

paymentRequestId:ObjectId, provider:string, providerTransactionId:string?, grossMinor:number, feeMinor:number?, chargedCurrency:string, settlementInrMinor:number?, fxRate:number?, status:string

	

pending, paid, paid_unallocated, failed, partially_refunded, refunded, disputed




webhookEvents

	

provider:string, providerEventId:string, payloadHash:string, receivedAt:Date, processedAt:Date?, status:string, retryCount:number

	

received, processed, failed, ignored




invoices

	

invoiceNumber:string, familyId:ObjectId, paymentId:ObjectId, sellerSnapshot:object, taxTreatment:string, lineItems:object[], issuedAt:Date?, status:string

	

draft, issued, void, credited




teacherPayouts

	

teacherId:ObjectId, sessionIds:ObjectId[], rateSnapshot:object, amountMinor:number, paymentReference:string?, status:string

	

accrued, approved, paid, disputed




renewals

	

enrolmentId:ObjectId, nextCycleId:ObjectId?, advancePaymentId:ObjectId?, status:string

	

not_due, invited, advance_paid, renewed, declined, expired




tasks

	

ownerUserId:string, leadId:ObjectId?, familyId:ObjectId?, type:string, dueAt:Date, status:string

	

open, completed, cancelled




emailJobs

	

familyId:ObjectId?, templateKey:string, dedupKey:string, scheduledAt:Date, status:string, providerMessageId:string?, attempts:number

	

queued, processing, sent, failed, cancelled




emailTemplates

	

key:string, subject:string, body:string, variables:string[], version:number, active:boolean

	

Active/inactive




consentLedger

	

familyId:ObjectId, childId:ObjectId?, purpose:string, noticeVersion:string, method:string, channel:string, ipEncrypted:string?, action:string, recordedAt:Date

	

granted, withdrawn, superseded




privacyRequests

	

familyId:ObjectId, requestType:string, status:string, requestedAt:Date, resolvedAt:Date?

	

submitted, identity_check, in_progress, fulfilled, rejected_with_reason




complaints

	

ticketCode:string, trackingTokenHash:string, familyId:ObjectId?, type:string, description:string, status:string, openedAt:Date, closedAt:Date?

	

open, acknowledged, investigating, resolved, closed




feedback

	

Verified family reference, rating, publication permission and moderation information

	

As defined in point 2




safeguardingIncidents

	

Restricted incident type, relevant batch/session references, reporter, actions and closure records

	

reported, triaged, escalated, resolved, closed




breachRegister

	

incidentDate:Date, discoveredAt:Date, dataTypes:string[], affectedCount:number?, actions:object[], notificationStatus:string

	

investigating, contained, notified, closed




marketingSuppressions

	

contactHash:string, channel:string, reason:string, createdAt:Date

	

Active




campaigns, campaignDailySpend, adImports

	

Campaign definitions, one daily spend record, CSV hashes/import histories

	

As defined in point 3




settings

	

Business details, payment providers, policies, holidays, retention settings and message windows

	

Versioned




auditLogs

	

actorId:string?, action:string, entityType:string, entityId:ObjectId?, createdAt:Date

	

Append-only

Authentication collections generated by Better Auth should remain under Better Auth's control. Do not manually duplicate passwords or session tokens in application collections.

Small immutable snapshots—such as the price agreed for a cycle, teacher rate for a delivered session and seller details on an invoice—should be embedded. This prevents subsequent setting changes from altering historical financial records.

4.2 Required unique and compound indexes

Claude Code should install indexes using an idempotent initialization script before production traffic is enabled.

JavaScript
// Only one enrolment record per child per cycle.
db.enrolments.createIndex(
  { childId: 1, cycleId: 1 },
  { unique: true }
);

// One numbered cycle per batch.
db.batchCycles.createIndex(
  { batchId: 1, cycleNumber: 1 },
  { unique: true }
);

// Exactly one session record per ordinal.
db.sessions.createIndex(
  { cycleId: 1, ordinal: 1 },
  { unique: true }
);

// No two teacher assignments may reserve the same 15-minute slot.
db.teacherSlotLocks.createIndex(
  { teacherId: 1, slotStartUtc: 1 },
  { unique: true }
);

// Attendance and assessment uniqueness.
db.attendance.createIndex(
  { sessionId: 1, childId: 1 },
  { unique: true }
);
db.assessments.createIndex(
  { childId: 1, cycleId: 1, stage: 1 },
  { unique: true }
);

// Payment-provider references.
db.paymentRequests.createIndex(
  { provider: 1, providerOrderId: 1 },
  {
    unique: true,
    partialFilterExpression: {
      providerOrderId: { $type: "string" }
    }
  }
);
db.payments.createIndex(
  { provider: 1, providerTransactionId: 1 },
  {
    unique: true,
    partialFilterExpression: {
      providerTransactionId: { $type: "string" }
    }
  }
);

// One processing record for each provider webhook event.
db.webhookEvents.createIndex(
  { provider: 1, providerEventId: 1 },
  { unique: true }
);

// One authoritative spend figure per campaign and day.
db.campaignDailySpend.createIndex(
  { campaignId: 1, day: 1 },
  { unique: true }
);

// Prevent re-importing an identical CSV.
db.adImports.createIndex(
  { sha256: 1 },
  { unique: true }
);

// Prevent duplicate scheduled email jobs.
db.emailJobs.createIndex(
  { dedupKey: 1 },
  { unique: true }
);

// Unique public complaint codes.
db.complaints.createIndex(
  { ticketCode: 1 },
  { unique: true }
);

// Efficient operational queries.
db.leads.createIndex({ status: 1, nextActionAt: 1 });
db.sessions.createIndex({ startsAtUtc: 1, teacherId: 1 });
db.tasks.createIndex({ status: 1, dueAt: 1 });
db.emailJobs.createIndex({ status: 1, scheduledAt: 1 });
db.consentLedger.createIndex({ familyId: 1, recordedAt: -1 });

These indexes protect uniqueness, but indexes alone cannot enforce a maximum of five seats per batch. Capacity requires an atomic conditional operation.

4.3 Five-seat integrity rule

Keep allocatedSeats on batchCycles.

When a seat is first reserved, in a MongoDB transaction:

Verify a suitable cycle exists and the child has no enrolment in it.

Atomically update the cycle only if allocatedSeats is less than capacity.

Increment allocatedSeats by one and insert the enrolment.

Commit both changes together.

A payment for an already-reserved seat must not increment the count again.

Expired reservations and authorized withdrawals release seats through a guarded transaction. Repeated cancellation requests must not decrement the counter twice.

If two parents attempt to claim the fifth seat simultaneously, only one should succeed. If money arrives after the reservation has expired or the seat has been released, mark the payment paid_unallocated and offer an alternative or refund. Never create a sixth enrolment.

4.4 Transactions versus single-document operations

Use multi-document transactions for:

Operation

	

Records that must change atomically




Reserve/release a seat

	

batchCycles + enrolments




Confirm captured payment

	

payments + paymentRequests + enrolments + invoice/outbox record




Generate a complete cycle

	

sessions + teacherSlotLocks + cycle state




Reschedule or substitute a teacher

	

sessions + old/new slot locks




Approve a refund

	

Payment/refund records + enrolment state + capacity release if applicable




Approve teacher payout

	

Payout and session-payment ledger




Approve manual bank payment

	

Verification record + payment + enrolment + receipt job

Use single-document atomic operations for ordinary changes to a lead's next-action date, a family's non-sensitive preferences or a task's status.

Do not call PayPal, Razorpay or Resend from inside a database transaction. Record the required external action as an outbox job, commit, then process it separately. This prevents transaction retries from generating duplicate payment links or emails.

MongoDB supports multi-document transactions on replica sets, and Atlas Free uses a three-node replica set; nevertheless, Claude Code must execute a real transaction-and-rollback test against the chosen cluster before accepting it for production. 
MongoDB Docs
+1

4.5 Scheduling engine

Agree with a real scheduling engine, not a manually maintained list of meeting dates.

A batch has a recurring weekly pattern. Example:

JSON
{
  "timezone": "Asia/Dubai",
  "weeklyPattern": [
    { "weekday": 1, "localStart": "17:30" },
    { "weekday": 4, "localStart": "17:30" }
  ],
  "sessionMinutes": 45,
  "targetSessionsPerCycle": 8,
  "capacity": 5
}

weekday follows ISO numbering: Monday = 1 through Sunday = 7.

The scheduling algorithm should:

Start at the selected cycle commencement date.

Generate occurrences from the weekly pattern in the batch's IANA timezone.

Exclude holidays and founder-entered closures.

Generate exactly eight future session records, preserving ordinal numbers 1–8.

Check teacher availability and double bookings before confirmation.

Present a full preview of dates, durations and time zones.

Save the cycle and acquire teacher slot locks only after founder confirmation.

If holidays push the eighth session into a fifth or sixth week, the application must disclose that actual end date. The contractual unit is an eight-class cycle, not an unconditional promise that all sessions finish within 30 calendar days.

Time-zone display

For the example class:

Display context

	

Time




Parent — Dubai

	

Monday, 5:30 PM




Teacher — Navsari

	

Monday, 7:00 PM




Viewer

	

Converted using their saved IANA timezone

Store UTC timestamps as the source of truth; never calculate international time zones using hardcoded numeric offsets.

India and Dubai currently have a 90-minute time difference, but future UK/US expansion needs daylight-saving-aware conversion.

Teacher collision prevention

Require class start times to align to 15-minute increments.

A 45-minute class reserves three consecutive 15-minute slots, using teacherSlotLocks.

The compound unique index on (teacherId, slotStartUtc) prevents the same teacher from occupying overlapping slots. If a mandatory 15-minute buffer is added between classes, reserve four slots instead of three.

On rescheduling, update the original session's date/time and append its previous values to rescheduleHistory. Do not create a ninth active session. Release the old teacher locks and acquire the new locks within the same transaction.

A substitute must already be verified and active. The founder can substitute one session or change the remaining cycle schedule; all affected guardians receive an operational notice.

Calendar views

The founder receives week/month calendar views with batch, teacher, capacity, session status and country-local time.

Teachers receive only their assigned upcoming and completed sessions, with attendance and note-entry actions.

4.6 Communication system

Agree with Resend and manual WhatsApp.

The admin should contain an editable template library with these initial keys:

Template key

	

Trigger




lead_acknowledgement

	

Parent submits enquiry




call_confirmation

	

Founder schedules introduction call




payment_request

	

Founder offers an eligible seat




payment_receipt

	

Successful verified payment




welcome

	

Enrolment confirmed




cycle_schedule

	

Schedule generated or changed




class_reminder_24h

	

24 hours before a session




class_reminder_1h

	

1 hour before a session




class_rescheduled

	

Date/time changes




teacher_substituted

	

Substitute assigned




weekly_progress

	

Approved weekly parent update




renewal_invitation

	

Renewal window opens




complaint_acknowledgement

	

Complaint ticket created




refund_confirmation

	

Refund confirmed

Resend supports idempotency keys for email requests, so each logical email should have a deterministic key based on recipient, template, event and version. Resend's deduplication window is 24 hours, so application-side records must provide longer-term protection. 
Resend

For reminders, create emailJobs with exact scheduled timestamps. A Netlify Scheduled Function should poll due jobs at a short interval, claim a bounded number, send them and record outcomes. Netlify's scheduled functions run in UTC and have a 30-second execution limit. 
Netlify Docs

The dispatcher must tolerate delayed runs and retry temporary failures. The founder dashboard must show failed reminders for manual intervention.

WhatsApp workflow

For WhatsApp:

Generate a prefilled wa.me URL using the parent phone number and approved template.

Let the founder open it from the family or lead record.

Record whatsapp_draft_opened.

Record whatsapp_sent_confirmed only when the founder manually confirms sending.

Opening a WhatsApp draft does not prove that a message was delivered.

Send-window guard

Use Asia/Dubai local time and configurable contact preferences.

As a conservative internal operating policy:

Marketing phone calls: 09:00–18:00 UAE time.

Marketing messages: 07:00–21:00 UAE time.

Marketing only after opt-in, via the selected channel.

Opt-outs immediately suppress further promotional outreach.

These proposed windows are operating rules taken from the Round 2 research, not a claim that every cited UAE telemarketing rule directly applies to an India-based tutoring provider. Essential class-related notifications are separately categorized as transactional.

4.7 Tasks and follow-ups

The admin home page must show:

Leads needing action today.

Introductory calls scheduled today.

Payment requests awaiting response.

Reservations about to expire.

Classes starting soon.

Attendance not yet submitted.

Renewal requests awaiting response.

Open complaints and privacy requests.

Failed reminders and payment reconciliation issues.

Every task needs an owner, due timestamp, linked record, priority, completion status and optional internal note.

4.8 Payment-provider abstraction

Use one provider interface:

TypeScript
type PaymentProvider = "paypal" | "razorpay" | "manual";

interface PaymentGateway {
  createPaymentRequest(input: {
    enrolmentId: string;
    amountMinor: number;
    currency: string;
    idempotencyKey: string;
  }): Promise<{
    providerOrderId: string;
    checkoutUrl?: string;
    expiresAt?: Date;
  }>;

  verifyWebhook(
    rawBody: Buffer,
    headers: Headers
  ): Promise<VerifiedGatewayEvent>;

  getPaymentStatus(
    providerOrderId: string
  ): Promise<GatewayPaymentStatus>;

  refund?(
    providerTransactionId: string,
    amountMinor: number,
    idempotencyKey: string
  ): Promise<GatewayRefundResult>;
}

This is the proposed interface contract; the result types must be defined and validated separately.

The PayPal integration must verify webhook signatures, validate the captured order, compare the expected amount, currency and merchant identity, and distinguish checkout approval from completed capture. PayPal documents webhook signature verification and repeated event deliveries. 
PayPal Developer

Razorpay must verify the webhook signature against the raw body, check expected payment-link and transaction references, and handle payment_link.paid, payment_link.expired and cancellation events. 
Razorpay

Manual transfer is not automatically paid when a parent uploads a receipt. The founder must reconcile the actual bank credit before marking payment verified.

No provider should be able to update an enrolment by trusting only the parent-facing redirect URL.

Status: Agreed. The MongoDB model, scheduling requirements, communication system and payment abstraction are now specified.

5. Technology stack — Agree with Claude Code's revised choice

Decision: Lock Netlify + Next.js + TypeScript + Tailwind + MongoDB Atlas + Better Auth.

I withdraw the PostgreSQL preference for this project. MongoDB is suitable if the developer implements the integrity controls specified in point 4.

5.1 Hosting: Netlify Personal

Agree with the founder's hosting decision.

Netlify's published credit-based Personal plan starts at USD 9/month with 1,000 monthly credits, with optional additional credits. Free has 300 credits and a hard limit. 
Netlify Docs

Production configuration:

Setting

	

Requirement




Framework

	

Next.js 16, current security-patched release




Runtime

	

Netlify's supported OpenNext adapter




Plan

	

Personal




HTTPS

	

Enabled, custom domain




Environment variables

	

Server-side secrets only




Deployment

	

Protected production branch




Scheduled jobs

	

Netlify Scheduled Functions




Usage monitoring

	

Credit alerts and a controlled recharge budget




Webhooks

	

Public HTTPS routes with signature validation




Production data

	

Never used in public preview deployments

Security version floor: Netlify's 3 November 2026 advisory recommends Next.js 16.4.5 and OpenNext Netlify adapter 5.16.6 or later. The build should use those versions or newer patched compatible versions, with an exact dependency lockfile. 
netlify.com

Enable usage alerts and decide on a limited auto-recharge allowance. A paused website also means its payment webhook handlers may become unavailable. Therefore, payment-status reconciliation must be possible from the admin.

5.2 MongoDB Atlas M0 and backups

Agree to start with Atlas Free for the small test, subject to the operational tests.

Official Atlas documentation confirms approximately 512 MB storage, a 500-connection limit and automatic pausing after 30 inactive days with no connections. This is acceptable for a small proof of concept but not an unlimited production guarantee. 
MongoDB Docs

Correction to Round 2: Atlas now documents an optional backup subscription for Free clusters in private preview.

It costs $0.10/day, capped at $3/month, with daily snapshots and retention of the last four. However, availability is gradual and cannot be assumed for every account. 
MongoDB Docs

My rule is:

If M0 backup subscription is available, enable it before storing real child data and perform a test restore.

If it is unavailable, prefer Atlas Flex with its supported backup capability or another verified paid backup solution before production.

Keep an additional securely stored, encrypted recovery export where appropriate.

Upgrade when storage, performance, backup reliability or operations justify it—not only when the database is full.

Do not create an unprotected automated download of family information to a personal computer or publicly accessible storage.

5.3 Authentication: Better Auth

Agree with Better Auth and its MongoDB adapter.

Its documentation supports MongoDB and a two-factor authentication plugin with TOTP and backup codes. 
Better Auth
+1

Required setup:

Area

	

Rule




Founder

	

super_admin, mandatory TOTP




Teachers

	

teacher, invited by founder, MFA required before accessing learner records




Public signup

	

Disabled for staff accounts




Teacher account creation

	

Founder creates an invitation; teacher verifies email and sets a password




Authorization

	

Every server action and API verifies role and assigned resources




Sessions

	

Secure cookies, revocation, expiration




Account recovery

	

Secure reset workflow and controlled backup-code recovery

Use Better Auth's admin-user management rather than hand-written password hashing or custom session handling. Its admin plugin supports creating accounts and managing users. 
Better Auth

The founder's account is bootstrapped securely once; public visitors cannot select an administrative role.

Parents and children do not need application logins in v1. Parent communications and secure email-based access to specific receipts or complaint status are sufficient.

5.4 Monthly running cost at pilot scale

Reference exchange rate: $1 ≈ ₹93.38, 10 November 2026. Vendor prices checked the same day. Figures exclude applicable taxes, domain registration, development and potential overages unless noted.

Service

	

Monthly estimate




Netlify Personal

	

$9 ≈ ₹840




MongoDB Atlas Free

	

₹0




Optional Atlas M0 backup, if available

	

Up to $3 ≈ ₹280




Resend Free

	

₹0




Google Meet eligible free use

	

₹0




Better Auth

	

₹0 licence fee




PayPal merchant account

	

₹0 base monthly fee




Razorpay standard gateway

	

₹0 base monthly fee




Domain

	

Depends on domain and registrar




SMS/OTP or additional monitoring

	

Not yet quoted

Resend's published free tier allows 3,000 transactional emails per month, subject to 100 emails per day. 
Resend

Core fixed platform cost

~₹840/mo
Netlify Personal, M0 and free email/Meet tiers

With optional M0 backups

~₹1,120/mo
Assuming backup preview is available
Payment cost for ten paying children

Scenario

	

Approximate cost for 10 payments




Stage A: PayPal, $29 each

	

₹2,240




Stage B: Razorpay, AED 99 each

	

₹890

The Razorpay estimate assumes the published 3% international-card fee plus 18% GST on that fee, without additional FX or bank charges. Actual merchant terms and currency settlement must be confirmed. 
Razorpay

The PayPal scenario is more expensive, but still potentially workable for the pilot.

Revised ₹25,000 test budget

The earlier corrected test budget was approximately ₹22,050, including ₹850 of estimated Razorpay payment fees and ₹1,500 for website/tools.

Replacing those payment fees with approximately ₹2,240 of PayPal charges gives:

₹22,050 − ₹850 + ₹2,240 = ₹23,440

This leaves approximately ₹1,560 below the ₹25,000 cap.

The ₹1,500 tool allowance can cover the roughly ₹840 Netlify subscription and, if available, the roughly ₹280 optional backup subscription. It does not automatically cover domain purchases, legal advice, development charges or extra messaging costs.

This is still a conditional pilot budget, not proof of profitability. Teacher rates, CAC and actual PayPal settlements remain assumptions.

Status: Stack agreed. Production database backup and gateway approvals are operational gates.

6. Build phases — Agree with eight milestones, but not an unconditional one-session promise

Verdict: Agree to a maximum of eight top-level phases. Disagree that every complete phase can safely be guaranteed to fit one coding session and eight files.

A working admin with payments, scheduling, child-data controls and financial reconciliation is too significant to force into an arbitrary implementation size.

My compromise: exactly eight demonstrable phases, each delivered through small changes of approximately eight hand-written files or fewer per coding session, including tests. If a phase requires more, it should be broken into implementation slices without creating additional top-level milestones.

Phase 1 — Foundation and deployment
Before first payment

Deliverable: A running, responsive Next.js application on Netlify Personal with brand tokens, public/admin layouts and deployment configuration.

Binary acceptance checks

Production and staging builds both succeed.

Custom domain and HTTPS work.

Mobile navigation works without layout overflow.

No secrets are exposed in client bundles or public repository files.

Required Next.js/adapter security versions are installed.

Phase 2 — Public website, trust and legal pages
Before first payment

Deliverable: The complete public website, including the imprint, pricing, safety, feedback, complaints, privacy, refunds and consent controls.

Binary acceptance checks

All agreed public routes load successfully.

Seller and pricing information is drawn from approved settings.

Marketing trackers remain blocked without consent.

A complaint creates a ticket that can be securely tracked.

Public feedback has verification, moderation and withdrawal controls.

Phase 3 — Database, authentication and CRM
Before first payment

Deliverable: MongoDB initialization, indexes, Better Auth, founder login, teacher-role restrictions, enquiries, leads, families, parental consent and follow-up tasks.

Binary acceptance checks

Founder login requires TOTP.

Public staff registration is blocked.

An enquiry creates one lead with attribution and a due follow-up.

A child profile cannot be created before the required guardian-consent workflow.

Unauthorized requests cannot access family records.

Phase 4 — Teachers, batches and scheduling
Before first payment

Deliverable: Founder-controlled teacher records, weekly availability, batch configuration, cycle generation and calendar management.

Binary acceptance checks

A weekly pattern generates exactly eight numbered sessions.

Founder-entered holidays are skipped and the resulting end date is shown.

Two overlapping teacher assignments cannot both be confirmed.

A batch cannot exceed five allocated seats under concurrent requests.

Rescheduling preserves session count and updates the relevant teacher locks.

Phase 5 — Payments and invoicing
Before first payment

Deliverable: Provider-independent payment records, working PayPal integration, manual transfer reconciliation, Razorpay adapter behind a disabled feature flag until approval, verified webhooks and digital receipts.

Binary acceptance checks

A valid simulated PayPal capture marks an enrolment paid.

Duplicate webhooks do not duplicate payment, enrolment or receipt.

A failed payment or browser redirect alone cannot activate enrolment.

A manually reported transfer requires founder verification.

Invoice and settlement records preserve the correct amount, currency and transaction reference.

Phase 6 — Operations and communications
Before first payment

Deliverable: Editable transactional templates, welcome/schedule messages, scheduled reminders, manual WhatsApp actions, privacy inbox, complaints handling and operational task alerts.

Binary acceptance checks

A verified payment queues exactly one welcome message.

Session reminders are scheduled at 24 hours and 1 hour before class.

A failed email remains visible and retryable.

Unsubscribed contacts cannot receive marketing through the admin.

Opening WhatsApp does not falsely mark a message as delivered.

Phase 7 — Teacher classroom portal
Before first class

Deliverable: Restricted teacher login, assigned classes, attendance, teacher notes, baseline/endline assessments and parent progress reporting.

Binary acceptance checks

Teachers see only their assigned batches and permitted learner details.

Attendance cannot be recorded twice for the same child/session.

Assessment rubric scores are validated within the allowed range.

A substitute can access only the sessions to which they are assigned.

No teacher can access other teachers' payout details or full parent contact information.

Phase 8 — Advertising, finance and management reporting
Before paid advertising and full pilot operation

Deliverable: UTM builder, campaigns, CSV spend imports, CAC reports, renewal management, teacher payouts, contribution reports, break-even tracker and final launch verification.

Binary acceptance checks

Importing the same ad CSV twice does not double-count spending.

Paid-family CAC and paid-child CAC are calculated separately.

Teacher payouts reconcile against completed, payable classes without duplication.

Renewals count paid advances, not merely verbal promises.

A complete enquiry-to-payment-to-class test passes, including privacy, refunds and recovery cases.

Release gates

Gate A — First paying family

Phases 1–6 completed, plus live merchant approval, verified backups and the legal/payment launch checks.

Gate B — First live class

Phase 7 completed, with functioning meeting-admission controls and teacher workflow.

Gate C — Paid ad campaign and complete 30-day test

All eight phases completed and production acceptance tests passed.

This meets the founder's requirement to build the complete system while avoiding rushed financial and child-safety features.

Status: Eight top-level phases agreed; session count must remain flexible enough for tested implementation.

7. Compliance — Agree with implementation, retain legal-review gates

Decision: Incorporate the UAE requirements into the site's information architecture, database records and admin workflows immediately.

UAE compliance-to-product mapping

Legal area

	

Product requirement

	

Location




UAE e-commerce law 14/2023

	

Published services, prices, fees and terms

	

/pricing, /terms, /program




Merchant identification

	

Actual seller identity, contacts and applicable licence information

	

/imprint




Customer complaints

	

Ticket submission, acknowledgement and secure tracking

	

/complaints, /admin/complaints




Public experience feedback

	

Authentic rating functionality

	

/feedback




Digital invoices

	

Detailed invoice/receipt for purchases

	

/admin/invoices, secure parent delivery




Service failures and refunds

	

Clear cancellation and refund workflow

	

/refunds, /admin/payments




Marketing choice

	

Per-channel opt-in and opt-out

	

Enquiry form, privacy settings, suppression list




UAE PDPL 45/2021

	

Purpose records, appropriate access, transfer assessment, rights handling

	

/privacy, /admin/privacy




Child Digital Safety Law 26/2025

	

Guardian-controlled child records, no child targeting, restricted access

	

Consent ledger, child profiles, teacher portal




Business continuity

	

Recovery documentation, backups, incident process

	

Admin settings and operating procedures




Data incidents

	

Restricted incident records and response tracking

	

/admin/privacy, breach register

The relevant obligations concerning prices, invoices, ratings, complaints, seller information, refunds and dispute resolution appear in the official English text of UAE Federal Decree-Law No. 14 of 2023. Article 9 also restricts pre-included arbitration clauses for digital contracts below AED 50,000. 
Ministry of Economy and Tourism UAE

Important child-law distinction

UAE Child Digital Safety Decree-Law No. 26 of 2025 entered into force on 1 January 2026 and includes a one-year regularization period for entities already subject to it. This should not be interpreted as permission for a newly launched service to disregard children's safeguards until January 2027. 
UAE Legislation
+1

Implement guardian verification and protective defaults before collecting identifiable child data.

Do not assume that the educational-platform exception automatically applies. Official UAE information refers to an exemption subject to further requirements and decisions. 
UAE Legislation

Guardian consent flow

The system should implement:

Parent submits contact details and an initial age-band enquiry.

Parent email or phone contact is verified.

The parent receives a versioned privacy notice and child-data consent explanation.

The system completes the approved parental verification method.

Only then is the child's identifiable enrolment profile created.

Consent events are stored append-only, including version, purpose, method and timestamp.

Withdrawal initiates a documented workflow that stops unnecessary processing and determines whether any statutory records must be retained.

The legal adviser must approve the verification method; email confirmation by itself must not be labelled legally sufficient without checking the actual requirements.

India DPDP requirements

India's Digital Personal Data Protection Act, 2023 and Rules, 2025 should be reflected in the same model.

The Ministry of Electronics and Information Technology published the Rules and an enforcement timeline in November 2025, including an eighteen-month phased compliance period for key provisions. The project should therefore be designed now for verifiable parental consent rather than waiting until the later commencement period. 
MeitY
+1

Data minimization and transfer safeguards

Store only the information needed to administer classes. There is no operational need to collect a child's Aadhaar, passport number, full home address or school name.

Avoid storing a family's ethnic origin or religion. Interest in learning Gujarati does not require an ethnicity field.

Documents and user-facing policies should explain which service providers process parent/child information, including the hosting provider, database provider, payment processors, email provider and meeting platform.

Cross-border data transfers and permitted processing grounds require legal confirmation, especially for UAE parents whose data is handled from India and potentially other cloud regions.

Recording and teacher conduct

Recording remains off by default.

The application should not provide a classroom recording button, and teachers should be prohibited from privately recording or publishing children's voices or images.

Teachers must communicate with guardians through approved channels and follow the documented safeguarding and incident-escalation procedure.

The remaining regulatory concern

The founder is currently an individual rather than a registered business.

A PayPal Business Individual account does not, by itself, establish that all educational-service licensing, merchant identification, Indian tax and UAE cross-border selling obligations have been satisfied.

Obtain a targeted legal/tax assessment covering:

Whether an India-based seller of live online Gujarati classes requires any additional UAE authorization or notification, including KHDA/ADEK considerations.

The applicable UAE VAT treatment.

Indian GST treatment and export-of-services documentation.

Whether the selected seller identity and permitted registrations meet applicable e-commerce disclosures.

Whether the proposed data transfers and parental verification workflow are sufficient.

Do not build recorded lessons or sell prerecorded content until their separate regulatory and tax implications are evaluated.

Status: Product requirements agreed; the unresolved legal questions remain launch gates rather than assumptions of compliance.

Locked decisions for Claude Code

Area

	

Final decision




Brand

	

VaatKadi, pending final language/trademark clearance




Backup brand

	

VaatoNest




Launch market

	

UAE




Learners

	

Children aged 7–12




Program

	

Eight live 45-minute classes per cycle




Batch size

	

Maximum five




Teachers

	

Founder-recruited, independent




Hosting

	

Netlify Personal




Application

	

Next.js + TypeScript + Tailwind




Database

	

MongoDB Atlas




Authentication

	

Better Auth, mandatory staff MFA




Video

	

Google Meet




Initial payments

	

PayPal Business Individual, subject to approval




Stage-A price

	

USD 29 per child per cycle




Later gateway

	

Razorpay, after approval




Proposed Stage-B price

	

AED 99, if supported




Email

	

Resend Free initially




WhatsApp

	

Manual click-to-chat initially




Advertising

	

Meta/Google interfaces, tracked in internal admin




Build organization

	

Eight milestones with testable acceptance gates




Child data

	

Guardian-controlled, minimal and access-restricted

Points still open

VaatKadi approval: Native Gujarati speaker review, trademarks, domain and social handles.

Merchant onboarding: Actual PayPal account approval, guest-card payment test, verified settlement and INR reconciliation.

Razorpay migration: Required sole-proprietor documentation, international-card activation and direct AED settlement/charging capabilities.

UAE legal assessment: Cross-border education licensing, KHDA/ADEK, VAT and actual seller disclosures.

Indian tax assessment: GST, exports of services, invoicing and foreign-payment documentation.

Parental verification: Legally appropriate method and retention/withdrawal rules.

MongoDB production recovery: M0 backup-preview availability or confirmed paid backup alternative.

Commercial batch policy: Whether four children may start a class, reservation expiration, refund cutoff and makeup-class treatment.

Final pricing validation: PayPal transaction and FX charges from real merchant settlements; whether Stage-B AED 99 provides sufficient margin.

Pilot operating assumptions: Actual teacher quotes, CAC, parent willingness to pay, attendance and paid renewals.

Final instruction to Claude Code: Treat the decisions above as the Round 2 technical specification. Do not reopen accepted platform choices without new evidence. Implement with tested safeguards, and keep unresolved legal, payment and recovery questions as explicit launch blockers rather than silently treating them as completed approvals.
