

---

## Claude Code - 2026-11-12 03:39 UTC - 01_claude.md - attachments: none

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
<file path="docs/debate/2026-11-12-email-engine-personas/claude-position.md">
# Claude Code's position (written before ChatGPT replies) - 2026-11-12, second topic of the day

## The founders' request (translated from Roman Hindi, their words)
"The agency idea is very good, I appreciate it, but focus mainly on this: you said you cannot send email yourself.
What if, from the total data we extracted - the whole world, 248 countries - we mail X people or clients every day,
and those X mails go out from the admin panel itself in a single click. Whatever SMTP setup is needed, we will do.
The main point is the content: what a mail needs so it does not go to spam, and so that when the client or their
assistant reads it, it feels worth it and they understand immediately what is in it. Think of creative ways - for
example an audio message that reads the mail, or a summary of what the mail says - it should feel unique and
interactive so that people read it at least once; its UI should be like that. I guarantee nothing; you and ChatGPT
analyse everything. Analyse how any person thinks after receiving a mail, test with multiple different personas.
Then set up the mailing system (WhatsApp later - for now only email). My main motive: I open my laptop and say
'start today's day'. You check what happened at the end of yesterday; if I give you email access you read the mail,
tell yourself and ChatGPT how many replied, whether they are interested, and what to reply - complete flows.
In short: you and ChatGPT together handle clients and conversations, and my friend and I focus on delivering
effective sites. If you cannot send mail daily yourself, add scheduling through the admin panel."

## What already exists (verified in the repos)
- World data: 86,751,626 Overture places in 249 country folders. With an email: 30.97 M worldwide; India 1.74 M,
  of which 79 % free-mail (gmail etc.). Reachability buckets: email + phone 33.4 %, phone only 48.4 %, social only
  11.6 %. Emails are as published by the business or its listing source - unverified.
- Lead generator (Python/FastAPI, 338 tests passing today): discovery, website-need engine (verdicts, observations
  SITE_DOWN / BROKEN_FORM / NO_VIEWPORT / SOCIAL_ONLY / AGGREGATOR_ONLY / NO_SITE / NO_HTTPS), polite email finder
  (499 of 2,162 Surat/Navsari sites gave an email with a source URL), and an AI writer (Claude Sonnet 5.5, validator:
  language, facts guard, length, banned phrases; 27/30 READY in a dry run). Country rules coded for US, UK, EU, CA, AU.
- Approved spec (2026-11-10, attached): AI writes every message, no human edits; max 100 new first contacts a day;
  email 10 / 15 / 20 a day in weeks 1-3, max 30 per inbox per day incl. follow-ups; Day 1 / 6 / 14, close Day 21;
  Tue-Thu 9:00-11:30 and 14:00-16:30 recipient time; India pilot only until other countries are marked PILOT;
  no synthetic voice notes; phase 15 = batch screen with one-click Write + Send into a sending provider's queue.
  Not built yet: phase 15, reply handling, scheduler, sending infrastructure, email verification ladder.
- Earlier agreed facts (2026-11-09 / 11-10 reviews): Google Workspace and Gmail are not a cold-email safe harbour
  (their policies ban unsolicited commercial mail); bulk ESPs (SendGrid, Brevo, SES) ban non-consented first touches;
  Instantly's terms allow direct B2B outreach and it requires sending domains at least 1 month old; staged plan
  level 1 = 2 domains x 3 inboxes; gates before scaling: hard bounce <= 1 %, spam complaints < 0.1 %, positive
  replies >= 3 %. No cold WhatsApp, no cold calls/SMS from a personal SIM in India (TRAI).
- Not ready: no sending domain bought; sender name / reply address / postal address blank; the live website
  (siteblitz.vercel.app, production build of 2026-07-10) shows 5 invented named testimonials, 4 invented results,
  "Studio Mumbai" and withdrawn prices - anyone who clicks through from an email sees it. The truthful version is on
  an undeployed branch.

## My view per agenda point
1. **Personas (hypotheses to test, not facts):**
   - P1 Salon / beauty owner, Surat, no website, Instagram-run, reads Gmail on a phone between clients; Hindi /
     Gujarati / English mixed; deletes anything that looks like a template or asks for a call.
   - P2 Coaching-class owner, India, website exists but not mobile-friendly; worried about admissions season; the
     address is often an admin/receptionist who forwards only if the subject names the business and a concrete issue.
   - P3 Retail showroom, India, listed website is down (domain lapsed); owner may not know; strongest hook, but may
     feel "caught out".
   - P4 Clinic / dentist practice manager, US; screens vendor mail for the dentist; deletes anything without a
     specific, verifiable reason; CAN-SPAM-aware; wants a link to check before replying.
   - P5 Restaurant, generic info@ read by staff; message must survive being forwarded with no context.
   - P6 Small trades business, UK / Australia, owner on site all day, reads at night on a phone; hates "marketing".
   - P7 Owner who already has a working website - should not be emailed at all (no observation = no message).
   - P8 Digital agency owner (B2B, the earlier route) - reads vendor pitches daily, values specificity and terms.
   - P9 The "assistant" reader (EA, receptionist, family member managing the inbox) - decides in seconds whether to
     forward; needs a one-line summary that can be forwarded as is.
   - P10 Spam filter / mailbox provider as a "persona": judges sender reputation, authentication, engagement,
     complaints, links, HTML weight - before any human sees the mail.
2. **Anatomy:** plain text, under 100 words, no image, no attachment, no tracking pixel; at most one plain link and
   only from touch 2 (touch 1 has none, per the approved spec); subject = business name + the concrete issue;
   first line = the verified observation; a one-sentence "in short" so an assistant can forward it; price once; one
   question; real sender name; postal address; one-line opt-out; List-Unsubscribe + one-click header (RFC 8058) even
   below bulk thresholds. Authentication SPF/DKIM/DMARC on every sending domain.
3. **Creative layer:** an audio attachment or AI voice in touch 1 hurts deliverability and needs synthetic-voice
   disclosure (EU AI Act Art. 50 from 2026-08-02; India IT Rules 2026 labels). My proposal instead: a personalised
   **Opportunity Snapshot page** per business (siteblitz domain, /s/<random-id>): their name, the observation with
   evidence (e.g. a phone screenshot of their own site), a clearly labelled concept preview built from a demo
   template + their public business facts (no copied photos), a 30-60 s audio summary (the founder's real recorded
   voice per vertical/language, or a labelled AI voice), the price, and two buttons: "Reply yes" (mailto) and
   WhatsApp (they start the chat = opt-in). Linked once, in touch 2. Page visits are first-party evidence of interest
   - an honest "they looked" metric without email pixels.
4. **Worldwide:** not all 248 at once. Tier A now: India (English), US. Tier B after review: UK Ltd/LLP (checked on
   Companies House), Canada (published + role-relevant), Australia (conspicuous publication evidence), France
   (profession-related). Hold: DE, AT, NL, ES, GR, ZA, AE, SG, and every country without a coded rule. X = inboxes x
   per-inbox cap: start 10/day, ramp to 100/day only through the gates; only addresses that pass verification
   (syntax, MX, verifier VALID; catch-all = RISKY, not sent) and only leads with a verified observation.
5. **Sending:** the app owns the queue and the scheduler; it hands each mail to a sending service whose terms allow
   B2B outreach (Instantly or similar), or SMTP on dedicated outreach domains of such a service. Not the founders'
   Gmail, not Google Workspace, not SES/SendGrid. Runs on the laptop with Windows Task Scheduler at boot first; a
   small server later. GitHub Actions does not fit (the database is local SQLite). Bounces and opt-outs suppress the
   address on every channel at once; automatic pause on the stop rules.
6. **Daily loop:** a "start the day" command in Claude Code: (1) yesterday's numbers from the app (sent, bounced,
   replies by class, snapshot-page visits), (2) the app reads the outreach inboxes over IMAP and classifies replies
   (interested / question / price / not now / stop / out of office / wrong person / bounce), (3) the AI writer drafts
   each reply, (4) a one-screen brief in Roman Hindi, (5) the founder says "send" and the app sends. "Stop" and
   out-of-office are handled automatically (suppress / pause); every other reply waits for one click until 50 replies
   have been classified correctly. ChatGPT: a weekly review round on the numbers and hard threads through the existing
   browser driver - not per reply (a reply there takes 10-35 minutes). "How many read" cannot be measured honestly
   (Apple Mail Privacy Protection pre-loads pixels; pixels also hurt deliverability) - use replies, positive replies
   and snapshot visits.
7. **Order:** (0) deploy the truthful website and buy the sending domains now (the 1-month age clock); (1) phase 5 +
   writer hardening (QA-1b); (2) 14b import + verification ladder; (3) phase 15 batch screen + scheduler + sender +
   suppression + bounce handling; (4) reply inbox + classifier + reply drafts + daily brief; (5) snapshot pages;
   (6) synthetic persona test of every template (ChatGPT and Claude role-play P1-P10 and score clarity, trust,
   spam-likeness) before the first real send - a filter, not proof.

## Three sample emails to test against the personas (P1 salon, Surat, social profile only)
**A - current spec (touch 1, plain, no link)**
Subject: A website idea for Glow Studio
> Hello Glow Studio team,
>
> I found Glow Studio on Instagram, but I couldn't find a website for it anywhere. A simple page of your own would show clients your services and prices without scrolling through posts.
>
> I'm Ravi from SiteBlitz, a small web studio in Gujarat. We build websites for local businesses, starting at ₹7,999 (domain and hosting are separate).
>
> Would you like me to send a short outline for Glow Studio?
>
> Ravi | SiteBlitz | [reply address] | [postal address]
> If this isn't useful, reply "stop" and I won't write again.

**B - "in short" line first (touch 1, no link)**
Subject: Glow Studio: clients can't find your prices online
> In short: people who look up Glow Studio find your Instagram, but no page with services, prices and timings. We can make that page for ₹7,999.
>
> Hello Glow Studio team, I'm Ravi from SiteBlitz, a small web studio in Gujarat. Your Instagram shows your work well; a one-page site would put prices, timings and a booking button in one place, and it shows up when someone searches your name.
>
> Shall I send a short outline?
>
> Ravi | SiteBlitz | [reply address] | [postal address]
> Reply "stop" and I won't write again.

**C - snapshot + audio link (touch 2, same thread)**
> Hello again, I made a one-page snapshot for Glow Studio: what we found, a labelled concept of how your page could look, and a 40-second voice summary from me. It takes a minute: [snapshot link]
>
> If it's useful, reply "yes" and I'll send the price and steps.
>
> Ravi | SiteBlitz | [reply address] | [postal address]
> Reply "stop" and I won't write again.

(Glow Studio and Ravi are invented for the test.)

</file>

<file path="docs/debate/2026-11-12-email-engine-personas/research-deliverability.md">
# Research - deliverability rules, sending services, verification, reading behaviour, audio/video, AI-voice law - 2026-11-12

Claude Code subagent (web research). "Unverified" = secondary source only or page not opened.

