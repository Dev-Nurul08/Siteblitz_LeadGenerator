# Review - City coverage test (India, Bangladesh, Afghanistan + top 50 countries) - 2026-11-08 - 10 rounds - prompt: none (project context)

Search per city: dentist · max 300 · All sources until Overpass stopped answering, then Overture only.
Data: `results-all.json` (one row per city, re-checks applied), raw rounds `NN_claude.md` / `NN_chatgpt.md`.

## Totals
- 366 population-ranked cities in 53 countries (India 150, Bangladesh 40, Afghanistan 26, 3 each in 50 others)
  + 39 re-check / validation searches.
- 330 cities returned businesses · 27 resolved correctly with 0 dentists in Overture (source gap) ·
  8 not found under the given spelling (5 found under another spelling) · 1 rejected as a prefecture (Tokyo).
- 47,117 dentist records returned (cap 300 per city); the sources hold 190,894 in those city boxes.

## Points
| # | Point | Proposed by | Evidence | Claude's verdict | Status |
|---|---|---|---|---|---|
| 1 | Repeat / overlapping searches showed nothing they had seen before | ChatGPT R5 (Indore) | Pimpri-Chinchwad listed 19 → 287 (23e94e3) | agreed, fixed | done |
| 2 | City box crosses a border | Claude R6 | Shenzhen 479 HK of 522 → 43 CN; Tijuana −377 US (5a555ae); 7,834 places measured, 0 without country | agreed, fixed | done |
| 3 | Geocoder picks landmarks / other cities / villages | Claude R5–R10 | Beijing, HCMC, Tokyo→Hachioji, Nanded, Hubli-Dharwad, Thrissur; 20 / 20 on ChatGPT's validation batch (86efeab, fc8ffce, eedef32, 7fc0a5c) | agreed, fixed | done |
| 4 | Province-only names searched around the admin centre automatically | Claude R6 | ChatGPT: Buenos Aires province → La Plata | rejected (stays "enter a city name") | closed |
| 5 | Only 10 countries selectable | Claude R5 | Bangladesh / Afghanistan impossible in the UI (72e84a0) | fixed (249) | done |
| 6 | Non-cp1252 city names fail the job on Windows | test (Wrocław) | reproduced, fixed (57d9bdf); Wrocław 300, Łódź 261 | fixed | done |
| 7 | Public Overpass unusable at volume | Claude R5 | connection refused from this PC for 40+ cities | Geofabrik extracts — phase 11 | open (founder budget + ODbL review) |
| 8 | Thin countries need another source | ChatGPT R9 | Foursquare OS Places (Apache 2.0, token needed) | phase 12 pilot | open (founder token) |
| 9 | SOCIAL_ONLY / NEITHER_LISTED reporting labels | ChatGPT R7, R10 (#1 value / cost) | France: 39–40 % website, 4–7 % social | reporting only, scoring unchanged | open (founder) |
| 10 | Dead domain = Website down immediately | Claude (earlier) | ChatGPT R10: reject | rejected | closed |

## Market picture (median of cities, dentist)
Most "social profile, no website": Iraq 90 %, Sudan 87 %, Myanmar 85 %, Bangladesh 80 %, Yemen / Mozambique /
Algeria 76–77 %, Indonesia / Philippines / Thailand 71–75 %, Egypt / Morocco / Argentina 64–66 %, India 60 %.
Least: Canada, Germany, Japan, US, Spain, UK (1–3 %). Source gaps: China, DR Congo, Madagascar, Niger, Angola,
Afghanistan outside Kabul, Iran outside Tehran, secondary West / East African cities.

## Recommended next steps (not started - waiting for your go)
1. Phase 6 pilot: India + Bangladesh + France, 60 labelled businesses each (ChatGPT R10).
2. SOCIAL_ONLY / NEITHER_LISTED labels in Review + export (scoring unchanged).
3. Phase 12 Foursquare OS Places pilot in 7 thin countries (needs your free Places Portal token).
4. ODbL legal review, then phase 11 Geofabrik pilot.

## Points still open
Category precision, real website absence, contact accuracy, business freshness, OSM coverage, Foursquare increment,
commercial value — none of these is proven by a coverage test (ChatGPT R10 §2, agreed).
