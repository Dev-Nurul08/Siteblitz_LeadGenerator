# World coverage - every country, every state, its main cities

Context: SiteBlitz finds small businesses (to sell websites to those without one). Its data source is
Overture Maps Places (open data, about 60-90 million places). We are extracting every place of every country
into files organised country -> state -> city. To check that no state or major city is missing, we need, for
every country in the world (A-Z, ISO 3166-1, 249 entries incl. territories), a reference list of its states
and main cities. We go alphabetically, about 13 countries per message, 19 messages in total.

## Message 1 of 19 - countries
Afghanistan (AF), Åland Islands (AX), Albania (AL), Algeria (DZ), American Samoa (AS), Andorra (AD), Angola (AO), Anguilla (AI), Antarctica (AQ), Antigua & Barbuda (AG), Argentina (AR), Armenia (AM), Aruba (AW)

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
