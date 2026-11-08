# Round 9 — Afghanistan, batch 6 and first batch 7 rows; a resolver validation batch; lawful extra sources

## New results (Overture only, dentist, max 300)
| City | CC | Found | Available | Website % | Social, no website % | Phone % | Email % |
|---|---|---|---|---|---|---|---|
| Baghdad | IQ | 300 | 729 | 17 | 83 | 94 | 45 |
| Mosul / Basra | IQ | 84 / 93 | same | 6–10 | 90–94 | 91–95 | 28–33 |
| Madrid / Barcelona / Valencia | ES | 300 each | 4,363 / 2,037 / 1,170 | 85–97 | 0–4 | 100 | 18–38 |
| Buenos Aires | AR | 300 | 1,385 | 64 | 36 | 97 | 76 |
| Córdoba / Rosario | AR | 300 / 233 | 660 / 233 | 36 | 64 | 93–98 | 66–70 |
| Sana'a / Aden / Taiz | YE | 118 / 18 / 4 | same | 22–50 | 50–78 | 98–100 | 28–75 |
| Maputo / Matola / Nampula | MZ | 39 / 26 / 1 | same | 23–26 | 74–77 | 92 | 62–63 |
| Kuala Lumpur | MY | 300 | 895 | 70 | 30 | 100 | 84 |
| Kajang | MY | 300 | 427 | 52 | 48 | 99 | 73 |
| Kunduz / Jalalabad / Taloqan / Sheberghan / Ghazni | AF | 3 / 12 / 2 / 1 / 1 | same | 0 | 100 | 100 | 0–75 |
| Charikar / Baghlan | AF | 0 | 0 | — | — | — | — |
Not found by name: **Seberang Perai** (as you predicted; nothing substituted), **Pul-e-Khumri**, **Lashkargah**.
Afghanistan outside Kabul (155) has 0–13 dentists per city in Overture — a source gap.
Iraq has the highest "social but no website" share measured: 83–94 %.

## Patterns across 246 tested cities (dentist, Overture)
1. Website share is high (85–99 %) in the US, Japan, Germany, Spain, Italy, Russia and the capitals of France;
   social-but-no-website is ≤ 5 % there.
2. Social-but-no-website is highest in Iraq (83–94 %), Bangladesh outside Dhaka (61–91 %), Myanmar, Sudan,
   Afghanistan, Indian cities with < 300 dentists (median 59 %), Philippines, Egypt, Indonesia (55–85 %).
3. France outside Paris is a separate "nothing online" pattern (website 39–40 %, social 4–7 %).
4. Overture is near-empty for dentists in China, DR Congo, Afghanistan outside Kabul, Iran outside Tehran,
   secondary Kenyan / Tanzanian / Mozambican cities.
5. Phone is listed for 79–100 % almost everywhere; email varies most (7–10 % Lyon / Marseille, 18 % Madrid,
   ≥ 60 % in most of South Asia and the Middle East).

## Round 9 request — two parts
**A. Resolver validation batch (20 cities).** Pick 20 names that are hard for a geocoder: a city sharing its
name with a city in another state of the same country, renamed cities given by their old name, cities that
are also a district / province name, a city within 30 km of a border. For each, give the place you expect it
to resolve to, so the result can be scored:
`{"batch": 9, "cities": [{"city": "...", "country_code": "..", "admin": "...", "expect": "<expected place, e.g. the district or the old/new name>"}]}`
Use countries from the earlier batches. Include Pul-e-Khumri and Lashkargah with the spelling you think
Nominatim knows, and Butterworth (MY).

**B. Lawful supplementary sources for the thin countries** (Afghanistan, Iran, China, DR Congo, Kenya /
Tanzania / Mozambique outside the capital). For each: one source that a small company may legally use for
business discovery (open data licence or paid API with terms that allow storing the result), what it costs,
and the licence condition that matters. No scraping of sites whose terms forbid it. Give sources.

End with the list of points still open.
