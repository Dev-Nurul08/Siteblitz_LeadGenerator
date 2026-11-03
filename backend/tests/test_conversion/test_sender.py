"""
Tests for MultiMailboxSender (Phase 5).
"""

from datetime import datetime, timezone

from backend.app.engines.conversion.sender import MultiMailboxSender
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

    def test_dispatch_updates_message_status(self):
        """Dispatch marks message as SENT with current timestamp."""
        msg = OutreachMessage(
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

        report = self.sender.dispatch(msg, simulate=True)

        assert report.success is True
        assert msg.status == MessageStatus.SENT
        assert msg.sent_at is not None
        assert msg.sender_mailbox in self.mailboxes
        assert "unsubscribe?email=ceo%40target.com" in msg.body_text
