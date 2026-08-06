from pydantic import BaseModel
from typing import List
from datetime import datetime

class ReservationBase(BaseModel):
    showtime_id: int

class ReservationCreate(ReservationBase):
    tickets_count: int

class ReservationResponse(ReservationBase):
    id: int
    user_id: int
    tickets_count: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
