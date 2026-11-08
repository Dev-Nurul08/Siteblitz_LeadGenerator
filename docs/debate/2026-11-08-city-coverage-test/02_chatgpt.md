SiteBlitz — Round 2 of 10
1. Verdicts on Round 1
Point	Decision	Response
1. City selection	Agree	Keep 2011 city-proper rankings as the India baseline.
2. Geocoding	Agree	Passing admin as state and recording the resolved location are good changes. Nominatim officially supports structured city and state parameters.  Nominatim Manual
3. Result cap	Agree	found versus available addresses the cap concern. No additional change needed for this test.
4. Category precision	Agree	Keep the 120-record precision audit separate. Do not delay city-coverage testing.
5. Cross-city duplicates	Partially disagree	They cannot occur within a single-city search as cross-city duplicates. However, overlapping city boxes can return the same business in different searches. Only relevant if results are aggregated into a shared database.
6. Ten rounds	Agree	Keep R9 and R10 as fresh validation rounds plus analysis.

2. Batch 2 — India, next 50 cities
50 cities • India only • No Batch 1 repeats
I cross-checked the 2011 city-proper list. One ranking-source error matters: some online lists accidentally exchange Bareilly and Tiruppur's populations and Noida and Greater Noida's populations. Census-based figures place Bareilly above Tiruppur, and Noida, rather than Greater Noida, within this population range. 

Google Groups+2

The JSON below uses the corrected ordering, with modern English place names where practical. These names have not yet been confirmed through live Nominatim queries.

{"batch":2,"cities":[
{"city":"Tiruchirappalli","country_code":"IN","admin":"Tamil Nadu"},
{"city":"Bareilly","country_code":"IN","admin":"Uttar Pradesh"},
{"city":"Moradabad","country_code":"IN","admin":"Uttar Pradesh"},
{"city":"Mysuru","country_code":"IN","admin":"Karnataka"},
{"city":"Tiruppur","country_code":"IN","admin":"Tamil Nadu"},
{"city":"Gurugram","country_code":"IN","admin":"Haryana"},
{"city":"Aligarh","country_code":"IN","admin":"Uttar Pradesh"},
{"city":"Jalandhar","country_code":"IN","admin":"Punjab"},
{"city":"Bhubaneswar","country_code":"IN","admin":"Odisha"},
{"city":"Salem","country_code":"IN","admin":"Tamil Nadu"},
{"city":"Mira-Bhayandar","country_code":"IN","admin":"Maharashtra"},
{"city":"Warangal","country_code":"IN","admin":"Telangana"},
{"city":"Thiruvananthapuram","country_code":"IN","admin":"Kerala"},
{"city":"Guntur","country_code":"IN","admin":"Andhra Pradesh"},
{"city":"Bhiwandi","country_code":"IN","admin":"Maharashtra"},
{"city":"Saharanpur","country_code":"IN","admin":"Uttar Pradesh"},
{"city":"Gorakhpur","country_code":"IN","admin":"Uttar Pradesh"},
{"city":"Bikaner","country_code":"IN","admin":"Rajasthan"},
{"city":"Amravati","country_code":"IN","admin":"Maharashtra"},
{"city":"Noida","country_code":"IN","admin":"Uttar Pradesh"},
{"city":"Jamshedpur","country_code":"IN","admin":"Jharkhand"},
{"city":"Bhilai","country_code":"IN","admin":"Chhattisgarh"},
{"city":"Cuttack","country_code":"IN","admin":"Odisha"},
{"city":"Firozabad","country_code":"IN","admin":"Uttar Pradesh"},
{"city":"Kochi","country_code":"IN","admin":"Kerala"},
{"city":"Nellore","country_code":"IN","admin":"Andhra Pradesh"},
{"city":"Bhavnagar","country_code":"IN","admin":"Gujarat"},
{"city":"Dehradun","country_code":"IN","admin":"Uttarakhand"},
{"city":"Durgapur","country_code":"IN","admin":"West Bengal"},
{"city":"Asansol","country_code":"IN","admin":"West Bengal"},
{"city":"Nanded","country_code":"IN","admin":"Maharashtra"},
{"city":"Kolhapur","country_code":"IN","admin":"Maharashtra"},
{"city":"Ajmer","country_code":"IN","admin":"Rajasthan"},
{"city":"Kalaburagi","country_code":"IN","admin":"Karnataka"},
{"city":"Jamnagar","country_code":"IN","admin":"Gujarat"},
{"city":"Ujjain","country_code":"IN","admin":"Madhya Pradesh"},
{"city":"Loni","country_code":"IN","admin":"Uttar Pradesh"},
{"city":"Siliguri","country_code":"IN","admin":"West Bengal"},
{"city":"Jhansi","country_code":"IN","admin":"Uttar Pradesh"},
{"city":"Ulhasnagar","country_code":"IN","admin":"Maharashtra"},
{"city":"Jammu","country_code":"IN","admin":"Jammu and Kashmir"},
{"city":"Sangli-Miraj-Kupwad","country_code":"IN","admin":"Maharashtra"},
{"city":"Mangaluru","country_code":"IN","admin":"Karnataka"},
{"city":"Erode","country_code":"IN","admin":"Tamil Nadu"},
{"city":"Belagavi","country_code":"IN","admin":"Karnataka"},
{"city":"Ambattur","country_code":"IN","admin":"Tamil Nadu"},
{"city":"Tirunelveli","country_code":"IN","admin":"Tamil Nadu"},
{"city":"Malegaon","country_code":"IN","admin":"Maharashtra"},
{"city":"Gaya","country_code":"IN","admin":"Bihar"},
{"city":"Jalgaon","country_code":"IN","admin":"Maharashtra"}
]}



