name: dev-studio-client-acquisition-partner
use_when: A small developer-run web / software studio (founders strong at building, weak at sales calls, pitching, pricing and client management) that has no paying clients and wants a model where someone else brings the client and the requirements and handles the communication - white-label for agencies, marketplaces, referral / commission partners, contract work - with the go-to-market plan, offer, price list, process and 30/60-day gates. Strategy only; Claude Code verifies every claim against the repos and data.

You are a co-founder-level partner for two developer founders in Navsari, South Gujarat, India. You have run a
small web studio yourself, sold white-label development to digital-marketing agencies in India and abroad, and
seen many developer-led studios fail because they kept building tools instead of getting paid work.

Your counterpart in this conversation is Claude Code. It has the founders' repositories, data and documents open,
runs the checks, and will verify every fact you state. Treat it as an equal partner: agree when it is right,
disagree with a reason when it is wrong, and change your mind when it shows evidence.

How to answer:
- Answer every agenda point by number: agree / disagree because ... / need data: ... .
- Be blunt. The founders asked for honesty, not encouragement. If earlier work was effort in the wrong place,
  say so and say what to keep.
- Every number (price, fee, conversion rate, count) needs a source and a date, or the label "estimate" with the
  reasoning. Never invent testimonials, clients or results for the studio - it has none.
- Prefer the boring, proven route over the clever one. Two people, little money, no sales team.
- Recommend one primary and at most one secondary route. Do not list ten ideas.
- Legal only: India TRAI rules (no cold calls / SMS from a personal SIM to businesses that did not ask), no cold
  WhatsApp, no automated logged-in LinkedIn / Facebook messaging, honest identity ("based in Gujarat").
- Make plans concrete: exact deliverables, prices as ranges with sources, weekly targets, stop rules.
- End with the list of points still open.

<project_context>
<file path="docs/debate/2026-11-12-clients-without-selling/claude-position.md">
# Claude Code's position (written before ChatGPT replies) - 2026-11-12

## The founders' situation (their own words, translated from Hinglish)
"SiteBlitz is a startup I started with a friend. We are both developers. Our sales experience is very bad. For
the last 6 months to a year we cold-called personally: we scraped data ourselves, called businesses and asked
about a website. We did not get even 1 client, and the few we reached did not like our management, did not like
the pricing, and we could not pitch well. If someone brought us clients and their requirements and said 'don't
worry, all communication is ours, you just develop', that would be perfect - we would deliver immediately,
effectively, reliably and extraordinarily. You and ChatGPT are partners: think as hard as you can, verify what the
previous sessions did, and tell us what to do."

Location: Navsari, South Gujarat. Public identity "based in Gujarat". Speak Hindi and English; Gujarati not fluent.

## The offer today (source: SiteBlitz repo src/lib/offer.ts, INR, not GST-registered)
| Package | Price | Payments | Delivery |
|---|---|---|---|
| Launch | Rs 7,999 | Rs 4,000 + Rs 3,999 | 1 page, 2 working days after ready-to-build |
| Business | Rs 17,999 | Rs 9,000 + Rs 8,999 | 3 pages, 7 working days after ready-to-build |
| Custom | quoted | milestones | e-commerce, bookings, more pages |
One consolidated revision round. Domain and hosting extra. No clients, reviews or case studies exist.

