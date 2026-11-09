## Check of your message-12 list
Round 12: 233 reference lines, 233 cities, 231 with business data (99 %).
Not covered: - NL: 20/22 cities covered, 537,748 businesses near them; no data at: The Bottom, Oranjestad

Same format again:


## Message 13 of 19 - countries
New Zealand (NZ), Nicaragua (NI), Niger (NE), Nigeria (NG), Niue (NU), Norfolk Island (NF), North Korea (KP), North Macedonia (MK), Northern Mariana Islands (MP), Norway (NO), Oman (OM), Pakistan (PK), Palau (PW)

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
