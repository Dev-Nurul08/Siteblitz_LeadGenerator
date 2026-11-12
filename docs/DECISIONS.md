# Decisions — SiteBlitz Lead Generator (append-only)

## 2026-11-08 — audit + ChatGPT review round
- **OpenStreetMap is the stored discovery source; Google Places is only an optional live verification
  adapter.** Why: the Maps Platform terms allow storing only the place ID permanently, and scraping the
  Maps website breaks Google's terms. (debate RESULT row 1)
- **No automated logged-in scraping of Instagram / Facebook / LinkedIn / TikTok.** Social links come from
  listings and the business's own pages and are recorded as discovered/confirmed/rejected. Why: platform
  terms (LinkedIn explicitly) and account bans; a social profile alone never proves need. (row 2)
- **"No website field" is not evidence of "no website".** A HOT lead needs a verified website verdict
  including a search or recorded manual search. Why: OSM is incomplete; the old rule produced mostly false
  HOT leads. (rows 3, 3c)
- **Three indicators, not one score:** Website Need Score, Evidence Confidence, Outreach Readiness.
  Why: contactability and certainty were mixed into "need", and confidence was a fake constant. (row 4)
- **Claude's 45/25/15/15 formula rejected in favour of 60/20/10/10 (provisional).** Why: reviews, phone and
  category are not proof of need; calibrate on the pilot. (row 4a)
- **WhatsApp is never automated; sending stays disabled until a real provider confirms delivery.** Why:
  WhatsApp opt-in policy; the old code marked unsent messages as SENT. (row 5)
- **CSV source ids are a hash of the row's identity fields**, not the row number. Why: row ids collided
  across files and silently dropped new data. (phase 1)
- **City search in Overpass resolves an administrative relation inside the country and maps it to an
  area.** Why: city areas never carry `ISO3166-1`; the old query always returned 0. (phase 1)
- **Phase-1 bug fixes were built before spec approval** because the founder's request explicitly
  authorised fixing broken APIs and the fixes add no new values — they restore what the code already
  promised. Website-need logic and UI redesign wait for spec-lock approval.

## 2026-11-08 — second request (why 29, validation, export)
- **Overture Maps Places is the default discovery source.** Why: OSM's Udaipur data really has only 29 named
  cafés; Overture (CDLA-Permissive-2.0 / Apache-2.0, Meta + Microsoft + Foursquare) has 246, with phones for
  83 % of places and social links for 87 %. Read with DuckDB from the public S3 GeoParquet by city bounding box
  (one Nominatim lookup per job). Release folder pinned in `OVERTURE_RELEASE` (update monthly).
- **Two records are merged only at "same city" or "within 5 km" confidence (≥ 0.70)**, not "same name in the
  same country" (0.60). Why: different shops with common names were being lost.
- **Every input limit comes from the DB column size or an existing rule** (ISO alpha-2, verifier email regex);
  free-form `query_params` are an allow-list (`min_confidence`); `adapter_class` is an allow-list. Why: no
  invented numbers; arbitrary module import was possible through POST /sources.
- **CSV upload cap 15 MB** = 5,000 rows (existing max_results limit) × ~3 KB max row at DB column sizes.
- **Exports:** CSV = all stored columns, formula-prefixed cells neutralised (OWASP CSV injection); PDF via
  fpdf2 (pure Python). Exports with real business contacts are not committed to git.

## 2026-11-08 — third request ("go … complete everything")
- **Both specs approved by the founder's "go"**: website intelligence (phase 2) and the UI redesign v2
  (dark graphite + safety orange, Mona Sans + Geist Mono, motion + MapLibre + NumberFlow + Lucide).
- **Website checks run concurrently per batch** (25 businesses ≈ 35 s instead of minutes); the DB writes stay sequential.
- **Google links (g.co, google.com, business.site) and directories (Justdial, Practo, Zomato…) are listings, not
  websites** — found live: "Dr Shweta's … Clinic" was "Has own website" because its website field was a g.co link.
- **The old Dashboard / Businesses / Opportunities / Contacts / Compliance / Campaigns screens were removed**
  from the UI; their APIs remain but are not used by the app (the Contacts API still fabricates `info@` — phase 5).
- **Screenshots containing real businesses' contact data are not committed** (`.gitignore`).
- **Open (founder):** social-only + phone can never be Hot under the approved weights (max 75). Options:
  (a) keep — only no-website businesses are Hot; (b) count "its listed web address is a social profile" as the
  10-point business-problem signal (social-only + phone + confirmed open + dentist = 85 → Hot).

