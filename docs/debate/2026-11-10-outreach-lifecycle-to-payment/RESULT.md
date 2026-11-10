# Review - Outreach by channel, human-sounding copy, lifecycle to payment, countries, unique hook - 2026-11-10 - 2 rounds - prompt: lead-intelligence-vision-partner

Inputs: founder-context.md (measured data), research-copy.md and research-legal.md (two Claude Code research
passes), claude-position.md (Claude's view written before ChatGPT replied), 01/02 ChatGPT replies.
Nothing was sent to any business, bought, deployed or changed in code. Nothing was deleted.

| # | Point | Proposed by | Evidence (file:line / round) | Claude's verdict | Status |
|---|---|---|---|---|---|
| 1 | Keep the 86.75 M source folder; outreach uses a lean filtered table with a reason for every rejection | Claude, ChatGPT R1 | contact_profile.csv; R1 §1 | agreed | Agreed |
| 2 | Email ladder + 6 statuses (CONFIRMED / VALID / RISKY / UNKNOWN / INVALID / SUPPRESSED); guessed = never sent; catch-all = RISKY, not sent in pilot; address on >= 5 places excluded (not declared fake); free-mail kept (79 % of Indian emails) | ChatGPT R1, Claude R2 | email_quality.csv; RFC 5321/7505; R2 §1 | agreed | Agreed |
| 3 | Remove guessed-email generation at source | Both | `backend/app/engines/enrichment/discovery.py:122-148`, `lead_radar_service.py:309`, `export_surat_leads.py:139-159` (2026-11-09 RESULT) | agreed - code work, needs go | Agreed |
| 4 | No cold WhatsApp, from the app or the API | Both | WhatsApp Business Messaging Policy 2026-09-23 (read): number given by the person + opt-in; app bans bulk; templates carry no audio | agreed | Agreed |
| 5 | No cold calls / SMS to Indian businesses from a personal SIM | Claude research | TRAI TCCCPR 2nd amendment 2025-02-12 (15-day bar, then 1-year disconnection + blacklist) | agreed | Agreed |
| 6 | India B2B email allowed in a manually reviewed pilot: business-published address, <= 20 new/day, identity + postal address + reply opt-out, provenance URL stored | Claude R2, ChatGPT R2 agreed | No Indian email anti-spam statute (Linklaters, CMS); DPDP core duties from 2027-05-13 | agreed - legal review still open | Agreed |
| 7 | Phone-only / no-contact India leads: 100 addressed letters with a printed Opportunity Snapshot + QR to WhatsApp with a pre-filled message, owner presses Send = opt-in for that conversation | Claude R2, ChatGPT R2 agreed | India Post letter <= 20 g Rs 5 (official tariff), printed postcard Rs 6 (rules compilation); WhatsApp opt-in docs list QR codes | agreed - one category, one area | Agreed |
| 8 | Google Workspace inboxes are not a cold-email safe harbour | ChatGPT R1 | Workspace AUP 2025-10-13 (read): bans large-scale unwanted email | agreed | Agreed |
| 9 | "Get explicit provider approval" as a gate | ChatGPT R1 | Google issues no approvals | rejected - replaced by row 10 | Rejected |
| 10 | Prefer a sender whose terms cover direct B2B outreach: Instantly native (AirMail, launched 2026-05-05); domains >= 1 month old; Instantly owns DFY domains/mailboxes | ChatGPT R2 | Instantly ToS 2026-11-04 §1.10 Permitted Purpose = own direct B2B sales/marketing, §4.6(g) Instantly owns DFY infrastructure; Sending Policy 2026-10-13 "domains at least one month old" (both read) | agreed - price not checked, founder to get the quote | Agreed |
| 11 | Zoho Mail policy excludes promotional mail; Microsoft 365 AUP bans spam | ChatGPT R2 | not opened by Claude | not used for any decision | Open (unverified) |
| 12 | Email copy: <= 100 words (target 60-85), plain text, no link / image / attachment / tracking pixel in touch 1, opens with one verified observation, price "from Rs 7,999", interest question, real name, reply opt-out | Both | Hunter 34 M emails (vendor): length barely matters; Gong (vendor): interest CTA; R2 §3 | agreed | Agreed |
| 13 | 3 touches: Day 1 / Day 6 / Day 14, close Day 21; reply / opt-out / bounce stop the sequence; OOO pauses it | ChatGPT R1, Claude R2 | Belkins (vendor): touch 4+ triples unsubscribes | agreed | Agreed |
| 14 | Payment moments: deposit (Rs 4,000 / 9,000) after written scope, before any build; balance (Rs 3,999 / 8,999) after staging approval, before launch and handover | Both | SiteBlitz `src/lib/offer.ts:26-77, 106-112` | agreed | Agreed |
| 15 | Free 3-hour bespoke concept replaced by a 15-20 min templated preview in one of the 3 existing demos, only after a positive reply + 3 qualifying answers, max 5/week, labelled "Illustrative concept" | Claude R2, ChatGPT R2 agreed | SiteBlitz `src/lib/demos.ts` (salon & beauty, coaching & tuition, retail & showroom); FD-26 cap in `offer.ts:91` | agreed - changes decision FD-26, founder must approve | Agreed |
| 16 | No AI-cloned voice in cold outreach; founder's real voice note / screen video only inside a conversation the owner started | Both | EU AI Act Art. 50 (from 2026-08-02); India IT Amendment Rules 2026 (synthetic audio labels); WhatsApp templates have no audio; Schilke & Reimann 2025 (exposure lowers trust) | agreed | Agreed |
| 17 | Language from evidence, not country alone; formal register; native review of the first 10-20 messages per language; pilot is India English | ChatGPT R1, Claude R2 | CSA Research 2020; JAMA 2019 machine-translation errors | agreed | Agreed |
| 18 | Abroad: quote-only pricing; unknown country = HOLD, never default opt-out | ChatGPT R1-R2 | `country_rules.py` defaults unknown countries to opt-out | agreed - code change, needs go | Agreed |
| 19 | Countries on hold: DE, AT, GR, NL, ES, ZA, AE, SG, UK sole traders; go later: US, CA (role-relevant), AU, UK Ltd/LLP (Companies House check), FR | Both | research-legal.md table; ChatGPT retracted its "UWG Feb 2026 stricter" claim (Feb 2026 law = EmpCo greenwashing) | agreed | Agreed |
| 20 | 30-day pilot: 3 parallel workstreams (sender setup, India email, 100 letters); founder sales time 5 h 30 min/day; stop rules | ChatGPT R2 | R2 §7 | agreed with one correction: email cannot start Nov 17 if domains are bought now (1-month domain age) - see plan | Agreed (dates corrected) |
| 21 | RBI FEMA Export and Import Regulations 2026 in force 2026-10-01; Stripe India invite-only; Razorpay sends unregistered freelancers to PayPal | ChatGPT R1, Claude research | RBI press release; Stripe support; Razorpay | agreed - accountant decides the foreign-payment route | Agreed |

---

## The playbook (what the founder asked for)

### A. Which data we use (the "delete" question)
Nothing is deleted from `E:\SiteBlitz-World-Business-Data`. For outreach, a lead is used only if: open, no own
website, not a chain/brand, a category that buys websites, country allowed for the channel, contact not suppressed.
Every rejected lead keeps its reason. Guessed emails are removed in the code that makes them.

| Bucket (world / India, measured) | Route |
|---|---|
| Email (30.97 M / 1.74 M) | Verify -> email sequence where the country allows it |
| Phone only (41.96 M / 1.82 M) | India: find an email on their own website/page; else letter + QR (pilot: 1 category, 1 Mumbai area); Mumbai walk-in. Abroad: skip for now |
| Social profile only (10.06 M / 1.08 M) | Letter + QR if an address exists; otherwise later (paid ads) |
| Nothing (2.22 M / 10 k) | Drop |
| Email looks fake | Ladder below; failing addresses move to the phone / letter route |

**Email ladder:** guessed by our tool -> never send · invalid syntax / null MX -> INVALID · same address on >= 5
places -> excluded from pilot · verifier ok -> VALID · catch-all or conflicting -> RISKY (not sent) · inconclusive ->
UNKNOWN (re-check later) · reply received -> CONFIRMED · "stop", complaint, hard bounce -> SUPPRESSED on every channel.
Before the first send: a manual audit of 100 accepted records; 95 must be classified right, and one guessed
address passing is a blocking defect.

### B. Writing rules - so it reads like a respectful person, not AI
1. One true, checkable observation first (from their own page). If none exists, do not email.
2. 60-85 words, max 100 with signature. Plain text. No link, image, attachment or tracking pixel in touch 1.
3. Plain words. Never: "I hope this email finds you well", "I came across", "elevate", "seamless", "unlock",
   "vibrant", "testament", lists of three, "not just X but Y", em dashes, compliments you cannot prove.
4. Say who you are honestly: a small studio in Mumbai. No invented clients, results or reviews.
5. One question at the end that can be answered in one line.
6. Real name, working reply address, postal address, one-line reply opt-out.
7. Templates are written once by a person, per language, and reviewed by a native speaker; per lead only the
   fields change. The AI never writes free text into a cold email and never invents an observation.
8. Subject: plain and true, no "Re:" on the first email.

### C. The three emails (India, English)
**Touch 1 - Day 1** · Subject: `A website idea for [Business Name]`
> Hello [Business Name] team,
>
> Your [Instagram page] shows [verified detail, e.g. your full menu and timings], but I couldn't find a website linked there.
>
> I'm [Founder name] from SiteBlitz in Mumbai. We build simple websites that put services, location and contact details in one place. Our packages start at ₹7,999, excluding domain and hosting.
>
> Would you like a short outline for [Business Name]?
>
> Regards,
> [Founder name] | SiteBlitz
> [reply address] | [postal address]
> If this isn't relevant, reply "stop" and I won't write again.

**Touch 2 - Day 6** (same thread)
> Hello [Business Name] team,
>
> One thought on [Business Name]: a simple website could help customers find [verified service], your hours and the right contact number without scrolling through posts.
>
> Would you like me to send a suggested page structure and a fixed quotation?
>
> Thanks,
> [Founder name] | SiteBlitz
> [reply address] | [postal address]
> Reply "stop" if you'd prefer no further emails.

**Touch 3 - Day 14** (same thread)
> Hello [Business Name] team,
>
> I'll close this after today. If a website becomes useful for [Business Name] later, you're welcome to write to me and I'll explain the options and prices.
>
> Thank you for your time.
>
> [Founder name] | SiteBlitz
> [reply address] | [postal address]
> No further follow-ups are planned.

**Day 21:** no reply -> CLOSED_NO_REPLY. No new campaign to the same business.

### D. Lifecycle of every business (state machine)
FOUND -> DEDUPLICATED -> QUALIFIED -> CONTACT_VERIFIED -> CHANNEL_APPROVED -> TOUCH_1 (Day 1) -> TOUCH_2 (Day 6) ->
TOUCH_3 (Day 14) -> CLOSED_NO_REPLY (Day 21). Weekend dates move to Monday. Any reply stops all scheduled touches.

| Reply | State | Next message / action (human sends) |
|---|---|---|
| Interested | QUALIFYING | "Thank you. Is this a new website or a change to an existing one? And what should customers be able to do on it?" Then the 3 qualifying questions, one at a time (decision-maker, Rs 7,999-17,999 range OK, launch within 60 days) |
| How much? | QUALIFYING | "For India, Launch is ₹7,999 (one page) and Business is ₹17,999 (three pages). Domain and hosting are separate. Tell me which pages you need and I'll confirm the right one." |
| Send details | QUALIFYING | 5-line scope + Opportunity Snapshot |
| Already have a website | QUALIFYING or CLOSED | "Are you happy with it, or is there something you'd like improved? If it works well, I won't take more of your time." |
| Not now | CLOSED (recontact only if they name a month) | "Understood. Is there a month when you'd welcome a message, or shall I close this?" |
| No / stop / unsubscribe | SUPPRESSED | "Understood, thank you for letting me know." Never contacted again on any channel |
| Wrong person | QUALIFYING or CLOSED | Ask for the right public contact, or close |
| Please call me | CALL_REQUESTED | Call at their time, about this enquiry only |
| Out of office | PAUSED_OOO | Resume 2 business days after the return date; no date -> review after 14 days |
| Hard bounce | SUPPRESSED (address) | Investigate the source; try the phone / letter route |

After a positive reply: **Opportunity Snapshot** (what we found / what could improve / proposed scope + price) for
everyone -> **preview** (15-20 min, max 5/week) only when all 3 qualifying answers are yes -> written quotation ->
AWAITING_DEPOSIT.

**Payment moments (unchanged from `offer.ts`):**
1. Written scope accepted -> deposit invoice: Launch ₹4,000 / Business ₹9,000. No design or build before it is in the bank.
2. Deposit + content + access + start date -> READY_TO_BUILD; delivery clock starts (2 / 7 working days).
3. Staging site + one consolidated revision approved in writing -> balance invoice: ₹3,999 / ₹8,999.
4. Balance received -> publish, hand over logins, domain in the client's name.
After launch: Day 7 check-in, ask for a factual review and permission to use the work as SiteBlitz's first real
case study, a referral ask, and a care-plan offer (no price exists yet - founder decision).
Payment status comes only from the bank / UPI record, never from "invoice sent".

### E. Countries and language
- Pilot: India, English (owners who write in Hindi/Hinglish get answers in the same language).
- Later, email allowed with the coded rules: US (CAN-SPAM), Canada (published + role-relevant), Australia
  (inferred consent), UK Ltd/LLP checked on Companies House, France (profession-related; generic info@ outside the
  consent rules). On hold until rules are coded and reviewed: DE, AT, GR, NL, ES, ZA, AE, SG, UK sole traders, every
  country without a rule.
- Language: business's own language evidence > their website/social language > region (Quebec FR, Swiss canton,
  Belgian region) > country default > manual. Formal register: Sie, vous, usted, Lei, 〇〇様 / ご担当者様.
