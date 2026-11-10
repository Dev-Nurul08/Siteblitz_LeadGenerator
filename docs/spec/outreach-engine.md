# SPEC LOCK - Outreach engine: AI writer, email finder, batch screen, letter (phases 13-16)

Status: ✅ APPROVED 2026-11-10 (founder: "go for it"). Phase 13 built in the same session (see HANDOFF.md);
phases 14-16 not started.
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
| 17 | Letter (phase 16) | Writer text on the front. The back carries a sample homepage image and a QR code to `wa.me/919274490242` with the pre-filled text from `reference-messages.md`. Paper size waits for the India Post class and price | RESULT F, G |
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
- [ ] Phase 14: the run covers 2,162 sites. Every stored email has a source URL on the business's own site, and
      0 emails exist without one. Totals are reported: emails found, sites down, NO_VIEWPORT, NO_HTTPS,
      robots-blocked.
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
  https://faq.whatsapp.com/5957850900902049
- WhatsApp Terms of Service (effective 2021-01-04): no "bulk messaging, auto-messaging, auto-dialing", and no
  non-personal use unless authorised. https://www.whatsapp.com/legal/terms-of-service
- LinkedIn User Agreement §8.2 (effective 2025-11-03): no bots or automated methods to "send or redirect messages".
  https://www.linkedin.com/legal/user-agreement
- Facebook Terms §3.2 (effective 2025-01-01): no access or collection by automated means without permission, and no
  spam. https://www.facebook.com/terms.php
- "But you are free": Carpenter 2013 (Communication Studies 64) found an effect. Fillon et al. 2023 (Meta-Psychology)
  found no effect in the low-risk-of-bias studies. So the opt-out line is kept for respect and the law, not as a
  persuasion trick. https://open.lnu.se/index.php/metapsychology/article/view/2640
