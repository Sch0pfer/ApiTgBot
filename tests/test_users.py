import logging
import pytest

logger = logging.getLogger(__name__)


@pytest.mark.asyncio
async def test_create_user(async_client, create_user_via_api, user_data):
    data_from_response = await create_user_via_api(user_data)
    assert data_from_response["id"] == str(user_data.id)
    assert data_from_response["name"] == user_data.name
    assert data_from_response["surname"] == user_data.surname
    assert data_from_response["age"] == user_data.age
    assert data_from_response["email"] == user_data.email
    assert data_from_response["phone"] == user_data.phone


@pytest.mark.asyncio
async def test_read_user(async_client, create_user_via_api, user_data):
    user_data = await create_user_via_api(user_data)

    user_id = user_data["id"]
    get_resp = await async_client.get(f"api/v1/users/{user_id}")
    assert get_resp.status_code == 200

    data = get_resp.json()
    assert data["id"] == user_id
    assert data["email"] == user_data["email"]


@pytest.mark.asyncio
async def test_read_users(async_client, create_user_via_api, multiple_users_data):
    users_data: dict = {}
    for user_data in multiple_users_data:
        create_resp = await create_user_via_api(user_data)

        users_data[create_resp["id"]] = create_resp["email"]

    get_resp = await async_client.get("api/v1/users")
    assert get_resp.status_code == 200

    response_data = get_resp.json()
    for item in response_data:
        assert item["id"] in users_data
        assert item["email"] == users_data[item["id"]]


@pytest.mark.asyncio
async def test_delete_user(async_client, create_user_via_api, user_data):
    create_resp = await create_user_via_api(user_data)

    user_id = create_resp["id"]

    delete_resp = await async_client.delete(f"api/v1/users/{user_id}")
    assert delete_resp.status_code == 204

    get_resp = await async_client.get(f"api/v1/users/{user_id}")
    assert get_resp.status_code == 404


@pytest.mark.asyncio
async def test_delete_users(async_client, create_user_via_api, multiple_users_data):
    for user_data in multiple_users_data:
        await create_user_via_api(user_data)

    delete_resp = await async_client.delete("api/v1/users/")
    assert delete_resp.status_code == 204

    get_resp = await async_client.get("api/v1/users")
    assert get_resp.status_code == 200
    assert get_resp.json() == []


@pytest.mark.asyncio
async def test_update_user(async_client, create_user_via_api, user_data):
    user_data = await create_user_via_api(user_data)

    update_resp = await async_client.put(
        f"api/v1/users/{user_data["id"]}", json=user_data
    )
    assert update_resp.status_code == 200
