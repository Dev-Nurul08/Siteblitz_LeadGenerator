# SiteBlitz Lead Generator — how to use it (redesigned app, 2026-11-08)

Written for: the founder / sales operator.

## 0. Start it
```powershell
# backend (repo root)
$env:DATABASE_URL = "sqlite+aiosqlite:///./dev.db"
.venv\Scripts\python -m uvicorn backend.app.main:app --port 8000
# frontend (second terminal)
cd frontend; npm run dev        # open http://localhost:5173
```

## 1. The order — the four steps across the top of the app
| Step | What you do | What happens |
|---|---|---|
| **01 Find** | Pick a source (**All sources** = Overture Places + OpenStreetMap is the default), country, city, kind of business, Max results (up to 5,000) → **Start search** | A search job runs (~20 s). The businesses land on the map and the panel says how many the sources have in that city ("426 … all of them", or "raise Max results to get more"). Then every website is checked automatically, 100 at a time (~25–40 s per 100); dots recolour as verdicts arrive. **Stop checking** pauses it; Review can continue later. |
| **02 Review** | Open any business (click, Enter, or J / K) | The drawer shows every check the system ran, with time. You can search Google for it, record "I found no website" or "Save website", confirm it is open (after a call) or closed, and mark the verdict **Correct / Wrong / Not sure** (keys 1 2 3). |
| **03 Hot leads** | Pick a tier (Hot / Warm / Cold / Review / Skip) and open a lead | The score builds from its reasons (+60 website gap, +10 activity …). "Before it can be Hot" lists what is still missing. |
| **04 Outreach** | Open a lead | Contact routes (Call, WhatsApp chat opened by hand, copy email, open profile), a draft written only from stored facts (hover a fact to see which sentence uses it), **Copy draft** after you tick "I checked every fact", and **Log contact**. Sending from the app is off on purpose. |
| Settings | — | Live status of every source; the do-not-contact list. |

## 2. Extract and see the data
- **See:** Find → Past searches → **View businesses** (opens Review filtered to that search), or click a dot on the map.
- **Extract:** **Export CSV** (every column incl. Facebook / Instagram links) or **Export PDF** on every search row and in the Current search panel.

## 3. What a verdict means
| Verdict | Meaning | Lead? |
|---|---|---|
| No website found | No website in any source, guessed domains do not exist or are other businesses | Yes |
| Social media only | Only Facebook / Instagram / WhatsApp / Linktree found | Yes |
| Website down | The listed website failed twice, at least 6 h apart | Yes |
| Needs review | Checks were blocked or conflicting (e.g. the site failed once) | Your call |
| Has own website | A website of its own opened (a Google Maps link or a directory page does **not** count) | No |
| Skipped | Chain/brand, bank, ATM, fuel, school, hospital, worship place, closed | Never |
| Not checked yet | The website checks have not run | — |

## 4. How a lead becomes Hot (approved spec `docs/spec/website-intelligence.md`)
Score = website gap (no site 60 · social only 55 · site down 50 · weak own site up to 35)
\+ business problem (max 20) + activity (max 10) + service fit (dentist / salon 10, other listed categories 7, else 4).
**Hot = 80+ AND** high evidence confidence (needs your recorded search) **AND** activity ≥ 7 (you confirmed it is
open) **AND** a phone or email. Without your search the best a lead can reach is Warm.

**Important calibration finding (2026-11-08):** with these approved weights a *social-media-only* business that
has a phone tops out at 55 + 0 + 10 + 10 = **75 → Warm**. Only "no website found" dentists/salons can reach 80.
In the Udaipur dentist test, 40 of 70 were social-only, so they all stay Warm. See the open question in
`docs/HANDOFF.md`.

## 5. Terms on a search (job)
| Word | Meaning |
|---|---|
| Found | Businesses the source returned |
| New | Saved for the first time |
| Duplicates | Already saved (same source record, or same name in the same city / within 5 km) — not added again, but still part of "View businesses" for that search |
| Errors | The source's own problem (rate limit, city not found …), shown in red |
| Done / Partial / Failed | No errors / finished with a source error / crashed |

## 6. Why OpenStreetMap gave "29"
OpenStreetMap really has only 29 named cafés in Udaipur (35 in total). Overture Places has 246 for the same
search, with phones for 83 % of places and social links for 87 %. Nothing was lost by the tool.

## 7. How much data a search returns (measured 2026-11-08, "All sources")
| Search | Before (old matching, one source) | Now | Time |
|---|---|---|---|
| Udaipur · dentist | 75 found / 70 new | **108 found / 100 new** | 41 s |
| Udaipur · cafe | 246 found / 225 new (+29 from a separate OSM run) | **418 found / 370 new** in one search | 50 s |
| Udaipur · salon | — | **426 found / 392 new** ("all of them") | 47 s |
| Pune · salon (Max 5,000) | job failed (one bad record) | **4,557 found / 4,065 new**, 0 errors | 95 s |

Why more: the kind of business now also matches the business **name** ("Smile Dental Care" filed under
"doctor"), both sources run in one search, OpenStreetMap searches the same city box as Overture (its old
city-boundary query timed out), busy Overpass answers are retried, and one bad record can no longer fail a
whole search. A search returns **every** matching business the sources hold for that city up to Max results;
if a city has fewer than you asked for, the panel says "all of them". More than that would mean a wider area
or a paid data source.

"Needs review" because the listed website "failed once": most of those (32 of 39 in the test) are domains
with no DNS record at all — the website is gone. Review → filter "Needs review" → **Check these again**
after 6 hours turns them into "Website down" (a lead).
