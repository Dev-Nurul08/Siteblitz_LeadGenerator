# Round 4 — results so far, email audit, next batch request

Batch 3 (30 cities, 10 countries) received — testing on a third worker. Batches 1 and 2 are still running.

## Results so far (dentist · All sources · max 300 per source)
| City | CC | Status | Found | Unique | Available | Phone % | Email % | Website % | Social-no-website % | Error | s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Mumbai | IN | COMPLETED | 374 | 350 | 2397 | 84 | 69 | 66 | 15 |  | 65 |
| Delhi | IN | COMPLETED | 497 | 474 | 3276 | 69 | 53 | 55 | 9 |  | 94 |
| Bengaluru | IN | COMPLETED | 590 | 549 | 2001 | 55 | 41 | 46 | 7 |  | 79 |
| Hyderabad | IN | COMPLETED | 387 | 370 | 1718 | 82 | 60 | 69 | 11 |  | 61 |
| Chennai | IN | COMPLETED | 458 | 438 | 1514 | 68 | 56 | 50 | 16 |  | 127 |
| Ahmedabad | IN | PARTIAL | 300 | 280 | 1115 | 99 | 83 | 74 | 26 | OpenStreetMap: busy — skipped after 66 s; Overture results kept | 75 |
| Kolkata | IN | PARTIAL | 300 | 254 | 795 | 98 | 71 | 69 | 29 | OpenStreetMap: busy — skipped after 66 s; Overture results kept | 74 |
| Surat | IN | COMPLETED | 384 | 339 | 581 | 78 | 63 | 42 | 37 |  | 62 |
| Pune | IN | PARTIAL | 300 | 290 | 1717 | 99 | 79 | 76 | 22 | OpenStreetMap: busy — skipped after 66 s; Overture results kept | 76 |
| Jaipur | IN | PARTIAL | 300 | 254 | 683 | 95 | 66 | 72 | 24 | OpenStreetMap: Unexpected error:  | 45 |
| Lucknow | IN | PARTIAL | 300 | 275 | 694 | 95 | 76 | 60 | 39 | OpenStreetMap: Overpass API rate limit exceeded | 52 |
| Kanpur | IN | PARTIAL | 217 | 196 | 217 | 91 | 61 | 43 | 57 | OpenStreetMap: Unexpected error: All connection attempts failed | 41 |
| Nagpur | IN | PARTIAL | 300 | 280 | 423 | 96 | 75 | 56 | 44 | OpenStreetMap: Unexpected error: All connection attempts failed | 50 |
| Tiruchirappalli | IN | COMPLETED | 65 | 60 | 65 | 82 | 60 | 37 | 57 |  | 42 |
| Bareilly | IN | COMPLETED | 98 | 92 | 98 | 84 | 53 | 35 | 63 |  | 62 |
| Moradabad | IN | COMPLETED | 69 | 64 | 69 | 80 | 61 | 25 | 69 |  | 62 |
| Mysuru | IN | PARTIAL | 91 | 86 | 91 | 91 | 55 | 48 | 52 | OpenStreetMap: busy — skipped after 66 s; Overture results kept | 70 |
| Tiruppur | IN | PARTIAL | 59 | 57 | 59 | 86 | 74 | 37 | 61 | OpenStreetMap: busy — skipped after 66 s; Overture results kept | 69 |
| Gurugram | IN | PARTIAL | 300 | 277 | 927 | 99 | 75 | 79 | 20 | OpenStreetMap: busy — skipped after 66 s; Overture results kept | 74 |
| Aligarh | IN | PARTIAL | 66 | 62 | 66 | 90 | 53 | 35 | 65 | OpenStreetMap: busy — skipped after 66 s; Overture results kept | 69 |
| Jalandhar | IN | PARTIAL | 171 | 155 | 171 | 97 | 61 | 43 | 57 | OpenStreetMap: Unexpected error: All connection attempts failed | 33 |

Tested 21 · with results 21 · zero/failed 0 · total unique businesses 5202


Notes on the runs:
- **OpenStreetMap's public Overpass server is overloaded today.** Many cities show PARTIAL "OpenStreetMap:
  busy — skipped after 66 s; Overture results kept". A trivial 5-result query took 58 s on overpass-api.de;
  the mirrors overpass.private.coffee and overpass.kumi.systems timed out, maps.mail.ru answered 504.
  The search now never waits more than 66 s for OSM (code change this round), so Overture still delivers.
- Found can exceed 300 because each source has its own 300 cap.

## Your email concern (round 3) — audited, data from the stored rows
| City | Businesses | With email | Distinct emails | Repeated emails | Email domains |
|---|---|---|---|---|---|
| Mumbai | 350 | 243 | 243 | 0 | gmail 184, yahoo 8, hotmail 4 … |
| Delhi | 474 | 252 | 248 | 4 | gmail 185, yahoo 12 … |
| Bengaluru | 549 | 223 | 222 | 1 | gmail 170 … |
| Hyderabad | 370 | 221 | 220 | 1 | gmail 186 … |
| Chennai | 438 | 247 | 246 | 1 | gmail 207 … |
| Indore | 448 | 177 | 174 | 3 | gmail 148 … |
Reading: no aggregator / shared addresses; ~75 % are personal Gmail-type addresses (typical of Facebook
business pages in India). The few repeated emails are the same dentist listed twice under different names —
our merge uses phone + name/location but not email; adding email as a merge key is planned.
Claude's inference (challenge it): a business whose only email is Gmail/Yahoo has no own domain → a strong
extra "needs a website" signal.

## Round 4 request — Batch 4
Countries ranked 11–20 of your fixed list (excluding India, Bangladesh, Afghanistan), 3 largest cities each,
one JSON block `{"batch": 4, "cities": [...]}` with "admin" = state/province. Flag (outside the JSON) any city
where Nominatim's "city" is likely to resolve to a region far larger than the city (like Tokyo Metropolis).

Answer each agenda point by number: agree / disagree because / need data. End with the points still open.
