# World coverage - every country, every state, its main cities

Context: SiteBlitz finds small businesses (to sell websites to those without one). Its data source is
Overture Maps Places (open data, about 60-90 million places). We are extracting every place of every country
into files organised country -> state -> city. To check that no state or major city is missing, we need, for
every country in the world (A-Z, ISO 3166-1, 249 entries incl. territories), a reference list of its states
and main cities. We go alphabetically, about 13 countries per message, 19 messages in total.

## Check of the lists so far (businesses within 10 km or with that city name)
Round 1: 263 reference lines, 260 cities, 259 with business data (100 %).
Round 2: 251 reference lines, 251 cities, 250 with business data (100 %).
Round 3: 192 reference lines, 190 cities, 190 with business data (100 %).
Round 4: 221 reference lines, 221 cities, 221 with business data (100 %).
Round 5: 223 reference lines, 223 cities, 219 with business data (98 %).
Round 6: 238 reference lines, 238 cities, 235 with business data (99 %).
Round 7: 160 reference lines, 159 cities, 159 with business data (100 %).
Round 8: 230 reference lines, 229 cities, 229 with business data (100 %).
Round 9: 349 reference lines, 349 cities, 349 with business data (100 %).
Round 10: 238 reference lines, 238 cities, 234 with business data (98 %).

Same format again:


## Message 11 of 19 - countries
Madagascar (MG), Malawi (MW), Malaysia (MY), Maldives (MV), Mali (ML), Malta (MT), Marshall Islands (MH), Martinique (MQ), Mauritania (MR), Mauritius (MU), Mayotte (YT), Mexico (MX), Micronesia (FM)

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
