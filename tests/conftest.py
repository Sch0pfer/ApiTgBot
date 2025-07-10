import logging
import uuid
from typing import Callable, Awaitable
import pytest_asyncio
from fastapi.openapi.models import Response
from httpx import AsyncClient, ASGITransport
from jaraco.functools import retry
from api_v1.users import CreateUser
from core.models import User
from main import app

logger = logging.getLogger(__name__)


@pytest_asyncio.fixture(scope="function")
async def async_client() -> AsyncClient:
    transport = ASGITransport(app=app)
    async with AsyncClient(
        base_url="http://test",
        transport=transport,
    ) as client:
        yield client


@pytest_asyncio.fixture(autouse=True)
async def cleanup_db(async_client):
    yield
    try:
        response = await async_client.delete("api/v1/users/")
        logger.info(f"Cleanup response: {response.status_code}")
    except Exception as e:
        logger.error(f"Cleanup failed: {str(e)}")


@pytest_asyncio.fixture
def user_data() -> CreateUser:
    return CreateUser(
        id=uuid.uuid4(),
        name="John",
        surname="Smith",
        age=18,
        email="john.smith@example.com",
        phone="tel:+7-777-777-7777",
    )


@pytest_asyncio.fixture
def update_user() -> User:
    return User(
        name="Pencil",
        surname="Baby",
        age=100,
        email="john.smith@example.com",
        phone="tel:+7-777-777-7777",
    )


@pytest_asyncio.fixture
def multiple_users_data() -> list[CreateUser]:
    users = []

    names = ["John", "Emma", "Alex", "Sophia", "James"]
    surnames = ["Smith", "Johnson", "Brown", "Williams", "Taylor"]
    ages = [18, 25, 32, 28, 45]

    for i in range(5):
        user = CreateUser(
            id=uuid.uuid4(),
            name=names[i],
            surname=surnames[i],
            age=ages[i],
            email=f"user{i + 1}@example.com",
            phone=f"tel:+7-777-777-77{70 + i}",
        )
        users.append(user)

    return users


@pytest_asyncio.fixture
def payload_factory() -> Callable[[CreateUser], dict]:
    def _payload_factory(user_data: CreateUser) -> dict:
        payload = user_data.model_dump()
        payload["id"] = str(payload["id"])
        return payload

    return _payload_factory


@pytest_asyncio.fixture
def create_user_via_api(
    async_client, payload_factory
) -> Callable[[CreateUser], Awaitable[dict]]:
    async def _create_user_via_api(user_data: CreateUser) -> dict:
        payload = payload_factory(user_data)
        response = await async_client.post("api/v1/users/", json=payload)
        assert response.status_code == 201, logger.error(
            f"Create failed: {response.status_code}, {response.json()}"
        )
        return response.json()

    return _create_user_via_api
