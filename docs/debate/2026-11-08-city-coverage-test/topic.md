# Topic — Test the SiteBlitz lead generator on as many cities as possible (10 rounds)

## The founder's words (translated from Hinglish)
"Get multiple cities from ChatGPT — as many Indian cities as possible, Bangladesh, Afghanistan, and in total
about the top 50 countries' cities — and test them. Take all the cities from ChatGPT round by round; at least
10 rounds."

## What Claude Code is testing (facts, verified in the repo)
The tool searches one city for one kind of business through "All sources": Overture Maps Places (Meta,
Microsoft, Foursquare … open data read by city bounding box) + OpenStreetMap (Overpass, same bounding box),
merged and de-duplicated. The city name is turned into a bounding box with ONE Nominatim lookup
(`city=<name>&countrycodes=<cc>`, first hit). A box larger than 1.5° × 1.5° is rejected as "a district or
state" (to avoid huge downloads). Category for this test: **dentist** (matched on category fields AND on
business names in English), max 300 results per city. For every city we record: status, found, new,
duplicates, available (all matches in the area), errors, seconds, and the share of businesses with phone /
email / website / social link / social link but no website.

## How the 10 rounds work
- Each round you give me the next batch as ONE JSON code block, exactly:
  `{"batch": <n>, "cities": [{"city": "Pune", "country_code": "IN", "admin": "Maharashtra"}, ...]}`
  City names in English as OpenStreetMap / Nominatim spell them (e.g. "Bengaluru", "Kolkata", "Dhaka",
  "Herat", "Mazar-i-Sharif"). No duplicates of earlier batches. If unsure of a spelling, say so outside the JSON.
- From round 2 on, I paste the measured results of the previous batch; answer the agenda points about them.
- Plan: R1 India top 50 by population + Bangladesh 25 + Afghanistan 20 · R2 India next 50 · R3–R7 the top 50
  countries by population (excluding India, Bangladesh, Afghanistan), 10 countries per round, their 3 largest
  cities each · R8 alternate spellings for failed cities + India next 50 · R9 coverage patterns and lawful
  data-source suggestions per country · R10 final review.

## Round 1 request
Batch 1: India's 50 largest cities by population (city proper), then Bangladesh's 25 largest, then
Afghanistan's 20 largest — 95 cities, one JSON block.

Answer each agenda point by number: agree / disagree because ... / need data: ... . End with the list of
points still open.
