"""
Tests for OutputValidator (Phase 4).
"""

from backend.app.engines.qualification.output_validator import OutputValidator


class TestOutputValidator:
    """Test suite for safety, compliance, and spam filter output validation."""

    def setup_method(self):
        self.validator = OutputValidator()
        self.valid_subject = "Question regarding Apex Dental's mobile user experience"
        self.valid_body = (
            "Hi Sarah,\n\n"
            "I noticed that your website isn't optimized for smartphone screens, which makes "
            "it challenging for mobile visitors to schedule visits.\n\n"
            "We build high-converting responsive websites that increase client bookings.\n\n"
            "Would you be open to a 5-minute preview of a modernized concept?\n\n"
            "Best regards,\nMarcus Vance\n\n"
            "---\n100 Innovation Way, Suite 400, New York, NY\n"
            "To unsubscribe click here: {{UNSUBSCRIBE_LINK}}"
        )

    def test_valid_pitch_passes(self):
        """Clean pitch with footer and valid text passes inspection."""
        res = self.validator.validate(self.valid_subject, self.valid_body)
        assert res.is_valid is True
        assert len(res.errors) == 0

    def test_missing_unsubscribe_link_fails(self):
        """Body without opt-out token fails compliance."""
        body_no_optout = self.valid_body.replace("{{UNSUBSCRIBE_LINK}}", "").replace("unsubscribe", "goodbye")
        res = self.validator.validate(self.valid_subject, body_no_optout)
        assert res.is_valid is False
        assert any("unsubscribe" in e.lower() for e in res.errors)

    def test_missing_physical_address_fails(self):
        """Body missing physical postal address fails CAN-SPAM check."""
        body_no_addr = (
            "Hi Sarah,\n\n"
            "I noticed that your website isn't optimized for smartphone screens, which makes "
            "it challenging for mobile visitors to schedule visits.\n\n"
            "Would you be open to a 5-minute preview of a modernized concept?\n\n"
            "To opt out click here: {{UNSUBSCRIBE_LINK}}"
        )
        res = self.validator.validate(self.valid_subject, body_no_addr)
        assert res.is_valid is False
        assert any("address" in e.lower() for e in res.errors)

    def test_spam_trigger_phrase_fails(self):
        """Deceptive claim like 'guaranteed 100% million' is blocked by safety validator."""
        spam_body = self.valid_body + "\n\nWe provide guaranteed 100% million dollar results!"
        res = self.validator.validate(self.valid_subject, spam_body)
        assert res.is_valid is False
        assert any("spam trigger" in e.lower() for e in res.errors)

    def test_unresolved_template_placeholder_fails(self):
        """Unresolved variable like {{unknown_token}} causes validation rejection."""
        broken_body = self.valid_body.replace("Sarah", "{{client_first_name}}")
        res = self.validator.validate(self.valid_subject, broken_body)
        assert res.is_valid is False
        assert any("unreplaced" in e.lower() for e in res.errors)
