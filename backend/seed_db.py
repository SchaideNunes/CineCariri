import asyncio
from datetime import datetime, timedelta
from app.db.session import AsyncSessionLocal
from app.models.movie import Movie
from app.models.showtime import Room, Showtime
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
            poster_url="/Assets/Homem%20aranha.webp"
        )
        odyssey = Movie(
            title="A Odisseia",
            duration_mins=172,
            genre="Ação, Aventura, Épico, Fantasia",
            poster_url="/Assets/Odysseia.webp"
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

        # Base date is today
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        # Homem-Aranha
        st1 = Showtime(movie_id=spiderman.id, room_id=sala1.id, start_time=today + timedelta(hours=20, minutes=35), format="2D", audio="DUB")
        st2 = Showtime(movie_id=spiderman.id, room_id=sala2.id, start_time=today + timedelta(hours=20, minutes=5), format="3D", audio="DUB")
        st3 = Showtime(movie_id=spiderman.id, room_id=sala3.id, start_time=today + timedelta(hours=20, minutes=40), format="2D", audio="LEG")
        
        # A Odisseia
        st4 = Showtime(movie_id=odyssey.id, room_id=sala5.id, start_time=today + timedelta(hours=20, minutes=40), format="2D", audio="LEG")
        st5 = Showtime(movie_id=odyssey.id, room_id=sala6.id, start_time=today + timedelta(hours=20, minutes=30), format="2D", audio="DUB")

        db.add_all([st1, st2, st3, st4, st5])
        await db.commit()
        print("Created showtimes")

if __name__ == "__main__":
    asyncio.run(seed())
