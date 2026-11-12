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
<file path="docs/outreach/pilot-templates.md">
# PILOT_EMAIL_TEMPLATES - email engine v2, India controlled pilot (phase E3)

Status: built in phase E3 (founder `go for all`, 2026-11-12). Sources: `docs/spec/email-engine-v2.md` rows 4-6,
`docs/debate/2026-11-12-email-engine-personas/RESULT.md` rows 13 and 16 and section C (reference touch-1 texts),
`company-facts.md` (price, demo table, WhatsApp). The observation sentences are the ones E1 stores
(`backend/app/engines/eligibility/rules.py`: `social_only_text`, `site_down_text`, `no_viewport_text`), copied word
for word by the writer; nothing here re-words them.

How it is used:
- The AI writer still writes every message. The block below is attached to every writer request as
  PILOT_EMAIL_TEMPLATES, next to the system prompt, COMPANY_FACTS, COUNTRY_LANGUAGE and REFERENCE_MESSAGES.
- The batch screen (`POST /api/v1/outreach/batches`) sends one TASK per touch with a `pilot` object (below). For a
  pilot task these rules replace STEP 5 "email, touch 1/2/3" of the system prompt and the email examples in
  `reference-messages.md`. Every other rule stays (language, banned phrases, punctuation, facts, honesty).
- The validator (`backend/app/engines/writer/validator.py`, `pilot_email_errors` and `assembled_pilot_errors`)
  re-checks every rule listed at the end of this file. A failure gets one rewrite, then HOLD `VALIDATION_FAILED`.
- The app, not the model, adds the signature block and the unsubscribe line. The unsubscribe URL is made by E2's
  message builder at send time (`backend/app/engines/sending/message.py`); until then the stored text carries the
  placeholder `[unsubscribe link added when sent]`, which the builder always replaces.

---

