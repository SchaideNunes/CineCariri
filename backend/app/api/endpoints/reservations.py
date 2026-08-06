from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from typing import List
import asyncpg

from app.db.session import get_db
from app.models.reservation import Reservation, SeatReservation
from app.models.user import User
from app.schemas.reservation import ReservationCreate, ReservationResponse
from app.api.deps import get_current_active_user, get_current_active_admin

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
    if not reservation_in.seat_ids:
        raise HTTPException(status_code=400, detail="Must provide at least one seat.")
        
    # Start a transaction to create the reservation and link seats
    try:
        reservation = Reservation(
            user_id=current_user.id,
            showtime_id=reservation_in.showtime_id,
            status="ACTIVE"
        )
        db.add(reservation)
        await db.flush() # Flush to get the reservation.id
        
        for seat_id in reservation_in.seat_ids:
            seat_res = SeatReservation(
                reservation_id=reservation.id,
                seat_id=seat_id,
                showtime_id=reservation_in.showtime_id
            )
            db.add(seat_res)
            
        await db.commit()
        await db.refresh(reservation)
        return reservation
        
    except IntegrityError as e:
        await db.rollback()
        # Check if the error is the unique constraint on (showtime_id, seat_id)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="One or more selected seats are already reserved for this showtime."
        )
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