- Send window: recipient's local time, Tue-Thu 9:00-11:30 and 14:00-16:30 (to be tested).
- Abroad: quote-only prices; foreign payment route decided with an accountant (Stripe India invite-only; PayPal
  needs a purpose code; GST LUT needs a GSTIN).

### F. The unique hook
- **Not** an AI-cloned voice in a cold message (WhatsApp cannot carry it, disclosure rules in the EU and India,
  trust drops when discovered, no evidence it lifts replies).
- **Yes:** (1) a letter on their desk: their business name, a one-page Opportunity Snapshot and an illustrative
  homepage, a QR that opens WhatsApp with "Hello SiteBlitz, I received your website idea for [Business Name]. Please
  show me the suggested design and price." The owner presses Send -> a real conversation they started. (2) Inside
  that conversation, the founder's own 30-60 s voice note and a screen video of their preview.

### G. First 30 days (dates corrected for the 1-month domain-age rule)
| Dates | Work | Email first touches | Letters |
|---|---|---|---|
| Nov 10-14 | Fix live site prices + contact email; remove guessed emails; India country rule; decide sender (Instantly AirMail quote vs level-1 plan); design letter + QR; choose 1 category + 1 Mumbai area | 0 | 0 |
| Nov 16-Dec 4 | Letters in 4 batches of 25; answer every WhatsApp the owners start; Snapshots, previews, quotes | 0 (domains younger than 1 month) | 100 |
| From the day the sending domain is 1 month old (~Dec 11 if bought Nov 11) | India email 10/day week 1, 15/day week 2, 20/day after; follow-ups count inside the 30/inbox/day ceiling | 275 over ~3 weeks | - |
| Dec 9 | Preliminary review (letters, workload, any deposit) | | |
| ~Jan 8 | Email review after sequences close | | |
If Instantly supplies ready accounts on domains that are already 1 month old, email starts the week it is set up.
Founder sales time: 5 h 30 min per working day (replies 30 min, qualifying 90 min, sending 60 min, letters 30 min,
calls 45 min, quotes/previews 45 min, CRM 30 min). A paying client's delivery always comes first.

