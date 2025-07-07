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

@pytest.mark.asyncio
async def test_read_user(client):
    pass