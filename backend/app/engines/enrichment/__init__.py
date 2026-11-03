"""
Phase 3 — Enrichment Engine package.

Discovers B2B contacts, verifies email syntax and deliverability,
and classifies contact seniority and departments.
"""

from backend.app.engines.enrichment.verifier import EmailVerifier, VerificationResult
from backend.app.engines.enrichment.classifier import ContactClassifier, ClassificationResult
from backend.app.engines.enrichment.discovery import ContactDiscoveryEngine, DiscoveredContact

__all__ = [
    "EmailVerifier",
    "VerificationResult",
    "ContactClassifier",
    "ClassificationResult",
    "ContactDiscoveryEngine",
    "DiscoveredContact",
]
