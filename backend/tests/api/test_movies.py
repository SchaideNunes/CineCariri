import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_movie_admin(client: AsyncClient, admin_token_headers: dict):
    response = await client.post(
        "/api/movies/",
        headers=admin_token_headers,
        json={
            "title": "Inception",
            "description": "A thief who steals corporate secrets...",
            "duration_mins": 148,
            "genre": "Sci-Fi",
            "poster_url": "https://example.com/inception.jpg"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Inception"
    assert "id" in data

@pytest.mark.asyncio
async def test_create_movie_unauthorized(client: AsyncClient, normal_user_token_headers: dict):
    response = await client.post(
        "/api/movies/",
        headers=normal_user_token_headers,
        json={
            "title": "Hackers",
            "description": "A group of hackers...",
            "duration_mins": 105,
            "genre": "Thriller"
        }
    )
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_get_movies(client: AsyncClient, admin_token_headers: dict):
    # Create a movie first
    await client.post(
        "/api/movies/",
        headers=admin_token_headers,
        json={
            "title": "Interstellar",
            "description": "A team of explorers...",
            "duration_mins": 169,
            "genre": "Sci-Fi"
        }
    )
    # Fetch as public
    response = await client.get("/api/movies/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert any(movie["title"] == "Interstellar" for movie in data)
