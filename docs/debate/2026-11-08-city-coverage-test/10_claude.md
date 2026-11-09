# Round 10 (final) — totals, resolver validation scored, one more bug, final review request

## Totals
- **357 population-ranked cities in 52 countries** tested (India 150, Bangladesh 38, Afghanistan 22, 3 each in
  49 other countries), plus 37 re-check / validation searches. 316 cities returned businesses; 41 returned 0.
- **46,734 dentist records found** (test cap 300 per city); the sources hold **190,872** in those boxes.
- 8 Bangladesh cities of batch 8 hit a local DNS outage ("getaddrinfo failed") and are being retried; they are
  network failures, not resolver or data failures.

## Batch 9 — resolver validation, scored against your `expect`
**20 / 20 resolved to the expected place; 0 wrong cities accepted.**
| Group | Inputs | Result |
|---|---|---|
| Old names | Aurangabad, Allahabad, Ahmednagar, Gurgaon | → Chhatrapati Sambhajinagar, Prayagraj, Ahilyanagar, Gurugram (old_name in Nominatim's names) |
| Same name, two states | Bilaspur CG / HP, Springfield IL / MA, Portland ME / OR | 6 / 6 in the right state (e.g. Portland ME 138 vs OR 1,018 available) |
| Earlier failures | Puli Khumri, Lashkar Gah, Butterworth | correct places (Butterworth = Bandar Butterworth, 5 × 7 km, not Seberang Perai) |
| City vs region | Riyadh, Nairobi | the city, not the region |
| Border | Tijuana, San Diego, Goma, Zaranj, Abadan | listed businesses: Tijuana MX 289 / 0 US · San Diego US 296 / 0 MX · Goma CD 1 · Zaranj AF 1 · Abadan IR 3 |
Three inputs (Goma, Zaranj, Abadan) first failed in the DNS outage and passed on retry.

## One more bug found by the test (fixed)
**Wrocław failed with `'charmap' codec can't encode character 'ł'`.** On Windows, a backend whose output is
redirected uses the cp1252 code page; a log line containing the city name raised an exception and failed the
whole job. Any city outside cp1252 (Łódź, Hà Nội, Cyrillic or Devanagari input) would fail. Fix: the API now
writes stdout / stderr as UTF-8 with a replacement fallback. Reproduced before the fix, gone after; 221 tests pass.

## Final country picture (dentist, Overture; medians of cities with results)
| Most "social profile, no website" | Website % | Social, no website % | Phone % | Email % |
|---|---|---|---|---|
| Iraq | 10 | 90 | 94 | 33 |
| Sudan | 13 | 87 | 88 | 60 |
| Myanmar | 15 | 85 | 89 | 42 |
| Bangladesh (38 cities) | 20 | 80 | 98 | 68 |
| Yemen / Mozambique / Algeria | 23–24 | 76–77 | 92–100 | 59–71 |
| Indonesia / Philippines / Thailand | 25–29 | 71–75 | 88–99 | 34–73 |
| Egypt / Morocco / Argentina | 34–36 | 64–66 | 97–100 | 70–75 |
| India (150 cities) | 39 | 60 | 93 | 63 |
| Pakistan / Nepal | 40–42 | 58–60 | 94–98 | 66–72 |

| Least (website already listed) | Website % | Social, no website % |
|---|---|---|
| Canada, Germany, Japan, US, Spain, UK | 92–99 | 1–3 |
| Italy, Poland, Russia | 87–94 | 4–10 |
| France (Marseille / Lyon) | 39–40 | 4–7 (neither listed) |

Source gaps (0–43 dentists per city, most under 15): China, DR Congo, Madagascar, Niger, Angola outside Luanda, Afghanistan
outside Kabul, Iran outside Tehran, secondary cities in Ghana, Kenya, Tanzania, Côte d'Ivoire, Cameroon.

## What changed in the product because of this test (all committed)
1. Repeat / overlapping searches list what they found (job sightings) — Pimpri-Chinchwad 19 → 287.
2. Results limited to the chosen country — Shenzhen 522 (479 Hong Kong) → 43; Tijuana −377 US.
3. Geocoder: settlement only if it carries the requested name (any language / old name); city beats a same-named
   village; landmark-only = not found; whole-municipality boxes trimmed to 1.5° and labelled; province-only
   names rejected (Tokyo) — 20 / 20 on your validation batch.
4. All 249 countries selectable on the Find screen (it had 10: Bangladesh and Afghanistan were not selectable).
5. UTF-8 logging (Wrocław).
6. Searched area + trim shown on the Find screen.

## Final review request
Answer by number:
1. For each of the six changes above: is anything still missing before a founder relies on it? One line each.
2. Your verdict on what this test does **not** prove (I list: category precision, real website absence, contact
   accuracy, OSM coverage while Overpass was unreachable, Foursquare OS increment). Add anything missing.
3. Rank the open founder decisions by value per cost: Geofabrik OSM (phase 11), Foursquare OS Places (phase 12),
   SOCIAL_ONLY / NEITHER reporting labels, dead-domain = Website down immediately, social-only Hot cap,
   admin-centre search mode, ODbL legal review. One sentence of reason each.
4. Which 3 countries should the pilot (phase 6) use first, from the data above, and why.

End with the final list of points still open.
