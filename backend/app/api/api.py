from fastapi import APIRouter
from app.api.endpoints import users, movies, rooms, showtimes, reservations

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(movies.router, prefix="/movies", tags=["movies"])
api_router.include_router(rooms.router, prefix="/rooms", tags=["rooms"])
api_router.include_router(showtimes.router, prefix="/showtimes", tags=["showtimes"])
api_router.include_router(reservations.router, prefix="/reservations", tags=["reservations"])
