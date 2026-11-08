"""Tests for the city geocoder (no network: the Nominatim request is stubbed)."""

import pytest

from backend.app.engines.discovery import geocode


def _hit(addresstype, bbox, lat=0.0, lon=0.0, name="x"):
    # Nominatim boundingbox order: south, north, west, east (strings)
    return {"addresstype": addresstype, "boundingbox": [str(v) for v in bbox],
            "lat": str(lat), "lon": str(lon), "display_name": name}


@pytest.fixture
def nominatim(monkeypatch):
    """Replace the HTTP call; `answers` maps 'with state' / 'no state' to the hits returned."""
    calls = []
    answers = {}

    async def fake_search(params):
        calls.append(dict(params))
        return answers["with state" if "state" in params else "no state"]

    monkeypatch.setattr(geocode, "_search", fake_search)
    monkeypatch.setattr(geocode, "_cache", {})
    monkeypatch.setattr(geocode, "_resolved", {})
    return calls, answers


@pytest.mark.asyncio
async def test_state_matching_only_a_landmark_retries_without_state(nominatim):
    calls, answers = nominatim
    answers["with state"] = [_hit("commercial", [39.906, 39.922, 116.351, 116.362], name="北京金融街")]
    answers["no state"] = [_hit("city", [39.17, 41.06, 115.42, 117.74], lat=39.906, lon=116.391, name="北京市")]
    west, east, south, north = await geocode.city_bbox("Beijing", "CN", "Beijing")
    assert len(calls) == 2 and "state" not in calls[1]
    assert geocode.resolved_place("Beijing", "CN", "Beijing")["name"] == "北京市"
    # 2.3° × 1.9° municipality trimmed to the 1.5° square around the city's point; the south edge
    # of that square (39.156) lies outside the boundary, so the boundary's own edge (39.17) is kept
    assert east - west == pytest.approx(1.5)
    assert west == pytest.approx(116.391 - 0.75) and north == pytest.approx(39.906 + 0.75)
    assert south == pytest.approx(39.17)
    assert geocode.resolved_place("Beijing", "CN", "Beijing")["trimmed_from_km"] == [258, 210]


@pytest.mark.asyncio
async def test_trim_stays_inside_the_city_boundary(nominatim):
    _, answers = nominatim
    # Shenzhen: 1.7° wide, 1.2° high, point near the west edge
    answers["no state"] = [_hit("city", [21.821, 23.017, 113.681, 115.389], lat=22.545, lon=114.055)]
    west, east, south, north = await geocode.city_bbox("Shenzhen", "CN")
    assert west == pytest.approx(113.681) and east == pytest.approx(114.805)
    assert south == pytest.approx(21.821) and north == pytest.approx(23.017)


@pytest.mark.asyncio
async def test_a_state_hit_is_never_trimmed(nominatim):
    _, answers = nominatim
    answers["no state"] = [_hit("state", [23.0, 30.2, 69.5, 78.3], lat=26.8, lon=73.8)]
    west, east, south, north = await geocode.city_bbox("Rajasthan", "IN")
    # left as is, so the sources still reject it as "a district or state"
    assert east - west > geocode.MAX_BBOX_DEGREES
    assert "trimmed_from_km" not in geocode.resolved_place("Rajasthan", "IN")


@pytest.mark.asyncio
async def test_settlement_preferred_over_an_earlier_landmark(nominatim):
    calls, answers = nominatim
    answers["no state"] = [_hit("commercial", [1, 1.01, 1, 1.01]),
                           _hit("city", [24.5, 24.7, 73.6, 73.8], lat=24.58, lon=73.71, name="Udaipur")]
    await geocode.city_bbox("Udaipur", "IN")
    assert len(calls) == 1
    assert geocode.resolved_place("Udaipur", "IN")["name"] == "Udaipur"


@pytest.mark.asyncio
async def test_unknown_city_raises_lookup_error(nominatim):
    _, answers = nominatim
    answers["no state"] = []
    with pytest.raises(LookupError):
        await geocode.city_bbox("Nowhereville", "IN")


@pytest.mark.asyncio
async def test_other_cities_of_the_state_are_not_used(nominatim):
    # "Tokyo" + state "Tokyo": Nominatim returned Hachioji, Chofu ... (cities inside Tokyo prefecture);
    # without the state only the prefecture matched. Result: the prefecture, untrimmed (sources reject it).
    calls, answers = nominatim
    answers["with state"] = [_hit("city", [35.6, 35.72, 139.16, 139.43], lat=35.67, lon=139.32, name="八王子市, 東京都, 日本")
                             | {"namedetails": {"name": "八王子市", "name:en": "Hachioji"}}]
    answers["no state"] = [_hit("province", [20.21, 35.9, 135.85, 154.21], lat=35.68, lon=139.76, name="東京都, 日本")
                           | {"namedetails": {"name": "東京都", "name:en": "Tokyo"}}]
    west, east, south, north = await geocode.city_bbox("Tokyo", "JP", "Tokyo")
    assert len(calls) == 2
    assert geocode.resolved_place("Tokyo", "JP", "Tokyo")["name"] == "東京都, 日本"
    assert east - west > geocode.MAX_BBOX_DEGREES


@pytest.mark.asyncio
async def test_name_found_in_any_language_or_old_name(nominatim):
    calls, answers = nominatim
    answers["with state"] = [
        _hit("city", [1, 1.1, 1, 1.1], name="Other") | {"namedetails": {"name": "Other"}},
        _hit("city", [24.5, 24.7, 73.6, 73.8], name="Thành phố Hồ Chí Minh")
        | {"namedetails": {"name": "Thành phố Hồ Chí Minh", "name:en": "Ho Chi Minh City", "old_name": "Sài Gòn;Saigon"}},
    ]
    await geocode.city_bbox("saigon", "VN", "x")
    assert len(calls) == 1
    assert geocode.resolved_place("saigon", "VN", "x")["name"] == "Thành phố Hồ Chí Minh"


@pytest.mark.asyncio
async def test_state_cities_without_the_name_and_nothing_without_state_is_not_found(nominatim):
    _, answers = nominatim
    answers["with state"] = [_hit("city", [1, 1.1, 1, 1.1], name="Some Other Town")]
    answers["no state"] = []
    with pytest.raises(LookupError):
        await geocode.city_bbox("Typo-ville", "IN", "Maharashtra")
