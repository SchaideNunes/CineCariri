import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_room(client: AsyncClient, admin_token_headers: dict):
    response = await client.post(
        "/api/rooms/",
        headers=admin_token_headers,
        json={
            "name": "Room 1",
            "capacity": 100
        }
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Room 1"

@pytest.mark.asyncio
async def test_create_showtime(client: AsyncClient, admin_token_headers: dict):
    # 1. Create Movie
    movie_res = await client.post(
        "/api/movies/",
        headers=admin_token_headers,
        json={
            "title": "Avatar",
            "duration_mins": 162
        }
    )
    movie_id = movie_res.json()["id"]

    # 2. Create Room
    room_res = await client.post(
        "/api/rooms/",
        headers=admin_token_headers,
        json={
            "name": "Room 2",
            "capacity": 50
        }
    )
    room_id = room_res.json()["id"]

    # 3. Create Showtime
    showtime_res = await client.post(
        "/api/showtimes/",
        headers=admin_token_headers,
        json={
            "movie_id": movie_id,
            "room_id": room_id,
            "start_time": "2026-12-01T20:00:00"
        }
    )
    assert showtime_res.status_code == 200
    data = showtime_res.json()
    assert data["movie_id"] == movie_id
    assert data["room_id"] == room_id
    
@pytest.mark.asyncio
async def test_get_showtimes(client: AsyncClient, admin_token_headers: dict):
    # Fetch public showtimes
    response = await client.get("/api/showtimes/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
