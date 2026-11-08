# SPEC LOCK — Phase 2: Website Intelligence Engine

Status: **APPROVED** — founder replied "go … complete everything" on 2026-11-08. Source of every value:
ChatGPT review round `docs/debate/2026-11-08-…/RESULT.md` rows 3–4b, 8 and the audit.
Replaces the current `detector.py` / `scorer.py` logic for "does this business need a website?".

| # | Ambiguity | Locked value | Why this default |
|---|---|---|---|
| 1 | Website verdict values | `OWN_SITE_VERIFIED`, `SOCIAL_ONLY_VERIFIED`, `NO_SITE_VERIFIED`, `SITE_DOWN_CONFIRMED`, `UNKNOWN`, `SKIP` | RESULT row 3 |
| 2 | Evidence storage | New table `website_checks`: business_id, check_type (`source_tag`, `social_link`, `link_in_bio`, `domain_guess`, `site_fetch`, `search`, `manual_search`, `manual_activity`), input, outcome, detail JSON, observed_at. Verdict recomputed from checks; old checks kept | RESULT row 3 ("history separate from verdict") |
| 3 | Social profile record | New table `social_identities`: business_id, platform (`instagram`, `facebook`, `linkedin`, `tiktok`, `youtube`, `x`, `whatsapp`, `linktree`), url, evidence_source, observed_at, match_status (`discovered`, `confirmed`, `rejected`) | RESULT row 2 |
| 4 | "Social" URL detection | Host equals or ends with `.`+ one of: instagram.com, facebook.com, fb.com, linkedin.com, tiktok.com, youtube.com, x.com, twitter.com, wa.me, whatsapp.com, linktr.ee, bio.link, beacons.ai — matched on the parsed host, never by substring (fixes fedex.com bug) | Audit B (`normalizer.py:243`) |
| 5 | Domain-guess candidates | From the normalised name without spaces: `<n>.com`, `<n>.<cctld>`, `<n>.co.<cctld>` (IN → .in / .co.in). Candidate only; a match needs ≥ 2 of: business name in title/H1, phone digits on page, city on page, link back from a confirmed social profile | RESULT row 3c |
| 6 | Site fetch rules | Timeout 12 s, max 5 redirects, max 2 MB body, block private/loopback/link-local IPs after DNS. 403/429 = `site_fetch: protected` (counts as site exists). Timeout/5xx/DNS fail = `failed`; `SITE_DOWN_CONFIRMED` only after 2 failures ≥ 6 h apart. Redirect to a social host = social link, not a website. Parked/"coming soon"/expired = `failed` | RESULT rows 3b, 6 |
| 7 | NO_SITE_VERIFIED + HOT-eligible | All of: no website in any source record; every linked social profile's external link resolved; no domain-guess matched; a `search` or `manual_search` check with 0 matching domains in the top 10 results; all checks ≤ 30 days old | RESULT row 3c |
| 8 | Limited verification | Same as #7 without a search check → `NO_SITE_VERIFIED`, Evidence Confidence `medium`, label "No website identified — limited verification", tier capped at WARM | RESULT row 3c |
| 9 | SKIP rules | OSM `brand`, `brand:wikidata` or `operator` tag (unless run option "include franchises" is on); `amenity` in atm, bank, fuel, place_of_worship, townhall, police, post_office, school, university, college, hospital, parking, toilets; any `disused:*`, `abandoned:*`, `was:*` key or `shop=vacant` | RESULT rows 3a, 3d |
| 10 | Need score — website gap (max 60) | NO_SITE_VERIFIED 60; SOCIAL_ONLY_VERIFIED 55; SITE_DOWN_CONFIRMED 50; own site with no viewport meta 30, no HTTPS 20, both 35; own site fine 0; UNKNOWN → unscored | RESULT row 4a |
| 11 | Need score — business problem (max 20, strongest single signal only) | Social-only profile whose only contact is WhatsApp/DM 10; menu/catalog only on an aggregator (Zomato, Swiggy, Justdial, Practo) and no owned page 8; tested broken inquiry/booking form 20; recorded owner statement 20. Category alone 0 | RESULT row 4a |
| 12 | Need score — activity (max 10) | Manual "verified active" (call/visit) 10; owner post ≤ 90 days 7; Places live `OPERATIONAL` 5 (not stored); OSM `check_date` ≤ 180 days 2; OSM edit date 0 | RESULT row 4b |
| 13 | Need score — service fit (max 10) | Pilot categories dentist, salon/hairdresser/beauty 10; clinic, doctors, gym/fitness_centre, restaurant, cafe, hotel, lawyer, accountant, estate_agent, education/coaching 7; other 4 | Pilot (RESULT row 8) |
| 14 | Tiers | HOT 80–100, WARM 60–79, COLD 0–59, REVIEW (unscored/UNKNOWN), SKIP. HOT also requires: verdict NO_SITE_VERIFIED / SOCIAL_ONLY_VERIFIED / SITE_DOWN_CONFIRMED with confidence high, activity ≥ 7, and at least one outreach route | RESULT rows 4, 4a |
| 15 | Evidence Confidence | high = rule #7 met; medium = rule #8; low = any mandatory check blocked or conflicting | RESULT rows 3c, 4 |
| 16 | Outreach Readiness | `ready` (published phone or found email or contact form), `research` (none yet), `blocked` (suppressed) | RESULT row 5 |
| 17 | Re-evaluation | Re-running replaces the verdict and score; opportunities that no longer apply move to status `DISQUALIFIED` (never silently kept) | Audit B (stale opportunities) |
| 18 | Removed | Automatic MOBILE_APP, ONLINE_BOOKING, ECOMMERCE, SEO opportunities from category alone; hard-coded confidence 0.92 | RESULT row 7 |
| 19 | Founder labels | Review screen buttons Correct / Wrong / Unsure; Wrong requires picking what was wrong: website ownership, activity, identity, exclusion, need | RESULT row 8 |

