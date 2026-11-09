## Check of your message-14 list
Round 14: 386 reference lines, 386 cities, 385 with business data (100 %).
Not covered: - PA: 16/17 cities covered, 50,653 businesses near them; no data at: Gaigirgordub

Same format again:


## Message 15 of 19 - countries
Russia (RU), Rwanda (RW), Samoa (WS), San Marino (SM), São Tomé & Príncipe (ST), Saudi Arabia (SA), Senegal (SN), Serbia (RS), Seychelles (SC), Sierra Leone (SL), Singapore (SG), Sint Maarten (SX), Slovakia (SK)

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