**Stop rules:** a guessed address in the queue -> stop that pipeline · 2 hard bounces in the first 50 -> pause ·
hard bounce > 1 % after 100 -> pause · any spam complaint -> pause that account · no positive reply after 150 first
touches -> fix targeting/copy before more volume · 0 replies from 100 letters -> no new batch · 5 previews with no
progress -> fix the offer · positive replies but no deposits -> fix trust, price, payment flow · 2 paid projects
running -> slow outreach.

**Illustrative funnel (assumptions, not measured):** 275 first touches x 3 % = ~8 positive replies -> ~4 quotes ->
~1 deposit. Enough to try for the first paid order; not proof of a scalable business.

## Recommended next steps (not started - waiting for your go)
1. Founder: approve FD-26 change (bespoke concept -> 20-min preview, 5/week) and the India pilot rules (rows 6, 7, 15).
2. Code (lead generator): remove guessed-email generation (3 places), add the 6 contact statuses + suppression list,
   India / NL / ES / ZA / AE / SG rules, unknown country = HOLD, CRM states and payment gates from section D.
3. SiteBlitz site: correct live prices and the bouncing contact email before any message goes out (from 2026-11-09).
4. Founder: get the Instantly AirMail quote and check domain age vs the 2026-11-09 level-1 plan; buy domains early
   because the 1-month clock starts at purchase.
5. Founder: pick 1 category + 1 Mumbai area for 100 letters; confirm printed-postcard class and price at the post office.
6. Code + founder: letter template, Snapshot template, QR with the pre-filled WhatsApp text, 3 email templates loaded.

## Points still open
- Legal review: India DPDP transition and the email procedure before any automated expansion.
- Instantly AirMail price and whether ready accounts on aged domains are available.
- India Post classification and final price of the personalised printed mailpiece; print cost (estimated Rs 5-12).
- Real response rates of the letter test and the email pilot (no independent India data exists).
- Care-plan price after launch; foreign price list (quote-only until 5-10 real quotes).
- Zoho / Microsoft 365 policy claims (row 11) not checked - not needed unless those providers are considered.