## OUT OF SCOPE (will NOT build in phase 2)
- Search API integration (only the manual-search check type and its UI field) — needs the founder's choice.
- Google Places adapter (phase after the key exists).
- Background jobs (phase 3), UI redesign (phase 4), outreach changes (phase 5).

## ACCEPTANCE CRITERIA (binary)
- [ ] A business whose only website is `https://instagram.com/x` gets `SOCIAL_ONLY_VERIFIED`, never `OWN_SITE_VERIFIED`.
- [ ] `https://www.fedex.com` is treated as a website, not social.
- [ ] An OSM record with `brand:wikidata` is SKIP; with "include franchises" on it is scored.
- [ ] An OSM record with `amenity=atm` or `shop=vacant` is SKIP.
- [ ] A site answering 403 is not `SITE_DOWN_CONFIRMED`.
- [ ] One timeout gives `UNKNOWN`; two failures ≥ 6 h apart give `SITE_DOWN_CONFIRMED`.
- [ ] Without a search/manual_search check, no lead is HOT (max WARM).
- [ ] With all checks + manual search + "verified active" + phone, a no-site dentist scores 60+0+10+10 = 80 → HOT.
- [ ] Every awarded point appears in the lead's evidence list with its check id.
- [ ] Re-evaluating a business that now has a site moves its NEW_WEBSITE opportunity to DISQUALIFIED.
- [ ] Unit tests for each rule above + one API test; full suite green.

## RISKS
- Domain-guess matching misses brand-name domains → mitigated: guesses never prove absence (#5, #7).
- Manual steps (search, activity) slow HOT creation → by design for the pilot; a search API removes one step later.
- Weights are provisional → calibrate on 100 labelled businesses, validate on 100 untouched ones.

Reply `go` to build all of it, or `change 2,5` with your values.