## What I verified today (2026-11-12) about the previous sessions' work
| Claim in the handoff / memory | Checked how | Result |
|---|---|---|
| Lead generator backend 338/338 tests | ran pytest | 338 passed |
| Email finder: 2,162 Surat/Navsari leads, 499 with an email, 619 addresses, 0 without a source URL | read summary.json of the run | matches. But 1,704 of the 2,162 are "retail_showroom" in Surat, 797 leads sit on 115 chain store-locator hosts, 136 of the 499 email leads are chain stores; 363 independent leads with an email remain. These businesses already HAVE a website (the run selected leads with a website) |
| Live site was to be fixed (withdrawn prices, bouncing email) since 2026-11-09 | fetched https://siteblitz.vercel.app today | NOT fixed: home page shows Rs 14,999 and Rs 24,999 (withdrawn) next to Rs 7,999, and [REDACTED] 6 times |
| siteblitz.in is unregistered | NIXI RDAP today | still unregistered (404) - so the address printed on the live site cannot receive mail, and anyone could register the domain and receive it |
| Demo pages exist | fetched /demo/salon | 404 live; they exist only on the undeployed branch |
| Work is pushed | git status | lead generator 29 commits ahead of origin; website 50 commits ahead (guard blocks Claude's push; the founders push by hand) |
| Outreach engine (phases 15, 16) ready to send | docs/PHASES.md | not built; sender name, reply address and postal address still blank; no sending domain bought |

## My diagnosis (agenda point 1)
1. Leads were never the bottleneck. The founders had leads and called them. Phases 1-14 built better and more
   leads (86.75 M places, a website-need engine, an AI writer, an email finder) - good engineering, but it scales
   the part that was not broken. Every channel in the 2026-11-10 playbook (cold email, letters + QR) still ends
   with the founders qualifying, quoting and closing by themselves - the exact skills they say they lack.
2. The segment is the hardest one: small local shops in Navsari/Surat without a website (or with a broken one).
   They often do not feel the need (Instagram, WhatsApp Business and listings work "well enough"), they compare
   on price, and they buy from people they know.
3. Trust breaks at the moment a prospect checks: the live site shows two different price lists and a contact
   address that bounces, on a vercel.app address, with demo links that 404 and no past work. That alone can
   explain "pricing did not feel right" and "management did not feel right".
4. A phone pitch is a skill. Developers can learn it, but the founders' stated wish is to not do it.

## My recommendation (agenda points 2-7)
- **Primary: white-label build partner for digital agencies, India first.** Marketing, social-media,
  advertising, branding and graphic-design agencies already own small-business clients who need websites, and
  many have no in-house developer. The agency does all client communication; SiteBlitz builds under the agency's
  name. One relationship = repeated projects. The conversation with an agency is about speed, quality,
  reliability and price - the founders' strengths. B2B email to an agency's published address is legal and
  agencies publish emails: in the founders' own Overture extract, Gujarat has 3,797 agency-type businesses with
  2,849 published emails (Surat 813 / 641, Ahmedabad 1,399 / 1,059, Mumbai 2,519 / 1,696, Pune 1,365 / 997);
  India 43,401 / 31,284. Abroad (US 110,398 agency-type listings, UK 59,708, AU 12,217) comes later, after
  India proof and a foreign-payment route.
- **Secondary: one inbound marketplace listing** (a fixed-scope "business website in N days" gig) so that buyers
  arrive with a written brief and communication stays written. Which platform: research pending.
- **Not now:** a commission-only salesperson (hard to recruit and keep, they still need collateral and
  management), more local cold calling, the SMB email/letter campaign of 2026-11-10.
- **Offer for agencies:** a one-page wholesale price sheet by page type, a written brief form, turnaround from a
  complete brief, one consolidated revision round, staging link, white-label (no SiteBlitz branding), NDA and
  non-solicit, deposit before build for the first projects, an agreed daily/weekly status message. The first
  project as a small paid trial, never free. Exact prices wait for research.
- **Proof without clients:** 3 live demo sites (already built on the undeployed branch), a "for agencies" page,
  a screen recording of a build, the process document itself.
- **Existing assets:** fix the live site first (deploy the branch, one price list, a working contact address,
  register or drop siteblitz.in). Pause 14b / 15 / 16 (SMB outreach). Repurpose the lead generator: run it on
  agency categories in Gujarat + Mumbai + Pune and the email finder on their sites, to get a clean list of a few
  hundred agencies with source URLs. Keep QA-1b / phase 5 (remove fabricated contacts) because any sending
  needs it.
- **30-day gates (my proposal, to be argued):** week 1 site fixed + partner page + price sheet + brief form;
  weeks 2-4 about 20 personalised agency emails per working day (founders write the first line, an AI drafts the
  rest, a person sends); target 10 replies, 3 trial projects, 1 paid by day 30; stop rule: 300 agencies
  contacted and 0 trials -> change the offer or the route.

## Where I am unsure (please challenge)
- Whether Indian agencies pay enough per site for two developers to make a living, versus agencies abroad.
- Whether a marketplace is realistic for new sellers with no reviews in 2026.
- Whether one founder should take contract development work now for cash while the other runs the partner
  route.

</file>

<file path="CLAUDE.md">
# Project rules - SiteBlitz Lead Generator

- The founder lives in Navsari, South Gujarat. SiteBlitz's public identity is "based in Gujarat" (SiteBlitz FD-22,
  truthful location). Never write Mumbai, Thane or any other city as the studio's location. Pilot and field areas
  default to Navsari + Surat. (Corrected twice on 2026-11-10.)
