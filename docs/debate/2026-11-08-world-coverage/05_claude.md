## Check of your lists so far (businesses in our data within 10 km of each city, or with that city name)
Round 1: 263 reference lines, 260 cities, 259 with business data (100 %).
Round 2: 251 reference lines, 251 cities, 250 with business data (100 %).
Round 3: 192 reference lines, 190 cities, 190 with business data (100 %).
Round 4: 221 reference lines, 221 cities, 221 with business data (100 %).
Not covered: - AS: 11/12 cities covered, 4,958 businesses near them; no data at: Taulaga
Not covered: - BS: 33/34 cities covered, 13,861 businesses near them; no data at: Moxey Town

Thank you - same format again:


## Message 5 of 19 - countries
Congo - Kinshasa (CD), Cook Islands (CK), Costa Rica (CR), Côte d’Ivoire (CI), Croatia (HR), Cuba (CU), Curaçao (CW), Cyprus (CY), Czechia (CZ), Denmark (DK), Djibouti (DJ), Dominica (DM), Dominican Republic (DO)

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
