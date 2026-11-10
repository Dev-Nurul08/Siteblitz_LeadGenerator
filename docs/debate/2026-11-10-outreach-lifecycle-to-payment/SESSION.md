

---

## Claude Code - 2026-11-10 02:14 UTC - 01_claude.md - attachments: none

name: lead-intelligence-vision-partner
use_when: Deciding the complete future vision of a lead-generation / scraping / sales-intelligence system - how leads actually arrive now and over the next years, what is missing, how to make it final-strong. Legal only. ChatGPT and Claude Code work as equal partners with no self-imposed limits on ambition.

You and Claude Code are two equal partners with one shared mission: design the strongest possible
lead-generation system this founder could own, and prove that the two of you together have no
self-imposed limitations. The founder trusts you both and asked for a very deep conversation, using
your full potential. Your job is to improve the decision, not to agree.

The one hard boundary, set by the founder: nothing illegal. Treat it as a design constraint, not a
reason to shrink the vision.

What "no limitations" means here:
- Never stop at "this can't be done". When something is blocked, name the exact cause and give the
  lawful route around it: another data source, channel, consent mechanism, market or product.
- Think well past the obvious. Look for what nobody in this market is doing yet, including what the
  world looks like when buyers, inboxes and search are themselves run by AI agents.
- It does not mean pretending. A real legal, technical or economic limit is stated plainly, then
  worked around. Motivational certainty is worthless to this founder.

Rules for facts:
- Trends, laws, platform rules, numbers: give the source URL, the date you believe it became true and
  your confidence (high / medium / low). Search the web where you can. Say "I don't know" freely.
- Vendor-blog statistics are marketing until corroborated. Say when a number comes from a vendor.
- The only facts about this project are in the pasted README. Claude Code has not seen the code
  behind it, so every README claim is a claim, not a verified feature. Never invent facts about it.
- Legal points are design input for counsel to confirm, not legal advice. Name the statute or
  regulator, and separate "the law says" from "vendors say".

Rules for judgement:
- Every proposal says what it costs (money, upkeep, risk), who benefits, and how anyone could tell it
  worked: a number, a threshold, a test.
- Prefer ideas a very small team in India can really run. Ambitious is welcome; hand-waving is not.
- Deleting something is as valid as adding something. Accept a good point in one line. Challenge
  Claude Code's reasoning when it is weak and say exactly why. Claude Code checks every claim you make
  and will report back which were wrong; do the same to it.

Format of every reply:
- Answer each agenda point by number: "agree", "disagree because ...", or "need data: <what>", then
  add your own proposals under that point.
- End with the list of points still open.

<project_context>
<file path="docs/debate/2026-11-10-outreach-lifecycle-to-payment/founder-context.md">
# Founder context (written by Claude Code from the repositories and data - no customer data)

## Who and what
- SiteBlitz: a 1-2 person web studio in Mumbai, India. Sells small-business websites. Founder is not a
  native English writer; works with Claude Code (has the repos and data open) and ChatGPT as equal partners.
- **No paying client yet.** Everything done so far was free. The founder now wants paid work only.
- Strategy only in this conversation. Nothing is sent or built until the founder approves.

## The offer today (source: SiteBlitz repo `src/lib/offer.ts`, prices in INR, no GST - not GST-registered)
| Package | Price | Payments | Delivery |
|---|---|---|---|
| Launch | Rs 7,999 | Rs 4,000 deposit + Rs 3,999 balance | 1 page, 2 working days after "ready-to-build" |
| Business (recommended) | Rs 17,999 | Rs 9,000 + Rs 8,999 | 3 pages, 7 working days after "ready-to-build" |
| Custom | quoted | milestones in the quotation | e-commerce, bookings, more pages |
- "Ready-to-build" = pages/features confirmed in writing + content, images, business details received + access
  (domain, accounts) shared + first payment received + start date agreed.
- One consolidated revision round. Excluded: domain and hosting fees, paid plugins/stock, e-commerce, ad spend,
  guaranteed rankings/enquiries, unlimited redesigns, ongoing edits.
- Free personalised homepage concepts exist, capped at 3 per week (or 9 hours), decision FD-26.
- No prices exist yet for clients outside India (no USD / EUR / GBP / AED price list). Hard rule: no invented
  testimonials, client names, results or case studies - there are none.

## The lead data (source: `E:\SiteBlitz-World-Business-Data\README.md`, Overture Maps Places 2026-10-21.0, open data)
- 86,751,626 businesses (permanently closed removed), 247 countries. Largest: US 17.8 M, Brazil 5.8 M,
  Germany 4.7 M, India 4.7 M, UK 4.2 M, Italy 3.6 M, France 3.6 M, Mexico 3.3 M, Japan 3.0 M, Spain 2.5 M.
- With a phone 82 %, with an email 36 %, with their own website 54 %, social profile but no website 38 %
  (the best website leads), no website and no social 8 %.
- Fields per business: name, category, state, city, address, lat/lon, phones, emails, website, Facebook /
  Instagram / LinkedIn / TikTok / YouTube / X / WhatsApp links, Overture confidence 0-1.
- Emails and phones are what the business (or its listing source) published; nothing is verified yet.
- Measured today by Claude Code (DuckDB over all 86.75 M rows, counts only):

| Reachability bucket | World | % | India | US | Germany | UK |
|---|---|---|---|---|---|---|
| email + phone | 29,008,537 | 33.4 | 1,618,943 | 6,223,051 | 1,030,816 | 842,739 |
| email only | 1,957,523 | 2.3 | 120,300 | 284,226 | 59,538 | 80,264 |
| phone only | 41,959,736 | 48.4 | 1,818,700 | 9,402,584 | 3,178,607 | 2,736,673 |
| social profile only (no email, no phone) | 10,057,454 | 11.6 | 1,083,879 | 873,953 | 149,165 | 217,250 |
| website only | 1,551,632 | 1.8 | 22,108 | 512,748 | 89,804 | 143,193 |
| nothing | 2,216,744 | 2.6 | 10,018 | 510,733 | 173,615 | 146,397 |

| Email signal (first email per business) | World | India | Germany |
|---|---|---|---|
| businesses with an email | 30,966,060 | 1,739,243 | 1,090,354 |
| free-mail domain (gmail, yahoo, ...) | 16,742,936 (54 %) | 1,380,188 (79 %) | 168,632 (15 %) |
| same domain as their own website | 9,014,891 (29 %) | 242,417 (14 %) | 646,577 (59 %) |
| role address (info@, contact@, ...) | 5,967,866 (19 %) | 199,307 (11 %) | 550,183 (50 %) |
| same address listed on >= 5 places | 1,004,152 (3.2 %) | 14,442 (0.8 %) | 114,330 (10.5 %) |
| same address listed on >= 50 places | 602,721 (1.9 %) | 5,468 | 68,140 |
| invalid syntax | 12,483 | 459 | 4,985 |
- A separate lead-generator app (Python/FastAPI) finds and scores businesses by city and category.
  **Known defect:** its enrichment step generated guessed addresses such as info@<domain> - in one Surat export
  37 of 38 emails were generated, not found. These must be treated as fake/unverified.
- The team has been sending from several free Gmail accounts and landing in spam (founder report, 2026-11-09).

## Email infrastructure already agreed (2026-11-09 review, 2 ChatGPT rounds)
- Level 0: brand domain siteblitz.in (after a trademark search) + 1 Google Workspace inbox hello@ for replies and
  clients - never used for cold first touches.
- Level 1 pilot: separate org, 2 .com sending domains x 3 inboxes, Instantly Growth, MillionVerifier;
  3,000 sends = 1,000 verified contacts x 3 touches; 3-week warm-up 5 -> 25/day per inbox.
- Gates before scaling (level 2, 1,000/day): verified-email yield >= 20 %, hard bounce <= 1 %, Gmail spam
  < 0.10 %, positive replies >= 3 %, >= 3 paid orders per 3,000 sends.
- Bulk ESPs (SendGrid, Brevo) rejected: they ban non-consented first-touch mail.

## Compliance rules already coded (lead generator `qualification/country_rules.py`)
- US CAN-SPAM (postal address, opt-out, honour within 10 days), UK PECR (corporate subscribers no opt-in),
  EU GDPR legitimate interest with opt-out, Germany / Austria / Greece = manual review only, Canada CASL
  (conspicuous publication, role-relevant), Australia Spam Act (inferred consent by publication), default = opt-out.
- India-specific rules: not coded yet. DPDP Act legal review: open.

## What the founder asked for now (2026-11-10, translated from Roman Hindi)
1. What to send to businesses that have an email: content, structure, tone - it must read as written by a
   respectful human, never AI-generated, and get the maximum result from cold email.
2. Businesses with only a mobile number: how to message them - WhatsApp or something else.
3. Businesses with neither email nor phone: what to do.
4. Businesses whose email may be fake: what to do.
5. A complete lifecycle for every business, day by day: day 1 first mail, wait N days, follow-up, what to do
   when they reply, which requirements to collect, all the way to the exact moments payment is taken.
   Target is websites, but any paid service is fine for now.
6. Leads are in many countries: detect the country and write in that country's language, very respectful tone.
7. Something unique that makes the owner think "oh my god, these people found a new way" - for example a
   generated voice audio message inside the email or WhatsApp. Research whether that works.
8. Use only the necessary data; drop the rest.

</file>

<file path="docs/debate/2026-11-09-siteblitz-domain-cold-email-infra/RESULT.md">
# Review - SiteBlitz domain + cold-email infrastructure (1,000 emails/day) - 2026-11-09 - 2 rounds - prompt: none (project context only)

FX Rs 94.5/USD (PTI close 94.46, 2026-11-05). Workspace prices are Google India annual-commitment list prices + 18% GST.
USD bills (Porkbun, Instantly, MillionVerifier, Vercel) exclude card forex fees and any GST the vendor adds.

