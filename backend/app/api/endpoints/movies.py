from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app.db.session import get_db
from app.models.movie import Movie
from app.models.user import User
from app.schemas.movie import MovieCreate, MovieResponse
from app.api.deps import get_current_active_admin

router = APIRouter()

@router.post("/", response_model=MovieResponse)
async def create_movie(
    movie_in: MovieCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_admin)
):
    movie = Movie(**movie_in.model_dump())
    db.add(movie)
    await db.commit()
    await db.refresh(movie)
    return movie

@router.get("/", response_model=List[MovieResponse])
async def read_movies(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Movie).offset(skip).limit(limit))
    movies = result.scalars().all()
    return movies
