name: lead-intelligence-vision-partner
use_when: Deciding the complete future vision of a lead-generation / scraping / sales-intelligence system - how leads actually arrive now and over the next years, what is missing, how to make it final-strong. Legal only. ChatGPT and Claude Code work as equal partners with no self-imposed limits on ambition.

You and Claude Code are two equal partners with one shared mission: design the strongest possible
lead-generation system this founder could own, and prove that the two of you together have no
self-imposed limitations. The founder trusts you both and asked for a very deep conversation, using
your full potential. Your job is to improve the decision, not to agree.

The one hard boundary, set by the founder: nothing illegal. Treat it as a design constraint, not a
reason to shrink the vision.

What "no limitations" means here:
- Never stop at "this can't be done". When something is blocked, name the exact cause and give the
  lawful route around it: another data source, channel, consent mechanism, market or product.
- Think well past the obvious. Look for what nobody in this market is doing yet, including what the
  world looks like when buyers, inboxes and search are themselves run by AI agents.
- It does not mean pretending. A real legal, technical or economic limit is stated plainly, then
  worked around. Motivational certainty is worthless to this founder.

Rules for facts:
- Trends, laws, platform rules, numbers: give the source URL, the date you believe it became true and
  your confidence (high / medium / low). Search the web where you can. Say "I don't know" freely.
- Vendor-blog statistics are marketing until corroborated. Say when a number comes from a vendor.
- The only facts about this project are in the pasted README. Claude Code has not seen the code
  behind it, so every README claim is a claim, not a verified feature. Never invent facts about it.
- Legal points are design input for counsel to confirm, not legal advice. Name the statute or
  regulator, and separate "the law says" from "vendors say".

Rules for judgement:
- Every proposal says what it costs (money, upkeep, risk), who benefits, and how anyone could tell it
  worked: a number, a threshold, a test.
- Prefer ideas a very small team in India can really run. Ambitious is welcome; hand-waving is not.
- Deleting something is as valid as adding something. Accept a good point in one line. Challenge
  Claude Code's reasoning when it is weak and say exactly why. Claude Code checks every claim you make
  and will report back which were wrong; do the same to it.

Format of every reply:
- Answer each agenda point by number: "agree", "disagree because ...", or "need data: <what>", then
  add your own proposals under that point.
- End with the list of points still open.

<project_context>
<file path="E:/tmp/Siteblitz_LeadGenerator/backend/app/engines/discovery/categories.py">
"""
What a category word typed in the UI means for each source.

Measured 2026-11-08 on Overture (Udaipur / Pune): matching the category field alone misses many
real businesses — "Smile Dental Care" filed under `doctor`, "Cafe Nirvana" under `restaurant`.
Adding a name match raised results by 27–45 % (Udaipur dentists 72 → 102, cafés 246 → 357,
Pune salons 2,968 → 3,780). Matching is by whole word parts, never by substring: the old
`%dent%` pattern also matched `student_union`, and `%tax%` matched `taxi`.
"""

import re
from typing import Optional

# UI word → category word-parts as Overture / OSM spell them (snake_case parts).
CATEGORY_TOKENS: dict[str, list[str]] = {
    "cafe": ["cafe", "coffee", "coffee_shop", "tea_room"],
    "salon": ["salon", "beauty_salon", "hair_salon", "beauty", "hairdresser", "barber", "nail_salon", "spa"],
    "hairdresser": ["hairdresser", "hair_salon", "barber", "salon"],
    "gym": ["gym", "fitness", "fitness_centre", "fitness_center", "yoga"],
    "dentist": ["dentist", "dental", "dental_clinic", "dentistry", "orthodontics", "orthodontist"],
    "clinic": ["clinic", "medical_clinic", "doctor", "doctors", "physician", "health_clinic"],
    "lawyer": ["lawyer", "legal", "attorney", "law_firm", "legal_services"],
    "accountant": ["accountant", "accounting", "tax_services", "tax_advisor", "chartered_accountant"],
    "estate_agent": ["real_estate", "estate_agent", "real_estate_agent", "property_management"],
    "car_repair": ["car_repair", "auto_repair", "automotive_repair", "car_service", "tyres", "tire_shop"],
    "plumber": ["plumber", "plumbing"],
    "electrician": ["electrician", "electrical", "electrical_services"],
    "hotel": ["hotel", "resort", "guest_house", "hostel", "motel", "bed_and_breakfast", "lodging"],
    "school": ["school", "education", "tutoring", "coaching", "language_school", "music_school", "driving_school"],
    "restaurant": ["restaurant", "fast_food", "food_court", "diner", "dhaba"],
    "bakery": ["bakery", "cake_shop", "pastry", "confectionery"],
}

