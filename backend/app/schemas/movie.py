from pydantic import BaseModel
from typing import Optional

class MovieBase(BaseModel):
    title: str
    description: Optional[str] = None
    poster_url: Optional[str] = None
    genre: Optional[str] = None
    duration_mins: int

class MovieCreate(MovieBase):
    pass

class MovieUpdate(MovieBase):
    title: Optional[str] = None
    duration_mins: Optional[int] = None

class MovieResponse(MovieBase):
    id: int

    class Config:
        from_attributes = True
