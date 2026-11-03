"""
Source adapter registry — maps adapter slugs to their classes.

Enables dynamic adapter resolution from database configuration.
"""

import importlib
from typing import Optional

import structlog

from backend.app.engines.discovery.base import BaseSourceAdapter

logger = structlog.get_logger(__name__)


class SourceAdapterRegistry:
    """
    Central registry for source adapter classes.

    Supports both explicit registration and dynamic import from
    fully-qualified class names stored in the database.
    """

    _adapters: dict[str, type[BaseSourceAdapter]] = {}

    @classmethod
    def register(cls, slug: str, adapter_class: type[BaseSourceAdapter]) -> None:
        """Register an adapter class by slug."""
        if not issubclass(adapter_class, BaseSourceAdapter):
            raise TypeError(
                f"{adapter_class.__name__} must be a subclass of BaseSourceAdapter"
            )
        cls._adapters[slug] = adapter_class
        logger.info("adapter_registered", slug=slug, cls=adapter_class.__name__)

    @classmethod
    def get(cls, slug: str) -> Optional[type[BaseSourceAdapter]]:
        """Get a registered adapter class by slug."""
        return cls._adapters.get(slug)

    @classmethod
    def get_or_import(
        cls, slug: str, class_path: Optional[str] = None
    ) -> type[BaseSourceAdapter]:
        """
        Get a registered adapter, or dynamically import from class_path.

        Args:
            slug: Adapter slug identifier
            class_path: Fully-qualified Python class path
                        (e.g., 'backend.app.engines.discovery.osm.OSMAdapter')

        Returns:
            The adapter class

        Raises:
            ValueError: If adapter not found and cannot be imported
        """
        adapter = cls._adapters.get(slug)
        if adapter:
            return adapter

        if not class_path:
            raise ValueError(
                f"Adapter '{slug}' not registered and no class_path provided"
            )

        try:
            module_path, class_name = class_path.rsplit(".", 1)
            module = importlib.import_module(module_path)
            adapter_class = getattr(module, class_name)

            if not issubclass(adapter_class, BaseSourceAdapter):
                raise TypeError(
                    f"{class_name} is not a subclass of BaseSourceAdapter"
                )

            cls.register(slug, adapter_class)
            return adapter_class

        except (ImportError, AttributeError) as e:
            raise ValueError(
                f"Failed to import adapter '{slug}' from '{class_path}': {e}"
            ) from e

    @classmethod
    def list_registered(cls) -> dict[str, str]:
        """List all registered adapters as {slug: class_name}."""
        return {
            slug: adapter.__name__ for slug, adapter in cls._adapters.items()
        }

    @classmethod
    def clear(cls) -> None:
        """Clear all registered adapters (useful for testing)."""
        cls._adapters.clear()