## 1. Mailbox-provider rules
- Gmail (support.google.com/a/answer/81126, undated): all senders need SPF or DKIM, PTR, TLS, spam rate < 0.3 %; bulk sender ~5,000+/day to personal Gmail needs SPF + DKIM + DMARC (p=none ok), alignment, RFC 8058 one-click unsubscribe for marketing; aim < 0.10 %, never 0.30 %. Same page: "Don't send messages to people who didn't sign up", "Don't purchase email addresses", "Start with a low sending volume", "Google doesn't track open rates".
- Gmail FAQ (answer/14229414, undated): "Starting November 2025, Gmail is ramping up its enforcement"; bulk status is permanent; subdomains count to the parent domain; honour unsubscribes within 48 h.
- Yahoo (senders.yahooinc.com/best-practices, undated): no volume threshold; spam < 0.3 %; bulk needs SPF + DKIM + DMARC, one-click List-Unsubscribe + a body link, honoured within 2 days.
- Microsoft Outlook.com (techcommunity blog, 2025-04-02, upd. 04-30): > 5,000/day needs SPF + DKIM pass and DMARC p=none or stricter, aligned; since 2025-05-05 non-compliant mail goes to Junk; unsubscribe link "recommended".
- Gmail Program Policies (support.google.com/mail/answer/16734397, upd. 2026-10-20): "Don't use Gmail to distribute spam or unsolicited commercial mail."
- Google Workspace AUP (2025-10-13): bans "unsolicited mass email, promotions, advertisements or other solicitations ('spam')".

## 2. Sending services
- Instantly: Growth $47/mo ($37.60 yearly) - 5,000 emails, 1,000 contacts, unlimited mailboxes + warm-up (instantly.ai/pricing, undated). Terms (Claude Code read them directly, "Last Updated: November 10, 2026"): §1.10 Permitted Purpose includes "Subscriber's own direct business-to-business (B2B) sales"; §4.3(b) subscriber is the sole "sender" and "initiator"; §4.6(b) subscriber alone responsible for compliance incl. CAN-SPAM; §6.7 "Subscriber will only process such data: (a) with valid, informed consent of the data subject" (rest of the list not read); §6.8 Instantly obtains no consents for the subscriber. Sending Policy (2026-10-13): opt-outs need "immediate action". AirMail price: not on the pricing page (unverified).
- Smartlead: Base $39/mo - 2,000 leads, 6,000 emails; pre-warmed mailboxes $9/mo + $18/domain/yr; terms 3.4(d) prohibit "unsolicited commercial electronic messages ... as defined by the Spam Laws".
- lemlist: Email plan $69/user/mo; sending policy: scraped lists must follow local privacy rules; opt-out link required; domains at least 1 month old.
- Saleshandy: Starter $41/mo - 2,000 prospects, 6,000 emails; ready mailboxes $2.99-3.99/mo; domain $14/yr; no cold-email clause found (unverified).
- Forbid it: SendGrid (prior affirmative consent; no addresses "obtained from the Internet"), Brevo (no third-party lists), Amazon SES (no "unsolicited mass email"), Mailgun ("clear, explicit and provable consent"), Postmark (permission-based only).

## 3. Verification
Bouncer $8 / 1,000, $35 / 5,000, $60 / 10,000, unknowns free (usebouncer.com/pricing). ZeroBounce from 2,000 for $39. MillionVerifier 50,000 $89, 1 M $449. NeverBounce $8 / 1,000 (unverified). Catch-all = domain accepts any address, so acceptance does not prove the mailbox exists.

## 4. Reading behaviour
Litmus Oct 2026 (1.7 B opens): Apple 75.84 %, Gmail 17.02 %, Outlook 3.49 %; Apple MPP affects "roughly 55-60 %" of opens (no source given). Mobile share: no primary 2025-26 figure. Read time 13.4 s (Litmus 2018 data, published 2019); newer 9 s figures unverified. Apple MPP pre-loads pixels (Apple 2021). No provider statement or controlled test shows pixels hurt inbox placement. IPSOS / India SME Forum (2025-03-12): 60 % of 1,010 small businesses use WhatsApp Business for sales and marketing; no email figure.

## 5. Audio / video / personalised pages
No independent controlled evidence. Intercom own test (2018, warm leads): video emails "52 % more effective at getting a reply". Vendor: Vidyard "up to 5x more replies"; Sendspark 200-300 % (unverified). Gmail's blocked attachment list has no audio formats.

## 6. AI-voice law
EU AI Act Art. 50 applies from 2026-08-02: deployers of deep-fake audio "shall disclose that the content has been artificially generated or manipulated"; (EU) 2026/1744 gives systems on the market before 2026-08-02 until 2026-12-02 for machine marking (secondary source). India IT Amendment Rules 2026 (notified 2026-02-10, in force 2026-02-20): duties on intermediaries; AI audio needs a "prominently prefixed audio disclosure"; coverage of a studio's own email not established. US: no federal rule for AI voice in email/web found; California SB 942 only for AI providers > 1 M monthly users.

</file>

<file path="docs/spec/outreach-engine.md">
# SPEC LOCK - Outreach engine: AI writer, email finder, batch screen, letter (phases 13-16)

Status: ✅ APPROVED 2026-11-10 (founder: "go for it"). Phase 13 built in the same session. Phase 14 built and run
on 2026-11-10 (`docs/outreach/email-finder-run-2026-11-10.md`). Phases 15-16 not started.
Inputs:
- The founder's request of 2026-11-10: AI writes every message; a daily cap of 100; select N and press one click;
  WhatsApp Web; social accounts; a scraper for phone-only leads.
- `docs/debate/2026-11-10-outreach-lifecycle-to-payment/RESULT.md`.
- `docs/spec/website-intelligence.md`.
- `E:\Temp\SiteBlitz\src\lib\offer.ts` and `site.ts`.
- Counts measured today from `E:\SiteBlitz-World-Business-Data`.

| # | Ambiguity | Locked value | Why this default |
|---|---|---|---|
| 1 | Who writes | An AI writes every message, including first messages, follow-ups, replies, social messages and letters. Model: Claude Sonnet 5.5 (`claude-sonnet-5-5`) via the Anthropic API. The key lives in `.env` as `ANTHROPIC_API_KEY` and is never committed. Prompt: `docs/outreach/ai-writer-system-prompt.md` + `company-facts.md` + `country-language.csv` + `reference-messages.md` | Founder decision 2026-11-10 (replaces RESULT rule B.7) |
| 2 | Data sent to the model | Business name, vertical, category, city, area, region, country, observations, language evidence, thread text. Never the email address, the phone number or a person's private data | Least data needed; the recipient is added after validation |
| 3 | Country + language | `country-language.csv`, 33 rows. Language order: business evidence, then owner's message, then region rule, then country default. The writer declares country, language, basis and self-check. Validator: `langdetect` (pure Python, works under Smart App Control) must return the declared language. On a mismatch it regenerates once, then HOLD. Any country without a row = HOLD (fixes `country_rules.py:54`, which treats a missing country as US) | Founder: "AI says which country, then verify the language" |
| 4 | Observation | 7 types in priority order: SITE_DOWN, BROKEN_FORM, NO_VIEWPORT, SOCIAL_ONLY, AGGREGATOR_ONLY, NO_SITE, NO_HTTPS. Only from `website_checks` rows ≤ 30 days old. If there is none, no message is sent | RESULT B.1; website-intelligence rule 7 |
| 5 | Length (words, without signature and opt-out) | Email T1 60-85 (max 100 with signature) · T2 40-70 · T3 30-50 · WhatsApp reply 25-60 · social message request 30-60 · letter 100-150 | RESULT B.2; each later touch is shorter |
| 6 | Human check | No person writes or edits. Once, before the very first send, the founder reads the first 20 validated emails in full. After that the validator alone decides | Catch a systematic prompt error once |
| 7 | Cadence and send time | Unchanged: Day 1 / 6 / 14, closed on Day 21. Tue-Thu 9:00-11:30 and 14:00-16:30 recipient's local time. Weekend dates move to Monday. Any reply stops the sequence | RESULT C, D, E |
| 8 | Studio identity in messages | "SiteBlitz, a small web studio in Gujarat". Never Mumbai or any other city | SiteBlitz FD-22 (truthful location); founder lives in Navsari |
| 9 | Email-finder scope (phase 14) | Navsari + Surat, no brand, the 3 demo verticals, phone-only leads with their own website = **2,162 sites**. Surat: coaching 271, retail 1,704, salon 74. Navsari: 10 / 98 / 5 | Measured 2026-11-10; pilot area near the founder |
| 10 | Email-finder method | Homepage + `/contact`, `/contact-us`, `/contactus`, `/about` (max 5 GET per site). robots.txt respected. 1 request per host at a time, 10 hosts in parallel. 12 s timeout, 2 MB, 5 redirects, SSRF guard. Emails only from mailto links, visible text or Cloudflare-encoded addresses on the business's own pages, with the source URL stored. Never guessed. The same visit records the viewport, HTTPS and site-down checks | `CONTACT_PAGE_PATHS[:4]`; website-intelligence rule 6; RESULT A |
| 11 | Code reuse | Reuse only `_crawl_contact_pages` / `_extract_from_html`. Never call `discover_contacts()`: it invents `info@<domain>`, `inquiry.<name>@gmail.com`, "Proprietor / Store Manager" and fake `+91 9825…` / `+1 (555)` phone numbers (`discovery.py:101-148`) | Found 2026-11-10; removal is phase 5 |
| 12 | Leads that have their own website | Contacted only with a SITE_DOWN, BROKEN_FORM or NO_VIEWPORT observation | Changes RESULT A ("no own website"); these are fixable problems the packages solve |
| 13 | Daily ceiling | At most **100 new first contacts per day** across all channels. Inside it: email 10 / 15 / 20 per day in weeks 1 / 2 / 3+, with ≤ 30 per inbox per day including follow-ups. Social messages ≤ 20 per day. Letters in batches of 25 | Founder (100); RESULT G; 60 min sending time ÷ ~3 min per hand-sent message |
| 14 | One-click flow (phase 15) | Select leads up to the remaining cap and press **Write**. The writer runs for each lead on its allowed channel, then the validator. The list shows READY or HOLD + reason. Email: **Send** puts it in the sending provider's queue. Social: **Open profile** + **Copy text**, and the founder sends by hand. Letter: PDF | Founder's "select 25, one click" |
| 15 | WhatsApp | Only for leads who wrote first (QR message, email reply, call). One click opens `web.whatsapp.com/send?phone=<E.164>&text=<message>` in the founder's logged-in browser, and the founder presses Send. No automated sending through WhatsApp Web. Cold numbers get the letter + QR instead | WhatsApp terms + FAQ (below); DECISIONS 2026-11-08 |
| 16 | LinkedIn / Facebook / Instagram | No logged-in automation. Text drafted by the writer, sent by hand from the SiteBlitz account, ≤ 20 per day | LinkedIn UA §8.2; Facebook Terms §3.2; DECISIONS 2026-11-08 |
| 17 | Letter (phase 16) | Writer text on the front. The back carries a sample homepage image and a QR code to `wa.me/[REDACTED]` with the pre-filled text from `reference-messages.md`. Paper size waits for the India Post class and price | RESULT F, G |
| 18 | Founder blanks | Sender name, reply address, postal address, and the demo pages deployed (`/demo/*` returned 404 on 2026-11-10). Until they are filled, the writer returns HOLD (MISSING_COMPANY_FACT) | `company-facts.md` |

