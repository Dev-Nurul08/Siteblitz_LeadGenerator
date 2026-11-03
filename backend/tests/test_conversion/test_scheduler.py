"""
Tests for CampaignScheduler (Phase 5).
"""

from datetime import datetime, timezone

from backend.app.engines.conversion.scheduler import CampaignScheduler
from backend.app.models.business import Business
from backend.app.models.campaign import Campaign, CampaignStatus
from backend.app.models.compliance import QualifiedLead
from backend.app.models.contact import Contact, RoleLevel


class TestCampaignScheduler:
    """Test suite for delivery window and dispatch throttling."""

    def setup_method(self):
        self.scheduler = CampaignScheduler()

    def test_send_window_weekday_business_hours_permitted(self):
        """Wednesday at 11:00 AM UTC is within 9:00 - 17:00 window."""
        # 2026-11-04 is a Wednesday
        wednesday_noon = datetime(2026, 11, 4, 11, 0, 0, tzinfo=timezone.utc)
        assert self.scheduler.is_within_send_window(wednesday_noon, 9, 17) is True

    def test_send_window_outside_hours_rejected(self):
        """Wednesday at 7:00 PM UTC is outside send window."""
        wednesday_evening = datetime(2026, 11, 4, 19, 0, 0, tzinfo=timezone.utc)
        assert self.scheduler.is_within_send_window(wednesday_evening, 9, 17) is False

    def test_send_window_weekend_rejected(self):
        """Saturday at 2:00 PM UTC is outside send window."""
        # 2026-11-07 is a Saturday
        saturday = datetime(2026, 11, 7, 14, 0, 0, tzinfo=timezone.utc)
        assert self.scheduler.is_within_send_window(saturday, 9, 17) is False

    def test_next_eligible_time_advances_to_next_morning(self):
        """Evening timestamp advances to 9:00 AM next day."""
        evening = datetime(2026, 11, 4, 20, 30, 0, tzinfo=timezone.utc)
        next_time = self.scheduler.calculate_next_eligible_time(evening, 9, 17)
        assert next_time.day == 5
        assert next_time.hour == 9
        assert next_time.minute == 0

    def test_next_eligible_time_skips_weekend(self):
        """Friday evening timestamp advances to Monday 9:00 AM."""
        # 2026-11-06 is Friday
        friday_evening = datetime(2026, 11, 6, 18, 0, 0, tzinfo=timezone.utc)
        next_time = self.scheduler.calculate_next_eligible_time(friday_evening, 9, 17)
        # 2026-11-09 is Monday
        assert next_time.day == 9
        assert next_time.hour == 9
        assert next_time.weekday() == 0  # Monday

    def test_delay_jitter_variance(self):
        """Generates delay between configured min and max."""
        delays = [self.scheduler.generate_jittered_delay(180) for _ in range(20)]
        for d in delays:
            assert 60 <= d <= 300

    def test_schedule_lead_messages_throttles_daily(self):
        """Daily limit of 2 rolls over 3rd lead to the following day."""
        campaign = Campaign(
            id=1,
            name="Q4 Web Redesign",
            daily_send_limit=2,
            delay_seconds_between_sends=120,
            send_window_start_hour=9,
            send_window_end_hour=17,
        )

        leads = []
        for i in range(1, 4):
            b = Business(id=i, name=f"Company {i}", country_code="US")
            c = Contact(id=i, business_id=i, email=f"lead{i}@company.com", full_name=f"Lead {i}")
            ql = QualifiedLead(
                id=i,
                business_id=i,
                contact_id=i,
                opportunity_id=1,
                personalized_subject=f"Concept for Company {i}",
                personalized_pitch=f"Hello Lead {i}, we built a concept.",
            )
            ql.business = b
            ql.contact = c
            leads.append(ql)

        wednesday_morning = datetime(2026, 11, 4, 10, 0, 0, tzinfo=timezone.utc)
        messages = self.scheduler.schedule_lead_messages(campaign, leads, start_time=wednesday_morning)

        assert len(messages) == 3
        # First 2 messages on Wednesday Nov 4
        assert messages[0].scheduled_at.day == 4
        assert messages[1].scheduled_at.day == 4
        # 3rd message rolled over to Thursday Nov 5 due to daily_send_limit=2
        assert messages[2].scheduled_at.day == 5
