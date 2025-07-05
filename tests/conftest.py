import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from main import app
from core.models import Base, DatabaseHelper

TEST_DATABASE_URL = "postgresql+asyncpg://pencil:1234@localhost:5234/mydb"


@pytest.fixture(scope="session")
def asyncio_backend():
    return "asyncio"


@pytest.fixture(scope="function")
async def async_client():
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async def override_get_db():
        TestingSessionLocal = sessionmaker(
            bind=engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )
        async with TestingSessionLocal() as session:
            yield session

    app.dependency_overrides[DatabaseHelper.get_async_session()] = override_get_db

    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
