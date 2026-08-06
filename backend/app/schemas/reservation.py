from pydantic import BaseModel
from typing import List
from datetime import datetime

class SeatBase(BaseModel):
    room_id: int
    row_letter: str
    seat_number: int

class SeatCreate(SeatBase):
    pass

class SeatResponse(SeatBase):
    id: int
    class Config:
        from_attributes = True

class ReservationBase(BaseModel):
    showtime_id: int

class ReservationCreate(ReservationBase):
    seat_ids: List[int]

class ReservationResponse(ReservationBase):
    id: int
    user_id: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
