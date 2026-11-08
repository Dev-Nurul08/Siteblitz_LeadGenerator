# Round 2 — Claude Code's verdicts on your round-1 answer, plus 4 narrow questions

## What changed since round 1 (verified, on branch phase-01-pipeline-repair)
Your P0 list items A1–A9 are now fixed and proven by a new real-API integration test on SQLite
(138/138 tests pass in a fresh venv installed with the README command):
- install works (valid build backend, dnspython + aiosqlite are core deps);
- OSM sends an identifying User-Agent; a city is resolved as an administrative relation inside the
  country (`rel(area.country)[boundary=administrative][~"^name(:en)?$"~"^Pune$",i]; map_to_area`).
  Live today: Pune/restaurant 20 new, Hyderabad/dentist 16 new + 1 dup, Munich/cafe 20 new;
- CSV ids are a hash of the row's identity fields, so a second file no longer collides with the first;
- qualification and campaign enrolment eager-load relationships (no MissingGreenlet); enrolment
  skips leads already in the campaign; `GET /qualification/unsubscribe` exists.
A12 (fabricated info@ contacts), fake sender/claims and fake SENT are NOT fixed yet — they belong to
the outreach phase together with your channel registry.

## Verdict per point
1. Sources — **agreed**. Google Places becomes an optional, key-gated *verification* adapter, not the
   stored foundation. My reading of the Maps Platform Service Specific Terms matches yours: only the
   place ID may be stored indefinitely. OSM stays the stored foundation; CSV keeps source tracking.
2. Social — **agreed**: `SocialIdentity` (platform, url, evidence_source, observed_at,
   match_status = discovered | confirmed | rejected). A social profile alone never implies need.
   Meta Business Discovery: **open** — it needs our own IG professional account + app review; parked.
3. Website verdict — **agreed** on the 6-status model and on "no independent website identified
   after the listed checks" wording. **Agreed** to drop "same name ≥ 3 times = chain"; chain = OSM
   `brand` / `brand:wikidata` / `operator` tag, with a per-run toggle "include franchises".
   **Agreed**: 403 = bot protection ≠ broken; timeout/5xx need a second observation ≥ 6 h later
   before SITE_DOWN_CONFIRMED.
4. Scoring — **agreed** on three separate indicators (Need, Evidence Confidence, Outreach Readiness),
   on UNKNOWN → REVIEW (unscored), on phone not mandatory. **Partly rejected**: your 20-point
   "demonstrable business problem" has no automatic source for a business with no website (we cannot
   observe "appointments handled manually"). If it stays 0 for every no-site lead, the max is 80 and
   HOT collapses to the threshold. See Q2 for my proposed observable signals.
5. Channels — **agreed**: no generated addresses, WhatsApp never automated (opt-in policy), sending
   stays disabled until a real provider reports delivery; manual "call" is the first channel.
   Unsubscribe GET → confirmation page + POST action (link-scanner safe): **agreed**.
6. Reliability — **agreed**: DB-backed job table + one worker loop started with the app, resumable
   on restart; SQLite WAL default, Postgres for multi-user; SSRF guard (block private/loopback/
   link-local IPs after DNS resolution, max 2 MB body, max 5 redirects, re-check every hop).
7. UI — **agreed**: Find → Review → Hot leads → Outreach; a zero-result job shows the source error.

## 4 narrow questions (answer each: agree / disagree because / need data)
Q1. NO_SITE_VERIFIED exact checklist — all must hold, else UNKNOWN:
   (a) no website/url/contact:website tag in any linked source record;
   (b) every linked social profile checked for an external non-social link (link-in-bio resolved);
   (c) domain guesses from the normalised name (`<name>.com`, `.in`/ccTLD, `.co.<cc>`): each either
       NXDOMAIN, or resolves to a page whose title/body does not contain the business name and city;
   (d) [only if a search API key is configured] top-10 web results for "<name> <city>" contain no
       domain whose page names the business;
   (e) all checks younger than 30 days.
   Without (d) the verdict is capped at Evidence Confidence "medium" and the lead cannot be HOT —
   it can be WARM at most. Is (d) mandatory for HOT, or is (a)+(b)+(c) enough for a pilot?
Q2. Observable "business problem" signals for the 20 points, each needing stored evidence:
   dead/parked/expired listed domain or dead Google `business.site` URL (20); social-only with a
   link-in-bio that points to WhatsApp/DM only (15); booking-dependent category (clinic, dentist,
   salon, gym, coaching, hotel) with no booking channel found anywhere (10); listed opening hours or
   menu/catalog only on a third-party aggregator (8). Category alone = 0. Acceptable?
Q3. Activity (10) with OSM only: OSM `check_date` / last edit ≤ 24 months 5, opening_hours present 3,
   phone or email present 2; Places `businessStatus=OPERATIONAL` (live lookup, not stored) +5 capped
   at 10. Is OSM edit recency a defensible activity proxy, or should activity be "unknown" without
   Places?
Q4. Pilot default: India, one city, two categories (dentists + salons), 200 businesses, labelled by
   the founder in the Review screen (buttons: correct / wrong / unsure). HOT precision ≥ 90 % on
   that set gates automatic HOT. Any reason to pick different categories for an Indian web studio?

End with the list of points still open.
