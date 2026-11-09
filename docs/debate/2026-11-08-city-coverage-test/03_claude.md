# Round 3 â€” first measured results + next batch request

## Batch 2 received (50 Indian cities) â€” testing started on a second worker. Thanks for the spelling list;
it is used only if a name fails.

## Batch 1 â€” first measured results (category dentist, All sources, max 300 per source)
| City | CC | Status | Found | Unique | Available | Phone % | Email % | Website % | Social-no-website % | Error | s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Mumbai | IN | COMPLETED | 374 | 350 | 2397 | 84 | 69 | 66 | 15 |  | 65 |
| Delhi | IN | COMPLETED | 497 | 474 | 3276 | 69 | 53 | 55 | 9 |  | 94 |
| Bengaluru | IN | COMPLETED | 590 | 549 | 2001 | 55 | 41 | 46 | 7 |  | 79 |
| Hyderabad | IN | COMPLETED | 387 | 370 | 1718 | 82 | 60 | 69 | 11 |  | 61 |

Tested 4 · with results 4 · zero/failed 0 · total unique businesses 1743

Columns: Found = rows returned by both sources; Unique = businesses after merging duplicates; Available =
all matches in the city box before the cap (Overture count); Phone / Email / Website = share of unique
businesses with that field; Social-no-website = has a Facebook/Instagram/etc. link but no website (the
founder's prime target). The 300 cap per source is clearly hit in metros (Mumbai 2,397 available).

Agenda point 2: does anything in these first four look like a wrong area or a suspicious count?

## Round 3 request â€” Batch 3
The top 50 countries by population, EXCLUDING India, Bangladesh and Afghanistan. Give countries ranked
1â€“10 of that list now, with each country's 3 largest cities (city proper), one JSON block:
`{"batch": 3, "cities": [{"city": "...", "country_code": "XX", "admin": "<state/province>"}, ...]}`
(30 cities). Use the English spelling OpenStreetMap / Nominatim uses. Also give, outside the JSON, the full
ranked list of the 50 countries (ISO codes) you will use for rounds 4â€“7, so the batches stay consistent.

End with the list of points still open.
