# Round 5 — results 22–56, a public Overpass block, three geocoding failures fixed, batch 5 request

Search for every city: category dentist · max 300 per source · All sources (Overture + OpenStreetMap)
unless noted. 56 cities tested so far, 54 returned businesses, 10,563 unique businesses saved.

## Results since round 4 (35 cities)
| City | CC | Found | Available | Phone % | Email % | Website % | Social, no website % | Resolved to (type, box km) |
|---|---|---|---|---|---|---|---|---|
| Indore | IN | 300 | 364 | 0 | 0 | 0 | 0 | city, [36, 36] |
| Thane | IN | 300 | 511 | 97 | 68 | 63 | 37 | administrative, [19, 19] |
| Bhopal | IN | 280 | 280 | 93 | 66 | 44 | 56 | city, [36, 36] |
| Visakhapatnam | IN | 231 | 231 | 94 | 64 | 56 | 43 | city, [36, 36] |
| Pimpri-Chinchwad | IN | 300 | 1563 | 100 | 95 | 84 | 16 | city, [36, 36] |
| Patna | IN | 300 | 439 | 97 | 68 | 52 | 47 | city, [28, 12] |
| Vadodara | IN | 300 | 431 | 96 | 70 | 59 | 41 | city, [36, 36] |
| Ghaziabad | IN | 300 | 1337 | 98 | 75 | 78 | 22 | city, [36, 36] |
| Ludhiana | IN | 264 | 264 | 93 | 65 | 43 | 56 | city, [36, 36] |
| Agra | IN | 156 | 156 | 91 | 68 | 32 | 68 | city, [36, 36] |
| Nashik | IN | 239 | 239 | 94 | 63 | 43 | 57 | city, [36, 36] |
| Bhubaneswar | IN | 187 | 187 | 96 | 71 | 51 | 48 | city, [36, 36] |
| Salem | IN | 75 | 75 | 94 | 68 | 35 | 64 | city, [36, 36] |
| Mira-Bhayandar | IN | 250 | 250 | 95 | 69 | 49 | 49 | administrative, [18, 11] |
| Warangal | IN | 45 | 45 | 95 | 51 | 41 | 59 | city, [36, 36] |
| Thiruvananthapuram | IN | 269 | 269 | 95 | 66 | 42 | 57 | city, [36, 36] |
| Guntur | IN | 91 | 91 | 96 | 60 | 49 | 51 | city, [36, 36] |
| Bhiwandi | IN | 26 | 26 | 83 | 67 | 29 | 71 | city, [5, 4] |
| Saharanpur | IN | 50 | 50 | 86 | 63 | 29 | 71 | city, [36, 36] |
| Gorakhpur | IN | 104 | 104 | 95 | 55 | 33 | 66 | city, [36, 36] |
| Bikaner | IN | 29 | 29 | 100 | 64 | 16 | 84 | city, [36, 36] |
| Amravati | IN | 52 | 52 | 90 | 65 | 27 | 73 | city, [36, 36] |
| Noida | IN | 300 | 703 | 95 | 59 | 77 | 19 | administrative, [24, 26] |
| Jamshedpur | IN | 84 | 84 | 94 | 58 | 36 | 64 | city, [36, 36] |
| Bhilai | IN | 75 | 75 | 90 | 49 | 30 | 68 | city, [36, 36] |
| Cuttack | IN | 98 | 98 | 80 | 58 | 56 | 44 | city, [36, 36] |
| Shanghai | CN | 13 | 13 | 100 | 69 | 100 | 0 | city, [36, 36] |
| Beijing | CN | 0 | 0 |  |  |  |  | commercial, [1, 2] |
| Shenzhen | CN | 0 | 0 |  |  |  |  | administrative, [190, 133] |
| New York City | US | 300 | 7551 | 99 | 72 | 95 | 3 | administrative, [62, 49] |
| Los Angeles | US | 300 | 5395 | 98 | 69 | 96 | 2 | administrative, [57, 75] |
| Chicago | US | 300 | 2556 | 98 | 64 | 94 | 3 | administrative, [46, 42] |
| Jakarta | ID | 300 | 452 | 92 | 40 | 33 | 67 | administrative, [15, 25] |
| Surabaya | ID | 293 | 293 | 89 | 40 | 25 | 75 | administrative, [28, 19] |
| Cairo | EG | 300 | 3169 | 100 | 74 | 45 | 55 | city, [76, 64] |
"Available" = matches before the 300 cap; where it is below 300 the source had nothing more for that box.