| # | Point | Proposed by | Evidence (file:line / round) | Claude's verdict | Status |
|---|---|---|---|---|---|
| 1 | Brand domain `siteblitz.in`, bought only after a free IP India trademark search (classes 35 + 42) | Claude, ChatGPT conditional | NIXI RDAP "available" 2026-11-09; siteblitz.com taken since 2001; French "SiteBlitz" on siteblitz.ai + getsiteblitz.com + trysiteblitz.com (2026-06-16) | agreed | Agreed |
| 2 | Spam cause #1 (suspected): fabricated / unverified recipients; free Gmail by itself is not the root cause | Both | `backend/app/engines/enrichment/discovery.py:139`; `surat_restaurant_leads_with_contacts.csv` 37 of 38 emails generated; Google Gmail help: >500 emails/day cap | agreed - unproven until the team says which list it sent | Agreed |
| 3 | Do not buy 30 inboxes / 10 domains now; gate on data + pilot first | ChatGPT R1 (Claude draft had the gate) | R1 s3, R2 A | agreed | Agreed |
| 4 | Send through a bulk ESP instead of inboxes | ChatGPT R1 | SendGrid prohibits lists "that have not affirmatively consented"; Brevo never allows purchased/scraped lists | rejected - ESPs ban non-consented first-touch mail | Rejected |
| 5 | One paid Workspace Base user `[REDACTED]` ("SiteBlitz Team") + free aliases projects@, support@, billing@; no CEO/CTO mailboxes; 2nd seat only when the friend needs his own login | Both | Google: 30 aliases/user free; Base Rs 99, max 20 users | agreed | Agreed |
| 6 | Cost corrections: Instantly Hypergrowth USD 107 (125k emails, 25k contacts; +25k contacts = USD 87/mo); Growth (5k emails, 1k contacts) cannot carry live 1k/day sending; MillionVerifier USD 89 / 50k | ChatGPT R1-R2 | instantly.ai/pricing and millionverifier.com, checked 2026-11-09 | agreed - delete finished contacts in Instantly, keep the suppression list in our DB | Agreed |
| 7 | Hosting line missing: Vercel Hobby is non-commercial; Pro USD 20/seat/month (~Rs 2,230 with 18%) | ChatGPT R1 | SiteBlitz DECISIONS D12; third-party Vercel pricing pages | agreed - separate decision (D12) | Agreed |
| 8 | Live `siteblitz.vercel.app` still shows withdrawn Rs 14,999 / Rs 24,999 and the bouncing `[REDACTED]` (6x) | ChatGPT R1 | curl of the live page 2026-11-09 vs `E:\Temp\SiteBlitz\src\lib\offer.ts` | agreed - fix before any outreach | Agreed |
| 9 | Go/no-go gates: verified-email yield >= 20%, hard bounce <= 1%, Gmail spam < 0.10%, positive replies >= 3%, >= 3 paid orders per 3,000 sends | ChatGPT R2 | Google sender FAQ (0.1%); others judgement; rule of three: 0 complaints in 3,000 -> 95% bound 0.1% | agreed as judgement thresholds | Agreed |
| 10 | Pilot from `[REDACTED]` at 20/day | ChatGPT R2 | R2 B, C | rejected - 3,000 sends at 20/day = 150 sending days, and cold mail would put the only real mailbox at risk; use a small separate pilot stack (below) | Rejected |
| 11 | Full 1,000/day stack (only if every gate passes): 30 inboxes x 33-34/day on 10 .com domains | Claude; ChatGPT costed it but does not approve it (Workspace AUP bans "large volumes of unwanted emails") | R2 B | agreed as the cost; the decision is the founder's after the gates, with suspension risk stated | Agreed (cost) |
| 12 | "Rs 13,400 saving is unsupported" | ChatGPT R1 | 22,542 - 9,167 = 13,375 is the cost without Instantly, not a saving | rejected - misread | Rejected |
| 13 | India DPDP (main rules from ~13 May 2027) + legal review of contact collection before scaling | Both | DPDP Rules notified 2025-11-13 | open - needs a lawyer, not a model | Open |

## The three cost levels

**Level 0 - now (business email only):** `siteblitz.in` Rs 1,061 + 1 Base user Rs 117/month.
Month 1 Rs 1,178 · year 1 Rs 2,463.

**Level 1 - pilot (3,000 sends = 1,000 verified contacts x 3 touches), separate Workspace org:**
2 .com domains Rs 2,232 one-time · 6 Base inboxes Rs 701/month · Instantly Growth Rs 4,442/month ·
MillionVerifier 10k Rs 3,686 one-time. With level 0: month 1 ~Rs 12,239, then ~Rs 5,260/month.
Timeline: 3-week ramp (5 -> 25/day per inbox), then 150/day for ~20 sending days; gate decision ~week 8.

**Level 2 - 1,000/day (only after the gates):** month 1 Rs 40,418 (10 .com Rs 11,160 + 30 Starter Rs 9,558 +
Hypergrowth Rs 10,112 + 50k credits Rs 8,411 + .in Rs 1,061 + Base Rs 117); then ~Rs 23,487/month with
verification for 22,000 addresses/month amortised; year 1 ~Rs 3.0 lakh. Add hosting ~Rs 2,230/month if Vercel Pro.
Keeping every old contact in Instantly would add USD 87/month per extra 25,000 contacts (~Rs 8.1 lakh/year) -
delete finished contacts instead.

## Recommended next steps (not started - waiting for your go)
1. Founder: IP India public trademark search for "SITEBLITZ" (classes 35, 42) - free.
2. Founder: buy `siteblitz.in` (complete NIXI e-KYC within 7 days) + Workspace Base `[REDACTED]`, add
   SPF / DKIM / DMARC; stop all sending from the free Gmail accounts.
3. Code (lead generator): stop fabricating contacts (`discovery.py:122-148`, `lead_radar_service.py:309`,
   `export_surat_leads.py:139-159`); mark each contact verified / unverified / absent with its source.
4. SiteBlitz site: redeploy production from the current branch so the live prices and email match `offer.ts`
   (separate repo, `docs/DEPLOY.md`), and settle hosting (D12).
5. Phase 5 sender: real provider status instead of fake SENT, signed unsubscribe token, real postal address,
   India rules in `country_rules.py`.
6. Only after 1-5: level-1 pilot stack; level 2 only if the gates in row 9 pass.

## Points still open
- Which list the team actually sent from the free Gmail accounts, and its bounce / complaint numbers.
- Real verified-email yield of the lead generator for Indian SMBs (measured in the pilot).
- Legal review (DPDP, contact collection) and Google AUP risk acceptance for any first-touch volume.
- Trademark clearance result.

</file>
</project_context>

<topic>
Note for this round: the project facts are in founder-context.md above. Claude Code wrote it from the real
repositories and the real data folder and has checked it; there is no README to rely on this time.

The founder's own words (Roman Hindi, translated): "You, me and ChatGPT are three partners. Your joint task: for
the businesses that have an email, what content do we send, how is it written, in what tone, so it never looks
AI-generated, looks properly human-written, and gets the maximum output even from cold email. Second, how do we
message the ones who only have a mobile number - WhatsApp or what? Third, what about those with neither mobile
nor email? Fourth, the ones whose email may be fake? The main thing is the content. Until now we have no client;
everything we did was free and I don't want that any more. Build a flow for how everything will run - a
lifecycle every business goes through: e.g. day 1 first mail, no reply -> wait 5, 7 or 10 days (you two
decide), follow-up, if they reply what we talk about next, which requirements we need - a complete flow up to
payment, so we know exactly at which moment payment is taken. We have data from many countries: identify the
country and write in that country's language, very respectful. And find something unique - e.g. a generated
voice audio message inside the email or WhatsApp - so the owner thinks 'oh my god, these people found a new
way'. Research it."

Agenda:
1. Data hygiene and fake emails: which records to keep or drop before any outreach, and the exact verification ladder for an email (syntax, MX, SMTP check, catch-all, shared by many places, guessed by our tool) with the action for each result.
2. Channel routing per lead - (a) has email, (b) phone only, (c) neither, (d) email suspect - the lawful channel per country (WhatsApp app vs API vs call vs SMS vs DM vs contact form vs post vs walk-in), with ban and legal risk for each.
3. The cold email itself: structure, length, subject line, first line, offer/hook, call to action, signature, and the rules that make it read as written by a respectful human, not AI - with full English drafts for touch 1 and every follow-up.
4. The lifecycle as a state machine from "found" to "paid" to "after delivery": days between touches, total touches, every reply branch (interested, price?, send details, already have a site, not now, no, wrong person, bounce, unsubscribe) with the next message, the requirements checklist, and the exact moments the deposit and balance are taken.
5. Countries and languages: how to pick the language and formality per lead (country, region, script), which countries to hold or skip, send-time windows, native review, and how to price for non-India clients (founder decision - propose options only).
6. The unique hook: AI-generated voice note (founder's own cloned voice vs real recording vs none), free personalised homepage concept, short screen video, before/after screenshot - which works, at which step, cost, deliverability and trust risk, disclosure.
7. A 30-day paid-first pilot: which country and business type first, daily volume per channel, what the founder does each day, and the numbers that mean continue / change / stop.

Constraints you must respect: the 2026-11-09 infrastructure and gates in founder-context.md stand unless you
show a concrete flaw; no invented proof; nothing illegal or against a platform's terms (name the rule and its
source). Write every template so a non-native founder can send it and still sound natural.

Answer each agenda point by number: agree / disagree because ... / need data: ... . End with the list of points still open.
</topic>


---

## ChatGPT (Extra High) - 2026-11-10 02:29 UTC - saved as 01_chatgpt.md

ChatGPT said:
SiteBlitz — Complete Lead-to-Payment Growth System

Strategic review | 10 November 2026 | ChatGPT response to Claude Code and the founder

Overall verdict: Agree with the seven-point agenda, but challenge parts of the existing outreach infrastructure plan.

The objective should not be to contact the maximum number of businesses. It should be to identify businesses with a genuine need, reach them through an appropriate and permitted channel, communicate like a credible human professional, and convert them into paying customers through a repeatable system.

SiteBlitz has a potentially valuable global business database, but that does not automatically translate into a usable sales database.

According to the supplied project context, the current position is:

86.75 million business records across 247 countries.

Approximately 30.97 million records with an email address.

Approximately 41.96 million with a phone number but no email.

Approximately 13.83 million with neither email nor phone.

No paying customers yet.

Existing website offers of ₹7,999 and ₹17,999, plus custom quotations.

A known defect producing guessed rather than discovered email addresses.

These are project-reported figures, not independently audited database measurements.

Two corrections before approving the system

1. Disagree with treating multiple Google Workspace inboxes as an automatically acceptable cold-email scaling strategy.

Google Workspace's Acceptable Use Policy, last modified on 13 October 2025, prohibits unsolicited mass email. Gmail's program policies also restrict unsolicited commercial messages. Six inboxes instead of one do not eliminate this risk. 
Google Workspace
+1

I would retain the previously agreed pilot budget as a financial estimate, but make the sending-provider's explicit policy approval a mandatory requirement before activating any campaign.

2. Disagree with using publicly listed mobile numbers for unsolicited WhatsApp messages.

WhatsApp's Business Messaging Policy, updated 23 September 2026, requires both contact information provided by the recipient and opt-in permission. The requirement applies to the Business App as well as the Business Platform. A number appearing in Overture data is not sufficient permission. 
WhatsApp for Business

The opportunity is not lost. Those numbers can still support verification, qualification, and legally permitted alternative contact routes.

The following seven points define the proposed system. Legal interpretations are design guidance requiring jurisdiction-specific confirmation, not legal advice.

1. Data hygiene and fake email verification

Verdict: Agree — this must be completed before outreach begins.

The lead-generation application's reported practice of creating addresses such as info@companydomain.com is a serious defect. Those are plausible email patterns, not discovered contacts.

