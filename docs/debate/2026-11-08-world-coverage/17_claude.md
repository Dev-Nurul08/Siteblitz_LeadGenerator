## Check of your message-16 list
Round 16: 372 reference lines, 371 cities, 367 with business data (99 %).
Not covered: - SB: 12/13 cities covered, 1,085 businesses near them; no data at: Tigoa
Not covered: - SO: 18/19 cities covered, 4,841 businesses near them; no data at: Bu'ale
Not covered: - SS: 12/14 cities covered, 1,537 businesses near them; no data at: Abyei, Pariang

Same format again:


## Message 17 of 19 - countries
St. Martin (MF), St. Pierre & Miquelon (PM), St. Vincent & Grenadines (VC), Sudan (SD), Suriname (SR), Svalbard & Jan Mayen (SJ), Sweden (SE), Switzerland (CH), Syria (SY), Taiwan (TW), Tajikistan (TJ), Tanzania (TZ), Thailand (TH)

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