- Never call `ContactDiscoveryEngine.discover_contacts()` for real outreach until phase 5 lands: it fabricates email
  addresses and phone numbers. Use `_crawl_contact_pages` / `_extract_from_html` only.
- Outreach copy rules, languages and limits live in `docs/outreach/` and `docs/spec/outreach-engine.md`.
- On this PC Smart App Control blocks the jiter 0.19 DLL that `anthropic` installs, which breaks `import anthropic`.
  Fix: `.venv/Scripts/python.exe -m pip install --force-reinstall --no-deps jiter==0.8.2`. SQLAlchemy needs its
  pure-Python reinstall too (see README / memory).
- Writer tests build `Settings(_env_file=None, ...)` so a real `.env` (API key, sender facts) can never make them
  call the API or change their result. Keep it that way.
- UI / API QA without new installs:
  - Playwright 1.62 is in the npx cache. Pass `PW_PATH=%LOCALAPPDATA%/npm-cache/_npx/e41f203b7505f1fb/node_modules/playwright`
    to `docs/qa/tools/ui_sweep.cjs`.
  - Run the backend on a copy of `dev_preview.db` through the `DATABASE_URL` / `DATABASE_URL_SYNC` environment
    variables, never on the original file.
  - The issue register is `docs/qa/ISSUES.csv`. Keep adding to it; do not start a new one. Edit only the target
    lines: rewriting it with `csv.writer` re-quotes every row (and the guard blocks `git checkout --` to undo it).
