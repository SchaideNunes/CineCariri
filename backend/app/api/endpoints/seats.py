from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app.db.session import get_db
from app.models.reservation import Seat
from app.models.user import User
from app.schemas.reservation import SeatCreate, SeatResponse
from app.api.deps import get_current_active_admin

router = APIRouter()

@router.post("/", response_model=SeatResponse)
async def create_seat(
    seat_in: SeatCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_admin)
):
    seat = Seat(**seat_in.model_dump())
    db.add(seat)
    await db.commit()
    await db.refresh(seat)
    return seat

@router.get("/{room_id}", response_model=List[SeatResponse])
async def get_seats_for_room(
    room_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Seat).filter(Seat.room_id == room_id))
    seats = result.scalars().all()
    return seats
