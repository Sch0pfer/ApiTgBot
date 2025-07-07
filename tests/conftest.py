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


@pytest.fixture(autouse=True)
def override_db_helper(db_session, monkeypatch):
    class TestDBHelper:
        async def get_async_session(self):
            yield db_session

    monkeypatch.setattr(core.models, "db_helper", TestDBHelper())


@pytest.fixture
async def app() -> FastAPI:
    return main_app


@pytest.fixture
async def client(app) -> AsyncClient:
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