## What these rows show (checked in the data, not inferred)
1. **OpenStreetMap is blocked for this machine, not just busy.** In the last 37 cities every Overpass call failed
   with "All connection attempts failed". A direct check: `overpass-api.de` refuses the TCP connection
   (connect time 0 s); `overpass.private.coffee` connects but returns nothing in 12 s; `maps.mail.ru` returns
   504. Cause, my reading: three test workers ran as three separate processes; the new Overpass lock is per
   process, so up to three requests overlapped from one IP. Every OSM part since then failed fast and the
   Overture rows were kept (status PARTIAL). Batch 4 now runs with Overture only so no further requests
   go to Overpass. Production runs one process, so the per-process lock is a real global queue there.
2. **Three geocoding failures, now fixed and committed (86efeab, 5 new tests, 215 pass):**
   - Beijing + admin "Beijing" → Nominatim's first hit was 北京金融街 (a 1 × 2 km commercial landuse) → 0.
   - Ho Chi Minh City + its admin → a radio-TV station building (0 × 0 km) → 0.
   - Shenzhen → the whole municipality, 1.7° × 1.2° → rejected by the 1.5° guard → 0.
   Fix: ask Nominatim for 5 hits and take the first whose address type is city / town / village /
   municipality; if the state-qualified lookup has none, ask again without the state; a city (not a state
   or district) whose boundary is larger than 1.5° is trimmed to the 1.5° square around the city's point,
   kept inside its boundary, and the job records `trimmed_from_km` so the trim is visible. Batch 4 is being
   re-run with this code (the first run of it gave HCMC = 0 for this reason).
3. **China is close to empty in both open sources**: Shanghai 13 dentists in a 36 km box around the centre.
   **DR Congo too** (first batch-4 run, Overture only): Kinshasa 5, Lubumbashi 1, Mbuji-Mayi 0 — with the
   correct city resolved (Kinshasa city node, 36 km box).
4. **Overlap between neighbouring cities is caught**: Pimpri-Chinchwad 282 of 300 were already saved from
   Pune (the boxes overlap); Cuttack 53 of 98 from Bhubaneswar. Indore's 300/300 duplicates are a test
   artefact: an earlier interrupted run had already saved them.
5. **Smaller Indian cities have far more businesses without a website.** Indian cities with ≥ 300 dentists
   available (19 cities): median website 66 %, social-but-no-website 22 %. Cities with < 300 available
   (27 cities): website 37 %, social-but-no-website 59 %. Phone stays 93–96 %, email 63–69 % in both.
   US cities (3): website 94–96 %, social-but-no-website 2–3 %.

## Verdicts on your round-4 points
1. Coverage qualification — **agreed**: PARTIAL stays PARTIAL in every table; your 5,202 correction noted.
2. Overpass — **agreed** on fail-fast and on not relying on public mirrors (point 1 above: they are down
   too). Global queue — **done for one process**; this test showed several processes from one IP can still
   overlap, so tests now use one OSM worker at most. Your three outcome labels — **open**: the job already
   returns PARTIAL + the per-source error; a separate OSM_DEFERRED retry queue belongs to the background-job
   phase (phase 3), not this test.
3. Email fields — **agreed** on present / unique-within-city / verified as separate facts; **open** (not built:
   no verification provider is connected; nothing is sent).
4. Free-email inference — **agreed**, it is not proof of no website. Kept as a prioritisation signal only;
   **open** until your 50 + 50 comparison is run (needs manual website checks).
5. Email dedup — **agreed and implemented** (2fb0ad1): a shared phone or email merges only with a second
   sign — within 0.5 km, or one name's distinctive words contained in the other's; branches stay separate.
   Test `test_shared_head_office_email_does_not_merge_two_branches`.
6. Batch 4 — **agreed**, running (re-run with the geocoding fix).
7. Geographic ambiguity — **partly agreed**: a box that is not a settlement is no longer used (fix above).
   **Rejected**: returning nothing with GEOGRAPHY_REVIEW_REQUIRED for oversized cities — the user asked for
   as much data per run as possible; the trimmed box is the city's own centre, inside its own boundary, and
   the trim is recorded on the job. A state or district hit is still rejected, never trimmed.

## Round 5 request — batch 5
Countries ranked 21–30 by population, as you listed: France, South Africa, Italy, Kenya, Myanmar,
Colombia, Sudan, Uganda, South Korea, Algeria. Three cities each (largest by city-proper population), same
JSON format:
`{"batch": 5, "cities": [{"city": "...", "country_code": "FR", "admin": "<state / province / region>"}, ...]}`
Use the city name Nominatim most likely knows (English or local). Outside the JSON, list any city whose
administrative boundary is much larger than its urban core.

Then one question for production: with public Overpass unusable at volume, which lawful way of getting
OSM business points per country do you recommend — regional extracts (e.g. Geofabrik) filtered locally,
a self-hosted Overpass, or something else — and what does each cost to run? Give sources.

End with the list of points still open.
