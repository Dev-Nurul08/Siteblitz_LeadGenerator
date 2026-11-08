# SiteBlitz Lead Generator — how to use it (current version, 2026-11-08)

Written for: the founder / sales operator. This describes the app **as it works today** (old
screens, repaired backend). The redesigned 4-step screens are specified in `docs/spec/ui-redesign.md`.

## 0. Start it
```powershell
# backend (repo root)
$env:DATABASE_URL = "sqlite+aiosqlite:///./dev.db"
.venv\Scripts\python -m uvicorn backend.app.main:app --port 8000
# frontend (second terminal)
cd frontend; npm run dev        # open http://localhost:5173
```

## 1. The order to work in
| Step | Screen (sidebar) | What you do | What you get |
|---|---|---|---|
| 1 | **Run Discovery** | Pick a source (use **Overture Places**), country, city, category, max results → Start | A *job* with Found / New / Dup / Errors |
| 2 | Run Discovery → job card → **View businesses** | Look at what that job found | The Businesses list filtered to that job |
| 3 | **Businesses** → **Export CSV / Export PDF** | Download what the filters show (or use the job card buttons) | `siteblitz-businesses-job9-….csv/.pdf` |
| 4 | **Businesses** → click a row → Run audit (or **Opportunities** → batch) | Website check of each business | Website status + opportunities ⚠ see note |
| 5 | **Contacts** | Find email contacts | ⚠ see note |
| 6 | **Compliance & Leads** | Qualify | Lead score + draft pitch ⚠ see note |
| 7 | **Campaigns & CRM** | Enrol, "dispatch" | ⚠ nothing is really sent |

⚠ Steps 4–7 still run the **old logic** that the audit found unreliable (any business without a
website field becomes "CRITICAL", invented `info@` contacts, fabricated pitch claims, simulated
sending). They are rebuilt in phases 2 and 5 (`docs/PHASES.md`). Until then, use steps 1–3 to get
lists, and judge websites yourself.

## 2. What every word on a discovery job means
| Word | Meaning |
|---|---|
| **Job** | One search: one source, one city/area, one category. Each click on Start = one job. |
| **Found** | Businesses the source returned for that search. |
| **New** | Saved for the first time. These are added to Businesses. |
| **Dup** (duplicate) | Already saved before — the same source record, or the same name in the same city / within 5 km (from any source). Not added again, but linked to the job, so "View businesses" still shows them. |
| **Errors** | Problems the source reported (rate limit, city not found, area too large…). The reason is shown in red on the job. |
| **Completed** | Finished with no errors. |
| **Partial** | Finished, but the source reported an error (often 0 results + the reason). |
| **Failed** | The job crashed; the error text is on the card. |

Website status (Businesses list):
| Value | Meaning |
|---|---|
| `UNKNOWN` | No website link in the source data yet — **not** proof that there is no website. |
| `SOCIAL_ONLY` | Only social links (Facebook / Instagram / WhatsApp / Linktree …) were found. |
| `FOUND` | A website link exists (not yet checked). After an audit it may become `BROKEN` / `UNDER_CONSTRUCTION`. |
| `NOT_FOUND` | Audit could not find the site (404/410). |

## 3. Which source to use
| Source | Use for | Data you get | Limits |
|---|---|---|---|
| **Overture Places** (default) | Any city | name, address, phone (83 % of places in the Udaipur test), website, Facebook/Instagram links, email sometimes | Needs a city name or coordinates; ~20 s per search; data from Meta/Microsoft/Foursquare, some categories are noisy |
| OpenStreetMap | Cross-check, free map data | name, address, few phones (3.8 % in Udaipur) | Volunteer-mapped: small cities have few businesses |
| CSV import | Your own lists | whatever columns you have (name required) | UTF-8 CSV, max 15 MB / 5,000 rows per file |

## 4. Why OpenStreetMap gave "29" (analysis 2026-11-08)
Your job #8 searched **cafe** in **Udaipur** on OpenStreetMap and returned 29. A direct check of the
OpenStreetMap database shows that is *all* it has: 35 `amenity=cafe` objects in every area named
Udaipur, 29 of them with a name (unnamed ones are skipped). Nothing was lost by the tool. The same
search on Overture Places finds **246** cafés (job #9: 225 new + 21 already known); Overture has
14,807 places in Udaipur, 12,919 with a social link and 7,718 with a social link but **no website**.
Other things fixed on the way: same-name shops in different cities were merged into one; CSV
imports stopped silently at 500 rows; CSV rows with missing trailing columns were rejected.

## 5. Exports
- CSV: every column (id, name, category, industry, address, city, state, postal code, country,
  phone, email, website, website status, facebook, instagram, linkedin, tiktok, youtube, twitter,
  whatsapp, linktree, latitude, longitude, status, discovered at). Opens in Excel with Indian
  characters intact. Cells that start with `= + - @` get a leading `'` so Excel cannot run them as
  formulas (phone numbers therefore show as text — correct).
- PDF: landscape A4 summary (name, category, city, phone, email, website/social, status).
- The export always matches the current filters (country, website status, category, search, job).
- Exported files contain businesses' contact data — keep them private.
