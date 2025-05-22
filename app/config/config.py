from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData
import os
from dotenv import load_dotenv
from typing import AsyncGenerator

load_dotenv()

DATABASE_URL = f"postgresql+asyncpg://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}" \
               f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

# Create async engine
engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10
)

# Create async session factory
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

metadata = MetaData()

# Dependency to get async session
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session