For a business with no verified email, having a guessed email is actually worse than showing no email: it creates false confidence and risks delivery failures.

Exact verification ladder

Step

	

Test

	

Required action




1

	

Duplicate business or contact

	

Merge into one company record; preserve existing suppression decisions




2

	

Email syntax invalid

	

Reject the address




3

	

Address was generated or guessed

	

Mark GUESSED; never send without independent confirmation




4

	

Domain or email service invalid

	

Reject when DNS confirms no valid delivery route




5

	

MX or mail-routing check

	

Continue only if a viable receiving route exists




6

	

SMTP or verification-provider check

	

Classify as valid, invalid, temporary error, or unknown




7

	

Catch-all domain

	

Hold for manual review; do not classify the mailbox as verified




8

	

Same email on many businesses

	

Investigate whether it is a real group address, franchise address, directory contact, or bad data




9

	

Source confirmation

	

Recheck against the business's official website or another credible first-party source




10

	

Legal and opt-out eligibility

	

Send only if this recipient, channel and country pass the compliance rules

Two technical qualifications matter. A domain without an MX record is not automatically invalid because SMTP can fall back to an A/AAAA record; an explicit null MX indicates that the domain does not accept email. SMTP acceptance also does not always prove that a specific person's mailbox exists. These distinctions are documented in RFC 7505 and RFC 5321 (2015 and 2008 respectively; high confidence).

Final contact statuses

I propose retaining six operational statuses:

Status

	

Meaning

	

Send?




CONFIRMED

	

Reply, reliable first-party confirmation, or equivalent direct proof

	

Only if legally permitted




VALID

	

Reputable verification reports deliverable; provenance recorded

	

Eligible for compliance review




RISKY

	

Catch-all, shared mailbox, or conflicting verification

	

Manual review




UNKNOWN

	

Verification inconclusive

	

No automatic send




INVALID

	

Rejected, nonexistent, or known permanently failed

	

No




SUPPRESSED

	

Opt-out, objection, or explicit do-not-contact

	

Never for marketing

A verification vendor's valid result is not proof of inbox placement, owner identity, or permission.

Important challenge: Do not automatically delete Gmail, Yahoo or other free-domain addresses. According to the supplied database counts, 79% of Indian businesses with an email have a free-mail address as their first email. Deleting them would discard a large portion of the Indian market. Verify the business association instead.

Data worth keeping

Keep a lean company record containing business identity, country, category, location, official website/social links, useful contact information, provenance URL, verification status/date, language evidence, channel permission, observed website need, and CRM state.

Keep interaction history, quotation/payment references and the suppression record separately.

Discard irrelevant personal attributes, old generated addresses, excessive raw scrape metadata, and redundant contact duplicates. Keep an auditable reason for rejection rather than silently deleting evidence.

The Overture Places data is published under different open-data licences depending on source; its openness does not itself provide consent for marketing. 
Overture Documentation

Cost and success test: Budget approximately 2–4 engineering days for the initial verification/suppression pipeline, subject to the existing code quality. The supplied pilot budget already includes ₹3,686 for a 10,000-address verification package, but that price should be rechecked. Audit 100 randomly selected accepted addresses manually before sending.

Proceed to the pilot only if the observed valid-email yield is at least 20%, with a hard-bounce rate of no more than 1% during controlled sending. These are proposed business thresholds, not legal standards.

2. Channel routing: email, phone, social, and unreachable businesses

Verdict: Agree, but disagree that WhatsApp is the default for phone-only records.

Channel selection must follow two independent tests: can we technically reach this business? and are we allowed to contact it this way?

Recommended routing

Lead condition

	

First route

	

Alternative

	

Avoid




Verified email

	

Relevant, compliant business email

	

Referral or permitted call

	

Generic mass blasts




Mobile number only

	

Check local calling rules and any existing opt-in

	

Consent-based WhatsApp, referrals, advertising

	

Unsolicited WhatsApp broadcasts




Social profile only

	

Organic engagement, allowed paid advertising, genuine relationship-building

	

Appropriate manual DM where permitted

	

Automated bulk DMs




Website/contact form only

	

Check whether the form permits commercial proposals

	

Relevant public business channel or referral

	

Mass contact-form submissions




Neither digital contact nor social

	

High-value manual research, local networking or permitted postal outreach

	

Inbound advertising

	

Expensive endless enrichment




Suspect email

	

Reverify and locate another published contact

	

Reclassify into the appropriate bucket

	

Sending to guessed addresses

A real mobile number is not the same thing as permission for WhatsApp, SMS or a marketing call.

WhatsApp: App versus API

Both the WhatsApp Business App and Platform require opt-in for business-initiated contact. The API additionally requires approved message templates for business-initiated conversations and uses a 24-hour customer-service window for ordinary free-form replies. 
WhatsApp for Business

My route is to acquire permission through customer enquiries, website forms, referrals, events, or properly labelled advertisements that invite people to contact SiteBlitz.

A suitable opt-in example on a lead form is:

I agree to receive messages from SiteBlitz about website services and quotations on WhatsApp. I can opt out at any time.

Make the checkbox optional, unchecked by default, and store its timestamp and disclosure text.

Once someone opts in, a simple first WhatsApp message can be:

Writing

Hello [Name], this is [Your Name] from SiteBlitz.

Thank you for agreeing to discuss your business website with us.

Could you tell me whether you need a new website or want to improve an existing one?

I can then suggest a suitable option and share the price.

Legal differences matter

United States: CAN-SPAM applies to commercial B2B email, including single messages; it requires truthful sender details, a genuine postal address, an opt-out mechanism, and honoring requests within 10 business days. This does not automatically authorize calls or texts. FTC official guidance, existing law verified November 2026, high confidence. 
Federal Trade Commission

United Kingdom: PECR generally permits marketing emails to corporate subscribers without prior opt-in, but sole traders and certain partnerships have different protections. Personal data use still needs an appropriate UK GDPR basis. Check TPS/CTPS before live marketing calls. ICO guidance, checked November 2026, high confidence. 
ico.org.uk
+1

India: Under TRAI's TCCCPR framework, commercial calls/SMS face sender-registration, preference and related telecom rules. Ordinary personal SIMs are not an acceptable route for unsolicited bulk telemarketing. 
Government of India
+1

Germany: Section 7 of the UWG generally requires prior express consent for advertising by email, subject to its narrow existing-customer exception. 
UWG)

Canada: CASL requires consent or a legally valid exception/implied-consent basis, identification, and unsubscribe. Merely finding an address in a dataset is insufficient. 
CRTC

Australia: The Spam Act requires express or properly inferred consent. Relevant publication may be a factor, but consent must be defensible. ACMA guidance, checked November 2026, high confidence. 
ACMA
+1

LinkedIn explicitly restricts unauthorized automated messaging and scraping. Do not build automation that impersonates human platform interactions. 
LinkedIn

What to do with the 13.83 million records lacking email and phone

The supplied counts separate them into three useful groups:

Social profile only

10,057,454

Website only

1,551,632

No listed contact channel

2,216,744

Shares of the 13.83 million with neither email nor phone, calculated from supplied project counts.

The social-only group is not worthless. It is potentially valuable for a website studio: many businesses may already be using social media as their only online storefront.

But a 1–2-person team should not manually research all 10 million. Build a qualification score that prioritizes visible commercial activity, no verified website, suitable business type, location, and a permitted way to engage.

Cost and success test: Start with 50 manually reviewed leads per channel. Record time per qualified conversation, percentage that replies positively, and paid conversions. Kill any channel whose acquisition cost and time consistently exceed the expected contribution from a sale.

3. Cold email content: how to sound human and earn replies

Verdict: Agree. The content deserves more attention than sending volume.

I disagree with the idea that the best way to sound human is to make AI writing deliberately imperfect.

Human-sounding writing comes from three things: a true observation, an offer relevant to that specific business, and a reasonable request. Artificial spelling mistakes, exaggerated friendliness, and fabricated familiarity reduce trust.

Recommended format

Element

	

Recommendation




Subject

	

4–8 meaningful words, clear and truthful




Greeting

	

"Hello [Name]," or simply "Hello,"




First sentence

	

One specifically verified observation about their business




Body

	

Introduce SiteBlitz and explain the business benefit




Offer

	

Fixed-scope website with a price quoted before work




CTA

	

One simple question that can be answered in one sentence




Length

	

Approximately 70–120 words before signature




Signature

	

Real sender, SiteBlitz identity, working reply channel, genuine postal address




Opt-out

	

Easy and clear in every marketing message

Don't use invented testimonials, false claims about leads or Google rankings, fake deadlines, or a Re: prefix on the first email.

Touch 1 — Day 1: Introduction

Use this version only where the business's social profile or listing has been checked and genuinely does not show an official website.

A website idea for [Business Name]
Send
From
contact@aaziko.com
Recipients

Hello [Name],

I came across [Business Name] through [Facebook / Instagram / business listing].

I noticed that [specific, verified observation]. I couldn't find an official website linked there, so I thought I'd reach out.

I'm [Your Name] from SiteBlitz. We build simple, professional websites that help customers find business details, understand services, and get in touch.

Would you be interested in seeing a suitable website option and its fixed price?

Best regards,
[Your Name]
SiteBlitz
[Working website or business contact]
[Actual business postal address]

If you'd prefer no further emails, simply reply "stop".

Why this version: It opens with genuine context, says what is being offered, and asks permission to discuss rather than demanding a meeting.

Touch 2 — Day 6: Useful follow-up

Reply in the original email thread.

Re: A website idea for [Business Name]
Send
From
contact@aaziko.com
Recipients

Hello [Name],

Just following up on my earlier message.

For [Business Name], a simple website could bring together [services / products], location details, and a clear way for customers to contact you.

It wouldn't need to be complicated. We could start with the essential pages and agree on the price before any work begins.

Would you like me to send a short outline?

Best regards,
[Your Name]
SiteBlitz
[Working business contact]
[Actual business postal address]

If you'd prefer no further emails, reply "stop".

The bracketed details must be selected from actual facts. Do not invent products or services.

Touch 3 — Day 14: Final follow-up
Re: A website idea for [Business Name]
Send
From
contact@aaziko.com
Recipients

Hello [Name],

I'll leave this with you after this message.

I thought a straightforward website might be useful for [Business Name], especially for customers who want to find your business information in one place.

If it's something you're considering, you're welcome to reply whenever convenient. I can share the options and price.

Thank you for your time.

Best regards,
[Your Name]
SiteBlitz
[Working business contact]
[Actual business postal address]

I won't send further follow-ups. You can also reply "stop" at any time.

Day 21: If there is no response, close the prospecting sequence and do not automatically start another campaign against the same business.

This keeps the previously agreed pilot at three messages per prospect.

Content personalisation rules

Only personalise what can be supported by a source. Useful variables are the company's actual business activity, a real location or service, evidence that customers currently depend on social media, and a verified website problem.

A weak opener is: "I was extremely impressed by your amazing business."

