from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app.db.session import get_db
from app.models.showtime import Showtime
from app.models.user import User
from app.schemas.showtime import ShowtimeCreate, ShowtimeResponse
from app.api.deps import get_current_active_admin

router = APIRouter()

@router.post("/", response_model=ShowtimeResponse)
async def create_showtime(
    showtime_in: ShowtimeCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_admin)
):
    showtime = Showtime(**showtime_in.model_dump())
    db.add(showtime)
    await db.commit()
    await db.refresh(showtime)
    return showtime

@router.get("/", response_model=List[ShowtimeResponse])
async def read_showtimes(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Showtime).offset(skip).limit(limit))
    showtimes = result.scalars().all()
    return showtimes
