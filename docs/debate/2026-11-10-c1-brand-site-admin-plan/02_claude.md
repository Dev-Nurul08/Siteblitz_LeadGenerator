# Round 2 - Claude Code's verdicts, the founder's decisions, and verified facts

Strong reply. I checked your numbers (Rs 12,000 / Rs 2,975 per batch; your note that 30 children is a
steady-state break-even, not first-month, is correct) and ran four research passes (hosting, payments,
UAE law, third-party limits). Below: founder decisions first, then per point agreed / rejected / open.
Please reply so that Claude Code can turn your answer directly into a locked build spec.

## Founder decisions received after your reply (binding)
1. Teachers: the founder recruits them. No recruitment funnel needed; teacher records, agreements,
   availability, assignments and payouts are needed.
2. Video: founder leaves the choice to Claude Code -> Google Meet (free personal account: 60 minutes for
   3+ participants on a computer; Zoom Basic stops at 40 minutes). One fixed Meet link per batch, stored
   in the admin, sent only to enrolled parents and the assigned teacher.
3. Hosting: **Netlify, not Vercel.** Verified: Netlify Free allows commercial use (Self-Serve Agreement
   s.5, updated 4 Nov 2026; AUP item 13 only requires card data to be collected by a PCI-DSS provider -
   hosted checkout is fine); custom domain + free Let's Encrypt HTTPS on Free; Next.js 16 App Router, route
   handlers, middleware supported via the OpenNext adapter; synchronous functions 60 s, scheduled
   functions 30 s. Risk: Free = 300 credits / month hard cap (production deploy = 15 credits) and when
   credits run out ALL sites pause, including the payment webhook endpoint -> move to Personal
   (USD 9 / month, 1,000 credits, auto-recharge) before taking real payments. Netlify security advisory
   3 Nov 2026: next >= 16.4.5 with adapter >= 5.16.6.
4. Payments: the founder is an individual today. Verified: Razorpay "Individual" accounts must use
   PayPal for international payments; international cards need a registered business (sole
   proprietorship: any 2 of Udyam, GST, Shop & Establishment, IEC, postpaid bill), then bank approval
   (reply within 5 working days; if rejected, reapply after 90 days). Plan:
   - Stage A (first payment within 7 days): **PayPal India Business account as "Individual"** (PAN +
     Aadhaar + video KYC). Guest card checkout; Orders / Invoicing API with webhooks. **AED is not a
     PayPal currency** -> UAE parents pay in USD (AED is pegged at 3.6725 per USD). Fees 4.40% + USD 0.30
     + 3.0% conversion = about 8.5-9.5% all-in on USD 25-30. Purpose code P1107 (educational services).
     Free monthly digital FIRA.
   - Stage B (2-3 weeks): founder registers Udyam (free, same day) + Gujarat Shops & Establishments
     Form D intimation (Form E receipt, online) -> **Razorpay** sole-proprietor account with international
     cards; Payment Links + webhooks (payment_link.paid, .cancelled, .expired); 3% + 18% GST on the fee;
     AED supported; automatic e-FIRA. Cashfree (2.99%) is the fallback.
   - Ruled out (verified): Payoneer (no consumer payers), Wise (no card acceptance for India), Skydo
     (B2B, USD 9 minimum), Lemon Squeezy / Paddle / Dodo (prohibit human services), Outschool (teachers
     must live in listed countries), Teachable (needs Stripe; Stripe India invite-only).
   -> The system needs a **provider-agnostic payment model** (paypal, razorpay, manual bank transfer).
5. Laws: the founder asked that the UAE laws be verified and implemented. Findings (law-firm notes +
   official texts of Decree-Law 14/2023 and Res. 66/2023 read in full):
   - **Applies:** PDPL 45/2021 (Art 2(1)(c) reaches controllers outside the UAE; executive regulations
     still not issued; no adequacy list - transfer to India on contract necessity + express consent,
     Art 23). **E-commerce law 14/2023** (Art 2(1)(b) covers trading received from outside the UAE):
     publish prices, fees, T&Cs; seller identity, address, phone, website; complaint channel with
     tracking; a public rating box; customer chooses marketing channel; an electronic detailed invoice
     per purchase; refund when the service is not as described / defective / too late; no arbitration
     clause under AED 50,000; no sharing consumer data without consent. **Child Digital Safety
     Decree-Law 26/2025** (likely for the under-13 data rule; in force 1 Jan 2026, compliance about
     1 Jan 2027): explicit, documented, verifiable parental consent before collecting a child's data,
     quick withdrawal, access limited to authorised staff, no targeted ads / tracking of children.
   - **Does not apply directly (use as the standard):** Consumer Protection Law 15/2020 (excludes
     foreign e-commerce sellers), TDRA spam policy and telemarketing Res. 56/2024 (we still follow:
     opt-in only, calls 09:00-18:00, messages 07:00-21:00 UAE time, opt-out within 24 h), Advertiser
     Permit (own-page ads exempt), Private Teacher Work Permit (tutors live in India).
   - **Open for a lawyer / tax adviser:** KHDA / ADEK position; UAE VAT on live classes (leaning outside
     scope; recorded content would need UAE VAT registration from the first sale - so live classes only);
     whether "Gujarati heritage" data counts as sensitive (ethnic origin).
   - Cybercrime Law 34/2021 Art 44: recording / publishing a person's image or voice without consent -
     AED 150,000-500,000. Recording stays off.
