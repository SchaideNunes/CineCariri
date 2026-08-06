from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class RoomBase(BaseModel):
    name: str
    capacity: int

class RoomCreate(RoomBase):
    pass

class RoomResponse(RoomBase):
    id: int

    class Config:
        from_attributes = True

class ShowtimeBase(BaseModel):
    movie_id: int
    room_id: int
    start_time: datetime

class ShowtimeCreate(ShowtimeBase):
    pass

class ShowtimeResponse(ShowtimeBase):
    id: int

    class Config:
        from_attributes = True
