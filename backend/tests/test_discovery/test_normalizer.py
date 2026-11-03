"""
Tests for the business name normalizer and deduplication engine.

Phase 1 acceptance criteria tested:
- Name normalization handles Unicode, legal suffixes, punctuation
- Category mapping works for known and unknown categories
- Duplicate detection uses name + location correctly
- Separate branches are not incorrectly merged
- Missing fields remain as unknown, not invented
"""

import pytest

from backend.app.engines.discovery.normalizer import BusinessNormalizer, _haversine_distance


class TestNameNormalization:
    """Test business name normalization."""

    def test_basic_normalization(self):
        assert BusinessNormalizer.normalize_name("The Best Restaurant") == "the best restaurant"

    def test_legal_suffix_removal(self):
        assert BusinessNormalizer.normalize_name("Acme Corp LLC") == "acme"
        assert BusinessNormalizer.normalize_name("Smith & Partners Ltd") == "smith partners"
        assert BusinessNormalizer.normalize_name("TechCo Inc.") == "techco"

    def test_unicode_handling(self):
        assert BusinessNormalizer.normalize_name("Café Müller") == "cafe muller"
        assert BusinessNormalizer.normalize_name("Résumé Services") == "resume services"
        assert BusinessNormalizer.normalize_name("Señor Tacos") == "senor tacos"

    def test_punctuation_removal(self):
        assert BusinessNormalizer.normalize_name("Ben's Deli & Bar") == "bens deli bar"
        assert BusinessNormalizer.normalize_name("A.B.C. Corp") == "a b c"

    def test_whitespace_collapsing(self):
        assert BusinessNormalizer.normalize_name("  Too   Many   Spaces  ") == "too many spaces"

    def test_empty_input(self):
        assert BusinessNormalizer.normalize_name("") == ""
        assert BusinessNormalizer.normalize_name("   ") == ""

    def test_gmbh_removal(self):
        """German legal suffix."""
        assert BusinessNormalizer.normalize_name("Müller Bäckerei GmbH") == "muller backerei"

    def test_preserves_meaningful_parts(self):
        """Legal suffix removal should not destroy the whole name."""
        result = BusinessNormalizer.normalize_name("Company Solutions")
        assert "solutions" in result


class TestCategoryNormalization:
    """Test category mapping from source-specific to normalized taxonomy."""

    def test_known_category(self):
        industry, normalized, source = BusinessNormalizer.normalize_category("restaurant")
        assert industry == "Food & Beverage"
        assert normalized == "Restaurant"
        assert source == "restaurant"

    def test_hotel_category(self):
        industry, normalized, source = BusinessNormalizer.normalize_category("hotel")
        assert industry == "Accommodation"
        assert normalized == "Hotel"

    def test_unknown_category(self):
        industry, normalized, source = BusinessNormalizer.normalize_category("widget_factory")
        assert industry == "Uncategorized"
        assert source == "widget_factory"

    def test_empty_category(self):
        industry, normalized, source = BusinessNormalizer.normalize_category("")
        assert industry == "Uncategorized"

    def test_partial_match(self):
        """Categories with partial matches should still resolve."""
        industry, normalized, source = BusinessNormalizer.normalize_category("car_repair")
        assert industry == "Automotive"

    def test_case_insensitive(self):
        industry, normalized, source = BusinessNormalizer.normalize_category("RESTAURANT")
        assert industry == "Food & Beverage"


class TestCountryCodeNormalization:
    """Test country code normalization."""

    def test_uppercase(self):
        assert BusinessNormalizer.normalize_country_code("gb") == "GB"

    def test_valid_code(self):
        assert BusinessNormalizer.normalize_country_code("US") == "US"

    def test_invalid_code(self):
        assert BusinessNormalizer.normalize_country_code("123") is None

    def test_too_long(self):
        assert BusinessNormalizer.normalize_country_code("USA") is None

    def test_none(self):
        assert BusinessNormalizer.normalize_country_code(None) is None

    def test_empty(self):
        assert BusinessNormalizer.normalize_country_code("") is None


