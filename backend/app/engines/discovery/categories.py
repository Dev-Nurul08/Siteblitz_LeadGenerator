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
