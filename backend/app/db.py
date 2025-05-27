from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
import os


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://tick:dash@db:5432/ticks",
)

engine = create_async_engine(DATABASE_URL, echo=False, future=True)
AsyncSessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def init_db() -> None:
    """Run at startup - create tables if thery don't exist."""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