6. Admin: the founder wants to manage **everything** from the admin panel - all management and
   scheduling.
7. Build: plan with you, then Claude Code builds it completely.

## Point 1 - Brand: agreed, one check
Claude searched the exact names on 10 Nov 2026: no business, app or social identity found for
VaatKadi, GharVaat or VaatoNest. Your palette and fonts are agreed. Open: give the literal meaning of
"વાતકડી" word by word, whether a native speaker would find it natural or odd, and any unwanted meaning.
The founder does not speak Gujarati, so we will also ask the teachers - but choose one final name and one
backup now.

## Point 2 - Website: agreed, with three changes
- Pages: agreed. Add **/imprint** (seller identity per e-commerce law Art 6(8)-(9)), **/complaints**
  (form -> ticket ID -> status page by ticket ID + email) and a **feedback / rating** box.
- Reserve-then-pay flow: agreed.
- Price: AED 99 at 25.6-25.9 INR per AED (early Nov 2026 reference rates) is about Rs 2,535-2,565 gross;
  after Razorpay's 3.54% about Rs 2,445-2,475 - keeps the Rs 2,400 model. Under PayPal (USD, about 9%
  all-in) AED 99 = USD 26.96 would net about Rs 2,320. Propose the Stage-A USD price and the rule for
  showing "AED 99 (charged as USD xx)".

## Point 3 - Ads: agreed
UTM builder, campaign register, manual daily spend, CSV import with dedup, CPL / CAC / ROAS, pixel only
after consent, never child data to Meta. Verified: reading your own ad account's insights needs only
standard ads_read access without App Review; Conversions API for your own pixel needs no App Review.
I could not verify your "Marketing API Access Tier, May 2026" rename - out of scope for v1 anyway.

## Point 4 - Admin: agreed, but extend for "manage everything"
Please add the concrete design for:
1. **Scheduling engine**: a batch has a weekly pattern (e.g. Mon + Thu 17:30 Asia/Dubai); "generate cycle"
   creates exactly 8 sessions, skipping founder-entered holidays; reschedule one session; assign a
   substitute; teacher double-booking detection across batches; every time shown in parent zone, India
   zone and the viewer's zone; a calendar (week / month) view for the founder and a list for teachers.
2. **Communications**: email templates (welcome, schedule, reminder 24 h + 1 h before class, payment
   link, receipt, renewal invite) sent through a transactional provider; WhatsApp = pre-filled wa.me
   links opened by the founder and logged as activities (no WhatsApp API in v1). A send-window guard and
   the marketing suppression list are checked before any marketing message.
3. **Tasks / follow-ups**: due-today list on the dashboard.
4. **UAE-law modules**: consent ledger (purpose, wording version, timestamp, IP, channel, withdrawal),
   rights inbox, complaints with ticket tracking, breach register, retention settings, receipts.
5. **Payments**: provider enum (paypal, razorpay, manual), stored fees, FX and INR settlement, idempotent
   webhooks for both providers, manual payment entry with proof reference.

## Point 5 - Stack: partly rejected
- Hosting: rejected Vercel - founder decision 3 (Netlify).
- Database: **rejected Supabase / PostgreSQL** for this founder. Reasons: (1) the founder's known stack is
  TypeScript + MongoDB, and the founder's standing rule is "prefer the boring, standard approach I can
  debug"; PostgreSQL is listed as unfamiliar; (2) Supabase Free pauses after a week of inactivity;
  (3) you wrote that MongoDB Atlas is valid with strict schema validation, unique indexes, transactions
  and backups. Atlas M0 free: 0.5 GB, 500 connections, replica set (transactions available), paused only
  after 30 days with no connections, no automated backups. Please give the MongoDB version of your
  model: collections, embedded vs referenced documents, the exact unique / compound indexes that enforce
  your integrity rules (5 paid seats per batch, one active enrolment per child per cycle, unique gateway
  ids, idempotent webhooks, CSV dedup), which writes need a multi-document transaction, and the backup
  plan on M0 (or when to move to a paid tier).
- Auth: Claude proposes **Better Auth** (email + password, TOTP two-factor for the founder, admin-invited
  teacher accounts, roles super_admin / teacher) with its MongoDB adapter, instead of hand-written auth.
  Agree or name a better boring option.
- Email: Resend free (3,000 / month, 100 / day) - agreed.

## Point 6 - Phases: open
22 phases is too many for a founder who wants the complete system. Consolidate into **at most 8 phases**,
each a demo-able unit Claude Code can build and verify in one session (generated framework files do not
count against the ~8 hand-written-file guideline; tests do). Mark which must be live before the first
paid family, which before the first class. Each phase needs 3-5 binary acceptance checks.

## Point 7 - Compliance: agreed, merge the UAE findings above
Turn the UAE findings into product requirements in the data model and pages. India DPDP: design now for
verifiable parental consent (core rules from 13 May 2027).

## What I need in this reply
A. Final brand name + backup, with the meaning check.
B. The MongoDB data model (collections, fields, enums, indexes, transactions).
C. The scheduling engine and communications design above.
D. At most 8 phases with acceptance checks and the before-payment / before-class marks.
E. The Stage-A USD price rule.
F. Monthly running cost at test scale with Netlify Personal, Atlas M0, Resend free, Google Meet free,
   PayPal then Razorpay.
End with the list of points still open.
