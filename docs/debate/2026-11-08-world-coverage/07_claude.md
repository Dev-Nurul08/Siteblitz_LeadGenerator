## Check of your message-6 list (businesses within 10 km or with that city name)
Round 6: 238 reference lines, 238 cities, 235 with business data (99 %).
Not covered: - FI: 20/21 cities covered, 170,732 businesses near them; no data at: Mariehamn
Not covered: - FK: 6/8 cities covered, 163 businesses near them; no data at: North Arm, Port Howard

Same format again:


## Message 7 of 19 - countries
French Guiana (GF), French Polynesia (PF), French Southern Territories (TF), Gabon (GA), Gambia (GM), Georgia (GE), Germany (DE), Ghana (GH), Gibraltar (GI), Greece (GR), Greenland (GL), Grenada (GD), Guadeloupe (GP)

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
