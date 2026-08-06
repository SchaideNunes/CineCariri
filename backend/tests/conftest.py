import pytest
from httpx import AsyncClient, ASGITransport
import asyncio
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import NullPool

from app.main import app
from app.db.base import Base
from app.models.user import User
from app.core.config import settings
from app.db.session import get_db

# Use NullPool for testing so connections are cleanly closed
test_engine = create_async_engine(settings.DATABASE_URL, poolclass=NullPool)
TestingSessionLocal = async_sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)

async def override_get_db():
    async with TestingSessionLocal() as session:
        yield session

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="session", autouse=True)
async def setup_db():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await test_engine.dispose()

@pytest.fixture(scope="function")
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

from app.core.security import create_access_token

@pytest.fixture(scope="function")
async def normal_user_token_headers(client: AsyncClient, setup_db) -> dict:
    # First, register a user
    email = "testuser@example.com"
    password = "password123"
    
    # Check if user already exists via login
    login_response = await client.post(
        "/api/users/login",
        data={"username": email, "password": password}
    )
    if login_response.status_code != 200:
        await client.post(
            "/api/users/register",
            json={"email": email, "password": password}
        )
        login_response = await client.post(
            "/api/users/login",
            data={"username": email, "password": password}
        )
    
    token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture(scope="function")
async def admin_token_headers(client: AsyncClient, setup_db) -> dict:
    from app.models.user import User
    from app.core.security import get_password_hash
    from sqlalchemy.future import select
    
    async with TestingSessionLocal() as session:
        result = await session.execute(select(User).filter(User.email == "admin@example.com"))
        admin_user = result.scalars().first()
        if not admin_user:
            admin_user = User(
                email="admin@example.com",
                hashed_password=get_password_hash("adminpassword"),
                is_admin=True,
                is_active=True
            )
            session.add(admin_user)
            await session.commit()
            await session.refresh(admin_user)
        user_id = str(admin_user.id)
    
    token = create_access_token(data={"sub": user_id})
    return {"Authorization": f"Bearer {token}"}