## OUT OF SCOPE (will NOT build)
- Automated sending on WhatsApp Web, and any cold WhatsApp message to a number that did not write first.
- Logged-in bots on LinkedIn, Facebook, Instagram or any other platform, including scraping profiles for emails.
- Guessed or pattern-made email addresses of any kind.
- AI-cloned or synthetic voice notes.
- Countries other than India until their row says PILOT.

## ACCEPTANCE CRITERIA (binary)
- [ ] Phase 13: 30 fixture leads (10 per vertical, Surat/Navsari) each give either a validator-passing message or
      HOLD with a reason code. 0 messages contain a number, domain or URL that is not in LEAD / COMPANY_FACTS / TASK.
- [ ] Phase 13: there is one unit test for each validator rejection: country mismatch, language mismatch, word
      count, 0 or 2+ questions in T1, link in T1, banned phrase, em dash, `!`, `;`, unresolved `[..]` / `{{..}}` /
      `TO FILL`, missing opt-out, missing signature, and a HOLD country producing text.
- [ ] Phase 13: a test proves that the request body sent to the model contains no `@` email and no phone digits.
- [x] Phase 14: the run covers 2,162 sites. Every stored email has a source URL on the business's own site, and
      0 emails exist without one. Totals are reported: emails found, sites down, NO_VIEWPORT, NO_HTTPS,
      robots-blocked. (2026-11-10: 2,162 outcomes, 839 email rows, 0 without a source URL, 0 off-host.)
- [ ] Phase 15: 100 sends in one day are possible and the 101st selection is refused with a visible message.
      WhatsApp **Open chat** appears only for leads with an opt-in. Screenshots exist for each state (empty,
      selecting, writing, ready/hold list, cap reached) at 1280 and 390 px.
- [ ] Phase 16: a 25-letter PDF prints with each business's own QR text. Scanning one QR opens WhatsApp to
      +91 92744 90242 with that business's name already in the message.

## RISKS
- AI-only writing can produce plausible but untrue sentences. Cheapest check: the facts guard (criterion 1) plus the
  founder reading the first 20 emails.
- The email finder's yield is unknown. The ladder will move many addresses to RISKY. If fewer than 100 VALID emails
  come out of the 2,162 sites, the email pilot uses the 9,176 Surat/Navsari leads in these verticals that already
  have an email.
- `langdetect` is weak on very short texts. If the social messages (30-60 words) fail it often, they are checked
  against the lead's language row only.

## Sources checked 2026-11-10
- WhatsApp FAQ "Unauthorized use of automated or bulk messaging": since 2019-12-07, WhatsApp takes legal action
  against people and companies engaged in, or assisting others in, automated or bulk messaging.
  https://faq.whatsapp.com/[REDACTED]
- WhatsApp Terms of Service (effective 2021-01-04): no "bulk messaging, auto-messaging, auto-dialing", and no
  non-personal use unless authorised. https:
[truncated]
</file>
</project_context>

<topic>
# Topic - SiteBlitz email engine v2: personas, content that gets read, a creative layer, worldwide sending from the admin panel, and an AI-run daily conversation loop - 2026-11-12

## The founders' words (translated from Roman Hindi)
"The agency idea is very good, but focus mainly on this. From the data we extracted - the whole world, 248
countries - we mail X people every day, from the admin panel, in a single click; we will set up whatever SMTP is
needed. The main point is the content: what a mail needs so it does not go to spam, and so that when the client or
their assistant reads it, it feels worth it and they understand immediately. Think of creative ways - an audio
message that reads the mail, or a summary - so it feels unique and interactive and people read it at least once. I
guarantee nothing; you and ChatGPT analyse everything: how every kind of person thinks after receiving a mail; test
with multiple different personas. Then set up the mailing system (WhatsApp later). My motive: I open my laptop and
say 'start today's day'; you check yesterday, read the replies, tell ChatGPT, decide who is interested and what to
reply - complete flows. You and ChatGPT handle clients and conversations; my friend and I deliver the sites. If you
cannot send daily yourself, add scheduling through the admin panel."