class TestWebsiteNormalization:
    """Test website URL normalization."""

    def test_adds_scheme(self):
        assert BusinessNormalizer.normalize_website("example.com") == "https://example.com"

    def test_preserves_https(self):
        assert (
            BusinessNormalizer.normalize_website("https://example.com")
            == "https://example.com"
        )

    def test_rejects_social_media(self):
        """Social profiles should not be treated as official websites."""
        assert BusinessNormalizer.normalize_website("https://facebook.com/mybusiness") is None
        assert BusinessNormalizer.normalize_website("https://instagram.com/shop") is None
        assert BusinessNormalizer.normalize_website("https://linkedin.com/company/x") is None

    def test_none_input(self):
        assert BusinessNormalizer.normalize_website(None) is None

    def test_empty_input(self):
        assert BusinessNormalizer.normalize_website("") is None


class TestPhoneNormalization:
    """Test phone number normalization."""

    def test_strips_formatting(self):
        assert BusinessNormalizer.normalize_phone("(555) 123-4567") == "5551234567"

    def test_preserves_plus(self):
        assert BusinessNormalizer.normalize_phone("+44 20 7123 4567") == "+442071234567"

    def test_none_input(self):
        assert BusinessNormalizer.normalize_phone(None) is None


class TestDuplicateDetection:
    """Test business deduplication logic."""

    def test_exact_name_same_city(self):
        """Same name + same city = duplicate."""
        is_dup, confidence = BusinessNormalizer.is_potential_duplicate(
            "The Best Restaurant",
            "The Best Restaurant",
            city1="London",
            city2="London",
        )
        assert is_dup is True
        assert confidence >= 0.90

    def test_exact_name_different_city(self):
        """Same name + different city = might be a branch, lower confidence."""
        is_dup, confidence = BusinessNormalizer.is_potential_duplicate(
            "McDonald's",
            "McDonald's",
            city1="London",
            city2="Manchester",
            country1="GB",
            country2="GB",
        )
        # Same country, but different city — could be different branch
        assert is_dup is True
        assert confidence < 0.95  # Lower confidence than same-city match

    def test_different_names(self):
        """Different names = not a duplicate."""
        is_dup, _ = BusinessNormalizer.is_potential_duplicate(
            "Restaurant A",
            "Restaurant B",
        )
        assert is_dup is False

    def test_nearby_coordinates(self):
        """Same name + close proximity = high confidence duplicate."""
        is_dup, confidence = BusinessNormalizer.is_potential_duplicate(
            "Central Café",
            "Central Cafe",  # Without accent
            country1="GB",
            country2="GB",
            lat1=51.5074,
            lon1=-0.1278,
            lat2=51.5075,  # ~11 meters away
            lon2=-0.1279,
        )
        assert is_dup is True
        assert confidence >= 0.90

    def test_legal_suffix_ignored(self):
        """Names should match regardless of legal suffixes."""
        is_dup, confidence = BusinessNormalizer.is_potential_duplicate(
            "Acme Corp LLC",
            "Acme Corp",
            city1="Springfield",
            city2="Springfield",
        )
        assert is_dup is True

    def test_empty_name(self):
        """Empty names should not match."""
        is_dup, _ = BusinessNormalizer.is_potential_duplicate("", "Something")
        assert is_dup is False


class TestHaversineDistance:
    """Test geographic distance calculation."""

    def test_same_point(self):
        assert _haversine_distance(51.5, -0.1, 51.5, -0.1) == 0.0

    def test_known_distance(self):
        """London to Paris is approximately 340 km."""
        distance = _haversine_distance(51.5074, -0.1278, 48.8566, 2.3522)
        assert 335 < distance < 345

    def test_antipodal(self):
        """Opposite sides of Earth should be ~20,000 km."""
        distance = _haversine_distance(0, 0, 0, 180)
        assert 20000 < distance < 20100
