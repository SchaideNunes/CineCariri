from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app.db.session import get_db
from app.models.showtime import Room
from app.models.user import User
from app.schemas.showtime import RoomCreate, RoomResponse
from app.api.deps import get_current_active_admin

router = APIRouter()

@router.post("/", response_model=RoomResponse)
async def create_room(
    room_in: RoomCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_admin)
):
    room = Room(**room_in.model_dump())
    db.add(room)
    await db.commit()
    await db.refresh(room)
    return room

@router.get("/", response_model=List[RoomResponse])
async def read_rooms(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Room).offset(skip).limit(limit))
    rooms = result.scalars().all()
    return rooms
