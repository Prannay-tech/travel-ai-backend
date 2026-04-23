from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
import redis.asyncio as redis
import os
from dotenv import load_dotenv

load_dotenv()

# PostgreSQL Configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./travel_ai.db")

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

# Redis Configuration for Session & Cache
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

async def get_redis():
    redis_client = redis.from_url(REDIS_URL, decode_responses=True)
    try:
        yield redis_client
    finally:
        await redis_client.aclose()
