import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_register_user(client: AsyncClient):
    response = await client.post(
        "/api/users/register",
        json={"email": "test@example.com", "password": "password123"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data
    assert "hashed_password" not in data

@pytest.mark.asyncio
async def test_register_existing_user(client: AsyncClient):
    # Register first time
    await client.post(
        "/api/users/register",
        json={"email": "duplicate@example.com", "password": "password123"}
    )
    
    # Register second time
    response = await client.post(
        "/api/users/register",
        json={"email": "duplicate@example.com", "password": "password123"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

@pytest.mark.asyncio
async def test_login_user(client: AsyncClient):
    # Register first
    await client.post(
        "/api/users/register",
        json={"email": "login@example.com", "password": "password123"}
    )
    
    # Login
    response = await client.post(
        "/api/users/login",
        data={"username": "login@example.com", "password": "password123"}
    )
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_get_current_user_profile(client: AsyncClient):
    # Register and login to get token
    await client.post(
        "/api/users/register",
        json={"email": "profile@example.com", "password": "password123"}
    )
    response = await client.post(
        "/api/users/login",
        data={"username": "profile@example.com", "password": "password123"}
    )
    token = response.json()["access_token"]
    
    # Get profile
    profile_response = await client.get(
        "/api/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert profile_response.status_code == 200
    assert profile_response.json()["email"] == "profile@example.com"

@pytest.mark.asyncio
async def test_admin_access_denied_for_regular_user(client: AsyncClient):
    await client.post(
        "/api/users/register",
        json={"email": "regular@example.com", "password": "password123"}
    )
    login_response = await client.post(
        "/api/users/login",
        data={"username": "regular@example.com", "password": "password123"}
    )
    token = login_response.json()["access_token"]
    
    # Access an admin route
    admin_response = await client.get(
        "/api/users/admin-only",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert admin_response.status_code == 403