## 2026-11-08 — fourth request ("as much data per run as I targeted")
- **Default source = All sources (Overture + OpenStreetMap in one job).** Overlap is merged by source id,
  phone (last 10 digits, same city / ≤ 5 km) and name + place.
- **Category = whole word-parts of the category fields OR keywords in the business name** (categories.py).
  Fixes `%dent%` → student_union and `%tax%` → taxi; adds 27–54 % real matches.
- **OpenStreetMap searches the geocoded city box**, not the named boundary (the "Udaipur" boundary matched the
  whole district + same-named villages and timed out).
- **Each discovery record runs in a SAVEPOINT** (SQLite needs SQLAlchemy's BEGIN recipe, enabled in database.py).
- **Not done, needs a decision:** (1) treat "listed domain has no DNS record, confirmed by a second resolver" as
  Website down immediately instead of waiting 6 h (changes approved spec row 6); (2) widen the area beyond the
  city when it has fewer businesses than asked (measured gain small: Udaipur dentists 102 → 112 at 3× area).

## 2026-11-08 — fifth request (city test: India, Bangladesh, Afghanistan + top 50 countries, 10 ChatGPT rounds)
- **Geocoder takes the first settlement hit** (city / town / village / municipality) of 5, retries without the
  state when the state-qualified lookup only finds a landmark, and trims a city boundary larger than 1.5° to the
  1.5° square around the city's point (inside the boundary; the job and the Find screen show it). Found live:
  Beijing → a 1 × 2 km business district, Ho Chi Minh City → a TV station building, Shenzhen → rejected; all 0.
  After: Shenzhen 0 → 522 available. A state or district hit is still rejected, never trimmed.
- **A repeat search lists what it found again** (`source_job_sightings`). Before: a job whose records an earlier
  job had saved showed nothing under "View businesses", the map, export and website checks (Pimpri-Chinchwad:
  300 found, 19 listed, because its box overlaps Pune's).
- **Find screen offers all 249 ISO countries** (it had 10 — Bangladesh and Afghanistan could not be chosen).
- **Public Overpass stopped answering this machine** after three test processes ran at once (connection refused
  for 40+ cities). The test continued with Overture only. Per-process Overpass lock is a global queue only while
  one API process runs.
- **Open (founder):** production OpenStreetMap data from Geofabrik country extracts processed locally (ChatGPT R5:
  ≈ $24–96 / month, 3–5 developer days) instead of public Overpass — proposed as phase 11.
- **Open (founder + counsel):** Overture's Places guide says joining Places with OSM "may need to carry the Open
  Database License (ODbL) if it is a derivative database". "All sources" joins them. Internal use only today;
  get advice before any merged list leaves the company.
- **Overture results are limited to the chosen country** (address country). Measured in six boxes, 7,834 dentist
  places: none lacks an address country, so the filter is complete there. Shenzhen 522 → 43 CN; Tijuana −377 US.
- **Geocoder uses a settlement only when it carries the requested name** (any language, old or alternative name);
  a city beats a same-named village (Nanded); a name that only matches a building is "not found"; a province-only
  name (Tokyo) is rejected — ChatGPT R6 and Claude agreed not to search a province's admin centre automatically
  (Buenos Aires province → La Plata). Ward names work (Shinjuku 485).
- **Open (founder):** Foursquare Open Source Places (Apache 2.0; names, phone, email, website, socials) as a third
  source for countries where Overture is thin (Iran, China). Needs a free Places Portal account + access token
  created by the founder; the paid Foursquare API terms forbid lead generation, the open dataset does not.
  Proposed as phase 12 (incremental-coverage test first: keep it only if it adds ≥ 20 % verified unique businesses).

## 2026-11-10 - outreach writer request
- **An AI writes every outreach message; no person writes any** (founder). This replaces RESULT B.7 of the
  2026-11-10 outreach debate. Safeguards: the observation comes only from stored checks, a validator re-checks every
  number, domain, word count, phrase and the declared language, and the founder reads the first 20 emails once.
  Spec: `docs/spec/outreach-engine.md` (waiting for go).
- **Messages say "a small web studio in Gujarat"; the pilot area is Navsari + Surat.** The outreach RESULT first said
  Mumbai, which was wrong (SiteBlitz FD-22, truthful location; the founder lives in Navsari). Corrected in RESULT.md.
- **Still no automated WhatsApp Web sending and no logged-in social bots, re-checked against sources today.**
  - WhatsApp FAQ: since 2019-12-07, WhatsApp takes legal action against those engaged in, or assisting, automated or
    bulk messaging.
  - WhatsApp Terms: no bulk or auto-messaging, and no non-personal use.
  - LinkedIn UA §8.2 (2025-11-03): no bots to send messages.
  - Facebook Terms §3.2 (2025-01-01): no automated access.
  - WhatsApp is used for a lead only after that lead writes first. The app opens the chat with the text typed, and
    the founder presses Send.
- **`discover_contacts()` fabricates more than `info@`.** It also makes `inquiry.<name>@gmail.com`, a fake
  "Proprietor / Store Manager" and fake `+91 9825...` / `+1 (555)` phone numbers (`discovery.py:101-148`).
  - Nothing may call it until phase 5 removes this.
  - `ai_personalizer.py` signs as "Marcus Vance" with a fake New York address, so it must never be used to send.

## 2026-11-10 - phase 13 build (AI writer + validator)
- **The model never writes the signature.**
  - It returns `body`, `signoff` and `opt_out_line`.
  - The app adds the sender name, "SiteBlitz", the reply address and the postal address.
  - Why: an address the model types can be wrong; an assembled one cannot.
- **Sender name, reply address and postal address live in `.env`, not in git.**
  - They are `SITEBLITZ_SENDER_NAME`, `SITEBLITZ_REPLY_EMAIL` and `SITEBLITZ_POSTAL_ADDRESS`.
  - The model sees only the sender name. For the two addresses it sees only "set".
  - Why: the postal address is personal.
- **Holds are decided by the rules before any model call.**
  - The rules: country, opt-in, observation, missing facts, suppression.
  - A held lead costs nothing and sends no data.
  - The validator recomputes the same rules, so a model that writes anyway is rejected.
- **Server-side fallback is on.** The request carries `fallbacks: "default"` with beta
  `server-side-fallback-2026-07-01`, so a declined request is re-run on Anthropic's recommended model. If every
  model declines, the lead is held (`MODEL_REFUSED`), never sent.
- **A missing country is now a hold in `country_rules.py`.** It used to fall back to "US" and pass as CAN-SPAM.
- **BROKEN_FORM is in the prompt but never produced yet.** No form-test check type exists. It will be produced once
  a form test is stored as a website check.
- **This machine needs `jiter==0.8.2`.** Smart App Control blocks the jiter 0.19 DLL that `anthropic` 2.7.0
  installs (see the comment in pyproject.toml).

## 2026-11-10 - QA-1 audit and fixes
- **The app now uses a SQLite file by default** (`./siteblitz_leads.db`, gitignored). PostgreSQL is used only when
  `DATABASE_URL` says so, as `docker-compose.yml` does.
  - Why: the old Postgres default made every API call return 500 on a fresh checkout, while the README promised
    zero-config SQLite.
- **An unsubscribe suppresses only that address.** A whole domain is suppressed only when one is given explicitly
  (`POST /qualification/opt-outs` with `domain`).
  - Why: deriving the domain from the address meant one gmail user unsubscribing blocked every gmail lead.
- **The old compliance evaluator no longer turns a missing country into "US".** A country-less lead, or any lead whose
  country profile does not permit outreach, becomes NEEDS_REVIEW with MANUAL_REVIEW_ONLY.
- **The frontend reads a timestamp without an offset as UTC.**
  - Why: the API stores UTC, but SQLite drops the offset, so India showed every date 5 h 30 min early.
- **The Lead Radar funnel is labelled as generated sample data, and its code is otherwise unchanged.**
  - Showing real places, Navsari + Surat defaults and input validation are in board row LR.
  - Why: it is colleague Dev-Nurul08's code, so the fix needs agreement first.
- **This session stopped fixing at 13 changed files**, following the ~8-file phase rule (the overrun was the 2
  high-severity phase-13 claim gaps). The 37 other open bugs are in the board rows QA-1b, 3, 5, 14, 15 and LR, with
  IDs in `docs/qa/ISSUES.csv`.

## 2026-11-10 - Phase 14 email finder
- **robots.txt is read by a small RFC 9309 parser in `site_visit.py`, not `urllib.robotparser`.**
  - Why: the standard library has no `*` / `$` wildcards and takes the first matching rule, so `Disallow: /*`
    allowed every page.
  - A robots.txt answering 429 or 5xx means "disallow everything" (RFC 9309 2.3.1.4). A 4xx means there is no
    robots.txt. A site whose robots.txt cannot be reached at all is recorded as failed (unreachable).
  - Our group name is `SiteBlitzEnricher`; otherwise the `*` group applies.
- **"Max 5 GET per site" counts page GETs:** the homepage plus `/contact`, `/contact-us`, `/contactus`, `/about`.
  robots.txt is fetched on top of those: once, or twice when HTTPS fails and plain HTTP is tried, or when the
  homepage moves to another host. The visit stops at the first page that shows an email.
- **Emails come only from mailto links, visible text (including "name [at] domain [dot] com") and Cloudflare-encoded
  addresses** (spec row 10). JSON-LD sits in a `<script>`, so it is no longer read; the old Schema.org test now
  checks that it is ignored. Example addresses (`you@example.com`), Sentry keys and comments are dropped (QA-040).
- **An email is stored only when its page is on the host the business lists, or the host its homepage redirects
  to** (`www.` ignored). A contact page that redirects elsewhere does not count as the business's own site.
- **Listing addresses (Google pages, business.site, directories) and social profiles are not fetched.** They are not
  the business's own site.
- **Schools are skipped by exact Overture category** (`school`, `elementary_school`, `middle_school`, `high_school`,
  `public_school`, `school_district_office`, `education_office`). College/university stays a fragment rule.
  Coaching classes (`specialty_school`), preschools, tutoring and educational services are prospects (QA-038).
- **"Sites down" in the totals means one failed check.** `SITE_DOWN_CONFIRMED` needs a second failure at least 6 h
  later (website-intelligence spec row 6). That second check was not run in this session.
- **The results stay outside the repository**, in `E:\SiteBlitz-World-Business-Data\_work\email_finder\2026-11-10\`,
  because they hold business contact data. They are not imported into the app database yet: phase 15 needs them as
  businesses, `website_checks` and contacts.

## 2026-11-12 - two review rounds (recommendations; founder approval pending)
- **Verified:** the live site (production deploy of 2026-07-10) shows invented testimonials, invented results,
  "Studio Mumbai" and withdrawn prices; the truthful version is on the website branch v2-redesign (not deployed).
  `siteblitz.in` is still unregistered. Both local lead databases hold 0 contact rows (no fabricated contacts stored).
- **Agency route** (`docs/debate/2026-11-12-clients-without-selling/RESULT.md`): white-label builds for agencies as
  the main route, contract work as the cash route; kit written in `docs/agency/`. The founder then asked to focus on
  email; the agency kit stays for later use.
- **Email engine v2** (`docs/debate/2026-11-12-email-engine-personas/RESULT.md`, spec `docs/spec/email-engine-v2.md`):
  India-only pilot, Tier 1 addresses only (published on the business's own site, source URL stored), three
  observation templates, Mailforge mailboxes (Terms §3.4(1) allows unsolicited B2B outreach where lawful) on two
  founder-registered domains, 30/25/5 caps per mailbox, ramp 10/15/20/20 new per sending day, RFC 8058 unsubscribe
  with a cloud suppression list, AI-drafted replies approved by the founder, `/start-day` brief. Phases E0-E6 on the
  board, all 🔒. Old 14b folds into E1, 15 is replaced by E3, 16 is paused.

## 2026-11-12 - E1 eligibility (email engine v2, founder `go`)
- **Who may be emailed is one stored row per (business, address)** in `email_eligibility`, recomputed by
  `POST /api/v1/outreach/eligibility/evaluate`. Evidence is append-only: `email_captures` (every sighting with source
  URL, method, capture time, excerpt), `website_checks` (homepage checks, and the new `PHONE_RENDER` check),
  `email_verifications` (verifier cache) and `social_confirmations` (the founder's Instagram-bio checks). Every HOLD
  row carries one or more codes from `HoldReason` (`backend/app/models/eligibility.py`, 23 codes, each documented).
- **Tier 1 = the address was read on the business's own site**: the page host is the listed website host or the host
  its homepage redirected to, and the source URL, capture time and an excerpt of at most 300 characters are stored.
  A founder confirmation of the Instagram bio is Tier 1 too. A listing address (Overture) is Tier 2 = HOLD.
  - Phase-14 addresses were found before the extractor kept excerpts, so they are HOLD `PROVENANCE_INCOMPLETE` until
    their page is visited again. Only the 2 phase-14 leads that could become eligible (no viewport + an address)
    were visited again; the other 837 rows have no pilot observation anyway.
- **Recipient type:** two or more name-like parts at a company domain (`priya.shah@`, `r.patel@`) = `employee_like`
  = HOLD. `unknown` (for example a free-mail address that does not name the business) is not a HOLD; it is shown for
  the founder's 30-lead provenance audit (spec row 17 f). Added: no-reply, postmaster, webmaster, abuse, privacy,
  legal, grievance and similar mailboxes are HOLD `SYSTEM_ADDRESS` - not for a sales message.
- **Chains and duplicates:** Overture `brand`, or a site shared by 3 or more businesses, or one address on 3 or more
  businesses = `CHAIN_OR_DIRECTORY`. `sites.google.com` sites are told apart by their first two path parts. An
  address on 2 businesses goes to the better-placed one (`DUPLICATE_RECIPIENT` for the other); a business with
  several addresses keeps its best one (`NOT_PRIMARY_RECIPIENT` for the rest).
- **Import matches businesses by Overture source id only.** The app's name + city duplicate rule merged 423 of the
  2,014 phase-14 leads (they have no phone or coordinates), mostly same-name chain branches, and merged branches
  stopped counting towards the chain rule.
- **Verifier ladder:** a free syntax + MX check first (null MX, or no MX and no A/AAAA = INVALID). Passing it is
  stored as UNVERIFIED with `mx_ok`, because an MX record does not prove a mailbox. Bouncer only with
  `BOUNCER_API_KEY`: deliverable = VALID, but deliverable or risky with `acceptAll: yes` = CATCH_ALL, other risky =
  RISKY, undeliverable = INVALID, unknown or any new value = UNKNOWN. An HTTP error (401, 402 no credits, 429) or a
  network error is "no answer" and is not cached. The paid check runs only for addresses nothing else holds back.
  Results are re-checked after 30 days. No key on this PC today, so no address is VALID and none is eligible.
- **Observation sentences are fixed texts with the date written as "12 November 2026" in India time** (11/12 is read
  both ways). The domain is the host without `www.`.
- **NO_VIEWPORT needs the rendered phone check** (`scripts/render_check.cjs`): Chromium with isMobile, 390 x 844,
  deviceScaleFactor 3, a mobile Chrome user agent that ends in `SiteBlitzEnricher/1.0`, 12 s navigation timeout;
  `window.innerWidth >= 900` after load = zoomed-out. When the load event does not fire in 12 s but the page is
  there, the width is still measured and `load_timeout` is stored. One PNG viewport screenshot per page under
  `E:\SiteBlitz-World-Business-Data\_work\evidence\<date>\`. URLs pass the same SSRF guard first; the script also
  aborts requests to localhost and private IP literals. A page rendered after its latest homepage check is not
  rendered again.
- **SITE_DOWN:** the trailing run of failed homepage checks must span at least 6 h; an ok, protected or
  robots-blocked answer breaks the run. Block and challenge pages (Cloudflare "Just a moment...", DDoS-Guard, Sucuri,
  "access denied" or captcha on an error answer) are now recorded as `protected`, never `failed`. A site confirmed
  down that loads again = HOLD `SITE_RECOVERED`. `recheck_before_send(business)` (for E2) runs a fresh robots.txt +
  homepage check and a fresh MX check; a SITE_DOWN lead may be sent to only when that fresh check failed.
  - Found: a SITE_DOWN lead can only be eligible with an address captured while the site still worked, or a founder
    confirmation; a down site shows no pages, so the pool cannot produce one.
- **SOCIAL_ONLY confirmations accept only an instagram.com profile URL** (the observation text names Instagram), a
  real true/false for `website_link_present` (`"no"` is refused), and no `checked_at` in the future. An `email_seen`
  becomes a Tier 1 capture (method `founder_confirmed`) whose excerpt records the founder's check. The pending list =
  India, an Instagram profile, no own website, no founder check in the last 30 days.
- **Fabricated contacts removed (old phase 5, part):** `discover_contacts()` and the Hunter.io lookup are deleted;
  the enrichment API uses `published_contacts()` (the listing email, stored audit emails, the polite own-site visit).
  `export_surat_leads.py`, `surat_restaurant_leads_with_contacts.csv` and `surat_leads_extracted.csv` are removed
  (38 rows each: 37 generated `inquiry.*@gmail.com` addresses, 36 generated `+91 9825...` numbers). The Lead Radar
  sample no longer makes up `info@<name>.in`. The old sender marks a message SENT only with a provider event that
  accepted it with its own message id; there is no provider yet, so `/campaigns/{id}/dispatch` sends and counts
  nothing. A test scans the code for guessed-address patterns.
- **This PC:** Smart App Control now also blocks fontTools' compiled modules (used by the PDF export), so the 6
  `.pyd` files in `.venv/Lib/site-packages/fontTools` were renamed to `*.pyd.blocked-by-sac`; fontTools then runs its
  pure-Python modules. A fresh install needs the same step.
- **Pool selection (`scripts/pool_e1.py`):** `IN_businesses.zip` has no `operating_status`, so permanently closed
  places cannot be left out as phase 14 did. The crawl visits Navsari and Surat completely first, then the other 9
  cities round-robin, and stops at the time limit, so a cap cuts every other city by about the same amount.

## 2026-11-12 - E1 pool crawl: MemoryError, fixes, and where it stopped
- **The crawl stopped at 12:48 after 101 minutes with a MemoryError**, at about 5,250 of 13,185 hosts (6,233 URLs
  in `visits.jsonl`, none lost). The machine had about 500 MB of free RAM (other sessions, Chrome, VS Code).
- **Part of the cause was our code, measured on a dense 2 MB page:** the viewport flag came from the full
  `WebsiteAuditor.audit_html` (a whole parse tree plus a lowercased copy of the page): ~97 MB peak for one flag. The
  email extractor parsed the page again: ~80 MB. Fixes:
  - the viewport flag parses only `<meta>` tags, with the auditor's rule (a test compares both on 6 cases): ~0 MB;
  - the extractor cuts `<script>`, `<style>` and comments before parsing (an `<a>` inside them was never parsed as a
    tag and their text was already dropped, so results do not change; a test proves it);
  - page bodies are released right after use, and the 2 MB read keeps one copy at a time;
  - the crawler runs N workers over one queue instead of one waiting task per host (13,185 tasks).
  A soak test of the fixed code (10 visits at a time of that page) stayed between 165 and 223 MB working set: a slow
  creep, no runaway growth. Parsing is synchronous, so only one page is parsed at a time even with 10 sites in
  flight; the low free RAM of the machine was the other half of the cause.
- **The pool crawl now stops cleanly when free RAM falls below 500 MB** (`--min-free-mb`, checked every 30 s) and
  records why it stopped (`time_limit`, `low_memory`) in `summary.json`.
- **Imported times are stored in UTC.** The importer kept visit times in IST; SQLite drops the offset and the app
  reads a stored time as UTC, so every imported check and capture was 5 h 30 min late (two pages were rendered
  twice because of it, and a SITE_DOWN gap or an observation date could have been wrong). The importer converts to
  UTC now; the 8,874 checks and 3,544 captures already imported were shifted once (backup kept outside the repo).

## 2026-11-12 - email engine v2 build (founder "go for all")
- **Phases ran as parallel workers in separate git worktrees** (E2 `email-engine-e2`, E3/E4 from E2) and were merged
  into `phase-01-pipeline-repair` (6f724b6, b75c6b3, d975c35). Merge conflicts were only additive lines (router,
  models, main, one constant block) and were resolved by keeping both sides; 795 tests passed after the last merge.
- **The production deploy was not done by Claude**: the safety classifier denied "Production Deploy" when setting a
  Vercel production variable. Not worked around; the founders run the steps in `docs/outreach/email-engine-setup.md`.
- **Pool reality**: 26 leads eligible once verified (all NO_VIEWPORT) from 10,725 visited Gujarat businesses; the
  SOCIAL_ONLY route needs the founder's Instagram check (automated reading stays banned) and a separate import.
- **Pre-send review changes** (ChatGPT + Claude panel, `docs/debate/2026-11-12-pilot-template-review/RESULT.md`):
  NO_VIEWPORT sentence and subject say only what the 390 px check showed; T2 starts with the identity line; replies on
  WhatsApp / phone can be marked (`/replied-elsewhere`, `/start-day` `replied` / `stop`); SOCIAL_ONLY leads with an
  own-domain address are held (`SOCIAL_ONLY_DOMAIN_ADDRESS`).
- **Recordings**: the founder's own recorded overview per vertical comes from `docs/outreach/recordings.json`; empty
  means no audio block. No synthetic voice.
- **Defaults chosen for open worker questions** (founder may change): business days Mon-Fri for the reply backlog;
  a duplicate caught before sending still pauses everything; 4xx = 3 attempts per window x 3 windows then FAILED soft;
  "not interested right now" is treated as stop (suppressed); a weak complaint ("is this a scam?") suppresses without a
  global pause; the stop confirmation reply is off by default; vertical `other` gets a snapshot without a concept demo.
