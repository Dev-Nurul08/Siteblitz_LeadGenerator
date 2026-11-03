"""
Inbound Reply Intent Classifier (Phase 5).

Classifies responses from prospective clients into structured intent categories
(INTERESTED, NOT_INTERESTED, UNSUBSCRIBE_REQUEST, OUT_OF_OFFICE) and routes
automated CRM deal progression and suppression list triggers.
"""

from dataclasses import dataclass
import re
from typing import Optional

from backend.app.models.campaign import DealStage, ReplyIntent

# Pattern matchers
UNSUBSCRIBE_PATTERNS = [
    r"\bunsubscribe\b",
    r"\bremove (?:me|us|this email|our business|my company|my details|my email)\b",
    r"\bstop emailing\b",
    r"\btake (?:me|us|our business|my company) off\b",
    r"\bdo not contact\b",
    r"\bopt[- ]?out\b",
    r"\bdelete my (?:data|email|info)\b",
    r"\bstop sending\b",
    r"\breport(?:ed)? (?:as )?spam\b",
    r"\bfrom your list\b",
]

INTERESTED_PATTERNS = [
    r"\blet'?s (?:talk|discuss|chat|connect|meet)\b",
    r"\bhow much\b",
    r"\bpricing\b",
    r"\bsend (?:me )?(?:a )?(?:proposal|quote|estimate|details|info)\b",
    r"\bavailable (?:on|next|this)\b",
    r"\bschedule a (?:call|demo|meeting)\b",
    r"\bopen to (?:seeing|reviewing|learning)\b",
    r"\bsounds (?:good|interesting|great)\b",
    r"\bcall me at\b",
    r"\bwhat would (?:it|this) cost\b",
]

NOT_INTERESTED_PATTERNS = [
    r"\bnot interested\b",
    r"\bno thank(?:s| you)\b",
    r"\balready have (?:a|an)\b",
    r"\bwe (?:already )?(?:use|have) an? agency\b",
    r"\bnot (?:looking|in the market)\b",
    r"\bwe'?re good\b",
    r"\bpass on this\b",
    r"\bnot at this time\b",
]

OUT_OF_OFFICE_PATTERNS = [
    r"\bout of (?:the )?office\b",
    r"\bauto[- ]?reply\b",
    r"\bautomatic reply\b",
    r"\bon (?:annual|parental|maternity|paternity) leave\b",
    r"\bi am away from\b",
    r"\breturning on\b",
]


@dataclass
class ReplyClassification:
    """Classified inbound response with recommended CRM pipeline action."""

    intent: ReplyIntent
    confidence: float
    recommended_stage: Optional[DealStage] = None
    should_suppress: bool = False
    action_summary: str = ""


class ReplyIntentClassifier:
    """
    Evaluates response sentiment and matches intent.
    """

    def classify_reply(self, reply_text: str) -> ReplyClassification:
        """
        Classify inbound email body into an actionable intent category.
        """
        text = (reply_text or "").lower().strip()

        # 1. Unsubscribe / Opt-out takes top priority for compliance
        if any(re.search(pat, text, flags=re.IGNORECASE) for pat in UNSUBSCRIBE_PATTERNS):
            return ReplyClassification(
                intent=ReplyIntent.UNSUBSCRIBE_REQUEST,
                confidence=0.98,
                recommended_stage=DealStage.LOST,
                should_suppress=True,
                action_summary="Recipient requested removal. Register immediately in global suppression list.",
            )

        # 2. Out of office autoresponders
        if any(re.search(pat, text, flags=re.IGNORECASE) for pat in OUT_OF_OFFICE_PATTERNS):
            return ReplyClassification(
                intent=ReplyIntent.OUT_OF_OFFICE,
                confidence=0.95,
                recommended_stage=None,
                should_suppress=False,
                action_summary="Autoresponder detected. Keep lead active and reschedule follow-up.",
            )

        # 3. Commercial Interest / Buying Intent
        if any(re.search(pat, text, flags=re.IGNORECASE) for pat in INTERESTED_PATTERNS):
            return ReplyClassification(
                intent=ReplyIntent.INTERESTED,
                confidence=0.92,
                recommended_stage=DealStage.MEETING_SCHEDULED,
                should_suppress=False,
                action_summary="High commercial interest detected! Advance to MEETING_SCHEDULED.",
            )

        # 4. Polite Decline
        if any(re.search(pat, text, flags=re.IGNORECASE) for pat in NOT_INTERESTED_PATTERNS):
            return ReplyClassification(
                intent=ReplyIntent.NOT_INTERESTED,
                confidence=0.90,
                recommended_stage=DealStage.LOST,
                should_suppress=False,
                action_summary="Recipient politely declined. Mark deal as LOST and preserve cooldown.",
            )

        # 5. General Inquiry fallback
        return ReplyClassification(
            intent=ReplyIntent.GENERAL_INQUIRY,
            confidence=0.60,
            recommended_stage=DealStage.CONTACTED,
            should_suppress=False,
            action_summary="General reply received. Requires operator review to determine next step.",
        )
