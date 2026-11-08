"""
Tests for Lead-Radar Section 2: Six Separate Facts per Business.
"""

import pytest
from backend.app.engines.lead_radar.types import (
    Authority,
    Availability,
    CustomerTaskCovered,
    OwnedPresence,
    SixFacts,
    TaskQuality,
    BuyingStatus,
)


def test_six_facts_defaults_and_serialization():
    facts = SixFacts()
    assert facts.owned_presence == OwnedPresence.UNRESOLVED
    assert facts.availability == Availability.UNKNOWN
    assert facts.customer_task_covered == CustomerTaskCovered.UNKNOWN
    assert facts.task_quality == TaskQuality.NOT_TESTED
    assert facts.buying_status == BuyingStatus.UNKNOWN
    assert facts.authority == Authority.UNRESOLVED
    assert not facts.identity_verified
    assert not facts.currently_active
    assert not facts.absence_search_done
    assert not facts.repeated_failure

    d = facts.to_dict()
    assert d["owned_presence"] == "UNRESOLVED"
    assert d["availability"] == "UNKNOWN"
    assert d["identity_verified"] is False


def test_six_facts_custom_values():
    facts = SixFacts(
        owned_presence=OwnedPresence.OWN_DOMAIN,
        availability=Availability.WORKING,
        customer_task_covered=CustomerTaskCovered.BOOKING,
        task_quality=TaskQuality.WORKS,
        buying_status=BuyingStatus.EXPLICITLY_SEEKING,
        authority=Authority.LOCAL_OWNER,
        identity_verified=True,
        currently_active=True,
        absence_search_done=True,
        repeated_failure=False,
    )
    assert facts.owned_presence == OwnedPresence.OWN_DOMAIN
    assert facts.authority == Authority.LOCAL_OWNER
    assert facts.identity_verified is True
    assert facts.currently_active is True

