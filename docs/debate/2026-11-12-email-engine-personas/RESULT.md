# Review - email engine v2: personas, content, creative layer, worldwide sending, daily AI-run conversations - 2026-11-12 - 2 rounds - prompt: lead-intelligence-vision-partner

Inputs: claude-position.md, research-deliverability.md (Claude Code research pass), persona-panel-claude.md (an
independent Claude subagent panel that did not see Claude's position), 01/02 ChatGPT replies. Round 1 context was
25.5 KB: the last source lines of docs/spec/outreach-engine.md were cut by the 25 KB cap (only WhatsApp source links).
The ChatGPT browser refused connections for ~15 minutes (low memory, 4 sessions); it recovered without a restart.
Claude checked first-hand: Instantly terms (§1.10, §1.16, §4.3(b), §4.6(b)(g), §6.7(a)(b); Last Updated 2026-11-10),
Mailforge terms §3.4 (Last Updated 2025-12-29) and pricing page, the truthful website branch, the local databases
(0 contact rows in siteblitz_leads.db and dev_preview.db). Nothing was sent, bought, deployed or changed in code.
Stop reason: after round 2 every point is agreed or resolved; what remains open is founder data and acceptance tests.

| # | Point | Proposed by | Evidence | Claude's verdict | Status |
|---|---|---|---|---|---|
| 1 | Personas are hypotheses: industry, reader (owner / admin / assistant / staff), device and legal status are separate attributes; simulated reactions are not evidence | ChatGPT R1, panel | 01_chatgpt.md s1; persona-panel-claude.md | agreed | closed |
| 2 | Real check before launch: 10 consenting business readers see a template for 5 s; >= 8 of 10 must explain sender, reason, offer and next action | ChatGPT R1 | - | agreed (founders recruit) | closed |
| 3 | Four separate questions: is it lawful / does the sending provider allow it / will the receiving provider accept it / will the reader find it worth it. Gmail all-sender rules (SPF or DKIM, PTR, TLS, spam < 0.3 %), set up SPF + DKIM + DMARC + RFC 8058 from day 1; Outlook > 5,000/day rejects with 550 5.7.515 since 2025-05-05 (ChatGPT corrected the research) | ChatGPT R1, research | support.google.com/a/answer/81126; RFC 8058; Microsoft techcommunity 2025 | agreed | closed |
| 4 | No audio attachment, no AMP, no GIF in the pilot; the email must be worth reading without a click | both panels, ChatGPT R1 | panel: touch-1 audio hurts with every persona; AMP needs Google sender registration | agreed | closed |
| 5 | Opportunity Snapshot page in 3 layers with a visible "Illustrative concept ... not an existing client project" label, transcript, no autoplay, licensed assets, removal route; hosted on the sending domain, no shortener or tracking redirect; in the pilot only after a positive reply | ChatGPT R1, panel, Claude | panel: a stranger's link looks like phishing to practice managers, staff, trades, assistants | agreed | closed |
| 6 | Voice: keep the approved synthetic-voice ban; the founder's own recording, described as a general recorded overview if reused per vertical | ChatGPT R1 | EU AI Act Art. 50 from 2026-08-02 (deployer duty for deep fakes); India IT Rules 2026 bind intermediaries | agreed | closed |
| 7 | Countries: India controlled pilot; US next reviewed pilot (CAN-SPAM has no B2B exemption: identity, honest subject, advertising disclosure, postal address, opt-out); UK corporate subscribers only (PECR + UK GDPR); Canada case by case (CRTC conspicuous publication); Australia hold (Spam Act harvesting rules); France later (CNIL 2026-06-10); all others hold | ChatGPT R1 | FTC, ICO, CRTC, ACMA, CNIL pages cited by ChatGPT; panel rated US/UK/AU Ignore/Spam | agreed | closed |
| 8 | 86.75 M places are a discovery inventory, not a prospect list; eligibility chain: identity -> provenance -> jurisdiction/recipient type -> legal/provider -> language -> fresh observation -> verification -> suppression -> capacity; catch-all and unknown stay out | ChatGPT R1 | - | agreed | closed |
| 9 | Free-mail: blanket HOLD withdrawn. Tier 1 = address published on the business's own site or controlled profile (source URL, capture date, excerpt) - eligible whether gmail or own domain; Tier 2 = listing-only - HOLD; unclear identity - HOLD; publication is provenance, not consent | Claude R2, ChatGPT R2 | Gmail Program Policies bind senders using Gmail; sender guidelines govern filtering | agreed | closed |
| 10 | DPDP core duties from 2027-05-13; s.3(c)(ii) excludes data made public by (or at the direction of) the individual - an owner publishing their own business contact is stronger than an employee's address; audit the first 30 selected leads for reproducible first-party publication | ChatGPT R2 | MeitY notification 2025-11-13 | agreed - legal review still open | closed |
| 11 | SITE_DOWN: two checks from separate connections, recheck right before sending; a block / challenge page is not "down"; an address on a lapsed domain may bounce - check the mailbox separately | ChatGPT R1-R2, panel | - | agreed | closed |
| 12 | NO_VIEWPORT from page source is a signal, not proof; ChatGPT's source-based wording ("no mobile viewport setting ... does not prove a display problem") is accurate but unclear to owners | ChatGPT R2 | - | agreed with a change: email only after a rendered 390 px phone check shows the page zoomed-out (screenshot stored); otherwise HOLD | closed (Claude change, in spec row 4) |
| 13 | Touch anatomy: T1 relevance + one small next step (60-85 words), T2 new information (40-70), T3 close (30-50); summary folded into the first two sentences, not a separate "In short" block; compliance links allowed in T1, promotional links not; punctuation bans are style rules | ChatGPT R1-R2, panel | - | agreed; Claude: T2 text-only offering the sample in the pilot | closed |
| 14 | Mailbox operator: **Mailforge** - Terms §3.4(1) "lawful commercial email outreach, including unsolicited business-to-business outreach where permitted by applicable law" (Last Updated 2025-12-29); requires an unsubscribe link, prompt opt-out, clear identity, address verification; $3/mailbox/month, minimum 10 slots; founders keep the registrar account. Mailreef (§27(1) express permission) and Maildoso (excludes Gmail recipients) do not fit; Instantly-provisioned infrastructure stays Instantly's (§1.16, §4.6(g)) | ChatGPT R2 | Claude read Mailforge §3.4 and pricing first-hand; SMTP/IMAP access and export are not on the pricing page - acceptance test | agreed | closed (acceptance tests open) |
| 15 | Capacity: 2 domains x 3 mailboxes; 30/mailbox/day hard ceiling incl. everything; 5 reserved for replies; 25 campaign; no warm-up pool; Tue-Thu 09:00-11:30 + 14:00-16:30 recipient time; Day 1/6/14 moved to the next permitted window with capacity; never exceed caps to catch up; one sender per business. 100 new/day would need >= 12 mailboxes on average, and up to 24 if all follow-ups fall on Tuesday | ChatGPT R1-R2 | arithmetic in 02_chatgpt.md Q5 F | agreed | closed |
| 16 | Ramp 10 / 15 / 20 / 20 new per sending day (max 195 in 4 weeks); technical gates per step (>= 30 recipients observed >= 72 h, 0 hard bounces, 0 complaints, 0 policy rejections, founder approval); commercial gate above 20 (mature cohort >= 100: Day 21 + 7 days after its last message; >= 3 positive replies; hard bounce <= 1 %; complaints < 0.10 % or none unresolved; then +5/day max); pause/stop table; positive reply = asks for the sample, price/scope, a next step or states a current need (auto-replies, "not now", opt-outs, forwards excluded) | ChatGPT R2 | 02_chatgpt.md Q5 | agreed | closed |
| 17 | Hosting: laptop sender is fine for a supervised pilot; the authoritative suppression list lives in the cloud DB, asked fresh before every send (unavailable = no send); RFC 8058 POST endpoint persists before success, GET must not unsubscribe, no redirect; IMAP reconciliation at least every 24 h even on non-sending days (or an always-on poller); honest limit: a message already accepted may still arrive; Vercel Hobby is non-commercial and Vercel's AUP bans sending unsolicited mass messages - no sending on Vercel; move sending to a server before > 40 new/day or unattended | Claude R2, ChatGPT R2 | Vercel fair-use (2026-09-14) and AUP (2026-04-21) cited by ChatGPT | agreed | closed (website plan = founder decision) |
| 18 | The daily loop runs in the app: reconcile -> protect -> interpret (multi-label) -> prepare -> authorise; Claude Code `/start-day` shows a Roman-Hindi brief with real counts; ChatGPT is a weekly reviewer and second opinion on high-risk threads, never a daily dependency; "both models agreed" is not an authority | ChatGPT R1, Claude | - | agreed | closed |
| 19 | Autonomy: automatic only for clear opt-out (suppress), out of office (pause), bounce (parse); everything commercial needs approval; 50 correct cases is no gate (0 errors in 50 -> 95 % upper bound ~5.8 %); a labelled evaluation set incl. adversarial cases and a shadow period; 0 missed opt-outs; a real sanitizer for emails/phones in thread text; inbound text is untrusted | ChatGPT R1 | rule-of-three arithmetic | agreed | closed |
| 20 | Honest metrics: accepted, bounces, unique human replies, positive replies, samples, quotes, deposits, paid, CAC, margin; complaint data unknown is shown as unknown; no "opens"/"read"; page requests include security scanners (raw vs filtered vs actions) | ChatGPT R1 | Apple MPP; Microsoft link scanning; Google low-volume Postmaster gaps | agreed | closed |
| 21 | Launch gates and failure tests (truthful site live, sender facts, seed tests with header/DKIM checks on received raw mail, unsubscribe end-to-end incl. laptop off, the race/duplicate/timeout/restart/stale/unknown-country/model-down/auto-reply-loop/prompt-injection tests, provenance audit 30/30, 10-reader test, synthetic persona review, founder reads first 20) | ChatGPT R1-R2 | - | agreed | closed |
| 22 | Build order: truth and identity -> data integrity -> eligibility -> safety infrastructure (incl. minimum reply processing) -> batch + scheduler -> pre-send evaluation -> controlled pilot -> expansion (snapshot test, limited reply automation, more markets) | ChatGPT R1 | - | agreed, mapped to phases E0-E6 in docs/spec/email-engine-v2.md | closed |

## C. Reference touch-1 texts (India; ₹7,999 must match the live offer before activation)
**SOCIAL_ONLY salon** - Subject: `[Business]: no website link in Instagram bio`
> On [date], the Instagram profile for [Business] showed no website link when I checked its bio.
>
> I'm [Sender] from SiteBlitz, a small web studio in Gujarat. We build simple pages showing salon services, prices, opening hours and appointment enquiries.
>
> Website setup starts at ₹7,999, with domain and hosting charged separately.
>
> Shall I make a sample page for [Business] and send it here?

**NO_VIEWPORT coaching (Claude change: needs the rendered phone check)** - Subject: `[Business]: your homepage on a phone`
> On [date], the homepage at [domain] opened zoomed-out on a phone screen in our check, so the text showed very small. We kept a screenshot.
>
> I'm [Sender] from SiteBlitz, a small web studio in Gujarat. We build mobile-friendly pages showing courses, timings and enquiry details.
>
> Website setup starts at ₹7,999, with domain and hosting charged separately.
>
> Shall I make a sample page for [Business] and send it here?

**SITE_DOWN retail** - Subject: `[Business]: [domain] did not load in our checks`
> On [date], the homepage at [domain] did not load in two checks from separate connections. The interruption may be temporary.
>
> I'm [Sender] from SiteBlitz, a small web studio in Gujarat. If you need a replacement, we build pages showing your showroom, products and enquiry details.
>
> Website setup starts at ₹7,999, with domain and hosting charged separately.
>
> Shall I make a sample page for [Business] and send it here?

Every text ends with: `[Sender] | SiteBlitz` / `[Reply address] | [Postal address]` / `WhatsApp: [studio WhatsApp]` /
`Reply "stop" or unsubscribe here: [unsubscribe URL]`.

## Recommended next steps (not started - waiting for your go)
The spec lock `docs/spec/email-engine-v2.md` (20 rows, phases E0-E6). Answer `go` or `change <row>`.

## Points still open
- Founder data: real sender names, postal address, brand keep/rename, sending-domain names, website hosting plan,
  approved sample-page scope, 10 readers, 3 voice recordings.
- Mailforge acceptance tests: SMTP/IMAP from the app, DKIM coverage of both unsubscribe headers on received mail,
  registrar control kept, website DNS records unaffected.
- Legal review of the Indian sourcing approach and of employee addresses.
- Which complaint and delivery signals are actually available at this volume (missing = unknown).
- Real results: reader test, reply rates per template and mailbox family, sample cost, paid conversion, margin.