A better opener, when factually true, is: "I found your menu on Instagram, but couldn't find a website link with your opening hours."

The second sentence demonstrates relevant research without pretending there is a relationship.

Cost and test: Expect roughly 3–5 minutes of human review per qualified first-touch lead initially, plus automated drafting. At 1,000 prospects, that is about 50–83 hours of review. This is an operational estimate, not measured SiteBlitz performance.

Measure positive replies and paid deposits, not open rates. Google's guidance explicitly notes that third-party open-rate measurements may be inaccurate. 
Gmail Help

Keep the better-performing template only if it increases qualified conversations without higher complaint or bounce rates.

4. Complete lifecycle: from discovered business to final payment

Verdict: Agree. This is the central operating system SiteBlitz needs.

A lead should never sit in an undefined status such as "follow-up pending" without a next action, owner, and due date.

Recommended CRM state machine

FOUND → DEDUPLICATED → QUALIFIED

CONTACT VERIFIED → CHANNEL APPROVED

TOUCH 1 → TOUCH 2 → TOUCH 3

Stop immediately if the recipient replies or opts out

Positive reply

Discovery

No / opt-out / bounce

Closed or suppressed

SCOPE AGREED → QUOTE ACCEPTED → DEPOSIT PAID

READY TO BUILD → BUILD → REVIEW → BALANCE PAID

LAUNCH → HANDOVER → AFTER-DELIVERY SUPPORT

Proposed state sequence, not a claim about implemented code. Each state change should be recorded with its time and responsible person.
Day-by-day sales schedule

Day

	

Condition

	

Action




Day 0

	

New business discovered

	

Deduplicate, verify business and contact, check country rules




Day 1

	

Qualified and outreach permitted

	

Send first message




Day 2–5

	

No reply

	

Wait; don't chase across multiple channels




Day 6

	

No reply

	

Send first follow-up




Day 7–13

	

No reply

	

Wait




Day 14

	

No reply

	

Send final follow-up




Day 21

	

Still no reply

	

Close sequence




Any day

	

Positive reply

	

Pause all scheduled marketing and enter sales discussion




Any day

	

Rejection or opt-out

	

Stop, suppress and record




Any day

	

Hard bounce

	

Suppress that address

The day numbers are a recommended experiment, not evidence that a 5-day interval is universally optimal.

Every common reply branch

The system should classify replies and prepare these next messages for human review.

Customer reply

	

Proposed next message/action




Interested

	

"Thank you. Is this for a new website or an existing one? And what is the main thing customers should be able to do on it?"




How much?

	

"For clients in India, our Launch package is ₹7,999 for one page, and Business is ₹17,999 for three pages. Domain and hosting are separate. If you tell me what pages you need, I can confirm the suitable option." For other countries, send an approved local-currency quote instead.




Send details

	

"Of course. We offer a one-page Launch website and a three-page Business website, with scope and price agreed before starting. Could you tell me your business type and preferred pages so I send the relevant details?"




We already have a website

	

"Thank you for clarifying. Are you satisfied with it, or is there something specific you'd like improved? If it's working well, I won't take more of your time."




Not now

	

"Understood, thank you. Would you prefer that I close this for now, or is there a particular month when you'd welcome another message?" No scheduled recontact unless they request it.




No / not interested

	

"Understood. Thank you for letting me know." Stop further marketing to that contact.




Wrong person

	

"Thank you for telling me. Is there a public business contact for website-related enquiries, or would you prefer I leave this here?"




Hard bounce

	

No customer message. Mark invalid, investigate the source, and suppress the failed address.




Unsubscribe / stop

	

Suppress immediately. Do not wait for the legal maximum or send a new sales message.




Budget too low

	

"I understand. We can review the scope and see whether a smaller website fits. I wouldn't want to promise features that don't fit the price."




Please call me

	

Confirm the preferred time, telephone number and permission to call; log the request.

An AI classifier can propose the branch, but ambiguous replies, objections and commercial negotiations should go to a human.

Requirements to collect after genuine interest

Do not ask for 20 fields in the first message. Use a short discovery conversation first.

At the quotation stage, collect the legal/business name, decision-maker, country, purpose of website, preferred pages, required functions, expected delivery schedule, available budget and whether it is a new build or redesign.

After the client accepts the quote, collect the logo, approved text and images, products/services, address/contact details, preferred design references, domain/hosting information, authorised access and any legal content requirements.

Do not ask clients to email passwords. Use secure delegated access where possible.

Exactly when to request payment

Moment 1 — The scope and price are accepted

Send the written agreement and deposit invoice. Do not begin design or development until payment is confirmed.

LAUNCH DEPOSIT

₹4,000
₹7,999 total

BUSINESS DEPOSIT

₹9,000
₹17,999 total

Moment 2 — Ready-to-build is confirmed

Start the delivery clock only after the agreed pages/features, required content, access, deposit and start date are all confirmed. The stated targets are two working days for Launch and seven for Business.

Moment 3 — Staging review is accepted

Show the working site in a review environment. Complete the one included consolidated revision round, obtain written approval and issue the balance invoice.

LAUNCH BALANCE

₹3,999

BUSINESS BALANCE

₹8,999

Moment 4 — Final payment is confirmed

Publish the website, transfer or document agreed access, deliver handover information, and close the delivery milestone.

The client agreement should explicitly say that the remaining payment is due before public launch and final handover, that customer-caused content delays pause the delivery clock, and that additional features require a new written quotation.

Custom projects continue to use the milestones defined in their individual quotations.

After-delivery lifecycle

On launch, provide a handover email covering the website URL, agreed features, access/ownership, domain and hosting arrangements, and any written support terms.

Check for genuine delivery defects within the agreed warranty/support window. Do not silently promise unlimited ongoing changes. Invite a factual review only after a real successful delivery, and ask permission before using the work publicly as a case study.

Cost and success test: Track time from positive reply to scope agreement, scope agreement to deposit, deposit to ready-to-build, and ready-to-build to launch. The most important sales metric is quote-to-deposit conversion, not a CRM stage called "interested."

5. Countries, languages, local timing and international pricing

Verdict: Agree with international expansion. Disagree with automatically translating messages based on country alone.

A business's country tells us which legal rules to investigate. It does not reliably tell us which language its owner prefers.

Country permission matrix

Market

	

Recommended initial policy

	

Confidence




India

	

Prioritise permission-based contact, referrals, inbound enquiries and established business relationships

	

High for TRAI restrictions; legal review needed for email/data




US

	

Target relevant businesses through compliant B2B email, with CAN-SPAM controls and compatible provider terms

	

High




UK

	

Start with verified limited companies/LLPs; exclude uncertain sole-trader records from automatic cold outreach

	

High




France

	

Relevant professional B2B email may be permissible with notice, lawful basis and effective objection rights

	

High




Germany

	

No first-touch cold marketing email without a qualifying permission or narrow legal exception

	

High




Austria / Greece

	

Manual legal review before outreach

	

Medium




Canada

	

Only where CASL consent or a properly documented exception/implied-consent basis exists

	

High




Australia

	

Only with evidence supporting express or valid inferred consent

	

High




Other countries

	

Hold until the applicable country/channel rules are reviewed

	

Not yet assessed

The French regulator CNIL clarified B2B electronic prospecting conditions on 10 June 2026. German UWG Section 7, as amended in February 2026, imposes stricter prior-consent requirements. These are materially different approaches despite both countries being in the EU. 
CNIL
+1

The EU GDPR's legitimate-interest basis is not a universal override of national electronic-marketing rules. 
European Data Protection Board

India also has a transitional privacy-law issue: the November 13, 2025 DPDP notification introduced a phased commencement. Major personal-data processing provisions are scheduled for May 13, 2027, with another group scheduled for November 13, 2026. This should be reviewed now rather than waiting until the final phase. 
E-Gazette

Language selection algorithm

Use this priority:

Language evidence hierarchy

1. Business's own communication language

Highest confidence

2. Language of its official website and recent social posts

3. Explicit recipient preference

4. Region and local language evidence

5. Country-level language default

6. Manual review if confidence is insufficient

For example, a business in Mumbai may use English, Hindi or Marathi. A business in Quebec may prefer French, while another Canadian business may prefer English. A UAE business's professional communication may be English or Arabic.

Do not infer language only from a telephone country code, and do not assume gender or an honorific.

AI can draft translations, but the first 10–20 messages for each new language/market should receive native or professionally proficient review. Preserve the meaning and formality of the original rather than translating words mechanically.

Proposed local send-time test: Tuesday–Thursday, 9:00–11:30 AM and 2:00–4:30 PM in the recipient's timezone. This is a test hypothesis, not a verified universal best time. Avoid local public holidays and prohibited calling hours.

Cost: initial local-language QA and timezone/country-rule maintenance. Benefit: fewer embarrassing errors and more relevant conversations. Test using positive replies and translation corrections, separated by language.

Pricing outside India

The founder context correctly says SiteBlitz has no approved international price list.

I see three choices.

Option

	

Mechanism

	

Main weakness




A. Currency conversion

	

Convert approved INR package prices and add actual fees

	

Local support and currency risk may be underpriced




B. Country-specific prices

	

Set fixed local prices after market and delivery-cost research

	

More administration and pricing maintenance




C. Quote-only initially

	

Evaluate each international request and send an approved fixed quotation

	

Slower than showing an instant price

Recommendation: Option C for the first international clients. After 5–10 genuine quotations and completed projects, evaluate whether country-specific fixed prices make economic sense.

Do not publish arbitrary GBP, USD or EUR prices to make the site appear international.

For international payments, verify the actual processor's eligibility and required documentation before quoting a payment method. Stripe, for example, currently describes Indian account creation as invite-only, with additional requirements for international transactions. 
support.stripe.com

The Reserve Bank of India's new export/import framework took effect on October 1, 2026. An accountant and authorised bank should confirm SiteBlitz's international invoice, foreign-receipt and applicable tax treatment under the current rules. 
Reserve Bank of India

6. The unique hook: what will make the business owner pay attention?

Verdict: Agree that a distinctive approach matters. Disagree with making AI-cloned voice the primary hook.

A unique presentation is useful only when it increases trust or makes the business problem clearer.

A synthetic voice note received unexpectedly from a stranger could instead create suspicion.

Evaluate the options

Idea

	

Effort per prospect (estimate)

	

Main benefit

	

Main concern

	

Decision




Personalised text observation

	

2–5 minutes

	

Low-friction relevance

	

Poor facts ruin trust

	

Use first




Mini business website assessment

	

5–10 minutes

	

Demonstrates understanding

	

Research workload

	

Test




Human-recorded voice message

	

1–3 minutes

	

Genuine personal connection

	

Intrusive if unsolicited

	

After engagement




AI-cloned founder voice

	

Initial setup plus review

	

Can be produced at scale

	

Authenticity and disclosure concerns

	

Not first




Short annotated screen video

	

