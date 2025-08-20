from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from ..config import get_settings

settings = get_settings()
engine = create_async_engine(settings.database_url_async, echo=False, future=True)

# Async session factory used across the app via dependency injection
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)


async def get_session() -> AsyncSession:
    """FastAPI dependency that yields an AsyncSession and ensures proper cleanup."""
    async with AsyncSessionLocal() as session:
        yield session
