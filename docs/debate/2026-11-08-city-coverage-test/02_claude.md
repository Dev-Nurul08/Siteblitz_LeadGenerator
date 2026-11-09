# Round 2 — verdicts on your round 1 + next batch request

Batch 1 (95 cities) was received and is being tested now (≈ 60–80 s per city, one at a time, so the free
OSM / Nominatim servers are not loaded). Its results come in round 3.

## Verdicts on your round-1 points
1. City selection — **agreed**; the population reference year is recorded in our notes as you stated it.
2. Geocoding — **agreed and already changed**: (a) the `admin` field you give is now passed to Nominatim as
   `state=` to disambiguate same-named cities; (b) every search now returns what the name resolved to
   (Nominatim display name, type, box size in km), and the test records it. Nominatim usage: one lookup per
   city, cached, ≥ 1 s apart, identifying User-Agent — ≈ 300 lookups over several hours for this whole test.
   A self-hosted geocoder is noted for production volume — **open** (cost decision for the founder).
3. 300 cap — **agreed**: the tool already reports `available` (all matches before the cap) and the UI says
   "raise Max results" when capped; the test records found vs available, so capped ≠ complete.
4. Category precision — **agreed** that precision must be measured; **rejected** for this test run to split
   category-only vs name-only (the test measures coverage per city; a precision audit of 120 rows is a
   separate founder task, recorded as open).
5. Metrics — **agreed** on source-specific counts and resolved place; cross-city duplicates are not possible
   in one search (each search is one city box) — **rejected** as not applicable.
6. Ten rounds — **agreed**: R9 and R10 will each also carry a fresh validation batch.

## Round 2 request — Batch 2
India's next 50 cities by population (ranks 51–100, city proper), none from batch 1, same JSON format:
`{"batch": 2, "cities": [{"city": "...", "country_code": "IN", "admin": "<state>"}, ...]}`.
Then list (outside the JSON) any batch-1 names whose spelling you are not sure Nominatim knows, with the
alternate spelling.

End with the list of points still open.
