import pytest
from httpx import AsyncClient, ASGITransport, Response
from api_v1.users import CreateUser
from main import app

transport = ASGITransport(app=app)
base_url = "http://test"
request_url = "api/v1/users"

async_client = AsyncClient(base_url=base_url, transport=transport)

user_data: CreateUser = CreateUser(
    id="00000000-0000-0000-0000-000000000000",
    name="John",
    surname="Smith",
    age=18,
    email="john.smith@example.com",
    phone="tel:+7-777-777-7777",
)


async def create_user_response(ac: AsyncClient) -> Response:
    return await ac.post(
        url=f"{request_url}/",
        json=user_data.model_dump(mode="json"),
    )


async def get_user_response(ac: AsyncClient) -> Response:
    return await ac.get(url=f"{request_url}/{user_data.id}")


async def delete_user_response(ac: AsyncClient) -> Response:
    return await ac.delete(url=f"{request_url}/{user_data.id}")


async def delete_users_response(ac: AsyncClient) -> Response:
    return await ac.delete(url=f"{request_url}/")


@pytest.mark.asyncio
async def test_create_user():
    response = await create_user_response(async_client)
    assert response.status_code == 200
    user = await get_user_response(async_client)
    data_from_response = user.json()
    assert data_from_response["name"] == user_data.name
    assert data_from_response["surname"] == user_data.surname
    assert data_from_response["age"] == user_data.age
    assert data_from_response["email"] == user_data.email
    assert data_from_response["phone"] == user_data.phone
    delete_response = await delete_user_response(async_client)
    assert delete_response.status_code == 200


@pytest.mark.asyncio
async def test_read_user():
    create_response = await create_user_response(async_client)
    assert create_response.status_code == 200
    user = await get_user_response(async_client)
    data_from_response = user.json()
    response = await async_client.get(url=f"{request_url}/{data_from_response["id"]}")
    assert response.status_code == 200
    delete_response = await delete_user_response(async_client)
    assert delete_response.status_code == 200


@pytest.mark.asyncio
async def test_read_users():
    response = await async_client.get(request_url)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_delete_user():
    create_response = await create_user_response(async_client)
    assert create_response.status_code == 200
    create_response = await delete_user_response(async_client)
    assert create_response.status_code == 200


@pytest.mark.asyncio
async def test_delete_users():
    response = await delete_users_response(async_client)
    assert response.status_code == 200
