"""
Tests for MultiMailboxSender (Phase 5).
"""

from datetime import datetime, timezone

from backend.app.engines.conversion.sender import MultiMailboxSender, ProviderEvent
from backend.app.models.campaign import MessageStatus, OutreachMessage


class TestMultiMailboxSender:
    """Test suite for mailbox rotation and token resolution."""

    def setup_method(self):
        self.mailboxes = [
            "sender1@siteblitz.agency",
            "sender2@siteblitz.agency",
        ]
        self.sender = MultiMailboxSender(self.mailboxes)

    def test_round_robin_rotation(self):
        """Alternates across configured mailboxes."""
        m1 = self.sender.get_next_mailbox()
        m2 = self.sender.get_next_mailbox()
        m3 = self.sender.get_next_mailbox()

        assert m1 == "sender1@siteblitz.agency"
        assert m2 == "sender2@siteblitz.agency"
        assert m3 == "sender1@siteblitz.agency"

    def test_dynamic_token_resolution(self):
        """Resolves {{UNSUBSCRIBE_LINK}} and {{PHYSICAL_ADDRESS}} with concrete URLs and addresses."""
        raw_body = (
            "Hi John,\n\nWe would love to help.\n\n"
            "---\n{{PHYSICAL_ADDRESS}}\n"
            "Unsubscribe: {{UNSUBSCRIBE_LINK}}"
        )
        resolved = self.sender.resolve_message_tokens(
            body_text=raw_body,
            recipient_email="john@bakery.com",
            sender_mailbox="marcus@siteblitz.agency",
        )

        assert "100 Innovation Way" in resolved
        assert "http://localhost:8000/api/v1/qualification/unsubscribe?email=john%40bakery.com" in resolved
        assert "{{UNSUBSCRIBE_LINK}}" not in resolved
        assert "{{PHYSICAL_ADDRESS}}" not in resolved

    def _message(self) -> OutreachMessage:
        return OutreachMessage(
            id=1,
            campaign_id=1,
            lead_id=1,
            contact_id=1,
            business_id=1,
            sender_mailbox="unassigned",
            recipient_email="ceo@target.com",
            subject="Idea for website",
            body_text="Hi, check our preview: {{UNSUBSCRIBE_LINK}}",
            scheduled_at=datetime.now(timezone.utc),
            status=MessageStatus.QUEUED,
        )

    def test_dispatch_without_provider_event_never_marks_sent(self):
        """E1 (old phase 5): no sending provider exists, so a dispatch leaves the message QUEUED and untouched."""
        msg = self._message()
        report = self.sender.dispatch(msg, simulate=True)

        assert report.success is False
        assert "no sending provider" in report.error
        assert msg.status == MessageStatus.QUEUED
        assert msg.sent_at is None
        assert msg.sender_mailbox == "unassigned"
        assert "{{UNSUBSCRIBE_LINK}}" in msg.body_text

    def test_dispatch_with_rejected_or_incomplete_provider_event_never_marks_sent(self):
        now = datetime.now(timezone.utc)
        for event in (ProviderEvent("smtp", "abc", accepted=False, at=now),
                      ProviderEvent("smtp", "", accepted=True, at=now)):
            msg = self._message()
            assert self.sender.dispatch(msg, provider_event=event).success is False
            assert msg.status == MessageStatus.QUEUED

    def test_dispatch_with_accepted_provider_event_marks_sent(self):
        """Only a provider that accepted the message (with its own message id) makes it SENT."""
        msg = self._message()
        accepted_at = datetime(2026, 11, 12, 4, 30, tzinfo=timezone.utc)
        report = self.sender.dispatch(msg, provider_event=ProviderEvent("smtp", "<id-1@mx>", True, accepted_at))

        assert report.success is True
        assert msg.status == MessageStatus.SENT
        assert msg.sent_at == accepted_at
        assert msg.sender_mailbox in self.mailboxes
        assert "unsubscribe?email=ceo%40target.com" in msg.body_text
