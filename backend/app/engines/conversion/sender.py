"""
Multi-Mailbox Sender & Token Resolver (Phase 5).

Rotates across verified agency mailboxes to balance sender reputation,
replaces dynamic opt-out and address tokens, and logs dispatch audits.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List, Optional
import urllib.parse

from backend.app.models.campaign import MessageStatus, OutreachMessage
from backend.app.models.contact import RoleLevel


@dataclass
class ProviderEvent:
    """What a real sending provider reported for one submission (email engine v2 E2 builds the provider).

    A message is SENT only when a provider accepted it and gave its own message id. There is no provider in this
    app yet, so the old Campaigns API can no longer mark anything SENT (email engine v2 E1, old phase 5)."""

    provider: str
    provider_message_id: str
    accepted: bool
    at: datetime


@dataclass
class DeliveryReport:
    """Outcome of message dispatch."""

    success: bool
    sender_used: str
    recipient: str
    message_id: int
    sent_at: datetime
    error: Optional[str] = None


class MultiMailboxSender:
    """
    Manages agency sender identity rotation and dynamic token resolution.
    """

    DEFAULT_MAILBOXES = [
        "marcus.vance@siteblitz.agency",
        "claire.dupont@siteblitz.agency",
        "alex.reid@siteblitz.agency",
        "partners@siteblitz.agency",
    ]

    PHYSICAL_POSTAL_ADDRESS = "100 Innovation Way, Suite 400, New York, NY 10001"
    COMPANY_NAME = "SiteBlitz Intelligence"
    BASE_UNSUBSCRIBE_URL = "http://localhost:8000/api/v1/qualification/unsubscribe"

    def __init__(self, mailboxes: Optional[List[str]] = None):
        self.mailboxes = mailboxes or list(self.DEFAULT_MAILBOXES)
        self._rotation_index = 0

    def get_next_mailbox(self, role_level: Optional[RoleLevel] = None) -> str:
        """
        Select next sender mailbox using round-robin rotation.
        """
        if not self.mailboxes:
            return "outreach@siteblitz.agency"

        chosen = self.mailboxes[self._rotation_index % len(self.mailboxes)]
        self._rotation_index += 1
        return chosen

    def resolve_message_tokens(
        self,
        body_text: str,
        recipient_email: str,
        sender_mailbox: str,
    ) -> str:
        """
        Replace compliance and identity tokens with concrete values.
        """
        encoded_email = urllib.parse.quote_plus(recipient_email)
        opt_out_link = f"{self.BASE_UNSUBSCRIBE_URL}?email={encoded_email}"

        resolved = body_text.replace("{{UNSUBSCRIBE_LINK}}", opt_out_link)
        resolved = resolved.replace("{{PHYSICAL_ADDRESS}}", self.PHYSICAL_POSTAL_ADDRESS)
        resolved = resolved.replace("{{SENDER_COMPANY}}", self.COMPANY_NAME)
        resolved = resolved.replace("{{SENDER_MAILBOX}}", sender_mailbox)

        return resolved

    def dispatch(
        self,
        message: OutreachMessage,
        role_level: Optional[RoleLevel] = None,
        simulate: bool = True,
        provider_event: Optional[ProviderEvent] = None,
    ) -> DeliveryReport:
        """
        Mark a message SENT - only with a provider event that accepted it. Without one (every call today: there
        is no sending provider) the message is left untouched in its queue and the report says why.
        `simulate` is kept for old callers and has no effect: a simulation is never recorded as a send.
        """
        if provider_event is None or not provider_event.accepted or not provider_event.provider_message_id:
            return DeliveryReport(
                success=False, sender_used=message.sender_mailbox, recipient=message.recipient_email,
                message_id=message.id, sent_at=datetime.now(timezone.utc),
                error=("Not sent: no sending provider accepted this message "
                       "(sending is built in email engine v2 E2)."))
        sender = self.get_next_mailbox(role_level)
        message.sender_mailbox = sender

        # Resolve tokens
        message.body_text = self.resolve_message_tokens(
            body_text=message.body_text,
            recipient_email=message.recipient_email,
            sender_mailbox=sender,
        )

        now = provider_event.at
        message.status = MessageStatus.SENT
        message.sent_at = now

        return DeliveryReport(
            success=True,
            sender_used=sender,
            recipient=message.recipient_email,
            message_id=message.id,
            sent_at=now,
        )
