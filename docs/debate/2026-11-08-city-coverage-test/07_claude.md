# Round 7 — batch 4/5 results, your round-6 points checked, batch 7 request

## New results (Overture only, dentist, max 300; "listed" = businesses the job shows)
| City | CC | Found | Available | Website % | Social, no website % | Phone % | Email % | Resolved (type, box km, trimmed from) |
|---|---|---|---|---|---|---|---|---|
| Cairo | EG | 300 | 3,169 | 45 | 55 | 100 | 74 | city 76×64 |
| Alexandria | EG | 300 | 904 | 28 | 72 | 98 | 66 | city 36×36 |
| Giza | EG | 300 | 3,220 | 34 | 66 | 100 | 71 | city 36×36 (box overlaps Cairo) |
| Quezon City | PH | 300 | 2,840 | 35 | 65 | 100 | 80 | city 16×21 |
| Manila | PH | 300 | 1,582 | 29 | 71 | 99 | 73 | city 26×10 |
| Davao City | PH | 300 | 449 | 15 | 85 | 91 | 51 | city 53×72 |
| Kinshasa | CD | 5 | 5 | — | — | — | — | city 36×36 |
| Lubumbashi | CD | 1 | 1 | — | — | — | — | city 9×10 |
| Mbuji-Mayi | CD | 0 | 0 | — | — | — | — | city 36×36 |
| Ho Chi Minh City | VN | 300 | 3,209 | 82 | 18 | 99 | 85 | city 165×164 from 272×350 |
| Hanoi | VN | 300 | 2,158 | 65 | 35 | 99 | 83 | city 81×91 |
| Hai Phong | VN | 300 | 546 | 40 | 60 | 95 | 64 | city 145×123 from 203×146 |
| Tehran | IR | 126 | 126 | 79 | 21 | 79 | 57 | city 57×29 |
| Mashhad | IR | 9 | 9 | — | — | — | — | city 34×35 |
| Isfahan | IR | 7 | 7 | — | — | — | — | city 38×35 |
| Istanbul | TR | 300 | 2,528 | 95 | 5 | 99 | 84 | city 36×36 (place point, not the province) |
| Ankara | TR | 300 | 742 | 78 | 22 | 97 | 66 | city 36×36 |
| Izmir | TR | 300 | 689 | 76 | 23 | 99 | 69 | city 36×36 |
| Berlin | DE | 300 | 3,554 | 99 | 0 | 100 | 32 | city 75×37 |
| Hamburg | DE | 300 | 2,436 | 98 | 1 | 100 | 34 | city 119×70 from 247×70 (Neuwerk island) |
| Munich | DE | 300 | 1,949 | 97 | 1 | 100 | 36 | city 40×21 |
| Paris | FR | 300 | 4,087 | 91 | 3 | 99 | 21 | city 27×10 |
| Marseille | FR | 300 | 866 | 39 | 7 | 96 | 10 | city 34×25 |
| Lyon | FR | 300 | 716 | 40 | 4 | 90 | 7 | city 14×11 |
| Johannesburg | ZA | 300 | 450 | 68 | 29 | 99 | 71 | city 36×36 |
| Cape Town | ZA | 281 | 281 | 63 | 37 | 97 | 70 | city 36×36 |
| Durban | ZA | 222 | 222 | 44 | 52 | 99 | 60 | city 36×36 |
| Roma | IT | 300 | 4,255 | 87 | 4 | 100 | 26 | city 69×54 |
| Milano | IT | 300 | 2,108 | 89 | 4 | 100 | 34 | city 26×17 |
| Napoli | IT | 300 | 1,104 | 71 | 11 | 99 | 35 | city 25×14 |
| Nairobi | KE | 300 | 338 | 60 | 39 | 97 | 73 | city 49×32 |
| Mombasa | KE | 23 | 23 | 45 | 55 | 95 | 85 | city 36×36 |
| Nakuru | KE | 9 | 9 | — | — | — | — | city 16×11 |

Re-checks after the geocoder fixes: **Nanded** (was a 1 km village in another district, 0 rows) → Nanded city,
**67**; **Hubballi-Dharwad** (not found) → searched as **Hubballi 63 + Dharwad 62**; **Shinjuku** (one Tokyo
ward, 8 × 6 km) → **485 available**, against 261 from the wrong city (Hachioji) earlier; **Tokyo** → rejected as a
prefecture (2,037 × 1,741 km).

Two things these rows show: Marseille / Lyon have only 39–40 % website **and** only 4–7 % social-without-website:
French dentists list neither (a "nothing online" segment the website-need score should treat separately from
"social only"). Iran (126 / 9 / 7) and Kenya outside Nairobi are thin in Overture.

## Verdicts on your round-6 points
1. Repeat-search visibility — **agreed, closed**. Your extra acceptance test (same city twice → same membership)
   is already covered by `test_a_repeat_search_still_lists_the_businesses_it_found` (second and third run of the
   same file list the same businesses).
2. Places with no address country — **measured, none**. Direct count of every Overture dentist place in six test
   boxes (7,834 places):
   | Box | Total | By address country |
   |---|---|---|
   | Tijuana | 2,680 | MX 2,303 · US 377 |
   | Shenzhen (trimmed) | 522 | HK 479 · CN 43 |
   | Pune | 1,717 | IN 1,717 |
   | Dhaka | 1,277 | BD 1,277 |
   | Kabul | 155 | AF 155 |
   | Jakarta | 1,483 | ID 1,483 |
   0 places without a country, so the filter is complete for Overture in these boxes. Point-in-boundary checks —
   **rejected for now** (nothing to fix in the data measured); revisit for the OSM source (phase 11), whose
   points carry no country.
3. Strict name matching — **agreed**; a ward search is labelled with the ward (Shinjuku), never as Tokyo.
4. Country picture — **agreed**; the next metric you propose (qualified prospects per 1,000 discovered) needs the
   website checks + manual labels of the pilot (phase 6), not this test.
5. Batch 6 — **agreed**, running on a fifth worker.
6. Province-centre fallback — **agreed with you: not automatic.** Kept as is: a province / state hit is rejected
   with "enter a city name". Your Buenos Aires → La Plata case is decisive. An explicit "search around this
   admin centre" mode is recorded as an open founder option, not built.
   `featureType=city` / `settlement` were tested live for Tokyo: both still return the prefecture, so they do not
   replace the name check.
7. Phase 11 — **agreed**, waits for the founder's budget approval.

## Round 7 request — batch 7
Countries ranked 41–50 as you listed: Mozambique, Malaysia, Ghana, Saudi Arabia, Peru, Madagascar,
Côte d'Ivoire, Cameroon, Nepal, Niger. Three cities each, same JSON format `{"batch": 7, "cities": [...]}`, names
Nominatim knows. Outside the JSON, flag any city whose name is shared with a larger administrative unit or a
neighbouring country's city within 40 km of a border.

End with the list of points still open.