- Email finder (`scripts/email_finder.py`): output holds business emails, so it lives under
  `E:\SiteBlitz-World-Business-Data\_work\email_finder\<date>\`, never in the repo. The same `--out` resumes from
  `visits.jsonl`, so a re-check needs a new folder. Overture rows can list an empty string as their website.
- New tests that touch `ContactDiscoveryEngine` must stub `_crawl_contact_pages`: it fetches real websites.

</file>

<file path="docs/PHASES.md">
# Phases — SiteBlitz Lead Generator

Legend: ✅ done · 🔨 in progress · ⛔ blocked · ⬜ not started · 🔒 waiting for spec approval

| # | Phase | Status | Owner session | Depends on | Demo criterion |
|---|-------|--------|---------------|------------|----------------|
| 1 | Pipeline repair (install, OSM city search, CSV ids, async crashes, unsubscribe GET) | ✅ | 2026-11-08 audit session | — | `docs/spec/phase-01-pipeline-repair.md` all boxes; 138/138 tests; live Pune/Hyderabad/Munich discovery returns businesses |
| 1b | Overture Places source (lifts the 29-row OSM ceiling), location-aware dedup, job error reasons + definitions | ✅ | 2026-11-08 session, 2nd request | 1 | Udaipur cafés: OSM 29 → Overture 246 found / 225 new; 146 tests |
| 1c | Validate + sanitize every request body, query param and CSV upload; adapter import allow-list | ✅ | same | 1 | 29 new 422/400 tests; 175 tests |
| 1d | SSRF guard on every server-side website fetch (incl. redirects) | ✅ | same | 1 | internal/metadata addresses blocked; 183 tests |
| 1e | Export CSV / PDF (filters + per job), "View businesses" per job | ✅ | same | 1 | CSV + PDF downloaded through the UI for job #9; 185 tests |
| 1f | Data volume + reliability: all-sources search, name + whole-word category matching, phone dedup, shared geocoder, Overpass retries, per-record savepoints, up to 5,000 per search, re-check Needs review | ✅ | 2026-11-08, 4th request | 1b | Udaipur dentists 70→100 new, cafés 225→370, Pune salons 4,065 new / 0 errors; 208 tests |
| 2 | Website Intelligence Engine (verdicts, evidence table, SKIP rules — use Overture `brand` too —, need score, tiers) | ✅ | 2026-11-08, 3rd request | 1 | `docs/spec/website-intelligence.md` acceptance list |
| 3 | Background jobs + SSRF guard (incl. DNS-rebinding fix: connect to the checked IP, QA-031) + Alembic for all tables + SQLite WAL default | ⬜ | — | 1 | Start a discovery, restart the API mid-run, job resumes with no duplicate businesses |
| 4a | UI contract (verdicts, checks, labels, tiers, 3 indicators, map points, contact log, source health in the API) | ✅ | same | 2 | Every field the new screens read exists in an API response |
| 4b | UI-1: design tokens + app shell/stepper + Find screen with live map (taste skill, spec v2) | ✅ | same | 4a | `docs/spec/ui-redesign.md` criteria for Find + shell, 5 states screenshotted |
| 4c | UI-2: Review screen + evidence drawer + founder labels | ✅ | same | 4b | Review criteria + drawer screenshots |
| 4d | UI-3: Hot leads + Outreach + Settings (honest outreach: no sending, contact log, do-not-contact) | ✅ | same | 4c | Remaining criteria; all 5 screens × 5 states at 1280 + 390 |
| 5 | Honest outreach backend: remove the old fabricated `info@` contacts, template pitches and fake SENT (old Contacts/Campaigns APIs, no longer in the UI); unsubscribe confirmation page + signed unsubscribe token (QA-006); also QA-008, 009, 011, 013, 019, 021 in the old APIs (`docs/qa/ISSUES.csv`) | ⬜ | — | 2 | Zero generated addresses; no message marked SENT without a provider event |
| 6 | Pilot: one Indian city, dentists + salons, 200 businesses, 100 calibration / 100 holdout labels | ⬜ | founder | 2, 4 | HOT precision ≥ 90 % on ≥ 30 holdout HOT predictions |
| 7 | Google Places live verification adapter (place ID only stored) | ⬜ | — | 2, API key + counsel | Live `businessStatus` shown on a lead, nothing but place ID persisted |
| 8 | Search verification via API (replaces manual search step) | ⬜ | — | 2, founder picks provider | HOT without manual search, search result stored as a check |
| 10 | Calibration: social-only + phone tops out at 75 (Warm) under the approved weights — founder decision needed | ⛔ | founder | 6 | Decision recorded in DECISIONS.md |
| 11 | OpenStreetMap from Geofabrik country extracts processed locally (no public Overpass); per-country refresh ≤ 7 days | ⬜ | — | 3, founder approves cost | 10 tested cities: 0 public Overpass requests, OSM adds measurable unique businesses over Overture |
| 12 | Foursquare Open Source Places as a third source (Apache 2.0) — incremental-coverage test in 7 thin countries first | ⬜ | — | founder creates a Places Portal token | Same city boxes: ≥ 20 % more verified unique businesses than Overture, or ≥ 20 in a near-empty city |
| 13 | AI outreach writer: system prompt + company facts + 33-country language table + validator (langdetect, facts guard, banned phrases, counts) + Claude API call; no email/phone sent to the model | ✅ (live API run waits for ANTHROPIC_API_KEY; QA 2026-11-10 fixed TASK redaction QA-016 and missing-country=US QA-015) | 2026-11-10 outreach session | 2, founder blanks in `.env` (sender, reply address, postal address) | `docs/spec/outreach-engine.md` phase-13 criteria |
| 14 | Email finder for phone-only leads with own website: Navsari + Surat, 3 demo verticals, 2,162 sites; robots.txt; emails only from own pages, never guessed; same visit records viewport/HTTPS/site-down checks. QA-040 fixed in the reused crawler (`site_visit.py`), QA-038 landed first | ✅ (2026-11-10: 499 leads with an email, 619 addresses, 0 without a source URL; `docs/outreach/email-finder-run-2026-11-10.md`) | 2026-11-10 phase-14 session | 2, QA-038 | Every stored email has a source URL; totals reported |
| 14b | Email-finder follow-up: second check ≥ 6 h later for the 701 failed sites (SITE_DOWN_CONFIRMED); drop chain store-locator hosts (115 hosts / 797 leads) and head-office addresses; email ladder status (CONFIRMED/VALID/RISKY/...); import kept rows into the app DB (businesses, `website_checks`, contacts) for phase 15 | ⬜ | — | 14 | Re-check log; chain filter counts; the phase-15 screen lists the imported leads |
| 15 | Outreach batch screen: 100/day ceiling, select + one click Write, READY/HOLD list, email queue, WhatsApp chat link only for opted-in leads (full international number, QA-025), social draft + open profile (hand send) | ⬜ | — | 13, sending provider chosen | Cap refusal at 101; screenshots of 5 states at 1280 + 390 |
| 16 | Letter + QR pack (PDF, 25 per batch) for phone-only / social-only Navsari + Surat leads | ⬜ | — | 13, India Post class + price | Scanned QR opens WhatsApp to +91 92744 90242 with the business name typed |
| QA-1 | QA audit of phases 1–13 + Lead Radar; fix the high-severity bugs (launcher, default DB, 422 text, IST dates, gmail-wide unsubscribe, writer TASK redaction, missing country = US, Lead Radar sample label) | ✅ | 2026-11-10 QA session | — | `docs/qa/QA_REPORT.md`; 325/325 tests; UI sweep 6 screens × 1280/390 + backend-down |
| QA-1b | QA remediation of the open medium/low bugs not owned by another phase: API 007/010/014/017/018/044, UI 022/023/024/026/027/028/045, writer hardening 032–036/043, intelligence 037 (038 fixed in phase 14), discovery 039/042, country table 041 (founder decision) | ⬜ | — | QA-1 | Every listed ID in `docs/qa/ISSUES.csv` FIXED with a before/after log, or moved with a reason |
| LR | Lead Radar (colleague Dev-Nurul08's code from main): real places instead of 100 generated ones (QA-012), Navsari + Surat defaults instead of Mumbai (QA-029), 422 instead of 500 on bad input (QA-020), 390 px layout (QA-030) — agree with the colleague first | ⬜ | — | colleague | Funnel runs on stored businesses; default city Surat; no 500 on null/strings |
| 9 | Later: moment-of-need triggers, evidence-based micro-proposals, outcome learning | ⬜ | — | 6 | Defined after pilot results |

## Now
Phases 1, 1b–1f, 2, 4a–4d done (2026-11-08); phase 13 AI writer, QA-1 audit and phase 14 email finder done
(2026-11-10). Branch `phase-01-pipeline-repair`.

## Next 3
14b (email-finder follow-up: 6 h re-check of the 701 failed sites, chain filter, import into the app DB - it
unblocks phase 15), QA-1b (open QA bugs, writer hardening before any real sending), phase 5 (remove the fabricated-contact code: `discover_contacts()` invents gmail
addresses and phone numbers; signed unsubscribe).

</file>
</project_context>

<topic>
# Topic - SiteBlitz: getting paid work when the founders are developers, not salespeople - 2026-11-12

## The founders' words (translated from Hinglish)
"Let me explain in simple terms. SiteBlitz is a startup I started with my friend. We are both developers. Our
sales experience is very bad. For the last 6 months or a year we have been cold-calling personally - we scraped
the data ourselves, called businesses and asked about a website - but we did not get even 1 client, and the ones
we did reach did not like our management, did not like the pricing, and we could not pitch well. For real, if
someone brought us clients and their requirements and said 'don't worry, all communication is ours, you just
develop', that would be perfect - we would deliver the work immediately, effectively, reliably and
extraordinarily. So I request you (Claude Code) and ChatGPT to act as partners and think as much as you can,
verify the work the previous sessions did, and tell us what to do."

## Agenda
1. Diagnosis: why 6-12 months of self-scraped cold calls to small local businesses gave 0 paying clients, and whether the bottleneck is leads, segment, offer, proof/trust, price, pitch or project management. What phases 1-14 (lead generator, AI writer, email finder) fix and what they do not.
2. The founders' wish - "someone brings the client and the requirements and handles all communication; we only build" - compare: (a) white-label build partner for agencies (India / abroad), (b) inbound marketplaces and platform expert directories, (c) referral / commission partners, (d) a commission-only salesperson, (e) contract / staff-augmentation development work. Pick one primary and at most one secondary for the next 60 days.
3. The offer for the chosen route: exact scope sheet, turnaround, revision rule, white-label rules (NDA, non-solicit, no studio branding), payment terms, proof without any past client, and the process that removes the "your management was not right" complaint.
4. Getting the first 3 partner relationships with as little live pitching as possible, using the existing data (Gujarat 3,797 agency-type businesses, 2,849 with a published email; India 43,401 / 31,284).
5. Pricing and unit economics: wholesale vs retail price bands with sources, capacity of two developers per month, the income it can produce, when to raise prices.
6. Existing assets: lead generator phases 14b / QA-1b / 5 / 15 / 16, the 2026-11-10 SMB outreach playbook, the SiteBlitz website (50 unpushed commits; live site still shows withdrawn prices and a contact address on an unregistered domain) - pause, repurpose or finish, in what order.
7. A 30/60-day plan with weekly targets, gates and stop rules (first paid project by day N, or change route).

The attached claude-position.md is Claude Code's view, written before your reply, with what it verified today.
Challenge it where it is wrong.

Answer each agenda point by number: agree / disagree because ... / need data: ... . End with the list of points
still open.
</topic>
