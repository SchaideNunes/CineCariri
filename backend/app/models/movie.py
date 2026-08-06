from sqlalchemy import Column, Integer, String, Text
from app.db.base_class import Base

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True, nullable=False)
    description = Column(Text, nullable=True)
    poster_url = Column(String(500), nullable=True)
    genre = Column(String(100), nullable=True)
    duration_mins = Column(Integer, nullable=False)
