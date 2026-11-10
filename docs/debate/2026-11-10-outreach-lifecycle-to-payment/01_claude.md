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