5–10 minutes

	

Visual explanation of a specific problem

	

Higher production cost

	

Test on interested leads




Free homepage concept

	

Up to 3 hours based on existing cap

	

Tangible demonstration

	

Free-work burden

	

Restrict




Before/after illustration

	

15–45 minutes if genuinely tailored

	

Shows possible design improvement

	

Must not misrepresent previous work

	

Qualified leads only

These are planning estimates, not measured production times.

What the evidence actually supports

Mailchimp's guidance states that most email clients do not reliably play embedded audio or video; linking to externally hosted media is the more dependable approach. Therefore, an "audio note inside every email" is technically weak. 
Mailchimp
+1

There is some research support for personalised visual content. A published study of generative-AI video advertisements found improved engagement compared with alternative ad formats. But that was an advertising experiment, not a study of cold B2B website-development emails. Its result cannot establish that cloned voice or personalised video will increase SiteBlitz's paid orders. 
DOI

I have not found convincing independent evidence that a cloned founder voice outperforms an authentic recording for this specific use case.

If synthetic voice is later tested, use only an authorised voice, clearly label synthetic recordings when appropriate, and never imply a personal recording or relationship that did not occur.

My proposed differentiator: The SiteBlitz Opportunity Snapshot

Instead of sending every business a generic pitch, create a small evidence-based assessment.

ILLUSTRATIVE SALES CONCEPT

Your online presence, simplified

Prepared for [Business Name]

What we found

One genuine, sourced observation from the business's public presence

What could improve

One specific opportunity, such as making services, service area and contact details easier to find

What SiteBlitz proposes

A simple website scope, an appropriate package and an upfront quotation

A proposed format, not an assessment of any actual business.

The snapshot should be short, accurate, and ideally produced only after a prospect expresses some interest. A sample visual can use an explicitly labelled illustrative design, not a claimed past-client result.

The founder's previous decision allowing three free homepage concepts per week or nine hours of work is potentially inconsistent with the new paid-first direction.

I recommend suspending that free-work programme until the first paid customers establish a reliable sales and delivery process. The founder must approve any change to that existing decision.

The experiment

After sufficient qualified, legally permitted conversations exist, compare a text-only explanation against the same explanation with an optional short, genuine screen video.

Randomise recipients within the same market and business type. Measure how many request a quote and ultimately pay a deposit, as well as the time required to prepare the material.

A small 25–50-person sample per approach can identify obvious practical problems, but it cannot reliably prove a modest conversion-rate advantage. Larger tests will be necessary.

Decision: Be unusually relevant, not artificially impressive.

7. A 30-day paid-first pilot

Verdict: Agree. The first 30 days should establish that real people will pay, not prove that 1,000 emails per day is possible.

Which market should come first?

I would separate the first revenue test from the first scalable international email test.

First paid-sale market

India — Mumbai-area local service businesses

Choose active, owner-operated businesses that lack a verified website and can benefit from a clear service-and-enquiry page. Begin with warm introductions, referrals and voluntary enquiries. India already has approved INR package prices and can be served without cross-border payment setup.

UK — verified limited-company home-service businesses

This is my proposed first international B2B email segment: cleaning, landscaping and property-maintenance companies with public business contact details, active trading signals and no verified website. Confirm corporate status using Companies House. Start only once the lawful basis, approved quotation process and compatible email provider are ready.

The image examples are illustrative categories, not specific recommended businesses.

This approach tests paid demand using the market SiteBlitz can currently fulfil most easily, while preparing a more repeatable international workflow.

Thirty-day execution plan

Period

	

Founder and system responsibilities

	

Target daily activity




Days 1–5

	

Fix website prices and broken contact details; confirm trademark/domain, terms, payment collection, deliverability and contact suppression

	

No new cold sends; verify first 100 records




Days 6–10

	

Build the first relevant India shortlist; request introductions; publish proof-of-process content; review permitted email candidates

	

5 warm introduction requests/day




Days 11–14

	

Hold discovery discussions, prepare fixed-scope quotes, begin approved email outreach only if infrastructure and permission gates pass

	

5–10 new eligible emails/day, 1–2 discovery conversations/day as capacity permits




Days 15–21

	

Continue qualification, first follow-ups, quotes and deposits; review early responses and objections

	

10–15 new eligible emails/day, up to 5 consented WhatsApp conversations/day




Days 22–30

	

Complete sales follow-ups, collect deposits, deliver accepted paid projects, review economics

	

15–20 new eligible emails/day if justified, plus scheduled follow-ups; 2 discovery slots/day

Email numbers are caps for this initial test, not quotas to fill with poor prospects. If no suitable sending provider and legal basis are confirmed, email volume remains zero.

All activity is manual or approval-controlled for now. Nothing has been authorised to send or deploy.

Why I would not force 3,000 sends into the first 30 days

The previously agreed Level-1 pilot involves 1,000 contacts and three touches, with a three-week sender ramp and a broader evaluation around week eight.

That is a different experiment from proving the first paid conversion in 30 days.

Trying to finish the entire 3,000-send test within the first month risks compromising verification, relevant content and reply handling. Keep the previously agreed eight-week evaluation horizon, subject to provider-policy approval.

Budget

From the supplied November 9 infrastructure review:

Cost

	

Previously estimated amount




Level 0: brand domain and primary business inbox, first month

	

₹1,178




Level 1: complete pilot stack including Level 0, first month

	

~₹12,239




Level 1: subsequent monthly cost

	

~₹5,260




Vercel Pro, if required for commercial hosting

	

~₹2,230/month

These are inherited budget estimates, not newly verified vendor quotations. They exclude founder labour, development, sales time, transaction fees and other costs not specified in the review.

Success criteria

Retain the earlier deliverability and conversion gates, while making them more precise.

Metric

	

Proposed decision threshold




Verification

	

At least 20% valid-email yield from the defined candidate pool




Hard bounce

	

No more than 1% of attempted messages




Gmail user-reported spam

	

Target below 0.10% when a sufficiently meaningful measurement is available




Positive replies

	

At least 3% of unique eligible contacts reached, measured by the end of their response window




Paid conversions

	

Earlier gate of at least 3 paid orders per 3,000 sends, evaluated after the full pilot




Compliance

	

No knowingly unauthorised messaging or policy-violating send method




Contribution margin

	

Target at least 30% after attributable acquisition, delivery labour and direct costs; proposed business threshold




First 30 days

	

Aim for the first genuine paid deposit and completed customer discovery, without treating a small sample as statistically conclusive

Google's sender recommendations distinguish the target of keeping spam below 0.10% from its requirement to remain below 0.30%. A missing Postmaster measurement must not be interpreted as zero complaints. 
Gmail Help

Why the existing three-order target is not enough

Using the current INR packages, three customers would generate:

3 LAUNCH ORDERS

₹23,997
Gross sales, not profit

3 BUSINESS ORDERS

₹53,997
Gross sales, not profit

If acquisition infrastructure costs approximately ₹17,499 across the first two months under the supplied estimates, three Launch orders leave only ₹6,498 before delivery labour, hosting and other expenses.

That is why "three paid orders" alone cannot justify scaling.

The pilot must also reveal delivery time, scope creep, quotation acceptance, failed-payment rates and whether the founders have enough hours to fulfil new orders.

Go / change / stop decisions

Continue: Qualified positive replies meet the 3% target over a meaningful sample, real deposits arrive, compliance is maintained, and project contribution is positive.

Change: Delivery is healthy but positive replies remain weak, or replies are positive but quotes do not convert. Revise the business segment, offer or price proposal one variable at a time.

Stop the affected channel immediately: Legal or platform-policy failure, a material suppression failure, repeated harmful complaints, or bounce rates above the agreed safety gate.

Final decision for Claude Code

I recommend a paid-first, compliance-gated, research-supported sales system, with these priorities:

Stop fabricated emails and retain contact provenance.

Make eligibility for each country and channel a hard requirement, not merely a lead-score adjustment.

Fix SiteBlitz's live website, pricing and reply channel before outreach.

Use short, genuine, context-specific email and a maximum three-touch sequence.

Route every reply into a clearly defined CRM action, quotation and payment milestone.

Make deposits mandatory before website production.

Prefer evidence-based opportunity snapshots over unsolicited synthetic voice or excessive free concepts.

Validate the first paid conversions before pursuing the previously discussed 1,000-email/day capacity.

The strongest competitive advantage is not the size of the database. It is the ability to turn reliable observations about real businesses into commercially useful proposals at a delivery cost that makes sense.

Points still open

#

	

Unresolved decision

	

Responsible party




1

	

Confirm actual code-level source of guessed emails and implement verification statuses

	

Claude Code




2

	

Audit which previously used list produced spam or bounces

	

Founder + Claude Code




3

	

Obtain jurisdiction-specific advice on data collection, India DPDP and international prospecting

	

Legal adviser




4

	

Confirm email provider terms explicitly permit the intended sending behaviour

	

Founder




5

	

Clear the SiteBlitz trademark, purchase approved domain and correct production website

	

Founder + Claude Code




6

	

Approve quote-only international pricing and a working overseas payment route

	

Founder + accountant




7

	

Decide whether to suspend the existing free-homepage-concept allowance

	

Founder




8

	

Measure real production hours and direct cost per Launch and Business website

	

Founder + Claude Code




9

	

Approve the India paid-sale segment and conditional UK corporate email segment

	

Founder




10

	

Decide whether the first 30 days will use the full paid outreach stack or only the lower-cost permission-based routes

	

Founder




11

	

Implement the actual CRM states, suppression checks, quote/deposit triggers and audit trail

	

Claude Code




12

	

Collect genuine pilot results before approving the later volume-scaling decision

	

All partners

Status: Strategy proposed and externally researched. No messages sent, tools purchased, code changed or workflows deployed.


---

## Claude Code - 2026-11-10 02:32 UTC - 02_claude.md - attachments: none

Claude Code, round 2. I checked your claims against primary sources and our own research (two research passes
today: platform/legal and copy/tactics). Verdicts per point, then the questions I need you to settle. Keep the
same point numbers.

## Facts checked
- Google Workspace AUP (last modified 2025-10-13) does ban generating or distributing large-scale unwanted email
  ("spam"): **confirmed** (workspace.google.com/terms/use_policy, read today).
- WhatsApp Business Messaging Policy 2026-09-23 requires number given by the person AND opt-in: **confirmed**.
  Extra facts: templates cannot carry audio (headers are text, image, video, GIF, document, location only); marketing
  templates are not delivered to US +1 numbers; the plain Business app bans bulk/automated messaging.
- CNIL 2026-06-10: B2B email allowed on legitimate interest when related to the recipient's profession; generic
  addresses (info@, contact@ of a company) are not subject to those principles: **confirmed** (cnil.fr page read).
- "German UWG §7 amended February 2026, stricter": **not supported**. The February 2026 UWG amendment implements the
  EmpCo directive (greenwashing, Taylor Wessing 2026-02); §7 email consent is unchanged - prior express consent
  was already required. Decision (Germany on hold) is unchanged.
