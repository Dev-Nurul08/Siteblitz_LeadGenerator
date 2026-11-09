## Check of your message-11 list
Round 11: 260 reference lines, 260 cities, 253 with business data (97 %).
Not covered: - FM: 9/10 cities covered, 498 businesses near them; no data at: Tol
Not covered: - MH: 28/31 cities covered, 538 businesses near them; no data at: Airuk, Jabat, Lib
Not covered: - MR: 16/17 cities covered, 4,364 businesses near them; no data at: Guerou
Not covered: - MU: 16/18 cities covered, 72,942 businesses near them; no data at: Vingt Cinq, Raphael Island

Same format again:


## Message 12 of 19 - countries
Moldova (MD), Monaco (MC), Mongolia (MN), Montenegro (ME), Montserrat (MS), Morocco (MA), Mozambique (MZ), Myanmar (Burma) (MM), Namibia (NA), Nauru (NR), Nepal (NP), Netherlands (NL), New Caledonia (NC)

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
