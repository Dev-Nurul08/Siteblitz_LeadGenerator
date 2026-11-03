"""
Database connection and session management.

Provides both async (for FastAPI) and sync (for Alembic/workers) engines.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from backend.app.config import get_settings


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""

    pass


# Async engine for FastAPI
_async_engine = None
_async_session_factory = None

# Sync engine for Alembic and background workers
_sync_engine = None
_sync_session_factory = None


def get_async_engine():
    """Get or create the async database engine."""
    global _async_engine
    if _async_engine is None:
        settings = get_settings()
        kwargs = {"echo": settings.DB_ECHO}
        if not settings.DATABASE_URL.startswith("sqlite"):
            kwargs["pool_size"] = settings.DB_POOL_SIZE
            kwargs["max_overflow"] = settings.DB_MAX_OVERFLOW
        _async_engine = create_async_engine(
            settings.DATABASE_URL,
            **kwargs,
        )
    return _async_engine


def get_async_session_factory():
    """Get or create the async session factory."""
    global _async_session_factory
    if _async_session_factory is None:
        engine = get_async_engine()
        _async_session_factory = async_sessionmaker(
            engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )
    return _async_session_factory


async def get_db_session() -> AsyncSession:
    """FastAPI dependency: yields an async database session."""
    factory = get_async_session_factory()
    async with factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


def get_sync_engine():
    """Get or create the sync database engine (for Alembic and workers)."""
    global _sync_engine
    if _sync_engine is None:
        settings = get_settings()
        kwargs = {"echo": settings.DB_ECHO}
        if settings.DATABASE_URL_SYNC.startswith("sqlite"):
            kwargs["connect_args"] = {"check_same_thread": False}
        else:
            kwargs["pool_size"] = settings.DB_POOL_SIZE
            kwargs["max_overflow"] = settings.DB_MAX_OVERFLOW
        _sync_engine = create_engine(
            settings.DATABASE_URL_SYNC,
            **kwargs,
        )
    return _sync_engine


def get_sync_session_factory():
    """Get or create the sync session factory."""
    global _sync_session_factory
    if _sync_session_factory is None:
        engine = get_sync_engine()
        _sync_session_factory = sessionmaker(
            engine,
            class_=Session,
            expire_on_commit=False,
        )
    return _sync_session_factory


def get_sync_session() -> Session:
    """Get a sync database session for background workers."""
    factory = get_sync_session_factory()
    return factory()
