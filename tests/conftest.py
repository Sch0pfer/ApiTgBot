import pytest
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import StaticPool
from core.models import Base
import core.models
from fastapi import FastAPI
from httpx import AsyncClient
from main import app as main_app


@pytest.fixture(scope="session")
async def async_client():
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine
    await engine.dispose()


@pytest.fixture
async def db_session(engine) -> AsyncSession:
    async with async_sessionmaker(
        bind=engine,
        expire_on_commit=False,
    ) as session:
        yield session


# @pytest.fixture(autouse=True)
# def override_db_helper(db_session, monkeypatch):
#