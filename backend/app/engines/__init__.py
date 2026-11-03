"""Discovery engine package — source adapters and business normalization."""

from backend.app.engines.discovery.base import BaseSourceAdapter, DiscoveredBusiness
from backend.app.engines.discovery.normalizer import BusinessNormalizer
from backend.app.engines.discovery.registry import SourceAdapterRegistry

__all__ = [
    "BaseSourceAdapter",
    "DiscoveredBusiness",
    "BusinessNormalizer",
    "SourceAdapterRegistry",
]
