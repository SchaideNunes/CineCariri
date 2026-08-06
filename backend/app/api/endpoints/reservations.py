from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from typing import List
import asyncpg

from app.db.session import get_db
from app.models.reservation import Reservation
from app.models.showtime import Showtime
from app.models.user import User
from app.schemas.reservation import ReservationCreate, ReservationResponse
from app.api.deps import get_current_active_user, get_current_active_admin
from sqlalchemy import func

router = APIRouter()

@router.get("/all", response_model=List[ReservationResponse])
async def read_all_reservations(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_active_admin)):
    result = await db.execute(select(Reservation))
    return result.scalars().all()

@router.post("/", response_model=ReservationResponse)
async def create_reservation(
    reservation_in: ReservationCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    if reservation_in.tickets_count <= 0:
        raise HTTPException(status_code=400, detail="Must reserve at least one ticket.")
        
    try:
        # Check capacity
        st_result = await db.execute(select(Showtime).where(Showtime.id == reservation_in.showtime_id))
        showtime = st_result.scalars().first()
        if not showtime:
            raise HTTPException(status_code=404, detail="Showtime not found.")
            
        # Get reserved count
        res_count_result = await db.execute(
            select(func.sum(Reservation.tickets_count)).where(Reservation.showtime_id == showtime.id)
        )
        reserved = res_count_result.scalar() or 0
        
        # We need the room capacity
        await db.refresh(showtime, ['room'])
        available = showtime.room.capacity - reserved
        
        if reservation_in.tickets_count > available:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Not enough tickets available. Only {available} left."
            )

        reservation = Reservation(
            user_id=current_user.id,
            showtime_id=reservation_in.showtime_id,
            tickets_count=reservation_in.tickets_count,
            status="ACTIVE"
        )
        db.add(reservation)
        await db.commit()
        await db.refresh(reservation)
        return reservation
        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/me", response_model=List[ReservationResponse])
async def read_my_reservations(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    result = await db.execute(select(Reservation).filter(Reservation.user_id == current_user.id))
    reservations = result.scalars().all()
    return reservations
