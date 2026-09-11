import pytest

@pytest.mark.asyncio
async def test_register_user(async_client):
    response = await async_client.post(
        "/api/v1/auth/register",
        json={"email": "test@example.com", "password": "securepass", "company_name": "Test Inc"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data

@pytest.mark.asyncio
async def test_login_user(async_client):
    # First register
    await async_client.post(
        "/api/v1/auth/register",
        json={"email": "login@example.com", "password": "password"}
    )
    # Then login
    response = await async_client.post(
        "/api/v1/auth/login",
        json={"email": "login@example.com", "password": "password"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
