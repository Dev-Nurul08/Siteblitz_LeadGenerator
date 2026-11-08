"""
Phase 2 — Opportunity Engine package.

Resolves websites, audits technical quality and capabilities,
detects service needs, and scores opportunities for agency outreach.
"""

from backend.app.engines.opportunity.resolver import WebsiteResolver
from backend.app.engines.opportunity.auditor import WebsiteAuditor, AuditResult
from backend.app.engines.opportunity.detector import OpportunityDetector, DetectedNeed
from backend.app.engines.opportunity.scorer import OpportunityScorer, ScoredOpportunity

__all__ = [
    "WebsiteResolver",
    "WebsiteAuditor",
    "AuditResult",
    "OpportunityDetector",
    "DetectedNeed",
    "OpportunityScorer",
    "ScoredOpportunity",
]
