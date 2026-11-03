"""
Tests for ReplyIntentClassifier (Phase 5).
"""

from backend.app.engines.conversion.replies import ReplyIntentClassifier
from backend.app.models.campaign import DealStage, ReplyIntent


class TestReplyIntentClassifier:
    """Test suite for inbound email sentiment and intent classification."""

    def setup_method(self):
        self.classifier = ReplyIntentClassifier()

    def test_interested_classification(self):
        """Phrases asking for demo or pricing classify as INTERESTED and advance to MEETING_SCHEDULED."""
        texts = [
            "Hi Marcus, sounds interesting. Can you send pricing?",
            "Let's discuss next Tuesday at 2pm.",
            "We are open to seeing a demo, what does it cost?",
            "How much would a mobile app reorder system run us?",
        ]
        for t in texts:
            res = self.classifier.classify_reply(t)
            assert res.intent == ReplyIntent.INTERESTED, f"Failed on: {t}"
            assert res.recommended_stage == DealStage.MEETING_SCHEDULED
            assert res.should_suppress is False

    def test_not_interested_classification(self):
        """Polite decline classifies as NOT_INTERESTED and marks deal as LOST."""
        texts = [
            "No thank you, we're good right now.",
            "Not interested. We already have an in-house webmaster.",
            "Please pass on this, we are not looking for agencies.",
        ]
        for t in texts:
            res = self.classifier.classify_reply(t)
            assert res.intent == ReplyIntent.NOT_INTERESTED, f"Failed on: {t}"
            assert res.recommended_stage == DealStage.LOST
            assert res.should_suppress is False

    def test_unsubscribe_request_classification(self):
        """Unsubscribe or stop commands trigger immediate suppression."""
        texts = [
            "Please unsubscribe me immediately.",
            "Remove our business from your list.",
            "Stop emailing me or I will report as spam.",
            "Take me off your outreach system.",
        ]
        for t in texts:
            res = self.classifier.classify_reply(t)
            assert res.intent == ReplyIntent.UNSUBSCRIBE_REQUEST, f"Failed on: {t}"
            assert res.should_suppress is True
            assert res.recommended_stage == DealStage.LOST

    def test_out_of_office_classification(self):
        """Vacation autoresponders classify as OUT_OF_OFFICE without altering deal stage."""
        texts = [
            "I am currently out of the office on annual leave returning next Monday.",
            "Auto-reply: Thank you for your email. I am away from my desk.",
        ]
        for t in texts:
            res = self.classifier.classify_reply(t)
            assert res.intent == ReplyIntent.OUT_OF_OFFICE, f"Failed on: {t}"
            assert res.should_suppress is False
            assert res.recommended_stage is None