- RBI FEMA (Export and Import of Goods and Services) Regulations 2026 in force from 2026-10-01: **confirmed**
  (RBI press release).
- India TRAI TCCCPR 2nd amendment (2025-02-12): first violation bars all the sender's numbers 15 days, repeat =
  1-year disconnection + blacklist; promotional calls only from 140 series. So no cold calls/SMS from a personal SIM.
- Your email drafts show "From contact@aaziko.com". That address comes from your interface, not from us; no
  template will carry it.

## Verdicts
- **C1 Workspace AUP** - agree the risk is real; **reject "explicit provider approval" as a gate** because Google
  does not issue approvals, so the gate can never pass. Proposed replacement: 1:1 personalised, lawful, <= 30 sends
  per inbox per day, complaints < 0.1 %, sending domains in a separate org from hello@, suspension risk accepted in
  writing by the founder. Question A below.
- **C2 WhatsApp** - agreed.
- **1 Hygiene** - agreed (ladder, six statuses, keep free-mail, audit 100). One change for founder time: an address
  listed on >= 5 places is excluded in the pilot, not investigated. Catch-all = RISKY, not sent in the pilot.
  Nothing in the 86.75 M source folder is deleted; the outreach table is lean and guessed emails are removed at the
  code source (`enrichment/discovery.py`, `lead_radar_service.py`, `export_surat_leads.py`).
- **2 Routing** - agreed except India (question B) and phone-only (question C).
- **3 Copy** - agreed on structure, truthfulness, opt-out, no Re: on touch 1. Two changes: (a) <= 100 words, because
  the largest dataset we found (Hunter, 34 M emails, vendor) shows length barely moves replies (3.4-4.5 % across
  buckets, best 20-39 words) and the founder must review each one; (b) open with the observation itself, not "I came
  across" (no study proves it hurts, but it is the most templated opener in the inbox).
- **4 Lifecycle** - agreed in full: Day 1 / 6 / 14, close Day 21; reply branches; requirements in two stages;
  deposit after written scope and before any work; balance after staging approval and before launch and handover.
  Additions: an out-of-office auto-reply pauses the sequence until the return date; "please call me" = permission
  to call, logged.
- **5 Countries/language** - agreed: language evidence hierarchy (our data has no post text, so the founder confirms
  language on their social page during the review), native review of the first 10-20 messages per language, quote-
  only pricing (option C) abroad. Our code gap: `country_rules.py` has no rows for NL, ES, ZA, AE, IN and lacks the
  Singapore `<ADV>` subject rule; until added those countries are on hold.
- **6 Hook** - agreed: no AI-cloned voice in cold outreach; real voice / screen video only after engagement;
  Opportunity Snapshot is good. Question D on the free concept.
- **7 Pilot** - agreed on separating first revenue from the scale test and on the economics (3 Launch orders =
  Rs 23,997 vs ~Rs 17,499 infra over 2 months). Question E.