```text
PILOT EMAIL TEMPLATES (India controlled pilot). They apply when TASK.pilot is set. For that task they replace
STEP 5 "email, touch 1/2/3" and the email examples in REFERENCE_MESSAGES. Every other rule above still applies.

TASK.pilot carries:
  "template": "T1" | "T2" | "T3"
  "observation_type": SOCIAL_ONLY | SITE_DOWN | NO_VIEWPORT
  "observation_sentence": the dated observation, checked and written by the app. Copy it word for word.
  "identity_line": "I'm <sender> from SiteBlitz, a small web studio in Gujarat."
  "price_line": "Website setup starts at ₹7,999, with domain and hosting charged separately."
  "question": "Shall I make a sample page for <Business> and send it here?"
  "vertical": salon_beauty | coaching_tuition | retail_showroom | other
  "vertical_page": what a page shows for this vertical (COMPANY_FACTS demo table), and "customer_word".
For T2 and T3, LEAD.thread holds the touches already written for this business, oldest first.

A pilot email has no greeting, no sign-off and no opt-out line of its own: set "signoff" and "opt_out_line" to
null. The app adds this block under every pilot email:
  <sender> | SiteBlitz
  <reply address> | <postal address>
  WhatsApp: <studio WhatsApp>

  Reply "stop" or unsubscribe here: <unsubscribe link>
There is no other link in a pilot email: no demo link, no website link, no shortener.

T1 (Day 1). "body" has 60-85 words.
  subject: "<Business>: " followed by a neutral fact the owner can check in ten seconds, 3-8 words, plain, no "?"
  or "!", no "Re:" or "Fwd:". Business name exactly as in LEAD.
  body, in this order, paragraphs separated by one blank line:
    1. observation_sentence, word for word. It is line 1; nothing comes before it.
    2. identity_line, word for word, then one sentence on what we build for this vertical, made from
       vertical_page in plain words. For SITE_DOWN start that sentence with "If you need a replacement, ". For
       NO_VIEWPORT say "mobile-friendly pages".
    3. price_line, word for word.
    4. question, word for word. It is the only question and the last sentence.
  Nothing else: no second offer, no other price, no claim about results.

T2 (Day 6, same thread; the app sends it as "Re: <touch 1 subject>"). "body" has 40-70 words.
  Text only. Offer the sample page again and add one new, useful piece of information that touch 1 did not give:
  what the sample page would show for this vertical (vertical_page), and the WhatsApp and call buttons that the
  Launch package includes. Do not say "just following up", "checking in", "circling back", "bumping" or refer to
  "my last email". Exactly one question, at the end, offering to make and send the sample page.

T3 (Day 14, same thread). "body" has 30-50 words.
  A polite close: you will close this and not write again, they can reply here any time for the sample page and
  the prices, thank them for their time, and a last line meaning "No further follow-ups are planned." No pressure,
  no deadline, no discount, no question needed.

Reference texts. Words in [brackets] are filled from LEAD and TASK. Match the shape, do not copy the vertical
sentence word for word for another vertical.

T1, SOCIAL_ONLY, salon_beauty (body 64 words with a one-word name and a date such as "12 November 2026")
Subject: [Business]: no website link in Instagram bio
On [date], the Instagram profile for [Business] showed no website link when we checked its bio.

I'm [Sender] from SiteBlitz, a small web studio in Gujarat. We build simple pages showing salon services, prices, opening hours and appointment enquiries.

Website setup starts at ₹7,999, with domain and hosting charged separately.

Shall I make a sample page for [Business] and send it here?

T1, NO_VIEWPORT, coaching_tuition (body 66 words, same counting)
Subject: [Business]: your homepage on a phone
On [date], the homepage at [domain] opened zoomed-out on a phone screen in our check, so the text showed very small.

I'm [Sender] from SiteBlitz, a small web studio in Gujarat. We build mobile-friendly pages showing courses, timings and enquiry details.

Website setup starts at ₹7,999, with domain and hosting charged separately.

Shall I make a sample page for [Business] and send it here?

T1, SITE_DOWN, retail_showroom (body 74 words, same counting)
Subject: [Business]: [domain] did not load in our checks
On [date], the homepage at [domain] did not load in our checks, the last one shortly before this email. The interruption may be temporary.

I'm [Sender] from SiteBlitz, a small web studio in Gujarat. If you need a replacement, we build pages showing your showroom, products and enquiry details.

Website setup starts at ₹7,999, with domain and hosting charged separately.

Shall I make a sample page for [Business] and send it here?

T1, SOCIAL_ONLY, other (body 62 words, same counting)
Subject: [Business]: no website link in Instagram bio
On [date], the Instagram profile for [Business] showed no website link when we checked its bio.

I'm [Sender] from SiteBlitz, a small web studio in Gujarat. We build simple pages showing your services, location and contact details.

Website setup starts at ₹7,999, with domain and hosting charged separately.

Shall I make a sample page for [Business] and send it here?

T2, salon_beauty (46 words)
One more detail about the sample page for [Business]. For a salon, it would show your services with prices, an appointment request and your timings, with WhatsApp and call buttons so clients can reach you from their phone. Shall I make it and send it here?

T3, any vertical (39 words)
I'll close this today so I don't keep writing. If a website becomes useful for [Business] later, just reply here and I'll send the sample page and the prices. Thank you for your time. No further follow-ups are planned.
```

---

## What the validator re-checks for a pilot email (on top of the phase-13 checks)
Phase-13 checks that stay: decision / hold reasons, country + declared language + `langdetect`, banned phrases,
"AI", em dash / en dash / `!` / `;`, unresolved `[..]` / `{{..}}` / `TO FILL`, the facts guard (every number and
domain must be in COMPANY_FACTS, LEAD or TASK), the observation type, and MISSING_COMPANY_FACT before any call.

