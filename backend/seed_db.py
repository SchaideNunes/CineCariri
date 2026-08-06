import asyncio
from datetime import datetime, timedelta
from app.db.session import AsyncSessionLocal
from app.models.movie import Movie
from app.models.showtime import Room, Showtime
from app.models.reservation import Seat
from app.models.user import User
from app.db.base_class import Base
from app.db.session import engine

async def seed():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        
    async with AsyncSessionLocal() as db:
        # Create Movies
        spiderman = Movie(
            title="Homem-Aranha: Um Novo Dia",
            duration_mins=144,
            genre="Ação, Aventura, Fantasia, Ficção Científica",
            poster_url="https://images.unsplash.com/photo-1635805737707-575885ab0820?q=80&w=800&auto=format&fit=crop" # Dummy spiderman-like poster
        )
        odyssey = Movie(
            title="A Odisseia",
            duration_mins=172,
            genre="Ação, Aventura, Épico, Fantasia",
            poster_url="https://images.unsplash.com/photo-1605806616949-1e87b487cb2a?q=80&w=800&auto=format&fit=crop" # Dummy epic poster
        )
        
        db.add(spiderman)
        db.add(odyssey)
        await db.commit()
        await db.refresh(spiderman)
        await db.refresh(odyssey)
        print(f"Created movies: {spiderman.title}, {odyssey.title}")

        # Create Rooms
        sala1 = Room(name="Sala 1", capacity=50)
        sala2 = Room(name="Sala 2", capacity=50)
        sala3 = Room(name="Sala 3", capacity=50)
        sala5 = Room(name="Sala 5", capacity=50)
        sala6 = Room(name="Sala 6", capacity=50)
        
        db.add_all([sala1, sala2, sala3, sala5, sala6])
        await db.commit()
        
        rooms = [sala1, sala2, sala3, sala5, sala6]
        for room in rooms:
            await db.refresh(room)
            
        print("Created rooms")
        
        # Create Seats for rooms
        seats = []
        for room in rooms:
            for row in ['A', 'B', 'C', 'D', 'E']:
                for num in range(1, 11):
                    seats.append(Seat(room_id=room.id, row_letter=row, seat_number=num))
        
        db.add_all(seats)
        await db.commit()
        print("Created seats")

        # Create Showtimes
        # Base date is today
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        # Homem-Aranha
        st1 = Showtime(movie_id=spiderman.id, room_id=sala1.id, start_time=today + timedelta(hours=20, minutes=35))
        st2 = Showtime(movie_id=spiderman.id, room_id=sala2.id, start_time=today + timedelta(hours=20, minutes=5))
        st3 = Showtime(movie_id=spiderman.id, room_id=sala3.id, start_time=today + timedelta(hours=20, minutes=40))
        
        # A Odisseia
        st4 = Showtime(movie_id=odyssey.id, room_id=sala5.id, start_time=today + timedelta(hours=20, minutes=40))
        st5 = Showtime(movie_id=odyssey.id, room_id=sala6.id, start_time=today + timedelta(hours=20, minutes=30))

        db.add_all([st1, st2, st3, st4, st5])
        await db.commit()
        print("Created showtimes")

if __name__ == "__main__":
    asyncio.run(seed())
