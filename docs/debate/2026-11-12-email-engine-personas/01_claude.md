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
