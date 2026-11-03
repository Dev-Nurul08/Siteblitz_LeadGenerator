"""
Campaign Scheduler Engine (Phase 5).

Manages deliverability-safe outreach dispatch windows, randomized jitter delays,
and daily send quotas to prevent mailbox burnout and spam heuristics.
"""

from dataclasses import dataclass
from datetime import datetime, time, timedelta, timezone
import random
from typing import List, Optional

from backend.app.models.campaign import Campaign, OutreachMessage
from backend.app.models.compliance import QualifiedLead


@dataclass
class ScheduleDecision:
    """Evaluation whether a message can be dispatched at this instant."""

    can_send: bool
    reason: str
    next_eligible_time: Optional[datetime] = None


class CampaignScheduler:
    """
    Enforces business-hour delivery windows, weekday filters, and organic delay jitter.
    """

    def __init__(
        self,
        default_start_hour: int = 9,
        default_end_hour: int = 17,
        min_delay_seconds: int = 60,
        max_delay_seconds: int = 300,
    ):
        self.default_start_hour = default_start_hour
        self.default_end_hour = default_end_hour
        self.min_delay_seconds = min_delay_seconds
        self.max_delay_seconds = max_delay_seconds

    def is_within_send_window(
        self,
        check_time: Optional[datetime] = None,
        start_hour: int = 9,
        end_hour: int = 17,
        allowed_weekdays: Optional[List[int]] = None,
    ) -> bool:
        """
        Check if datetime is within business hours (default Mon-Fri 9:00 - 17:00).
        allowed_weekdays: 0=Monday, 6=Sunday. Default [0, 1, 2, 3, 4] (Mon-Fri).
        """
        dt = check_time or datetime.now(timezone.utc)
        allowed = allowed_weekdays if allowed_weekdays is not None else [0, 1, 2, 3, 4]

        # Check weekday
        if dt.weekday() not in allowed:
            return False

        # Check hour
        if not (start_hour <= dt.hour < end_hour):
            return False

        return True

    def calculate_next_eligible_time(
        self,
        from_time: Optional[datetime] = None,
        start_hour: int = 9,
        end_hour: int = 17,
        allowed_weekdays: Optional[List[int]] = None,
    ) -> datetime:
        """
        Calculate the next valid business-hour timestamp.
        """
        dt = from_time or datetime.now(timezone.utc)
        allowed = allowed_weekdays if allowed_weekdays is not None else [0, 1, 2, 3, 4]

        candidate = dt

        # If too late today or outside allowed hours, advance
        if candidate.hour >= end_hour or candidate.weekday() not in allowed:
            candidate = candidate + timedelta(days=1)
            candidate = candidate.replace(hour=start_hour, minute=0, second=0, microsecond=0)
        elif candidate.hour < start_hour:
            candidate = candidate.replace(hour=start_hour, minute=0, second=0, microsecond=0)

        # Advance until we land on an allowed weekday
        while candidate.weekday() not in allowed:
            candidate = candidate + timedelta(days=1)
            candidate = candidate.replace(hour=start_hour, minute=0, second=0, microsecond=0)

        return candidate

    def generate_jittered_delay(self, base_delay_seconds: int = 180) -> int:
        """
        Calculate randomized delay variance (+/- 40%) to ensure humanized dispatch patterns.
        """
        variance = int(base_delay_seconds * 0.40)
        jitter = random.randint(-variance, variance)
        delay = max(self.min_delay_seconds, min(self.max_delay_seconds, base_delay_seconds + jitter))
        return delay

    def schedule_lead_messages(
        self,
        campaign: Campaign,
        leads: List[QualifiedLead],
        start_time: Optional[datetime] = None,
    ) -> List[OutreachMessage]:
        """
        Transform qualified leads into scheduled OutreachMessages adhering to throttle limits.
        """
        messages = []
        current_time = start_time or datetime.now(timezone.utc)
        start_hour = campaign.send_window_start_hour or self.default_start_hour
        end_hour = campaign.send_window_end_hour or self.default_end_hour
        base_delay = campaign.delay_seconds_between_sends or 180

        # Ensure start time is in valid window
        if not self.is_within_send_window(current_time, start_hour, end_hour):
            current_time = self.calculate_next_eligible_time(current_time, start_hour, end_hour)

        sent_today = 0
        current_date = current_time.date()

        for lead in leads:
            if not lead.contact or not lead.personalized_pitch:
                continue

            # If daily limit reached, roll over to the next day's send window
            if sent_today >= campaign.daily_send_limit:
                current_time = self.calculate_next_eligible_time(
                    current_time + timedelta(days=1), start_hour, end_hour
                )
                current_date = current_time.date()
                sent_today = 0

            # Add jittered delay
            delay = self.generate_jittered_delay(base_delay)
            current_time = current_time + timedelta(seconds=delay)

            # If current_time crossed outside send window, roll over
            if not self.is_within_send_window(current_time, start_hour, end_hour):
                current_time = self.calculate_next_eligible_time(current_time, start_hour, end_hour)
                if current_time.date() != current_date:
                    current_date = current_time.date()
                    sent_today = 0

            msg = OutreachMessage(
                campaign_id=campaign.id,
                lead_id=lead.id,
                contact_id=lead.contact_id,
                business_id=lead.business_id,
                sender_mailbox="outreach@siteblitz.agency",  # Assigned dynamically by MultiMailboxSender
                recipient_email=lead.contact.email,
                subject=lead.personalized_subject or f"Digital opportunity for {lead.business.name}",
                body_text=lead.personalized_pitch,
                scheduled_at=current_time,
            )
            messages.append(msg)
            sent_today += 1

        return messages