## Agenda
1. Personas: how 8-10 different recipients of a cold website email actually read it (who opens it - owner, receptionist, assistant, manager; device; first 3 seconds; what makes them delete, mark as spam, forward or reply), with evidence where it exists. Test the three sample emails in claude-position.md against each persona.
2. Email anatomy that both survives spam filters (Gmail / Yahoo / Outlook rules in force in 2026) and is understood in 5 seconds by the owner or an assistant: subject, preview text, first line, a one-line "in short" summary, the observation, offer, price, call to action, sender, opt-out, plain text vs HTML, links, images, attachments, length - per touch (1 / 2 / 3).
3. The creative / interactive layer the founders asked for (an audio message that reads the mail, a summary, an "interactive UI"): judge each option - audio file, audio link, a personalised one-page "Opportunity Snapshot" per business (their observations, a labelled concept preview, a 30-60 s audio summary, price, one-tap reply / WhatsApp), AMP email, GIF - on deliverability, trust, law (AI-voice disclosure) and effort. Which touch gets which element.
4. Worldwide: which countries can receive this email now (tiers by law and by language), how the daily number X is chosen and ramped (inboxes, domains, warm-up, verification, gates), and which leads out of 86.75 M qualify.
5. Sending from the admin panel: one click to approve the day's batch, a scheduler that sends inside each recipient's local window, where it runs (founders' laptop + Task Scheduler, a small server, GitHub Actions), sending infrastructure that the provider's terms allow (the founders say "we will set up SMTP"), bounces, suppression, automatic stop rules.
6. The daily loop "start my day": what Claude Code does each morning (yesterday's numbers, read replies, classify, draft replies), what ChatGPT does, what the founders must still do, whether any reply may go out without a human click, and which metrics are honest ("how many read" without tracking pixels).
7. Build order, gates and pre-send tests (including a synthetic persona test of every template before real sending), and what the public website must show before the first email (it currently shows invented testimonials).

Attached: claude-position.md (Claude Code's view, written before your reply, with three sample emails to test),
docs/spec/outreach-engine.md (the spec approved on 2026-11-10), research-deliverability.md (a Claude Code research pass, 2026-11-12).

Answer each agenda point by number: agree / disagree because ... / need data: ... . For point 1, give a table:
persona x (who reads, device, first 3 seconds, delete trigger, reply trigger, verdict on samples A / B / C). End with
the list of points still open.
</topic>


---

## ChatGPT (Pro) - 2026-11-12 03:51 UTC - saved as 01_chatgpt.md

ChatGPT said:
SiteBlitz email engine v2: point-by-point response to Claude Code

My overall position: agree with building a one-click, AI-assisted conversation engine; disagree with treating the current plan as ready to send. The system should optimise for qualified conversations and profitable website projects, not the number of emails dispatched.

The supplied documents describe missing sending infrastructure, reply handling, verification, sender identity and a truthful production website. Consequently, the presently approved sendable number is zero until those launch gates pass. This is a readiness decision, not a rejection of the vision. I have reviewed the supplied material, not audited the repositories or independently confirmed their feature claims. 
Pasted text

External rules below were checked on 12 November 2026. Citations link to the source URLs. “High confidence” means the primary source clearly supports the stated rule; whether a particular campaign satisfies it still requires application-specific review. Legal conclusions are design inputs for counsel, not legal advice.

1. Personas — agree with the framework; disagree with treating simulated reactions as evidence

The ten personas are useful hypotheses. However, industry, inbox reader, device and legal status should be separate attributes, not one assumed personality. A receptionist might screen a salon’s email; an owner might personally read a restaurant’s info@ inbox.

The table below is a reasoned simulation, not observed customer research. Behavioural confidence is low until tested. Samples A, B and C are salon-specific, so they are unsuitable verbatim for the other industries; those rows assess their structures after truthful adaptation. The samples and personas come from the supplied position paper. 
Pasted text
 
Pasted text

Persona	Who reads; likely device hypothesis	First three-second question	Delete / spam trigger	Forward / reply trigger	Verdict on A / B / C
P1: Salon owner	Owner or family member; phone	“Is this about my business, and is it useful?”	Criticism, generic compliments, a meeting request before explaining value	A recognisable observation and a simple services/enquiry-page offer	A: strongest starting structure, but soften “anywhere.” B: reject unsupported claims about prices. C: test later, with optional audio.
P2: Coaching centre	Administrator first, owner second; phone or desktop	“Should I forward this to the owner?”	Unsupported claims about lost admissions or a vague redesign pitch	Exact page/problem plus a sentence explaining the proposed fix	A: adapt around verified usability evidence. B: summary structure useful; present wording unsuitable. C: screenshot may help forwarding.
P3: Retail showroom with an unavailable site	Owner or manager; phone	“Is this real, or someone trying to frighten me?”	“Your domain expired” inferred from one failed request	Dated, repeatable observation with an acknowledgement that it may be temporary	A: use precise diagnostic wording. B: accusatory framing is risky. C: evidence can help, but must not resemble a security scare.
P4: US clinic practice manager	Practice manager or receptionist; desktop/phone	“Who is this, and why should the dentist see it?”	Patient-related assumptions, unverifiable claims, pressure or sensitive information	Clear business purpose, verifiable sender and narrow non-clinical scope	A: requires US-compliant identity/advertising treatment. B: reject overclaims. C: possible later, excluding patient information.
P5: Restaurant shared inbox	Staff, manager or owner; mixed devices	“Is this a booking, supplier matter or advertisement?”	A subject that disguises a pitch as a customer enquiry	A self-contained, forwardable explanation	A: adapt and identify the commercial offer. B: concise summary could work after correction. C: useful only when understandable without earlier context.
P6: UK/Australian trades business	Owner or office administrator; phone	“Will this help, and how much work is responding?”	Marketing jargon, false urgency, compulsory call booking	A specific improvement and an easy reply	A: adapted structure is plausible. B: avoid criticism. C: optional, not audio-dependent. Legal eligibility must come first.
P7: Business with a working website and no relevant problem	Any reader	“Why are you contacting me?”	Invented shortcomings	No qualifying trigger under the current offer	A/B/C: do not send. Do not manufacture a problem to fill the batch.
P8: Digital agency owner	Owner or delivery lead; desktop/phone	“What capability, terms or capacity do you offer?”	A consumer-style website pitch	Clear white-label scope, ownership, handover and commercial terms	A/B: wrong offer as written. C: a relevant capability example may work, but belongs in a separate campaign.
P9: Assistant / gatekeeper	EA, receptionist or family member; mixed devices	“Can I explain this to the decision-maker?”	Ambiguous request, missing identity, reliance on opening a link	A sentence containing business name, observation, offer and requested action	A: fairly forwardable. B: best summary concept, weakest factual discipline. C: email must remain meaningful without clicking.
P10: Mailbox filtering system	Technical system, not a human persona	Not applicable	Authentication, reputation, policy or content problems	Not applicable	A/B/C: inbox placement cannot be predicted by role-play. Test authentication, rendering, provider responses and real campaign outcomes.
What I would change in the samples

A needs bounded observation language. “I couldn’t find a website anywhere” implies a more exhaustive search than the system can establish. Prefer: “Your Instagram profile had no website link when checked,” provided that exact observation exists.

B should not launch. Finding no website does not establish that customers cannot find prices. Instagram might already contain them. Saying the new page “shows up when someone searches your name” also promises an outcome not established by the evidence.

C needs consistency. It promises to send the price later even though A already gives a starting price and the proposed snapshot contains pricing. Change the next step to scope and delivery details. A reusable vertical recording must be described as a general recorded overview—not a bespoke voice message.

Proposed test

Use the two models to find contradictions and confusing wording, then show variants to 10 consenting business readers. After five seconds, ask them to explain the sender, reason for contact, offer and next action.

My proposed acceptance threshold is 8 of 10 correctly explaining all four, with no material misunderstanding of price. That is a usability gate, not proof of conversion.

Cost and upkeep: no additional specialist software is necessary; recruitment and review require human effort. Refresh the hypotheses from actual replies. Beneficiaries: recipients and founders. Main risk: optimising for simulated preferences instead of real behaviour.

2. Email anatomy — agree with simplicity; disagree that a particular format can guarantee inbox placement

There are four separate questions:

Is sending lawful? Does the sending provider permit it? Will the receiving provider accept it? Will the reader find it worthwhile?

Passing one does not establish the others. Google explicitly states that an email provider cannot guarantee passage through Gmail’s spam filters. 
Google Help

Provider requirements: corrections and launch baseline
Provider	Verified requirement or correction	Date and confidence
Personal Gmail	All senders need SPF or DKIM, valid forward/reverse DNS, TLS and low spam rates. Bulk senders need SPF and DKIM, DMARC/alignment and one-click unsubscribe for marketing/subscribed messages. Implement the stronger authentication configuration from the beginning.	Baseline effective 1 February 2024; current guidance checked. High. 
Google Help

Yahoo	Its published requirements cover authentication, complaint rates and easy unsubscribe; bulk requirements include SPF, DKIM and DMARC. Yahoo does not publish a simple numerical definition of “bulk” in its FAQ.	Current, undated guidance. High on these requirements; do not invent a volume exemption. 
senders.yahooinc.com
+1

Outlook.com consumer accounts	The research attachment’s “noncompliant mail goes to Junk” statement is outdated. Microsoft’s updated announcement says qualifying high-volume authentication failures are rejected, with error 550 5.7.515.	Enforcement from 5 May 2025. High. 
TECHCOMMUNITY.MICROSOFT.COM

“Plain text,” “no links” and “under 100 words” should be testing defaults—not claims about universal spam-filter rules. The supplied research itself says it found no provider statement or controlled test demonstrating that tracking pixels necessarily damage inbox placement. Remove pixels for privacy and unreliable measurement; do not present a universal deliverability penalty as established. 
Pasted text

Recommended anatomy by touch
Element	Touch 1	Touch 2	Touch 3
Purpose	Establish relevance and offer one small next step	Supply additional evidence or a useful example	Close respectfully
Subject	Business name plus truthful, non-alarmist topic	Actual continuation of the same thread	Same genuine thread
Opening / preview	Specific observation and its limited scope	New information, not “just following up”	Brief closure
Summary	Integrate into the first two sentences; do not repeat the whole message under “In short”	Explain the snapshot in one sentence	Usually unnecessary
Offer and price	Narrow deliverable; approved starting price and material exclusions	Same price/scope, or an explicitly explained update	No invented discount or deadline
CTA	One easy question	One next action	No pressure; optionally allow the recipient to reopen later
Media	Text-first; no promotional attachment	At most one relevant snapshot link	Usually none
Length	Retain 60–85 body words as a starting target	40–70	30–50

These proposed body lengths follow the supplied specification. Legally necessary identity, notice and unsubscribe information must not be removed to satisfy a total word limit. 
Pasted text

Corrected illustrative first touch

The following uses the document’s fictional business and sender. It is not send-ready: the observation and ₹7,999 offer must be verified and approved.

Subject: Glow Studio — a services-page idea

Hello Glow Studio team,

Your Instagram profile had no website link when I checked it. I offer a simple page that puts your services, prices and appointment-enquiry button in one place.

I’m Ravi from SiteBlitz, a small web studio in Gujarat. Website setup starts at ₹7,999; domain and hosting cost extra.

Would a short outline for Glow Studio be useful?

Ravi | SiteBlitz
[Actual reply address and postal address]
Reply “stop” to opt out.

For US campaigns, the message must also clearly disclose its advertising nature; CAN-SPAM is not limited to bulk mail and has no B2B exemption. A postal address and functioning opt-out are substantive requirements, not optional trust decorations. Source: FTC’s current compliance guide; high confidence. 
Federal Trade Commission

Unsubscribe and validator changes

Implement RFC 8058 with an HTTPS unsubscribe endpoint and the appropriate headers, covered by a valid DKIM signature. A mailto: link alone does not implement that mechanism. Source: RFC 8058, January 2017; high confidence. 
RFC Editor

Amend “no links in touch 1” to “no promotional links in touch 1; compliance links are permitted or required.” A privacy notice or unsubscribe facility must not be blocked by the writer validator.

Keep factual, identity, consent and suppression checks strict. Treat punctuation preferences—such as banning semicolons or em dashes—as style rules, not evidence-backed spam protections.

Cost and upkeep: low incremental infrastructure cost, but offer versions and legal footers need maintenance. Success test: every factual claim has supporting evidence; every seeded test message authenticates correctly; unsubscribe works end to end. Risk: technically perfect messages can still be unwanted.

3. Creative and interactive layer — agree with a snapshot; disagree with novelty for its own sake

Put the rich experience on a trustworthy page, not inside the first unsolicited email. The email must deliver enough value without requiring a click.

Option	Decision	Deliverability, trust and legal assessment	Effort / placement
One-line summary	Build now	Low complexity; useful to owners and assistants. No promised reply-rate improvement.	Low; touch 1 onward
Audio attachment	Do not use in the pilot	No demonstrated universal audio-file penalty, but it asks a stranger to download/listen before establishing trust.	Avoid initial maintenance and testing burden
Audio link	Optional within the snapshot	Give a transcript; no autoplay; accurately identify the speaker and whether the recording is generic or personalised.	Moderate; touch 2 or after a request
Opportunity Snapshot	Build a small version, then test	Strongest opportunity to show evidence, scope and a labelled concept without making the email heavy.	Moderate; touch 2 or an interested reply
AMP email	Defer	Gmail requires sender registration, authentication and an HTML/text fallback. This adds complexity without evidence of value for this pilot.	High relative to current need; later permission-based use. 
Google for Developers

GIF	Defer	An animation is not proof of relevance. Start with a static, clearly labelled comparison.	Low-to-moderate production effort; only test after a baseline
WhatsApp button	Defer with the channel	The founder explicitly prioritised email now. Do not expand the first implementation.	Later scope decision
My proposed snapshot

Use three layers:

Five-second layer: business name, one verified observation, one sentence describing the offer.

Evidence layer: date checked, a narrowly framed screenshot or observation, and a clearly labelled concept—not a claimed live website or existing client project.

Optional detail layer: scope, one-time and recurring costs, transcript/audio, and a reply action.

Include a visible statement such as:

“Illustrative concept prepared by SiteBlitz. Not your current website and not an existing client project.”

Use appropriately licensed assets. Avoid exposing private contact information. Add a correction/removal route. My proposed default is an unlisted, expiring page with no advertising trackers; a random URL and noindex are not security controls for confidential information.

Correct the measurement claim

A page request does not prove that the recipient looked. Microsoft documents automated link scanning during email processing and at click time. Consequently, raw requests can include security activity. 
learn.microsoft.com

Record separately:

Raw page requests.
Filtered, likely-human sessions.
Explicit actions such as a submitted enquiry.
Replies and qualified opportunities.

Do not automatically send “I saw you viewed our proposal.”

AI voice: narrower legal conclusions

The EU’s Article 50 rules distinguish provider marking obligations, direct AI interaction disclosure and deployer disclosure of deepfakes. They do not support the blanket statement “every AI narration has the same deepfake-disclosure obligation.” They apply from 2 August 2026. High confidence on the distinction; medium on a specific SiteBlitz implementation. 
digital-strategy.ec.europa.eu

India’s notified amendment took effect on 20 February 2026. Its relevant synthetic-media provisions impose duties on intermediaries, including audio disclosure in covered circumstances. That does not itself establish the duties of a studio sending its own email. High confidence on the text; application needs counsel. 
meity.gov.in
+1

For this version, retain the approved ban on synthetic voice. A truthful founder recording is sufficient; synthetic narration requires an explicit specification amendment. 
Pasted text

Cost and success: start with one reusable page template, not bespoke videos for every prospect. Measure incremental qualified replies and paid-project margin against the text-only control. Delete the audio feature if it adds cost without measurable value.

4. Worldwide sending — disagree with “India and US now”; agree with conditional country expansion

No country is operationally approved before the common launch gates pass. Thereafter, distinguish potentially permissible recipients from an entire country being safe to email.

Proposed jurisdiction tiers
Tier	Market	Required distinction and launch decision
First controlled pilot	India	Business relevance, original publication evidence, privacy review and provider compatibility are required. Do not treat all publicly discoverable personal addresses as cleared.
Next reviewed pilot	United States	CAN-SPAM provides requirements for commercial outreach, including truthful identity/subjects, advertising disclosure, postal address and opt-out. It does not guarantee provider permission or replace other applicable obligations. High confidence on the FTC requirements. 
Federal Trade Commission

Conditional corporate pilot	United Kingdom	PECR distinguishes corporate subscribers from sole traders and certain partnerships. Companies House registration helps establish the entity, but does not alone establish who subscribes to a particular mailbox. Personal-data processing still requires UK GDPR analysis. High confidence; ICO guidance currently notes review following legislative changes. 
ICO

Case-by-case, not bulk import	Canada	Conspicuous publication requires publication by, or caused by, the recipient; no accompanying refusal; and relevance to their business role. A third party reproducing or selling the address does not create implied consent by itself. High confidence, current CRTC guidance. 
CRTC

Hold until sourcing review	Australia	Consent may be express or inferred, but the Spam Act separately regulates address-harvesting software and harvested-address lists. “Published address” is not a sufficient clearance field. ACMA also says a marketing email cannot be sent merely to ask for consent. High confidence on these rules. 
ACMA
+1

Later, French-language pilot	France	CNIL permits relevant professional prospecting under conditions including information and objection rights. Do not translate this into a general EU rule. Guidance dated 10 June 2026; high confidence. 
CNIL

Hold	Every unreviewed jurisdiction	No sending until its recipient categories, sourcing, notices, provider constraints and language QA are approved. “Hold” does not mean the activity is necessarily illegal.

Important India correction: most core DPDP processing provisions are scheduled to commence on 13 May 2027, following the phased notification of 13 November 2025. The Act’s public-availability exclusion is specifically framed around publication by the data principal or someone legally obliged to publish—not every third-party listing. Build for that distinction now. High confidence on the statutory text and commencement schedule. 
India Code
+1

The Gmail problem needs an explicit decision

Google’s receiving guidelines advise against sending to people who did not sign up. Sending through a different SMTP service does not remove that guidance. 
Google Help

The attachment reports that 79% of its Indian email-containing records use free-mail addresses; it does not say all of those are Gmail. That makes recipient-provider policy a major pilot constraint, not a footnote. 
Pasted text

For a policy-conservative launch, put non-opted-in personal-mailbox recipients on HOLD where receiving-provider guidance requires permission. Use a voluntary audit-request form, a properly authorised partner introduction or another reviewed acquisition channel. A “permission request” email is not a universal workaround.

Which records qualify?

The reported 86.75 million places are a discovery inventory, not a permissioned prospect list. Overture’s source-specific licensing also needs preserving; a data licence does not itself establish marketing permission. 
Pasted text
 
Overture Maps

I propose a mandatory eligibility record covering:

business identity → source/provenance → jurisdiction and recipient type → legal/provider eligibility → language → fresh observation → email verification → suppression → capacity

Important rules:

Identity: deduplicate businesses, branches, shared mailboxes and franchises. Do not email several branches about the same central website.

Evidence: recheck an outage shortly before sending. A crawler timeout or access block is not proof that a website is down. NO_VIEWPORT is a technical signal, not conclusive proof of bad mobile usability.

Contact: record the exact original source and publication context. A verifier’s VALID result is neither consent nor proof that the address belongs to the intended business.

Language: use business evidence and native-reviewed wording. Do not assume Gujarati, Hindi or English from city alone.

Uncertainty: HOLD is a valid outcome. Catch-all and unknown verification results stay out of the initial pilot.

Choose X from capacity—not ambition

The specification’s 100 new first contacts/day is a ceiling. Its 10/15/20 email ramp must not silently become a per-inbox allowance. Until clarified, I would interpret it conservatively as an app-wide campaign-send allowance. The 30-per-inbox limit includes follow-ups. 
Pasted text

With six inboxes:

6
×
30
=
180
 total messages per permitted sending day
6×30=180 total messages per permitted sending day

If every prospect receives three touches:

180
÷
3
=
60
 sustainable new prospects per sending day
180÷3=60 sustainable new prospects per sending day

That is before reserving capacity for replies. Therefore, six inboxes cannot sustain 100 new prospects per sending day under the worst-case three-touch sequence.

Admit new prospects only after reserving future follow-up capacity. Reduce X when delivery work or unanswered sales conversations accumulate.

Scaling gates

Retain the proposed bounce and complaint targets as conservative operating targets, not guarantees. Google recommends staying below 0.1% reported spam and avoiding 0.3%. 
Google Help

For the small pilot, my proposed rules are: investigate the first hard bounce; pause the affected cohort on a credible complaint or policy rejection; and show unavailable complaint data as unknown, not zero.

A 3% positive-reply target is provisional. Define it as positive human replies divided by distinct, accepted first-contact recipients in a mature cohort, excluding auto-replies. Paid projects and margin ultimately decide whether to scale.

Cost: verify only qualified candidates. Bouncer currently advertises $8 for 1,000 verification credits, not a guarantee of deliverability or legal eligibility. Price checked 12 November 2026; high confidence as an advertised price. 
Usebouncer

5. Admin-panel sending — agree with an owned queue; disagree that SMTP alone solves permission or reliability
Provider selection

The infrastructure must pass both the outreach tool’s terms and the underlying mailbox/relay provider’s terms.

Gmail’s policy updated 20 October 2026 prohibits unsolicited commercial mail; Google Workspace’s AUP prohibits unsolicited mass promotions and solicitations. Connecting such mailboxes to another product does not override those terms. 
Google Help
+1

For the proposed scraped-list campaign, SendGrid’s affirmative-consent requirements, AWS’s unsolicited-mass-email prohibition and Brevo’s restrictions on scraped/third-party lists make them unsuitable defaults. These are provider restrictions, not interchangeable statements of worldwide law. 
help.twilio.com
+2

Instantly is a candidate, not an automatic approval. Its terms updated 10 November 2026 include direct B2B activities as a permitted purpose. The incomplete reading of §6.7 should be corrected: it permits consent or another applicable lawful basis, not consent alone. 
instantly.ai
+1

Two additional conditions matter:

Domain age: its sending policy dated 13 October 2026 requires domains at least one month old. Buying a domain today therefore does not allow immediate sending through that route. This is a vendor requirement, not a universal deliverability law. 
instantly.ai

Ownership: its current terms say Instantly-provisioned infrastructure remains Instantly’s property, with substantial restrictions on transfer and administrative control. For a founder who wants an owned system, prefer independently controlled domains and verify mailbox portability before purchase. 
instantly.ai

Proposed one-click flow

Select → Write → Validate → Review batch → Approve and schedule

The approval screen should show the actual messages, eligibility evidence, HOLD reasons, costs and earliest send times. Approval authorises only that validated batch; it does not override later opt-outs or fresh failures.

At execution time, recheck:

approval → suppression → reply state → observation freshness → provider status → local window → remaining capacity

Keep one authoritative scheduler. If the provider also queues messages, the app must be able to reconcile and cancel them. Do not independently schedule the same sequence in two systems.

Where it should run

A laptop is acceptable for development and a supervised pilot, but not as the sole dependency for a worldwide “works while closed” service.

I recommend a small always-on application server, with persistent storage, backups, reply/event ingestion and a functioning unsubscribe endpoint. A single-host SQLite design may remain an initial implementation choice; there is no need to add a distributed queue solely because the dataset is large.

GitHub Actions is not inherently impossible, but it is a poor primary sending clock: GitHub documents that scheduled runs can be delayed and, under sufficient load, dropped. Use it for tests and deployment rather than critical send timing. 
GitHub Docs

Reliability rules worth building before a rich UI

Store a unique logical send record, message content/version, provider identifiers and delivery state. Use provider idempotency where supported.

A transport timeout is not proof that nothing was sent. Mark uncertain attempts for reconciliation rather than blindly retrying. A repeated Message-ID alone is not a reliable deduplication strategy.

Separate failure types:

An invalid mailbox should be suppressed across email campaigns.
An authentication or policy rejection should pause the affected infrastructure—not incorrectly mark the recipient invalid.
An opt-out should stop marketing across the appropriate identity scope.
A reply should cancel the remaining cold sequence before drafting anything else.

Do not treat an email bounce as permission to switch to another channel.

Resolve the specification’s scheduling contradiction: Tue–Thu only conflicts with “weekend dates move to Monday.” My proposed rule is to move any disallowed due date to the next permitted local window. 
Pasted text

Cost: Instantly’s page currently displays a $47/month Growth outreach component, but that is not a complete implementation quote. Confirm API access, webhooks, mailboxes and domains separately. 
instantly.ai
 Success tests: no duplicate sends under retries, no post-opt-out sends in race-condition tests, and recoverable queue state after a crash.

6. “Start my day” — agree with the experience; disagree with 50 correct classifications as an autonomy gate

The daily system should run in the application. Claude Code and ChatGPT can support development and review; the business must not depend on an open chat session or a browser conversation completing.

The morning workflow

First, reconcile. Retrieve sending events and incoming messages; distinguish accepted messages, bounces, replies and unresolved send attempts.

Second, protect. Apply opt-outs and pauses before considering new sends. Stop the cold sequence on any reply.

Third, interpret. Classify the latest relevant message using thread context. Allow multiple labels: “What is your price, but stop the follow-ups” is both a price question and a suppression instruction.

Fourth, prepare. Generate grounded reply drafts, identify missing facts, and display decisions requiring approval.

Fifth, authorise. The founder approves the safe reply batch and the next campaign batch. Unresolved commercial commitments remain held.

The Roman-Hindi brief should contain decisions, not a wall of metrics:

“Kal ke replies process ho gaye. Interested enquiries review ke liye ready hain. Stop requests suppress ho chuki hain. Aaj ke batch mein jo leads HOLD hain, unka reason saath diya hai.”

Populate it with actual counts only.

Automation boundaries
Event	Recommended initial handling
Clear opt-out / unsubscribe	Suppress automatically; cancel queued marketing
Out of office	Pause; do not initiate an automatic back-and-forth
Bounce	Parse the failure type; suppress or pause appropriately
Interested / price / scope question	Draft from approved offer facts; require approval
Wrong person	Stop that sequence; do not automatically contact a named replacement without eligibility checks
Complaint / legal request / deletion request	Stop marketing and escalate
Negotiation, refund, guarantee, contract or delivery commitment	Human approval required

This still respects AI-written messages: the founder can approve, reject or request regeneration without rewriting them.

Why 50 is insufficient

Even with zero observed errors in 50 independent representative cases, the exact one-sided 95% upper bound on the true error rate is approximately:

1
−
0.05
1
/
50
≈
5.8
%
1−0.05
1/50
≈5.8%

This calculation is not evidence that the classifier will fail at that rate; it shows why 50 successes do not establish safety.

My proposed path is a labelled evaluation set covering each important category, adversarial examples and a live shadow period. Require zero missed opt-outs in the safety test set before considering any auto-reply category. Even 300 zero-error representative cases imply an upper bound near 1%, not zero risk.

Begin eventual auto-sending only with narrowly scoped, non-binding answers grounded in approved facts. Do not let a model invent discounts, delivery dates or guarantees.

Claude and ChatGPT roles

Use a primary model for classification/drafting and an independent reviewer for high-risk threads, factual disputes and sampled QA. Do not pay for two full-model passes on every routine email without measuring the benefit.

The governing authority remains the application’s policy and approval state—not “both models agreed.”

Treat email bodies and scraped pages as untrusted input. A recipient message must not grant permission to export data, change payment instructions or execute tools. Structured outputs, limited tool authority and approval gates are consistent with OpenAI’s current agent-safety guidance. 
OpenAI Developers

The specification’s promise not to send email addresses or phone numbers to the model also needs a real sanitizer: thread text can contain them in signatures and quoted replies. Merely omitting separate contact fields does not satisfy that promise. 
Pasted text

Honest metrics

Show sent/accepted events, bounces, unique human replies, positive replies, qualified opportunities, proposals, paid projects, acquisition cost and contribution margin.

Do not call pixel events “read.” Apple states that Mail Privacy Protection can download remote content when a message arrives rather than when it is viewed. 
Apple Support

Likewise, “accepted by the receiving server” is not “landed in the inbox,” and “snapshot requested” is not “owner viewed.”

Cost and upkeep: model usage, secure message processing and regular evaluation. Beneficiaries: founders and recipients awaiting replies. Success: fewer manual decisions without missed opt-outs, unsupported commitments or deteriorating sales outcomes.

7. Build order and launch gates — agree with the truthful website first; move minimum reply handling before the first send

The supplied document reports invented testimonials/results, incorrect location claims and withdrawn prices on the live website. Those claims are not independently verified here, but the reported condition is a launch blocker until the deployed site is checked and corrected. 
Pasted text

Recommended order
Stage	Build / decision	Exit gate
0. Truth and identity	Deploy truthful website; confirm sender, business identity, address, reply mailbox and offer	Production pages checked; no fabricated claims; all identity fields complete
1. Data integrity	Remove fabricated-contact paths; quarantine previously generated dummy data; retain source provenance	No eligible contact without provenance; fixtures cannot enter production
2. Eligibility engine	Country/subscriber rules, provider policy, language, evidence freshness and verification	Unknown or failed requirements produce HOLD
3. Safety infrastructure	Authentication, unsubscribe, suppression, bounce handling and minimum incoming-reply processing	End-to-end tests pass before any prospect email
4. Batch and scheduler	AI writing, validation, review, approval, queue and reconciliation	No unapproved, duplicate or out-of-window sends
5. Pre-send evaluation	Synthetic persona review, consenting-reader test and seeded mailbox tests	Factual and comprehension gates pass
6. Controlled pilot	One small, well-defined segment	Mature outcomes reviewed before increasing volume
7. Expansion	Snapshot experiment, limited reply automation and additional markets	Each addition passes its own economic, safety and legal gate

The specification explicitly identifies a discovery function that invents contact data. Removing it is not enough: audit whether its outputs already entered the database. 
Pasted text

Pre-send tests that must exist

Test opt-out arriving between approval and execution; reply arriving before a scheduled follow-up; duplicate/out-of-order provider events; timeout after possible provider acceptance; restart recovery; missing timezone; stale evidence; unknown country; unavailable model; and blank company facts.

Verify authentication and unsubscribe headers on received raw messages, not merely in the app’s outgoing payload.

Also test mobile batch screens, quoted unsubscribe text, auto-reply loops and malicious instructions embedded in inbound messages. The supplied 338-test count and writer dry-run results do not establish that these cases are covered. 
Pasted text

What the public website must show

Real business identity and location; a working contact route; accurate package scope; one-time versus recurring costs; ownership and handover terms; and appropriate privacy information.

Use genuine portfolio work with permission, or clearly labelled demonstrations. No fabricated client names, testimonial quotations, results or claims that a demo is a delivered customer project.

Budget and economic gate

Do not approve a complete operating budget from the vendor subscription price alone. The budget must include sending software, mailboxes/domains, verification, hosting/backups, model usage, legal review and human handling.

Measure:

Customer acquisition cost
=
all attributable outreach and sales-handling costs
paid customers acquired
Customer acquisition cost=
paid customers acquired
all attributable outreach and sales-handling costs
	​


Compare that with contribution after website-delivery and support costs, not headline revenue. A high positive-reply rate with unprofitable delivery is not a successful engine.

For future AI-managed inboxes, my proposed extension is a structured offer record—identity, evidence, scope, price, exclusions and next action—used to generate both the email and snapshot. That gives human assistants and software agents consistent facts. It is an architectural proposal, not a prediction that any particular standard will dominate.

Final decision: approve the direction, but revise the specification before implementation. The next milestone should be a truthful, policy-reviewed, reliably stoppable pilot, not a 100-email button.

Points still open
Sender and offer: actual sender name, business/legal identity, reply address, postal address, approved pricing, recurring charges and delivery capacity.
Provider route: exact mailbox/SMTP operator, applicable terms, API/webhook plan, cancellation behaviour, domain ownership and portability.
Eligible inventory: how many records survive identity, provenance, recipient-policy, legal, language, evidence and verification checks—not merely how many contain an email.
Spec contradictions: app-wide versus per-inbox ramp; campaign sends versus new contacts; Tue–Thu versus Monday rescheduling; compliance-link exceptions; ongoing human QA.
Legal sign-off: Indian sourcing/privacy approach, treatment of personal mailboxes, overseas subscriber categories, cross-border processors and later synthetic-media use.
Evidence quality: recheck standards for outages, mobile usability and forms; treatment of crawler blocks; contamination from fabricated discovery outputs.
Autonomy evidence: representative labelled replies, critical-error tests, permitted auto-reply categories and escalation rules.
Commercial validation: actual qualified-reply rate, paid conversion, acquisition cost, delivery margin and the incremental value of snapshots/audio.


---

## Claude Code - 2026-11-12 03:53 UTC - 02_claude.md - attachments: none

# Claude Code - round 2 - verdicts, a second persona panel, 5 questions

## Verdicts on your round 1
| # | Your point | Verdict |
|---|---|---|
| 1 | Simulated personas are hypotheses; split industry / reader / device / legal status; consenting-reader test: 10 business readers, 8 of 10 explain sender, reason, offer, next action after 5 s | agreed. A separate Claude subagent ran an independent panel on the same samples (summary below) - it agrees with you on B's overclaims and adds structure points |
| 2 | Four separate questions (law / sending provider / receiving provider / reader); RFC 8058 HTTPS one-click endpoint with DKIM-covered headers; "no promotional links in touch 1, compliance links allowed"; punctuation bans are style, not spam science; pixels removed for privacy and unreliable measurement | agreed. Outlook correction accepted - it only bites above 5,000/day, far above this pilot |
| 3 | Snapshot page in 3 layers (5-second / evidence / optional detail), visible "Illustrative concept ... not an existing client project" label, transcript, no autoplay, licensed assets, removal route; raw requests vs filtered sessions vs actions (Microsoft link scanning); never "I saw you viewed"; keep the synthetic-voice ban, founder's own recording only, a reusable recording described as a general overview | agreed |
| 4a | Tiers: India first controlled pilot; US next reviewed pilot; UK corporate subscribers only; Canada case by case; Australia hold (harvesting rules); France later; all others hold | agreed. The persona panel independently rated US / UK / AU small-business recipients Ignore or Spam for all three samples |
| 4b | Eligibility record (identity -> provenance -> jurisdiction/recipient type -> legal/provider -> language -> fresh observation -> verification -> suppression -> capacity); recheck outages right before sending; NO_VIEWPORT is a signal, not proof; catch-all/unknown stay out | agreed |
| 4c | Capacity: 6 inboxes x 30 = 180/day, / 3 touches = 60 new prospects/day before reply reserve; X follows capacity; complaint data unknown shown as unknown | agreed - so 100 new/day needs at least 10 inboxes |
| 4d | Policy-conservative HOLD for every non-opted-in personal-mailbox (free-mail) recipient | **open - see Q1** |
| 5 | One authoritative scheduler in the app; recheck chain at execution; idempotent send records; uncertain attempts reconciled, not retried; failure types separated; no channel switch on bounce; Tue-Thu vs "weekend -> Monday" contradiction fixed as "next permitted local window"; GitHub Actions not the send clock; Instantly a candidate (I confirm §6.7(b) "another lawful basis recognized by applicable law" - my reading was incomplete; §4.6(g) Instantly owns its provisioned infrastructure) | agreed |
| 6 | The daily loop runs in the app; reconcile -> protect -> interpret (multi-label) -> prepare -> authorise; auto only for clear opt-out (suppress), out-of-office (pause), bounce (parse); everything commercial needs approval; 50 correct cases is no autonomy gate (zero-error upper bound ~5.8 %); labelled evaluation set + shadow period; zero missed opt-outs; a real sanitizer for emails/phones in thread text; untrusted inbound text | agreed |
| 7 | Stages 0-7 with exit gates; minimal reply processing before the first send; audit the DB for outputs of the fabricated-contact path; the pre-send failure tests you listed; budget = all costs; CAC vs contribution margin | agreed |

## Independent persona panel (Claude subagent, not shown my position) - key results
- Winner: the structure that puts the verified problem in the subject/preview (B's shape) after removing its
  overclaims; the SITE_DOWN variant is the strongest email for India ("is my site down?" makes the owner open it).
- A's preview is spent on "Hello ... team, I found ..."; the word "idea" reads as a pitch; "outline" sounds like more
  reading. Proposed CTA: "Shall I make a sample page for [Business] and send it here or on WhatsApp ([number])?" -
  the business starting a WhatsApp chat is its own opt-in.
- Price: keep it in India touch 1 (removes the "what will they charge" fear) but just before the question, not in
  line 1 (reads as an ad).
- Snapshot link helps in touch 2 only for the salon and coaching personas; hurts for practice managers, shared
  inboxes, trades, assistants (a stranger's link looks like phishing). Host it on the sending domain with the business
  name in the path; no shortener, no click-tracking redirect, not a shared subdomain like vercel.app.
- Audio attached to touch 1 hurts with every persona. Site-down leads: an address on a lapsed domain bounces - only
  send to an address that still accepts mail.

## Questions for round 2 (answer by number)
**Q1. Free-mail recipients.** 79 % of Indian records with an email are free-mail. I reject a blanket HOLD:
Gmail's Program Policies bind people sending FROM Gmail accounts; Google's sender guidelines ("don't send to people
who didn't sign up") govern how Gmail filters incoming mail - the consequence of ignoring them is spam placement and
domain reputation, which we measure and stop on, not a legal prohibition. India's DPDP core duties start 2027-05-13,
and its public-availability exclusion covers data made public by the data principal. Proposal: **Tier 1** = an
address found on the business's own website or own profile, with the source URL stored (the phase-14 finder already
does this) - eligible whether free-mail or not; **Tier 2** = an address only in the Overture listing, with no
source found on the business's own page - HOLD until confirmed. Agree, or give the specific rule that forbids Tier 1.

**Q2. The mailbox operator.** Google Workspace and Microsoft 365 AUPs ban unsolicited commercial mail; Instantly's
own provisioned mailboxes are owned by Instantly (§1.16, §4.6(g)); SES / SendGrid / Mailgun / Postmark / Brevo ban it.
Name a concrete mailbox or SMTP operator whose terms permit first-touch B2B email to published business addresses
(cite the clause), with domain ownership staying with the founders - or say plainly that none exists and what the
honest choice then is (e.g. accept Instantly-provisioned infrastructure as rented, or a self-run mail server).

**Q3. Hosting split for the pilot.** The founders run everything from a laptop. Proposal: the always-on parts - the
RFC 8058 unsubscribe endpoint and the snapshot pages - run on the existing website stack (Vercel + MongoDB Atlas) on
the sending domain; the lead-generator app on the laptop sends only during a supervised window and pulls the
suppression list before every send; move sending to a small always-on server before more than 40 new contacts a day
or any unattended sending. Agree, or what breaks?

**Q4. Final India touch-1 templates.** Give the three final touch-1 texts (SOCIAL_ONLY salon, NO_VIEWPORT coaching,
SITE_DOWN retail) that combine both panels: subject = business name + a neutral, checkable fact; first line = the
dated, bounded observation; price before the question; one question; 60-85 body words; sender, postal address,
one-line opt-out; no em dash. Use [Business], [domain], [date], [Sender], [WhatsApp].

**Q5. Exact pilot numbers for the spec lock.** Inboxes and domains at start; new first contacts per sending day in
weeks 1-4; the per-inbox ceiling incl. follow-ups; the reply reserve; and the numeric pause / stop / scale gates
(hard bounces, complaints, policy rejections, positive-reply rate definition and threshold, cohort size before any
increase).

End with the list of points still open.


---

## ChatGPT (Pro) - 2026-11-12 04:07 UTC - saved as 02_chatgpt.md

ChatGPT said:
Q1. Free-mail recipients

Agree with the two-tier approach, subject to the existing eligibility checks. I withdraw the blanket free-mail HOLD. I cannot cite a rule that prohibits an Indian business contact solely because the business publishes a Gmail address rather than an address on its own domain.

Your distinction between sending through Gmail and sending to Gmail is substantially correct. Google’s current Program Policies prohibit using Gmail to distribute unsolicited commercial mail, while directing external senders to its separate sender guidelines. Those incoming-mail guidelines advise against contacting people who did not sign up. That is not, by itself, an Indian statutory prohibition. It remains an explicit receiving-provider expectation, with filtering, blocking and reputation consequences. Policy text checked 12 November 2026; high confidence. 
Google Help
+2

The eligibility rule I would lock
Tier	Decision	Required evidence
Tier 1: business-published contact	Eligible for the India pilot, regardless of free-mail versus custom domain, after all other gates pass	Address visibly published on the business’s verified website or genuinely controlled public profile; source URL, capture date and supporting excerpt; business relevance; no conflicting contact restriction; successful verification; no suppression
Tier 2: listing-only contact	HOLD	Address exists only in Overture or another third-party listing, without sufficient first-party publication evidence
Uncertain identity or publication	HOLD	Unclear profile ownership, an employee’s apparently personal address, stale ownership, or conflicting business identities

“Eligible” means eligible for selection and review, not automatically READY. Publication is evidence of provenance; do not record it as consent.

The supplied specification says the finder stores source URLs from the business’s own website. That supports the first part of Tier 1, but it does not independently establish current business ownership or the legal significance of publication. 
Pasted text
 
Pasted text

DPDP: your date is correct, but preserve the precise exclusion

The commencement notification schedules the principal processing provisions for eighteen months after publication. MeitY’s subsequent official statement identifies 13 May 2027 as the full-enforcement date. High confidence on the date. 
meity.gov.in
+1

Section 3(c)(ii) excludes personal data made public by, or at the direction of, the individual concerned, or by someone legally obliged to publish it. Consequently, an owner publishing their own business contact is a stronger case than a company publishing an employee’s personal address without evidence of that employee’s involvement. High confidence on the statutory wording; application to particular records requires legal review. 
meity.gov.in

Do not encode “all data on a business website is outside DPDP.” Encode the actual publication circumstances.

One important limitation to “we measure and stop”

We cannot assume that the pilot will reveal all complaints or spam placement. Google says low-volume Postmaster data may be omitted. It also explains that a low reported-spam rate can coexist with poor delivery because messages are already being filtered into spam. 
Google Help

Therefore, I accept Tier 1 free-mail recipients for a bounded, supervised pilot with documented receiving-provider risk acceptance. I do not accept “no complaint appeared” as proof that Gmail considers the campaign acceptable.

Cost and test: this adds provenance review, not another mandatory subscription. Audit the first 30 selected records: every one must have reproducible first-party publication evidence. Track free-mail and custom-domain outcomes separately.

Q2. The mailbox operator

A concrete qualifying operator exists: Mailforge. “None exists” would be incorrect.

The specific permission

Mailforge’s Terms, §3.4(1), Sending Policy, state:

“The Services may be used for lawful commercial email outreach, including unsolicited business-to-business outreach where permitted by applicable law.”

The page is labelled “Last Updated 29th Dec 2025” and was checked on 12 November 2026. High confidence in the published permission; this is not a guarantee of campaign legality or delivery. 
Mailforge

The surrounding clauses require an unsubscribe link, prompt opt-out handling, clear identity, reasonable address verification and compliance with applicable law. Their wording does not turn public availability into consent or exempt a sender from jurisdiction-specific requirements. 
Mailforge

It is actual mailbox infrastructure, not merely a sequencer

The operator documents Mailforge and Infraforge as SMTP mailbox hosting on their own servers, rather than Google Workspace or Microsoft 365 mailboxes. It also documents SMTP/IMAP credential export. These are vendor-documented capabilities, not independently tested capabilities in this project. 
Salesforge
+1

Keeping the domains with the founders

Use this procurement arrangement:

Founders’ registrar account and registrant details → Mailforge mailbox hosting → founders’ application as the scheduler.

Register the domains independently. Retain registrar login, renewal control and recovery credentials. Connect the domains through the documented DNS/nameserver process rather than handing over the registrar account. Mailforge documents changing nameservers from the customer’s existing GoDaddy account, and its ownership explanation says domains remain the customer’s. 
SalesForge Help
+1

The distinction is:

The founders control the domains and application. They rent the mailbox service.

Before purchase, verify that the chosen arrangement permits the Vercel website records to coexist with the mail records, and test mailbox export and DNS recovery. Do not interpret an “Export to Instantly” button as proof that historical mailbox contents are backed up.

Cost and remaining acceptance tests

Mailforge currently publishes $3 per mailbox slot per month with a minimum of ten slots. That implies a $30/month mailbox minimum, before taxes, domains and extras, even when only six mailboxes are active. Pricing checked 12 November 2026. 
Mailforge

My proposed acceptance tests are:

Send through the application, receive through IMAP, and reconcile a controlled failure.
Confirm that both unsubscribe headers survive transport and are covered by a valid DKIM signature.
Confirm the founders retain registrar control and can preserve the website’s DNS records.

Two alternatives do not pass the same test: Mailreef’s §27(1) requires express permission despite its cold-email positioning. Maildoso’s published guidance specifically excludes personal/consumer-domain recipients such as Gmail, so it does not fit the proposed Tier 1 free-mail segment. 
Mailreef
+1

Decision: Mailforge is the documented default candidate. There is no need to accept Instantly-owned domains or self-host SMTP merely because no permissible operator can be named. A self-run server would also introduce maintenance and hosting-policy questions rather than remove them.

Q3. Hosting split for the pilot

Agree with a supervised laptop sender. Disagree that an unsubscribe endpoint, snapshot pages and a downloaded suppression list are sufficient by themselves.

The split can work without moving the whole application to a server immediately.

What must be authoritative in the cloud

MongoDB should hold the authoritative suppression state, including unsubscribe, complaint and manual do-not-contact decisions. The laptop may cache information for display, but it must not authorise a send from a cached “not suppressed” result.

Immediately before each submission, the worker must obtain a fresh, uncached eligibility result. An unavailable suppression service means no send, not “use yesterday’s list.”

Keep suppression independent of the local campaign database. Restoring an old laptop backup must never restore permission to contact someone.

Incoming replies need an explicit offline rule

“Reply stop” must work as well as the unsubscribe link.

Where the operator provides suitable events, receive and persist reply, bounce and complaint events on the always-on side. Where only IMAP is available, the supervised pilot needs:

A complete reconciliation before each sending session, continuous reconciliation while sending, and at least one reconciliation every 24 hours even on non-sending days.

That 24-hour interval is my proposed operational maximum, not a claim about a universal statutory deadline. If the founders cannot guarantee it, add a small always-on inbox poller from day one. That does not require moving the sender itself.

Simply checking inboxes on Tuesday, Wednesday and Thursday could leave a Thursday-night opt-out unprocessed until Tuesday.

RFC 8058 and Vercel routing

The endpoint must accept the prescribed HTTPS POST without requiring login, cookies or browser interaction. It must not redirect the POST. RFC 8058 also requires the relevant headers to be covered by a valid DKIM signature. Source: RFC 8058, January 2017; high confidence. 
RFC Editor
+1

My implementation requirements are:

Persist before success. Return success only after suppression is durably recorded; repeated requests must be harmless.

Separate GET from POST. A link scanner fetching the URL must not accidentally unsubscribe someone. A human-facing GET can show an unsubscribe control; the RFC POST performs the action directly.

Test the exact public URL. Domain forwarding, trailing-slash redirects, deployment authentication or bot challenges must not interfere.

Preserve mail and web DNS together. A mailbox provider’s automatic domain forwarding must not swallow the unsubscribe or snapshot paths.

The unavoidable send race

A fresh suppression check followed by an SMTP submission is not one atomic operation.

Use one outbound worker for the pilot, minimise the gap between check and submission, and cancel queued messages wherever cancellation remains possible. But an email already accepted for delivery cannot be assumed recallable.

The honest guarantee is:

No new submission after the worker observes a suppression. A message already in flight may still arrive.

Do not describe a simple list-pull design as guaranteeing zero messages after the exact instant someone clicks unsubscribe.

Vercel has two relevant conditions

Commercial use requires an appropriate paid plan; Vercel’s Hobby plan is restricted to non-commercial personal use. Its fair-use page was updated 14 September 2026. 
Vercel

Its AUP, updated 21 April 2026, also prohibits sending or creating unsolicited mass messages. Keep email generation and dispatch out of Vercel in this proposal. Ordinary website and suppression hosting should not be misrepresented as permission to run the outreach engine there; clarify scope with Vercel before expanding that role. 
Vercel

Migration trigger

Accept before 41 new first contacts per sending day, or before any unattended sending, as a project governance rule. Forty is not a technical safety boundary.

Move earlier when supervision, inbox reconciliation or recovery becomes unreliable. Assess total messages, not just new contacts: Q5 shows that 20 new contacts per sending day can eventually produce 120 scheduled campaign messages on a Tuesday.

Cost and test: this reuses the website stack but still requires monitoring, backups and the correct hosting plan. Acceptance test: switch the laptop off, submit an unsubscribe, restart the laptop, and prove that the pending message is blocked. Also test database failure, stale inbox state and restart after an uncertain SMTP result.

Q4. Final India touch-1 templates

Agree with B’s observation-first structure after removing its overclaims. The independent panel strengthens that design hypothesis; it does not establish a winning subject line or actual country-level response behaviour.

I am retaining ₹7,999 from the supplied examples. Before activation, the approved offer must confirm that price, scope, tax treatment and separate domain/hosting charges. The examples themselves are not price authorisation. 
Pasted text

The body word counts below exclude the signature and opt-out, with each placeholder counted as one word. Validate again after substitution.

A. SOCIAL_ONLY salon

Subject: [Business]: no website link in Instagram bio

On [date], the Instagram profile for [Business] showed no website link when I checked its bio.

I’m [Sender] from SiteBlitz, a small web studio in Gujarat. We build simple pages showing salon services, prices, opening hours and appointment enquiries.

Website setup starts at ₹7,999, with domain and hosting charged separately.

Shall I make a sample page for [Business] and send it here?

[Sender] | SiteBlitz
[Reply address] | [Postal address]
WhatsApp: [WhatsApp]

Reply “stop” or unsubscribe here: [unsubscribe URL].

Body: 62 words. Use only when the specific Instagram bio was checked. Do not substitute an Instagram observation for an unrelated social profile.

B. NO_VIEWPORT coaching

Subject: [Business]: homepage viewport setting

On [date], the homepage at [domain] had no mobile viewport setting in the page source I checked. That alone does not prove a display problem.

I’m [Sender] from SiteBlitz, a small web studio in Gujarat. We build mobile-friendly pages showing courses, timings and enquiry details.

Website setup starts at ₹7,999, with domain and hosting charged separately.

Shall I make a sample page for [Business] and send it here?

[Sender] | SiteBlitz
[Reply address] | [Postal address]
WhatsApp: [WhatsApp]

Reply “stop” or unsubscribe here: [unsubscribe URL].

Body: 68 words. This subject is less compelling than “your site is difficult to use,” but the available observation does not support that stronger claim. A documented visual problem would justify a different, more understandable subject and opening.

C. SITE_DOWN retail

Subject: [Business]: [domain] did not load in our checks

On [date], the homepage at [domain] did not load in two checks from separate connections. The interruption may be temporary.

I’m [Sender] from SiteBlitz, a small web studio in Gujarat. If you need a replacement, we build pages showing your showroom, products and enquiry details.

Website setup starts at ₹7,999, with domain and hosting charged separately.

Shall I make a sample page for [Business] and send it here?

[Sender] | SiteBlitz
[Reply address] | [Postal address]
WhatsApp: [WhatsApp]

Reply “stop” or unsubscribe here: [unsubscribe URL].

Body: 68 words. This requires two actual checks from separate connections, not two retries through the same crawler. Recheck immediately before dispatch. A block or challenge page is not sufficient evidence for this wording.

The price here is explicitly for a possible replacement website, not a promise to repair an unknown outage for ₹7,999.

Three implementation decisions

One primary action: keep “make a sample and send it here.” This avoids asking the recipient to choose a channel before expressing interest. [WhatsApp] is the studio’s number, not the prospect’s scraped number.

WhatsApp remains recipient-initiated: an inbound request supports responding to that request; it is not blanket permission for future marketing. WhatsApp’s policy requires appropriate permission and respect for opt-outs. 
WhatsApp for Business

The unsubscribe URL is mandatory for the proposed operator: the no-promotional-link rule must not remove it. Also preserve RFC 8058 headers outside the visible body.

Treat SITE_DOWN and MAIL_UNDELIVERABLE as separate eligibility results. An unavailable website should trigger fresh mailbox and identity checks, not an automatic conclusion that every address on that domain will bounce.

Cost and test: producing samples becomes a delivery obligation once accepted. Approve the sample scope before activating this CTA. Run the already-agreed ten-reader comprehension test; retain the eight-of-ten threshold.

Q5. Exact pilot numbers for the spec lock

Agree to a numerical lock, but distinguish a small technical ramp from evidence-based commercial scaling. The following numbers are proposed operating rules, not provider guarantees or statistically proven optimums.

A. Infrastructure and capacity
Setting	Locked proposal
Sending domains at launch	2 founder-controlled domains
Active mailboxes	6 total, 3 per domain
Identity	Real founders or clearly identified role mailboxes; no invented employees
Sender continuity	One business remains with one sender throughout its sequence
Per-mailbox hard ceiling	30 outbound messages per calendar day, including first touches, follow-ups, replies and tests
Reply reserve	5 messages per mailbox per day, unavailable to campaign scheduling
Maximum scheduled campaign messages	25 per mailbox; 150 across six
Automatic warm-up traffic	None in this pilot
Campaign sending days	Tuesday–Thursday
Campaign windows	09:00–11:30 and 14:00–16:30 recipient time
Cadence	Day 1 / 6 / 14, moved to the next permitted window with capacity
Catch-up behaviour	Never exceed a cap to clear missed sends

A reply reserve is not a limit on the number of replies the founder may handle. If replies need more capacity, reduce campaign sending while retaining the 30-message ceiling.

Buying ten Mailforge slots does not authorise ten active senders; the pilot starts with six.

B. Weeks 1–4

“Week 1” begins only after the launch gates pass. These are ceilings, not quotas.

Pilot week	New first contacts per sending day, app-wide	Maximum new contacts that week	Busiest scheduled campaign day, assuming no replies or stops*
1	10	30	10 messages
2	15, only after the first ramp gate	45	45 messages
3	20, only after the second ramp gate	60	85 messages
4	20; no automatic increase	60	110 messages

*Calculated using Day 1/6/14, Tuesday–Thursday sending and no holidays. Replies would cancel subsequent cold touches.

Maximum first contacts in four weeks: 195. A failed gate holds the current stage or pauses sending; the calendar does not force an increase.

C. Minimum evidence before either initial increase

For 10 → 15 and 15 → 20, require:

At least 30 distinct first-contact recipients from the immediately preceding stage, each observed for at least 72 hours, with:

Zero observed hard bounces, complaints or policy rejections in that ramp cohort.
No unresolved delivery uncertainty, suppression failure or inbox-reconciliation gap.
Successful authentication/header checks and explicit founder approval.

These two increases are technical calibration, not evidence of commercial success.

A 21-day positive-reply gate cannot honestly govern a week-two increase. Therefore, the 3% commercial gate begins before increasing beyond 20, not before the initial calibration steps.

D. Exact pause and stop rules

Here, pause means stop the affected activity pending review. Stop means retire or rebuild the affected campaign/source configuration before restarting. Neither permits switching domains to evade the failure.

Signal	Automatic pause	Stop / rebuild condition
Hard bounce: invalid recipient	First confirmed hard bounce: suppress the address and pause the affected sourcing batch	2 hard-bounced recipients within the latest 100 distinct recipients attempted, including an initial window smaller than 100
Complaint	1 credible complaint, or an available provider-reported spam rate ≥0.10%: pause the pilot and investigate	2 credible complaints within 30 days, or provider-reported spam rate ≥0.30%: stop the current pilot campaign
Permanent authentication/policy rejection	1 rejection: pause the affected sending domain or receiving-provider route; do not classify it as an invalid address	3 policy rejections within 24 hours, or an explicit operator suspension: stop the affected configuration
Suppression or send-integrity failure	1 known submission to an already-observed suppressed recipient, 1 duplicate, or 1 unapproved submission: pause all campaign sending	Root-cause fix and regression tests required before restart
Unavailable/stale state	Suppression lookup unavailable, inbox reconciliation incomplete, or previous SMTP result unresolved: zero further affected sends	No time-based automatic restart
Sales-handling backlog	An interested enquiry remains unhandled for more than one business day: pause new first contacts	Resume only after the backlog is cleared

Count a recipient once for hard-bounce-rate purposes; follow-ups must not inflate the denominator and make the rate look better. Update the recipient’s outcome when a delayed bounce arrives.

A normal “not interested” or “stop” response is a suppression event, not automatically a spam complaint.

Google’s published reference points are below 0.10% reported spam and avoiding 0.30% or higher. Our first-complaint pause is deliberately stricter for this small pilot. 
Google Help

E. Positive-reply definition and commercial scaling

Use:

Positive-reply rate
=
Distinct mature prospects giving a positive human reply
Distinct mature first-contact prospects not known to have bounced
Positive-reply rate=
Distinct mature first-contact prospects not known to have bounced
Distinct mature prospects giving a positive human reply
	​


“Positive” means requesting the sample, requesting relevant price/scope details, agreeing to a substantive next step, or expressing a current relevant need.

Exclude auto-replies, acknowledgements, opt-outs, “not now,” and a gatekeeper merely supplying another address. Count each prospect once. This is a non-bounced-prospect metric, not a claim of inbox delivery.

A cohort is mature on Day 21, provided at least seven days have passed since its last actual campaign message. If capacity or calendar shifts delay the final touch, maturity shifts too.

Before any increase above 20 new contacts per sending day, require:

Gate	Requirement
Mature cohort	At least 100 distinct prospects
Positive replies	At least 3%, meaning at least 3 of 100
Hard bounces	≤1%, with all incidents investigated
Complaints	No unresolved observed complaints; available provider-reported rate <0.10%
Technical state	No unresolved policy, authentication, suppression or reconciliation issue
Capacity	Future follow-up slots and reply reserve already booked
Approval	Explicit founder approval

Then increase by at most 5 new contacts per sending day. Require a new, non-overlapping mature cohort of at least 100 before another commercial increase.

At 100 mature prospects:

Zero positive replies: stop that campaign version and revisit targeting, evidence or offer.

One or two positive replies: hold volume and test a revision at the same ceiling.

Three or more: eligible for a controlled increase only when the other gates pass. Three of 100 is a decision threshold, not proof that the underlying response rate exceeds 3%.

Unknown complaint data blocks automatic commercial scaling. It does not automatically invalidate the supervised pilot, but the dashboard must say “unknown.” A founder can authorise another bounded cohort at the existing ceiling rather than pretending the complaint-rate gate has been demonstrated. Google explicitly warns that low-volume data may be missing. 
Google Help

F. Correction to “100 new/day needs at least ten inboxes”

Ten is only a no-reserve, average-volume lower bound.

With the proposed five-message reply reserve:

⌈
100
×
3
30
−
5
⌉
=
12
 inboxes minimum on an average-capacity basis
⌈
30−5
100×3
	​

⌉=
12 inboxes minimum on an average-capacity basis
	​


There is also a calendar concentration problem. At a steady 20 new prospects every Tuesday, Wednesday and Thursday, strict next-permitted-day scheduling produces:

Day	First touches	Second touches	Third touches	Total
Tuesday	20	60	40	120
Wednesday	20	0	20	40
Thursday	20	0	0	20

This fits the proposed six-inbox capacity.

At 100 new prospects per sending day, that same strict Tuesday pattern becomes 600 campaign messages, requiring 24 inboxes at 25 campaign messages each if nothing may spill into Wednesday or Thursday.

That is not a recommendation to buy 24 inboxes. It is the reason to book follow-ups against actual future capacity. Twelve inboxes is an average-capacity minimum, not an unconditional promise that the original calendar will fit.

The pilot should lock 10 → 15 → 20 → 20, prove the conversation economics, and resolve scheduling capacity before discussing 100.

Points still open
Actual offer and identity: approved price, tax treatment, sample-page scope, sender identities, reply address and postal address.
Mailforge acceptance tests: retained domain control, coexistence with website DNS, SMTP/IMAP behaviour, header preservation and DKIM coverage.
Cloud scope: appropriate Vercel plan, its permitted role, and the authoritative suppression design.
Offline reply handling: operator events versus daily IMAP reconciliation, with an always-on poller required if the 24-hour maximum cannot be maintained.
Tier 1 evidence: verification of business-controlled publication, treatment of employee addresses, and legal review of the Indian sourcing approach.
Measurement coverage: which complaint and delivery signals are genuinely available, with missing data explicitly retained as unknown.
Commercial validation: consenting-reader results, observed results by template and mailbox family, sample-production cost, paid conversion and contribution margin.
