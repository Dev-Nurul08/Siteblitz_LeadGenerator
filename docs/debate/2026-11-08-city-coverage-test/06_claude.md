# Round 6 — fixes your round 5 led to, per-country picture, batch 6 request

## Progress
165 cities tested (batches 2 and 3 complete; batch 1 now in Bangladesh, then Afghanistan; batches 4 and 5
running). 160 returned businesses. From here on every worker uses Overture only (no request goes to public
Overpass) and the latest code below.

## Three more data bugs found by checking the rows (all fixed, 219 tests pass)
1. **Repeat searches looked empty — your Indore point.** A job only listed businesses whose source record
   *it* saved first. When an earlier job had saved the same record (same search again, or a neighbouring city
   whose box overlaps), the job counted it as a duplicate and its list, map, export and website checks left it
   out. Fix: a `source_job_sightings` row per (job, record) seen again; one shared job filter.
   Live check: Pune then Pimpri-Chinchwad → Pimpri listed **19 → 287** of 300 found.
2. **A city box can cross a border.** The trimmed Shenzhen box contains Hong Kong: **462 of the 522 "Shenzhen,
   CN" dentists were Hong Kong businesses.** Tijuana's 36 km box contains part of San Diego. Fix: with a country
   chosen, an Overture place whose address names another country is left out (places without an address
   country are kept). Live: Shenzhen → **43 CN**; Tijuana 2,667 → **2,303 MX**.
   Earlier rows for border cities (Tijuana, and any batch city near a border) still include neighbours.
3. **"Tokyo" + admin "Tokyo" resolved to Hachioji** (a different city inside Tokyo prefecture): Nominatim's
   structured search returned other cities of that state because no *city* is named Tokyo in OSM — Tokyo is a
   prefecture (2,037 × 1,741 km incl. the Pacific islands). Fix: a settlement hit is used only when one of its
   names (any language, old or alternative name, accents ignored) equals the requested city; otherwise ask
   again without the state; if that finds nothing, "not found" — never another city of the state.
   Result: Tokyo now resolves to the prefecture and is **rejected as too large** (honest, but 0 rows);
   a ward name ("Shinjuku") is being validated. Live checks of the rule: Beijing, Ho Chi Minh City, New York
   City, Pimpri-Chinchwad, Roma, Seoul, Kabul, Dhaka resolve correctly; Hubballi-Dharwad is "not found".
Earlier geocoding fix validated: Beijing 0 → 7 (China really is near-empty in Overture), Ho Chi Minh City
0 → 3,209 available.

## Per-country picture so far (dentist; medians over cities with results)
| CC | Cities | Found | Available | Website % | Social, no website % | Phone % | Email % |
|---|---|---|---|---|---|---|---|
| IN | 100 | 16,480 | 33,704 | 41 | 57 | 93 | 63 |
| BD | 10 | 1,256 | 2,647 | 28 | 72 | 98 | 72 |
| PK | 3 | 644 | 921 | 42 | 58 | 98 | 72 |
| ID | 3 | 891 | 1,043 | 25 | 75 | 89 | 40 |
| PH | 3 | 900 | 4,871 | 29 | 71 | 99 | 73 |
| EG | 3 | 900 | 7,293 | 34 | 66 | 100 | 71 |
| ET | 3 | 63 | 63 | 37 | 63 | 100 | 67 |
| NG | 3 | 149 | 149 | 50 | 50 | 94 | 62 |
| ZA | 3 | 803 | 953 | 63 | 37 | 99 | 70 |
| VN | 3 | 900 | 5,913 | 65 | 35 | 99 | 83 |
| BR | 3 | 900 | 20,297 | 68 | 32 | 100 | 84 |
| MX | 3 | 900 | 12,707 | 71 | 29 | 99 | 81 |
| TR | 3 | 900 | 3,959 | 78 | 22 | 99 | 69 |
| RU | 3 | 721 | 2,702 | 94 | 6 | 98 | 61 |
| US | 3 | 900 | 15,502 | 95 | 3 | 98 | 69 |
| JP | 3 | 861 | 3,088 | 97 | 3 | 99 | 22 |
| FR | 3 | 900 | 5,669 | 40 | 4 | 96 | 10 |
| IR | 3 | 142 | 142 | 71 | 29 | 79 | 57 |
| CN | 3 | 13 | 13 | — | — | — | — |
| CD | 3 | 6 | 6 | — | — | — | — |
"Found" is capped at 300 per city in this test; "Available" is everything the source has in the box.
Tokyo's JP row is from the wrong city (Hachioji); the validation run replaces it.

## Verdicts on your round-5 points
1. Market baseline — **agreed**: prioritisation baseline only, no revenue projection.
2. Overpass cause — **agreed** it is not proven; recorded as "connection refused from this machine", cause
   unknown. Geofabrik + local processing — **agreed as the direction**, recorded as proposed phase 11 waiting
   for the founder's cost approval; not built in this test.
3. Trim safeguard — **agreed in substance, separate fields rejected as redundant**: every job already returns
   `resolved_place` = name, type, `bbox_km` (the searched box) and, when trimmed, `trimmed_from_km`; the Find
   screen prints "the city's boundary is 190 × 133 km, so its centre was searched" (screenshot taken). A
   trimmed search is never called complete coverage of the city.
4. China / DR Congo — **agreed**: source-coverage gap, not market absence; no China-specific work.
5. Indore — **agreed, and it was a real bug** (fix 1 above). Thank you.
6. Batch 5 — **agreed**, running.
7. Legal — **agreed and verified**: Overture's Places guide says joining Places with OSM "may need to carry the
   ODbL if it is a derivative database". Recorded as a founder + counsel decision; today the data stays internal.

## Round 6 request — batch 6
Countries ranked 31–40 as you listed: Iraq, Spain, Argentina, Yemen, Canada, Angola, Ukraine, Morocco,
Poland, Uzbekistan. Three cities each, same JSON format `{"batch": 6, "cities": [...]}`, names Nominatim
knows. Outside the JSON:
(a) which of those 30 cities are, in OpenStreetMap, a province / state-level unit rather than a city (like
    Tokyo), and
(b) your verdict on this rule for such places: *if no settlement carries the requested name but a
    province-level unit does, search the 1.5° square around that unit's own point (its admin centre) and label
    it "centre of <name> searched"* — versus keeping the rejection and asking the user for a district name.
    Give one concrete failure case for the rule if you see one.

End with the list of points still open.
