## Check of your message-15 list
Round 15: 271 reference lines, 271 cities, 267 with business data (99 %).
Not covered: - RS: 27/31 cities covered, 80,266 businesses near them; no data at: Pristina, Gjilan, Peja, Prizren

Same format again:


## Message 16 of 19 - countries
Slovenia (SI), Solomon Islands (SB), Somalia (SO), South Africa (ZA), South Georgia & South Sandwich Islands (GS), South Korea (KR), South Sudan (SS), Spain (ES), Sri Lanka (LK), St. Barthélemy (BL), St. Helena (SH), St. Kitts & Nevis (KN), St. Lucia (LC)

For EACH country above give:
1. every first-level administrative division (state / province / region / governorate ... as it is today),
   with its capital or largest city (kind S);
2. the 10 largest cities of the country by population (kind N) - fewer if the country has fewer.
   A city can appear as both S and N; list it once with kind SN.
Uninhabited territories: one line `CC|-|-|||none`.

Output ONLY one code block, one line per city, pipe-separated, no header, no commentary inside it:
`CC|state|city|lat|lon|kind`
- CC = ISO code above; state and city in English (the name a map would show); lat / lon with 2 decimals.
After the code block: one line per country with any naming caveat (renamed divisions, disputed areas),
then the list of points still open.
