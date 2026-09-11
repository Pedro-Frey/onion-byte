import pytest

@pytest.mark.asyncio
async def test_create_and_get_lead(async_client):
    # Register & Login
    await async_client.post("/api/v1/auth/register", json={"email": "lead@example.com", "password": "pass"})
    login_resp = await async_client.post("/api/v1/auth/login", json={"email": "lead@example.com", "password": "pass"})
    token = login_resp.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Enrich lead
    enrich_resp = await async_client.post(
        "/api/v1/leads/enrich",
        headers=headers,
        json={"name": "John Doe", "email": "john@example.com", "phone": "123456"}
    )
    assert enrich_resp.status_code == 200
    lead_id = enrich_resp.json()["id"]
    
    # Get lead
    get_resp = await async_client.get(f"/api/v1/leads/{lead_id}", headers=headers)
    assert get_resp.status_code == 200
    assert get_resp.json()["original_data"]["name"] == "John Doe"
