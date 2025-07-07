import pytest
from uuid import UUID, uuid4
from fastapi import status
from api_v1.users import CreateUser

TEST_USER = {
    "name": "John",
    "surname": "Doe",
    "age": 30,
    "email": "john.doe@example.com",
    "phone": "+1234567890",
}


@pytest.mark.asyncio
async def test_create_user(client):
    response = await client.post("/api/v1/users", json=TEST_USER)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["message"] == "User John created successfully!"
    assert UUID(data.get("user_id", ""), "Invalid UUID returned")


@pytest.mark.asyncio
async def test_read_user(client):
    create_response = await client.post("/api/v1/users", json=TEST_USER)
    user_id = create_response.json().get("user_id")

    response = await client.get(f"/api/v1/users/{user_id}")
    assert response.status_code == status.HTTP_200_OK
    user = await response.json()
    assert user == TEST_USER


@pytest.mark.asyncio
async def test_update_user(client):
    create_response = await client.post("/users/", json=TEST_USER)
    user_id = create_response.json().get("user_id")

    update_data = {**TEST_USER, "name": "Updated"}
    response = await client.put(f"/users/{user_id}", json=update_data)
    assert response.status_code == status.HTTP_200_OK

    get_response = await client.get(f"/users/{user_id}")
    assert get_response.json()["name"] == "Updated"


@pytest.mark.asyncio
async def test_delete_user(client):
    create_response = await client.post("/users/", json=TEST_USER)
    user_id = create_response.json().get("user_id")

    response = await client.delete(f"/users/{user_id}")
    assert response.status_code == status.HTTP_200_OK

    get_response = await client.get(f"/users/{user_id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_filter_users(client):
    users = [
        {**TEST_USER, "email": f"user{i}@test.com", "age": 20 + i} for i in range(1, 6)
    ]
    for user in users:
        await client.post("/users/", json=user)

    response = await client.get("/users/?min_age=23&max_age=25")
    assert response.status_code == status.HTTP_200_OK
    filtered = response.json()["users"]
    assert len(filtered) == 3
    assert all(23 <= u["age"] <= 25 for u in filtered)


@pytest.mark.asyncio
async def test_unique_constraints(client):
    response1 = await client.post("/users/", json=TEST_USER)
    assert response1.status_code == 200

    response2 = await client.post("/users/", json={**TEST_USER, "phone": "+0987654321"})
    assert response2.status_code == status.HTTP_409_CONFLICT
    assert "Email or phone already exists" in response2.json()["detail"]
