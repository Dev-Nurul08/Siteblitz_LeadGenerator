"""
SiteBlitz Lead Intelligence OS — FastAPI Application.

Main entry point for the backend API server.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.router import api_v1_router
from backend.app.config import get_settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan — startup and shutdown events."""
    # Register default source adapters
    from backend.app.engines.discovery.registry import SourceAdapterRegistry
    from backend.app.engines.discovery.osm import OSMAdapter
    from backend.app.engines.discovery.csv_import import CSVImportAdapter
    from backend.app.engines.discovery.wikidata import WikidataAdapter
    from backend.app.engines.discovery.overture import OvertureAdapter
    from backend.app.engines.discovery.combined import CombinedAdapter
    from backend.app.database import get_async_engine, Base
    import backend.app.models.source  # ensure models are loaded
    import backend.app.models.business
    import backend.app.models.opportunity
    import backend.app.models.contact
    import backend.app.models.compliance
    import backend.app.models.campaign
    import backend.app.models.intelligence

    SourceAdapterRegistry.register("openstreetmap", OSMAdapter)
    SourceAdapterRegistry.register("csv_import", CSVImportAdapter)
    SourceAdapterRegistry.register("wikidata", WikidataAdapter)
    SourceAdapterRegistry.register("overture", OvertureAdapter)
    SourceAdapterRegistry.register("all_sources", CombinedAdapter)

    # Initialize tables if needed
    engine = get_async_engine()
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    except Exception as e:
        import structlog
        structlog.get_logger(__name__).warning("table_init_failed", error=str(e))

    yield

    # Cleanup
    await engine.dispose()


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    settings = get_settings()

    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description=(
            "Internal sales intelligence and customer acquisition platform. "
            "Discovers businesses, identifies digital-service opportunities, "
            "and manages personalized outreach campaigns."
        ),
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # API routes
    app.include_router(api_v1_router)

    # Health check
    @app.get("/health")
    async def health_check():
        return {
            "status": "healthy",
            "app": settings.APP_NAME,
            "version": settings.APP_VERSION,
        }

    return app


# Application instance
app = create_app()
