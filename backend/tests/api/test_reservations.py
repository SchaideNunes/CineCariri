import pytest
import asyncio
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_make_reservation_and_concurrency(client: AsyncClient, admin_token_headers: dict, normal_user_token_headers: dict, setup_db):
    # 1. Admin sets up Movie, Room, and Showtime
    movie_res = await client.post("/api/movies/", headers=admin_token_headers, json={"title": "Test Movie", "duration_mins": 120})
    movie_id = movie_res.json()["id"]
    room_res = await client.post("/api/rooms/", headers=admin_token_headers, json={"name": "Test Room", "capacity": 10})
    room_id = room_res.json()["id"]
    showtime_res = await client.post("/api/showtimes/", headers=admin_token_headers, json={"movie_id": movie_id, "room_id": room_id, "start_time": "2026-12-01T20:00:00"})
    showtime_id = showtime_res.json()["id"]

    # 2. Admin creates a Seat
    seat_res = await client.post("/api/seats/", headers=admin_token_headers, json={"room_id": room_id, "row_letter": "A", "seat_number": 1})
    seat_id = seat_res.json()["id"]

    # 3. Simulate two users booking the same seat at the same time
    async def book_seat(token_headers):
        return await client.post(
            "/api/reservations/",
            headers=token_headers,
            json={"showtime_id": showtime_id, "seat_ids": [seat_id]}
        )

    # Use asyncio.gather to fire both requests concurrently
    res1, res2 = await asyncio.gather(
        book_seat(normal_user_token_headers),
        book_seat(admin_token_headers) # admin can also be a user making a reservation
    )

    # 4. Verify one succeeded (200) and one failed (400 or 409) due to UniqueConstraint
    status_codes = [res1.status_code, res2.status_code]
    assert 200 in status_codes
    assert 400 in status_codes or 409 in status_codes