| Rule | T1 | T2 | T3 |
|---|---|---|---|
| Body words | 60-85 | 40-70 | 30-50 |
| Link in the model's text (subject, body) | none | none | none |
| `signoff` / `opt_out_line` | null | null | null |
| Line 1 = the E1 observation sentence, word for word | yes | - | - |
| Identity line right after it, word for word | yes | - | - |
| A sentence on what we build for the vertical between identity and price | yes | - | - |
| Exact price line just before the question (India) | yes | - | - |
| Exactly one `?`, the question is the last sentence, word for word | yes | one `?`, last | - |
| Subject `<Business>: <fact>`, fact 3-8 words, no `?` / `!` / `Re:` | yes | (kept by the app) | (kept by the app) |
| Mentions the sample page | - | yes | - |
| No "following up" / "checking in" / "circling back" / "bumping" / "my last email" | - | yes | yes |
| No pressure words (limited, last chance, hurry, urgent, only this week, act now, offer ends, deadline, discount, don't miss) | yes | yes | yes |

The 100-words-with-signature cap of the outreach spec (row 5) is not applied to pilot emails: spec v2 row 5 fixes
the body at 60-85 words and adds two signature lines (WhatsApp, unsubscribe), so the cap would depend on the length
of the postal address. Decision recorded in `docs/outreach/e3-notes.md`.

On the assembled text the app stores for sending (`assembled_pilot_errors`): the signature block is present
(`<sender> | SiteBlitz`, `<reply> | <postal>`, `WhatsApp: ...`), the last line is
`Reply "stop" or unsubscribe here: <URL or the placeholder>` exactly once, and there is no other URL anywhere.

</file>
</project_context>

<topic>
# Topic - pre-send persona review of the FINAL pilot email templates (launch gate h) - 2026-11-12

Context: SiteBlitz (two developers, "a small web studio in Gujarat", no clients yet) will start a supervised
India-only cold email pilot: 10 new businesses per sending day, Tue-Thu, three touches (Day 1 / 6 / 14). Every
lead has a dated, verified observation; the most common one in the real pool is NO_VIEWPORT (the business's own
homepage opened zoomed-out on a 390 px phone in a rendered check; screenshot stored). An AI writes each email inside
the fixed templates below; a validator enforces them. The app adds the signature block and the unsubscribe line.
These templates were agreed in two earlier rounds with you today; this is the pre-send review the spec requires
(gate h: "a synthetic persona review of every template, ChatGPT + Claude"). A real 10-reader test follows later.

The attached file pilot-templates.md has the exact templates and validator rules.

## Agenda
1. For each persona, read T1 (all three observation variants), T2 and T3 as that person on a phone, and give a
   table: persona x template -> can they state in 5 seconds (a) who is writing, (b) why, (c) what is offered, (d)
   what to do next (yes/no each); trust 1-5; spam-likeness 1-5; Reply / Maybe / Ignore / Spam.
   Personas: P1 salon owner in Surat (Gujarati/Hindi first, reads English slowly), P2 coaching-class admin who
   forwards to the owner, P3 retail showroom owner whose site lapsed, P5 restaurant staff reading a shared info@
   inbox, P9 the owner's son/daughter managing the inbox, P10 Gmail's filtering (content only, new domain with
   SPF/DKIM/DMARC, 10 sends a day).
2. The NO_VIEWPORT T1 is the one most leads will get. Is "opened zoomed-out on a phone screen in our check, so the
   text showed very small" understood by a non-technical owner? Propose at most one better wording that stays
   strictly true to what was checked.
3. Up to 5 concrete changes (before -> after) that keep every locked rule: no link but the unsubscribe line, dated
   observation first, ₹7,999 line, one question, 60-85 / 40-70 / 30-50 words, no greeting/sign-off from the model.
4. Anything in the templates that is untrue, risky or likely to cause a spam complaint.

Answer each agenda point by number: agree / disagree because ... / need data: ... . End with the list of points
still open.
</topic>