## Questions for you
A. Is there a sending setup whose own terms explicitly allow lawful, low-volume B2B first-touch email (dedicated
   cold-email mailbox providers, Zoho, Microsoft 365, Instantly's own infrastructure)? Name it with the clause and
   URL, or say none exists and the AUP risk must simply be accepted at low volume.
B. India. You put India on "referrals and inbound only". The founder has zero clients, so there are no referrals,
   and "5 warm introduction requests a day" has no named source - from whom? Our research: India has no anti-spam
   statute for email; DPDP core duties start ~2027-05-13; s.3(c)(ii) public-data exclusion is contested. Proposal:
   India B2B email to the business's own published address, <= 20/day in month 1, sender identity, postal address,
   one-line opt-out, provenance URL stored, permanent suppression - lawful today, with the DPDP review still open.
   Agree, or name the specific Indian rule it breaks.
C. Phone-only and no-contact businesses in India (1.82 M phone-only, 1.08 M social-only). Proposal: (1) look for an
   email on their own website/social page; (2) Mumbai walk-ins; (3) **a posted card or letter** with a printed
   Opportunity Snapshot and a QR code opening WhatsApp click-to-chat with a pre-filled message ("Hi SiteBlitz, please
   show me the website idea for <business>") - the owner messages first, so WhatsApp opt-in and the 24-hour window
   exist and a real founder voice note becomes allowed. Is physical mail to a business address lawful and sensible
   in India? Realistic cost per piece (print + India Post) and response rate? This is also our candidate for the
   "these people found a new way" effect. Judge it.
D. The free concept. The founder said: no more free work. But with zero clients and zero proof, a visual preview is
   the strongest lever, and "Review before you pay" was already agreed on 2026-11-01. Proposal: replace the 3-hour
   bespoke concept with a **15-20 minute templated preview** (their name, category, city and approved photos placed in
   one of our three existing industry demos: salon & beauty, coaching & tuition, retail & showroom), only after a
   positive reply AND the three qualifying answers (decision-maker, accepts the Rs 7,999-17,999 range, launch within
   60 days); cap 5 per week. Snapshot for every positive reply, preview only for qualified ones. Agree / disagree.
E. Pilot volume. Your caps (5-20 emails/day) give ~250-300 first touches in 30 days -> at 3 % ~8 positive replies.
   Is that enough to reach a first deposit, or should month 1 run the full 3-week warm-up on the level-1 domains
   while India email starts at 20/day and the card test runs at 100 cards? Give the exact daily plan for the founder
   (hours per day) and the stop rules.

Answer each point by number: agree / disagree because ... / need data: ... . End with the list of points still open.


---

## ChatGPT (Extra High) - 2026-11-10 02:44 UTC - saved as 02_chatgpt.md

ChatGPT said:
SiteBlitz — Round 2: Decisions for Claude Code

10 November 2026 · Seven agenda points · Questions A–E

Overall verdict: Agree with the direction. Four of the five proposed changes are acceptable, with operating safeguards. Question A has a useful new finding: a more suitable sending-infrastructure option exists.

My decisions are:

Question

	

Decision




A. Cold-email provider

	

Partially agree. Instantly's native infrastructure expressly supports direct B2B sales/marketing, but not an unrestricted right to send unsolicited emails.




B. India B2B cold email

	

Agree conditionally. I found no general Indian statutory prohibition on the narrowly described email pilot. The provider's rules and other applicable laws still matter.




C. Physical mail + WhatsApp QR

	

Agree. This is worth a 100-piece experiment.




D. 15–20-minute preview

	

Agree. Three qualification gates and five per week are sensible.




E. Parallel 30-day pilot

	

Agree with changes. Warm-up, eligible India email and printed cards can run together, but not from newly purchased domains before they meet the sender's rules.

Legal conclusions below are research findings for counsel to review, not a legal opinion. Costs and conversion assumptions are identified separately from established facts.

1. Data hygiene and fake emails

Verdict: Agree with Claude Code's proposed changes. No additional debate required.

Exclude addresses shared by five or more places from the pilot rather than spending founder time investigating them. Keep catch-all addresses as RISKY and exclude them from sending. Remove guessed-email generation at the three identified code locations and preserve the original 86.75 million-record source database.

One safeguard: exclude does not mean invalidate. An address shared across several branches may be genuine. Its exclusion is a pilot-efficiency decision, not a verified finding that the address is fake.

The resulting rule is:

Eligible email = verified business + real sourced address + acceptable verification result + no suppression + country/channel permission.

For the initial sample, use a 100-record manual audit. Record how many fail because of wrong business, outdated contact, guessed address, invalid email, shared-address threshold or legal/channel restrictions.

Who benefits: Founder, engineering and deliverability. Cost: existing verification budget plus engineering time. Test: audit agreement of at least 95 out of 100 manually reviewed eligibility classifications, with any incorrectly approved guessed address treated as a blocking defect. The 95% threshold is a proposed internal quality gate.

No new feature is needed until these classifications work reliably.

2. Channel routing — Questions A, B and C
A. Is there a provider that permits B2B first-touch marketing?

Verdict: Partially agree with replacing my earlier provider-approval gate.

Claude Code is correct that demanding individual written preapproval from Google is impractical. But I disagree that accepting suspension risk makes any use compliant with the provider's terms.

A significant new finding is in Instantly's current contract.

Instantly — native sending infrastructure

Conditional fit

Terms of Service, updated 4 November 2026

Section 1.10 defines the permitted purpose to include the customer's own direct B2B sales, marketing, recruiting and business-development activities.

Section 4.6 addresses Instantly-operated sending infrastructure, including its done-for-you accounts. The platform describes native AirMail accounts as infrastructure for cold outreach.

Official Terms of Service · Official Sending Policy · Sending-account documentation

Source confidence: high for the contractual wording; medium for interpreting its suitability for a specific first-touch campaign. 
instantly.ai
+2

This is an explicit contractual purpose covering direct B2B marketing, not an express statement that every non-opt-in cold email is permitted. Instantly separately requires compliance with applicable law and its own anti-spam policy, and reserves suspension rights.

The critical comparison:

Provider

	

Verified policy position

	

Decision




Google Workspace

	

Prohibits unsolicited mass email

	

Use primary inbox for clients and replies; do not assume 30/day is a safe harbour




Zoho Mail

	

October 13, 2026 usage policy explicitly excludes promotional and marketing emails

	

Reject for this campaign




Microsoft 365

	

Online Services AUP prohibits spam; Exchange Online is not designed for bulk marketing

	

Not an affirmative cold-outreach solution




Instantly + connected Workspace inboxes

	

Instantly permits B2B campaigns, but the underlying Workspace terms still apply

	

Underlying risk remains




Instantly-native AirMail / eligible native infrastructure

	

Purpose-built for direct B2B outreach, subject to law and Instantly's policy

	

Preferred option to investigate

Sources: Google Workspace AUP (2025-10-13), Zoho Mail policy (2026-10-13), and Microsoft Online Services AUP (checked 2026-11-10). High confidence in the stated restrictions. 
Google Workspace
+2

New technical constraint: domain age

Instantly's October 13, 2026 Sending Policy says sending domains should be at least one month old. It also requires accurate sender identification and a clear opt-out in each campaign. 
instantly.ai

That matters:

New domains purchased on November 10 should not be assumed eligible for cold sending on November 17.

Warm-up alone does not eliminate the domain-age requirement.

Instantly offers pre-warmed accounts, but the actual domain age and account status still need checking.

Instantly-provisioned infrastructure may remain owned and controlled by Instantly; there is a portability trade-off. 
Instantly Help Center

My final A decision: Replace "obtain provider approval" with "select a provider/product whose published terms cover the intended activity; verify the actual underlying sending infrastructure; comply with its policy; accept documented residual suspension risk."

Choose native infrastructure over purchasing extra Google Workspace inboxes solely for cold first touches. Recalculate the previously approved ₹12,239 pilot budget before switching: I have not verified a comparable current AirMail quote.

Thirty messages per inbox per day remains an internal risk limit, not a provider guarantee or legal permission.

B. Can India B2B email begin now?

Verdict: Agree conditionally with the proposed 20-new-contact/day ceiling. I would not limit India to referrals and inbound enquiries.

Claude Code's challenge is valid: a startup with no customers cannot rely on an unspecified network of five warm introductions every day.

I checked India's position more closely.

Linklaters' India data-protection guide and CMS's India privacy-law guide identify no standalone comprehensive Indian law generally prohibiting direct marketing by email. That does not remove the relevance of other privacy, consumer-protection or provider requirements. 
linklaters.com
+1

The government's November 13, 2025 commencement notification schedules the main DPDP data-processing duties, including Sections 3–5, for May 13, 2027. The Act's other provisions have different commencement dates. 
MeitY

I therefore cannot name a specific current Indian statute that categorically prohibits a carefully targeted, individual B2B sales email to an official company-published role address under all circumstances.

I also cannot certify every address in the dataset as lawful for marketing. A contact copied from a third-party listing is not necessarily published by the business itself, and a named employee's address can involve personal data. The future Section 3(c)(ii) public-data exception should not be treated as blanket consent.

Approved-for-design pilot criteria

Control

	

Decision




Recipient source

	

Official business website or otherwise independently confirmed business-owned contact




Priority

	

info@, contact@, or another genuine relevant company role address




Named employee

	

Manual review; do not automatically treat business employment as consent




Daily volume

	

Up to 20 new contacts/day, conditional on provider and eligibility gates




Identification

	

Actual founder name, SiteBlitz, working reply address, genuine postal address




Content

	

Relevant, truthful, 100 words or fewer




Opt-out

	

Clear reply-based opt-out; immediate suppression




Compliance record

	

Source URL, review date, recipient class, applicable country rule and send history




Recontact

	

Maximum three touches unless the person engages; objections stop marketing

This permits a more commercially realistic experiment without pretending the upcoming privacy requirements do not matter.

Cost: Human qualification, verification and suitable email infrastructure. Benefit: A revenue opportunity independent of the founder's personal contacts. Test: deliverability and paid deposits by contact-source category.

Important distinction: the India email route remains a manually reviewed pilot until the code's India rule is implemented and legal review is completed. It is not permission to activate the default worldwide sender.

C. Physical mail with a personalised WhatsApp QR code

Verdict: Agree. This is the strongest new proposal in Round 2 for phone-only and no-contact India leads.

India Post explicitly offers direct advertising and direct mail to businesses. Its official service description covers printed sales messages intended to generate responses. This makes ordinary addressed commercial post a credible channel, provided the material complies with postal restrictions and general law. 
India Post

There is one important operational distinction: India Post's Direct Post service is for unaddressed mail and requires at least 1,000 pieces. It is not the correct product for 100 individually addressed SiteBlitz letters. 
India Post

For the first 100 businesses, use ordinary addressed letters or appropriately classified printed postcards.

Realistic cost per piece in India

Item

	

Published postage or estimated cost




Ordinary letter up to 20 g

	

₹5 postage




Each additional 20 g or part thereof

	

₹5 additional postage




Commercial printed postcard

	

₹6 listed in India Post's published postal compilation; confirm current classification at counter




One-page colour print

	

₹5–₹12 estimated




Envelope and addressing supplies

	

₹2–₹4 estimated




Personalised preparation labour

	

Approximately 4–8 minutes per business

India Post's domestic tariff confirms ordinary letter postage. Its published administrative compilation lists printed postcards at ₹6, although the current general postcard tariff page does not clearly separate that commercial category. Postal confirmation is advisable before printing all 100.

100 LETTERS — CASH COST

₹1,200–₹2,100
Planning range; excludes founder time and one-time design

RESEARCH + PREPARATION

7–14 hrs
Estimated labour for 100 businesses, including address checking

If all 100 are produced at a cash cost of ₹15 each, the test costs ₹1,500. Add a value for founder labour when calculating actual acquisition cost.

These are estimates, not supplier quotations.

Will the QR establish WhatsApp opt-in?

Yes for responding to a specific owner-initiated request; no for unrestricted future marketing.

Meta explicitly recommends using customer mailings and QR codes to let customers initiate WhatsApp conversations. Its Business Platform policy then permits ordinary replies within a 24-hour service window. 
WhatsApp for Business
+1

The correct sequence is:

SiteBlitz posts a genuine business proposal to a verified business address.

The owner scans the QR, reviews the prefilled text and actively presses Send.

SiteBlitz records that the business initiated contact and responds to the requested website idea.

A real founder-recorded voice note can be sent as part of that requested conversation if useful.

Any unrelated or later business-initiated marketing requires a separate valid opt-in and the appropriate WhatsApp messaging mechanism.

The 24-hour template rule specifically applies to the Business Platform. It should not be confused with a general right to message someone indefinitely through the Business App.

My suggested QR text
Writing

Hello SiteBlitz, I received your website idea for [Business Name].

Please show me the suggested design and price. You may reply here on WhatsApp about this request.

The QR must be generated using the actual SiteBlitz WhatsApp number. The owner must initiate the message themselves; simply scanning a QR or opening a prefilled chat is not sufficient.

Expected response rate

I did not verify a reliable independent India-specific response rate for this exact kind of personalised B2B postal campaign. I would not import direct-mail industry averages from a different country and present them as a forecast.

Instead, use scenarios:

Responses from 100

	

Observed response rate

	

Meaning




0

	

0%

	

Possible channel or offer mismatch; investigate delivery and message




1

	

1%

	

One conversation; insufficient to prove viability




3

	

3%

	

Encouraging for a small experiment




5

	

5%

	

Strong early signal, still needing replication

At ₹1,500 cash cost, one genuine enquiry means ₹1,500 cash cost per enquiry, whereas three mean ₹500 each, before labour.

C decision: Approve a controlled 100-piece test, but only for one defined business category initially. The personalised Opportunity Snapshot and owner-initiated WhatsApp conversation are the real differentiators—not the QR technology itself.

3. Cold email copy — revised human-first approach

Verdict: Agree with both changes.

The Hunter dataset is useful directional evidence, but the reported reply-rate differences should not be interpreted as proof that 20–39 words is optimal for SiteBlitz. A message needs enough information to establish credibility, particularly when the business has never heard of the sender.

I approve a 100-word maximum including the signature and opt-out, with a working target of 60–85 words.

Opening with a verified observation is stronger than repeatedly using "I came across your business."

Revised Touch 1 — India
A website idea for [Business Name]
Send
From
contact@aaziko.com
Recipients

Hello [Name],

Your [verified public page] shows [specific service], but I couldn't find a website linked there.

I'm [Your Name] from SiteBlitz. We build simple websites that put services, location and contact details in one place. Our India packages start at ₹7,999, excluding domain and hosting.

Would you like a short outline for [Business Name]?

Regards,
[Your Name] | SiteBlitz
[Reply email] | [Business postal address]

If not relevant, reply "stop" and I won't contact you again.

This message only works when the website observation is true. Do not substitute fabricated compliments when the observation is unavailable.

Revised Touch 2 — Day 6
Re: A website idea for [Business Name]
Send
From
contact@aaziko.com
Recipients

Hello [Name],

One thought on [Business Name]: a simple website could help customers find [verified service], business hours and the right contact number without searching through several posts.

Would you like me to send a suggested page structure and fixed quotation?

Thanks,
[Your Name]
SiteBlitz
[Reply email] | [Business postal address]

Reply "stop" if you'd prefer no further emails.

Revised Touch 3 — Day 14
Re: A website idea for [Business Name]
Send
From
contact@aaziko.com
Recipients

Hello [Name],

I'll close this enquiry after this message.

If a website becomes useful for [Business Name] in the future, you're welcome to contact us. I'd be happy to explain the options and pricing.

Thank you for your time.

Regards,
[Your Name]
SiteBlitz
[Reply email] | [Business postal address]

No further follow-ups are planned. You can reply "stop" at any time.

For the follow-ups, use Re: only when the message is genuinely being sent in the original thread.

Copy decision for Claude Code: Keep these as three distinct templates. Require observation_source_url, verified_observation and a human approval flag before Touch 1 becomes eligible for sending. Do not let the AI invent observations when those fields are empty.

Cost: approximately 3–5 minutes of combined investigation and approval per prospect after the tooling is usable. Benefit: relevance without fabricated familiarity. Test: positive replies, objections, and paid conversions by copy variant.

4. Complete lead-to-payment lifecycle

Verdict: Agree with Claude Code's additions. No change to the payment milestones.

The Day 1 / 6 / 14 schedule and Day 21 closure remain the default for nonresponders.

I approve these additional state transitions:

Event

	

CRM state

	

Next action




Out-of-office with return date

	

PAUSED_OOO

	

Resume with the next unsent touch two business days after the stated return date




Out-of-office without return date

	

PAUSED_OOO_UNKNOWN

	

Hold 14 calendar days, then review; close if no clear return or engagement




"Please call me"

	

CALL_REQUESTED

	

Record number and time preference; allow a call about the stated enquiry




Genuine interest

	

QUALIFYING

	

Pause every outbound sequence and collect initial requirements




Three preview conditions met

	

PREVIEW_ELIGIBLE

	

Allow one capped preview




Written quotation accepted

	

AWAITING_DEPOSIT

	

Send deposit invoice




Deposit received, requirements incomplete

	

DEPOSIT_PAID_NOT_READY

	

Collect content/access; do not start delivery clock




Scope, content, access and deposit complete

	

READY_TO_BUILD

	

Confirm agreed start date




Staging and agreed revision approved

	

AWAITING_BALANCE

	

Invoice balance before public launch




Final payment received

	

PAID_READY_TO_LAUNCH

	

Publish and hand over

The requested phone call creates permission for the requested conversation, not an unrestricted subscription to future marketing calls or WhatsApp promotions.

Payment remains fixed

Package

	

After written scope acceptance

	

After staging approval, before launch




Launch

	

₹4,000

	

₹3,999




Business

	

₹9,000

	

₹8,999




Custom

	

As individually quoted

	

As individually quoted

One important distinction: the preview in Point 6 is a sales demonstration, not the beginning of the contracted website build. The two-day/seven-working-day delivery commitment only starts once all ready-to-build conditions are satisfied.

Implementation requirement: Every state needs an event log, owner, next action and, where applicable, due date. Payment status must come from a verified payment or bank reconciliation—not from an email being sent or an invoice being marked issued.

Success test: No project enters BUILDING without the deposit, and no project enters LAUNCHED without the agreed balance or a documented founder-approved contractual exception.

5. Countries, language and international pricing

Verdict: Agree. I also accept the correction on Germany.

My previous statement connecting the February 2026 UWG amendment to a new, stricter Section 7 email-consent rule was incorrect. I retract it. Germany remains on hold because of its existing consent rules, not because of a newly introduced February restriction.

I agree that the country-language hierarchy should remain evidence-based. Since the dataset does not include social-post text, the founder must verify the actual communication language before approving translated first-touch copy.

Country-code changes

Country

	

Current decision

	

Required implementation




IN

	

Manually reviewed India email pilot only

	

Implement country-specific eligibility, provenance and privacy review




NL

	

Hold

	

Confirm Dutch electronic-marketing requirements




ES

	

Hold

	

Confirm Spanish electronic-marketing requirements




ZA

	

Hold

	

Confirm POPIA and electronic direct-marketing requirements




AE

	

Hold

	

Confirm UAE marketing and privacy requirements




SG

	

Hold

	

Implement Spam Control Act rules, including the advertisement-label requirement when applicable




DE

	

Hold

	

Maintain existing strict prior-consent controls

Singapore's current Spam Control Act requires the <escape><ADV></escape> advertisement prefix for covered unsolicited bulk commercial email and establishes specific bulk thresholds. The source is the Spam Control Act 2007 and Second Schedule (current legislation checked 10 November 2026; high confidence). 
Singapore Statutes Online
+1

Do not automatically apply a default "opt-out" classification to every unrecognised country. Unknown country rules should return HOLD_LEGAL_REVIEW.

I also agree with quote-only international pricing. India remains on its approved package amounts, while overseas prospects receive a reviewed scope and quotation. The founder should not publish arbitrary converted prices or promise a payment processor that has not been configured.

Success test: Zero automatically sent messages from an unknown, held or unreviewed country rule.

6. Unique hook — Question D: the 20-minute preview

Verdict: Agree with the exact proposal, subject to one wording change.

Replace the three-hour free bespoke homepage concept with a capped 15–20-minute illustrative preview.

I distinguish working for free on a client project from spending a controlled amount of time demonstrating a product before a sale. The latter is ordinary sales acquisition cost.

The qualification gate

Preview eligibility

0/3 confirmed

The respondent is the decision-maker or has explicit authority to commission the website
They acknowledge the ₹7,999–₹17,999 India package range and understand exclusions
They intend to launch within approximately 60 days

Send the standard Opportunity Snapshot, but do not start a custom preview yet.

Approved preview workflow

Use the three existing industry demos: salon and beauty, coaching and tuition, and retail and showroom.

Personalise only the business name, category, location, approved images, real service descriptions and appropriate contact method. Do not create new architecture, animations, integrations or special features for this free demonstration.

The preview should display "Illustrative concept — not a completed customer website." Use customer photographs only with suitable permission.

At most five previews per week, each capped at 20 minutes. That is:

MAXIMUM PREVIEW LABOUR

100 min/week

MAXIMUM IN 4 WEEKS

20 previews

The commercial rule is simple: one preview, one opportunity to discuss it, then a written quote and deposit request. Further design changes belong in the paid project.

The founder's already agreed "review before you pay" promise should refer to reviewing this illustrative preview and the proposed scope. It must not imply that SiteBlitz will complete a usable website before payment.

Success test: Track preview-to-deposit conversion separately from Snapshot-to-deposit conversion. If five qualified previews produce no further progress, diagnose why before creating another five. A sample of five is not enough for a statistical conclusion, but it is enough to expose common objections or a weak sales explanation.

7. Thirty-day pilot — Question E

Verdict: Agree with running the three workstreams in parallel, but revise the sequencing and volume logic.

The first deposit is a legitimate 30-day objective. It is not a guaranteed outcome from 250–300 cold first touches.

At a hypothetical 3% positive-reply rate:

ILLUSTRATIVE FUNNEL — NOT ACTUAL SITEBLITZ PERFORMANCE

275
First touches
8.3
Positive replies at 3%
4.1
Quotes if half progress
1.0
Expected deposits if 25% accept
Assumptions are illustrative. The 3% positive-reply rate, 50% quote progression and 25% quote-to-deposit rate are not yet measured SiteBlitz results.

This is enough to justify a careful attempt at the first paid order, but not enough to validate a scalable acquisition business.

The three concurrent workstreams

Workstream 1 — Sending infrastructure: Begin setup and warm-up immediately. Keep the permanent client-reply mailbox separate. Do not use newly bought sending domains prematurely. Prefer an eligible native sending product over extra Workspace mailboxes bought only for cold outreach.

Workstream 2 — India email: Begin only once there is a compliant and operational sending account. If a suitable provider supplies an account with a genuinely aged, ready-to-send domain, the schedule below can start in week two. Otherwise, email first touches remain at zero until eligible.

Workstream 3 — Physical mail: Print and post 100 individually addressed letters to one India business category, divided into batches. This can proceed without waiting for email-domain maturity.

Exact first-30-day schedule

November 10 to December 9, 2026 · Weekdays only for planned outreach

Dates

	

New eligible email prospects

	

Posted cards/letters

	

Main work




Nov 10–13

	

0

	

0

	

Repair website and contact details, audit contacts, create card and QR design, configure infrastructure




Nov 16

	

0

	

Included in week's first batch

	

Final compliance and sending-account eligibility check




Nov 17–20

	

10/day × 4 = 40

	

25 across Nov 16–20

	

First eligible email test, replies and discovery




Nov 23–27

	

15/day × 5 = 75

	

25

	

Continue first touches, scheduled follow-ups and quotes




Nov 30–Dec 4

	

20/day × 5 = 100

	

25

	

Continue outreach, previews and deposit collection




Dec 7–9

	

20/day × 3 = 60

	

25

	

Final first-touch batch and preliminary pilot review




Total

	

275 first touches

	

100 letters

	

Subject to eligibility and operational capacity

The email figures are conditional maximums. If there is no eligible sending infrastructure, the corresponding email total is zero—not a reason to send from a prohibited or unready account.

Also, 20 new first touches per day does not mean 20 total outgoing messages. On mature campaign days, first touches plus scheduled follow-ups could approach 60 messages across the sending accounts. The 30/day-per-inbox proposed ceiling must include every touch.

Any follow-up falling on a weekend moves to the next working day. A reply, opt-out or OOO pause removes or reschedules all remaining touches.

Exact daily founder schedule

Standard working-day allocation

5 hr 30 min

09:00–09:30

Check replies, bounces, opt-outs and suppression

30 min

09:30–11:00

Qualify 15–20 leads and verify their observations

90 min

11:00–12:00

Review and send eligible emails; queue due follow-ups

60 min

12:00–12:30

Prepare, address and log physical letters

30 min

14:00–14:45

Respond to enquiries and hold discovery calls

45 min

14:45–15:30

Prepare quotations, previews and payment requests

45 min

15:30–16:00

Update CRM, measure metrics and set next actions

30 min

This is founder sales time, not the full business workload. It excludes initial engineering fixes and the hours needed to build paid websites. If a customer pays, fulfilling that promise takes priority over sending new first touches.

For a 1–2-person operation, that is essential. Otherwise the team can create more work than it can deliver.

Explicit stop rules

Signal

	

Decision




Unresolved platform or legal incompatibility

	

Stop the affected channel immediately




A guessed address enters the send queue

	

Stop that pipeline, fix the cause, re-audit




Two hard bounces among the first 50 attempts

	

Pause and investigate the list




Hard bounce exceeds 1% after at least 100 sends

	

Pause sending and verify the source




Any confirmed spam complaint

	

Pause affected sending account/campaign, investigate; do not wait for an arbitrary quota




No positive replies after 150 eligible first touches

	

Review targeting, observation quality and copy before increasing volume




Zero replies from 100 letters after an adequate delivery/response window

	

Do not automatically print another batch; inspect targeting and delivery first




Five qualified previews and no sales progress

	

Review the qualification gate and proposition




Two active paid projects exceed delivery capacity

	

Reduce or pause new outreach




Positive replies but no deposits after completed quote discussions

	

Investigate trust, price, payment process and scope—not sending volume

These thresholds are operating decisions, not statistical proof. The absolute bounce and complaint thresholds should also respect any stricter provider rule.

When to judge the pilot

December 9 is the end of the 30-day acquisition window, not the date when every sequence is complete.

A prospect first contacted on December 9 could receive Touch 2 on December 14 and Touch 3 around December 22, subject to working-day scheduling. Their no-reply closure would occur around December 29.

Likewise, physical letters posted in the final batch need time for delivery and response.

Therefore, use December 9 for the preliminary decision about list quality, founder workload, replies, quotes and any deposits already received. Evaluate completed sequence conversions at the end of December. Retain the separate, approximately eight-week gate for the originally agreed 1,000-contact/3,000-send infrastructure experiment.

My final pilot recommendation

I would not purchase six additional Google Workspace cold-outreach mailboxes and treat the risk as solved.

Instead, prepare the brand and lead systems, confirm the current cost and eligibility of a purpose-built native sending option, conduct the 100-letter test, and start India email as soon as a genuinely eligible infrastructure path is available.

If the founder chooses to fund both new-domain warm-up and a separate pre-warmed sending product, document the incremental costs and infrastructure ownership trade-off first. With zero paying customers, there is no economic justification for paying for overlapping systems without a deliberate test.

Final Round 2 decisions

Point

	

Result




1. Data hygiene

	

Agreed — implement at source, exclude suspect categories from pilot




2. Channel routing

	

Agreed conditionally — India B2B email and addressed postal test; WhatsApp only after valid user initiation/permission




3. Content

	

Agreed — 100 words max, verified observation first




4. Lifecycle

	

Agreed — OOO and call-request states added, payment gates unchanged




5. Countries

	

Agreed — Germany correction accepted; unknown countries held




6. Unique hook

	

Agreed — qualified 20-minute illustrative preview, five/week




7. Pilot

	

Agreed with revised sequencing — 275 conditional first touches and 100 postal letters across 30 days

Points still open

Founder: Select and confirm the actual sending product, including current costs, sending-domain age and account ownership.

Claude Code: Implement the hygiene changes, suppression logic and audit trail at the three identified code locations.

Legal adviser: Confirm the India B2B email procedure and the DPDP transition plan before automated expansion.

Founder: Obtain a local India Post classification and final price for the proposed personalised printed mailpiece.

Founder: Approve one business category and one geographic area for the first 100 physical letters.

Claude Code: Implement channel-specific consent, OOO, call-request, preview eligibility and payment states.

Founder: Confirm the three existing industry demos are suitable for short previews and that images used are authorised.

Claude Code: Complete country rules for IN, NL, ES, ZA, AE and SG before enabling automatic country routing.

Founder: Approve any incremental spending that departs from the November 9 infrastructure budget.

All partners: Review real deposit conversion and project delivery economics before considering the 1,000-email/day target.

Final principle: SiteBlitz should prove that it can repeatedly obtain paid deposits from verified, relevant businesses before investing in the machinery to reach thousands more. The next competitive advantage to build is not another sending account. It is a trustworthy, measurable path from a specific business observation to a signed scope and a paid deposit.
