from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base

class Seat(Base):
    __tablename__ = "seats"

    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False)
    row_letter = Column(String(10), nullable=False)
    seat_number = Column(Integer, nullable=False)

    room = relationship("Room")

class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    showtime_id = Column(Integer, ForeignKey("showtimes.id"), nullable=False)
    status = Column(String(50), default="ACTIVE")
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")
    showtime = relationship("Showtime")
    seats = relationship("SeatReservation", back_populates="reservation")

class SeatReservation(Base):
    __tablename__ = "seat_reservations"

    reservation_id = Column(Integer, ForeignKey("reservations.id"), primary_key=True)
    seat_id = Column(Integer, ForeignKey("seats.id"), primary_key=True)
    showtime_id = Column(Integer, ForeignKey("showtimes.id"), nullable=False)

    __table_args__ = (
        UniqueConstraint('showtime_id', 'seat_id', name='uix_showtime_seat'),
    )

    reservation = relationship("Reservation", back_populates="seats")
    seat = relationship("Seat")
