# Round 8 — Bangladesh, Afghanistan, Myanmar, Sudan, Colombia, Thailand results; India + BD + AF next

## Results (Overture only, dentist, max 300)
| City | CC | Found | Available | Website % | Social, no website % | Phone % | Email % |
|---|---|---|---|---|---|---|---|
| Dhaka | BD | 300 | 1,277 | 47 | 53 | 100 | 84 |
| Narayanganj | BD | 300 | 714 | 39 | 61 | 99 | 80 |
| Gazipur | BD | 218 | 218 | 36 | 64 | 97 | 77 |
| Chattogram | BD | 180 | 180 | 27 | 73 | 94 | 65 |
| Sylhet | BD | 88 | 88 | 27 | 73 | 95 | 63 |
| Rajshahi | BD | 45 | 45 | 28 | 72 | 93 | 67 |
| Khulna | BD | 44 | 44 | 23 | 77 | 98 | 70 |
| Cumilla | BD | 40 | 40 | 24 | 76 | 100 | 63 |
| Rangpur | BD | 34 | 34 | 26 | 74 | 94 | 59 |
| Tarabo | BD | 31 | 31 | 17 | 83 | 100 | 63 |
| Barishal / Bogura / Brahmanbaria / Feni / Tangail / Jashore | BD | 22–27 each | same | 9–16 | 84–91 | 81–100 | 54–76 |
| Mymensingh / Savar / Kushtia / Dinajpur / Faridpur / Chandpur / Chapai Nawabganj | BD | 8–21 each | same | 0–50 | 50–100 | 80–100 | 38–87 |
| Sreepur, Kaliakair | BD | 0 | 0 | — | — | — | — |
| Kabul | AF | 155 | 155 | 22 | 78 | 96 | 73 |
| Mazar-i-Sharif | AF | 13 | 13 | 0 | 100 | 100 | 91 |
| Herat | AF | 8 | 8 | 12 | 88 | 100 | 50 |
| Kandahar | AF | 0 | 0 | — | — | — | — |
| Yangon | MM | 300 | 463 | 21 | 79 | 96 | 60 |
| Mandalay | MM | 96 | 96 | 11 | 89 | 89 | 42 |
| Khartoum / Omdurman / Khartoum North | SD | 76 / 33 / 15 | same | 7–22 | 78–93 | 87–88 | 57–66 |
| Bogotá / Medellín / Cali | CO | 300 each | 2,196 / 1,254 / 1,053 | 51–63 | 36–49 | 95–99 | 77–83 |
| Bangkok | TH | 300 | 3,355 | 63 | 37 | 100 | 70 |
| Nonthaburi / Pak Kret | TH | 153 / 107 | same | 29 | 71 | 84–88 | 34 |
| Kampala | UG | 154 | 154 | 44 | 56 | 97 | 76 |
| Dar es Salaam / Arusha / Dodoma | TZ | 35 / 7 / 2 | same | — | — | — | — |
Every city resolved to the intended place (checked in `resolved_place`); the zeros (Sreepur, Kaliakair, Kandahar,
Mbuji-Mayi) are correct places with no Overture dentist, not spelling failures.
**Bangladesh is the strongest "social profile but no website" market measured so far**: 53 % in Dhaka, 61–91 %
everywhere else, with phone ≥ 81 % and email ≥ 54 %.

## Verdicts on your round-7 points
1. NEITHER_LISTED segment — **agreed that it must not score low, and it already does not**: the approved spec
   (website-intelligence.md rows 7, 8, 10) gives a business with no website in any source the highest website-gap
   score (NO_SITE_VERIFIED = 60, vs social-only 55) once the domain-guess checks and a search check find nothing;
   without the search check it is capped at WARM as "No website identified — limited verification". A separate
   SOCIAL_ONLY / NEITHER label for reporting — **open**, founder decision (it changes an approved spec).
2. Round-6 fixes closed; Iran / DRC / Kenya kept as "limited Overture coverage" — **agreed**.
3. Batch 7 — **agreed**, running. Seberang Perai: the resolver will either match the name or report "not found";
   it never substitutes Butterworth — **agreed**.
4. Maradi border check — **agreed**, the country filter applies to every box.

## Round 8 request — the user's own priority: more India, Bangladesh, Afghanistan
`{"batch": 8, "cities": [...]}`, same format, no city from earlier batches:
- India: cities ranked 101–150 by city-proper population (state in `admin`);
- Bangladesh: cities / municipalities ranked 26–40;
- Afghanistan: cities ranked 21–30 (fewer if the list ends).
Outside the JSON, give alternate spellings only where you think Nominatim may not know your spelling.

End with the list of points still open.