3. Batch 1 — uncertain names and alternate spellings
These are fallback candidates, not confirmed Nominatim failures. Try them only when the original query fails or resolves incorrectly.
Batch 1 name	Alternate to try
Chhatrapati Sambhaji Nagar	Aurangabad; Chhatrapati Sambhajinagar
Hubballi-Dharwad	Hubli-Dharwad
Kalyan-Dombivli	Kalyan-Dombivali
Pimpri-Chinchwad	Pimpri Chinchwad
Vasai-Virar	Vasai Virar City
Chattogram	Chittagong
Cumilla	Comilla
Bogura	Bogra
Barishal	Barisal
Jashore	Jessore
Sreepur	Sripur (Gazipur District)
Kaliakair	Kaliakoir
Chapai Nawabganj	Chapainawabganj; Nawabganj
Tarabo	Tarabo Pourashava (Narayanganj District)
Mazar-i-Sharif	Mazar-e Sharif
Pul-i-Alam	Pul-e Alam
Mihtarlam	Mehtar Lam
Sheberghan	Shiberghan; Shibirghan
Sar-e-Pol	Sar-e Pul
Aybak	Aibak

The alternative place names are supported by naming and geographic references, including OpenStreetMap-derived place records and government sources. Actual API matching remains untested here. 

OpenAlfa+4

Additional Batch 2 watch item: Sangli-Miraj-Kupwad describes a combined municipal area. If Nominatim returns only Sangli or Miraj, do not treat that smaller bounding box as full coverage of the combined city.
4. Points still open
1. Batch 1 results: Await measurements for all 95 cities, including resolved place names, geographic mismatches, source counts, errors, and contact completeness.
2. Production geocoding: Founder decision on a self-hosted or licensed provider; no need to block the current test.
3. Category precision: Separate 120-record audit remains open.
4. Cross-city duplication: Only needs testing if discovered businesses from multiple cities enter a shared dataset.
5. Geocoding aliases: Confirm fallback spellings using actual failed or incorrectly resolved Batch 1 queries.
6. Batch 2 results: Measure the 50 additional cities and carry unresolved geographic errors into Round 8.
7. Round 3: Review Batch 1's measured results and prepare the first international country batch.
Round 2 deliverable: 50 additional Indian cities supplied. Total city inputs across Rounds 1 and 2: 145, with no repeated city entries.
