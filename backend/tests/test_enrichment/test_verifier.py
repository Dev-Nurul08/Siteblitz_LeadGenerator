"""
Tests for EmailVerifier (Phase 3).
"""

from unittest.mock import MagicMock, patch
import dns.resolver

from backend.app.engines.enrichment.verifier import EmailVerifier
from backend.app.models.contact import EmailVerificationStatus


class TestEmailVerifier:
    """Test suite for EmailVerifier."""

    def setup_method(self):
        self.verifier = EmailVerifier()

    def test_syntax_validation_valid(self):
        """Valid RFC 5322 syntax returns True."""
        assert self.verifier.verify("john.doe@company.co.uk").is_valid_syntax is True
        assert self.verifier.verify("sarah+leads@startup.io").is_valid_syntax is True
        assert self.verifier.verify("alex_smith@global.org").is_valid_syntax is True

    def test_syntax_validation_invalid(self):
        """Rejects malformed email syntax."""
        assert self.verifier.verify("plainaddress").status == EmailVerificationStatus.INVALID
        assert self.verifier.verify("@missinglocal.com").status == EmailVerificationStatus.INVALID
        assert self.verifier.verify("missingdomain@").status == EmailVerificationStatus.INVALID
        assert self.verifier.verify(None).status == EmailVerificationStatus.INVALID

    def test_disposable_domain_detection(self):
        """Detects temporary / burner email providers."""
        res = self.verifier.verify("tester@mailinator.com")
        assert res.is_disposable is True
        assert res.status == EmailVerificationStatus.DISPOSABLE
        assert res.verification_score == 0.0

        res_temp = self.verifier.verify("fake123@tempmail.com")
        assert res_temp.is_disposable is True
        assert res_temp.status == EmailVerificationStatus.DISPOSABLE

    def test_role_based_detection(self):
        """Detects department and role-based mailboxes."""
        role_emails = [
            "info@acme.com",
            "support@software.io",
            "sales@store.co",
            "admin@platform.net",
            "contact@agency.com",
            "hello@studio.design",
        ]
        for em in role_emails:
            # Mock MX lookup to return active MX
            with patch.object(self.verifier.resolver, "resolve") as mock_dns:
                mock_ans = [MagicMock(exchange="mail.example.com")]
                mock_dns.return_value = mock_ans

                res = self.verifier.verify(em)
                assert res.is_role_based is True
                assert res.status == EmailVerificationStatus.ROLE_BASED
                assert res.verification_score == 0.70

    def test_verified_personal_mailbox(self):
        """Personal corporate email with active MX is VERIFIED with high confidence."""
        with patch.object(self.verifier.resolver, "resolve") as mock_dns:
            mock_ans = [MagicMock(exchange="mx1.enterprise.com")]
            mock_dns.return_value = mock_ans

            res = self.verifier.verify("elena.rostova@enterprise.com")
            assert res.status == EmailVerificationStatus.VERIFIED
            assert res.is_role_based is False
            assert res.has_valid_mx is True
            assert res.verification_score == 0.95
            assert "mx1.enterprise.com" in res.mx_records