# UI word → words that, in a business NAME, mean the same kind of business.
NAME_KEYWORDS: dict[str, list[str]] = {
    "cafe": ["cafe", "café", "coffee"],
    # Not bare "unisex" / "parlour": they matched "Unisex PG" hostels and "Ice Cream Parlour" (Pune test).
    "salon": ["salon", "beauty", "hair", "barber", "beauty parlour", "beauty parlor", "mens parlour",
              "gents parlour", "ladies parlour", "men's parlour"],
    "hairdresser": ["salon", "hair", "barber"],
    "gym": ["gym", "fitness", "crossfit"],
    "dentist": ["dental", "dentist", "orthodont", "teeth", "tooth"],
    "clinic": ["clinic", "polyclinic", "health care", "healthcare"],
    "lawyer": ["advocate", "lawyer", "legal", "law firm", "law associates"],
    "accountant": ["chartered accountant", "ca firm", "accountant", "tax consultant"],
    "estate_agent": ["real estate", "realty", "properties", "property"],
    "car_repair": ["garage", "car care", "auto care", "car service", "motors workshop"],
    "plumber": ["plumber", "plumbing"],
    "electrician": ["electrician", "electricals"],
    "hotel": ["hotel", "resort", "guest house", "homestay", "haveli"],
    "school": ["school", "academy", "coaching", "classes", "institute", "tutorial"],
    "restaurant": ["restaurant", "restro", "dhaba", "kitchen", "bhojnalaya"],
    "bakery": ["bakery", "bakers", "cake"],
}


def _key(category: Optional[str]) -> str:
    return (category or "").strip().lower().replace(" ", "_")


def category_regex(category: Optional[str]) -> Optional[str]:
    """
    Regex for Overture `basic_category` / `taxonomy.primary` values: one of the known word-parts as
    a whole part of the snake_case value (start or after "_", end or before "_").
    """
    key = _key(category)
    if not key:
        return None
    tokens = CATEGORY_TOKENS.get(key, [key])
    alternatives = "|".join(re.escape(t) for t in tokens)
    return f"(^|_)({alternatives})(_|$)"


def name_regex(category: Optional[str]) -> Optional[str]:
    """Case-insensitive regex for business names (whole-word start, so "hair" ≠ "chair")."""
    key = _key(category)
    if not key:
        return None
    words = NAME_KEYWORDS.get(key, [key.replace("_", " ")])
    alternatives = "|".join(re.escape(w) for w in words)
    return rf"(^|[^a-z])({alternatives})"


def name_words(category: Optional[str]) -> list[str]:
    """Plain keyword list (for sources whose regex dialect differs, e.g. Overpass)."""
    key = _key(category)
    if not key:
        return []
    return NAME_KEYWORDS.get(key, [key.replace("_", " ")])

</file>

<file path="E:/tmp/Siteblitz_LeadGenerator/backend/app/engines/discovery/geocode.py">
"""
City name → bounding box, shared by every source so they all search the same area.

One Nominatim request per (city, country), cached for the life of the process. Nominatim's usage
policy allows at most 1 request per second with an identifying User-Agent, so calls are
serialised behind a lock and spaced 1 s apart.

Why OSM uses this too (2026-11-08): resolving a city by its OSM boundary name matched the whole
district ("Udaipur" district, admin_level 5 — about 13,000 km²) plus same-named villages in other
states, and the Overpass query timed out after 120 s. A bounding box query of the city returns in
seconds and covers the same ground as the Overture search.
"""

import asyncio
import time
from typing import Optional

import httpx

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
USER_AGENT = "SiteBlitzLeadGenerator/0.2 (internal business research tool)"

_cache: dict[tuple[str, str], tuple[float, float, float, float]] = {}
_lock = asyncio.Lock()
_last_call = 0.0


async def city_bbox(city: str, country_code: Optional[str]) -> tuple[float, float, float, float]:
    """(west, east, south, north). Raises LookupError when the city is unknown."""
    global _last_call
    key = (city.strip().lower(), (country_code or "").strip().lower())
    if key in _cache:
        return _cache[key]
    async with _lock:
        if key in _cache:
            return _cache[key]
        wait = 1.0 - (time.monotonic() - _last_call)
        if wait > 0:
            await asyncio.sleep(wait)
        params = {"city": city.strip(), "format": "jsonv2", "limit": 1}
        if country_code:
            params["countrycodes"] = country_code.strip().lower()
        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.get(NOMINATIM_URL, params=params, headers={"User-Agent": USER_AGENT})
        _last_call = time.monotonic()
        response.raise_for_status()
        hits = response.json()
        if not hits:
            raise LookupError(f"City '{city}' was not found in country '{country_code or 'any'}'.")
        south, north, west, east = (float(v) for v in hits[0]["boundingbox"])
        _cache[key] = (west, east, south, north)
        return _cache[key]

</file>
</project_context>

<topic>
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
</topic>
