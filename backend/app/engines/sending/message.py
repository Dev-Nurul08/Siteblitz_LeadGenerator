"""
Builds one campaign message (spec rows 5 and 12; contract "Lead-generator side").

Plain text, UTF-8 (quoted-printable, so the ₹ sign survives any relay), no HTML part, no attachment, no image, no
tracking pixel. Headers:

    From: "<display name>, SiteBlitz" <mailbox>      To, Subject, Date, Message-ID
    Reply-To: <mailbox>
    List-Unsubscribe: <{base}/u/{token}>, <mailto:{mailbox}?subject=unsubscribe>
    List-Unsubscribe-Post: List-Unsubscribe=One-Click
    In-Reply-To / References (steps 2 and 3 thread under step 1; subject "Re: <step 1 subject>")

The body's last line is always `Reply "stop" or unsubscribe here: {base}/u/{token}`, added here: a stored body that
already ends with such a line (a writer placeholder) has it replaced. DKIM signing is the mailbox provider's job
(Mailforge signs on submission; launch gate 17 c checks the received headers).
"""

import re
import uuid
from dataclasses import dataclass
from datetime import datetime
from email import policy
from email.headerregistry import Address
from email.message import EmailMessage
from email.utils import format_datetime
from typing import Optional

from backend.app.engines.sending.tokens import token_for_email, unsubscribe_url

BRAND = "SiteBlitz"
UNSUBSCRIBE_LINE = 'Reply "stop" or unsubscribe here: {url}'
_OLD_LINE = re.compile(r'^\s*Reply\s+"?stop"?\s+or\s+unsubscribe\s+here:.*$', re.IGNORECASE)
# Long enough that the List-Unsubscribe URL (about 200 characters) is never folded inside a token.
MESSAGE_POLICY = policy.SMTP.clone(max_line_length=998)


def new_message_id(sending_domain: str) -> str:
    return f"<{uuid.uuid4()}@{sending_domain}>"


def reply_subject(step1_subject: str) -> str:
    subject = step1_subject.strip()
    return subject if subject.lower().startswith("re:") else f"Re: {subject}"


@dataclass
class OutgoingMessage:
    message: EmailMessage
    unsubscribe_url: str
    token: str

    def as_bytes(self) -> bytes:
        return self.message.as_bytes(policy=MESSAGE_POLICY)


def body_with_unsubscribe(body: str, url: str) -> str:
    lines = body.replace("\r\n", "\n").rstrip().split("\n")
    while lines and (not lines[-1].strip() or _OLD_LINE.match(lines[-1])):
        lines.pop()
    return "\n".join(lines) + "\n\n" + UNSUBSCRIBE_LINE.format(url=url) + "\n"


def build_message(*, mailbox_address: str, display_name: str, recipient: str, subject: str, body: str,
                  message_id: str, send_record_id: str, base_url: str, signing_secret: str, date: datetime,
                  thread_parent_ids: Optional[list[str]] = None) -> OutgoingMessage:
    """thread_parent_ids = Message-IDs of the earlier steps, oldest first (empty / None for step 1)."""
    token = token_for_email(recipient, send_record_id, signing_secret)
    url = unsubscribe_url(base_url, token)
    message = EmailMessage(policy=MESSAGE_POLICY)
    message["From"] = Address(display_name=f"{display_name.strip()}, {BRAND}", addr_spec=mailbox_address)
    message["To"] = recipient
    message["Subject"] = subject
    message["Date"] = format_datetime(date)
    message["Message-ID"] = message_id
    message["Reply-To"] = mailbox_address
    if thread_parent_ids:
        message["In-Reply-To"] = thread_parent_ids[-1]
        message["References"] = " ".join(thread_parent_ids)
    message["List-Unsubscribe"] = f"<{url}>, <mailto:{mailbox_address}?subject=unsubscribe>"
    message["List-Unsubscribe-Post"] = "List-Unsubscribe=One-Click"
    message.set_content(body_with_unsubscribe(body, url), subtype="plain", charset="utf-8",
                        cte="quoted-printable")
    return OutgoingMessage(message, url, token)
