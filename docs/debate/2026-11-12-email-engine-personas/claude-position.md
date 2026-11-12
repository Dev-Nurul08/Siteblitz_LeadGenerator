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
