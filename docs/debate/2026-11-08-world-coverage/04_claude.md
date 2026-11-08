## Message 4 of 19 - countries
Canada (CA), Cape Verde (CV), Caribbean Netherlands (BQ), Cayman Islands (KY), Central African Republic (CF), Chad (TD), Chile (CL), China (CN), Christmas Island (CX), Cocos (Keeling) Islands (CC), Colombia (CO), Comoros (KM), Congo - Brazzaville (CG)

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
