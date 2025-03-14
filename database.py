from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from models.base import Base
from sqlalchemy import text

# Update the default database URL to match your local PostgreSQL settings
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:Pratt1008@localhost:5000/daftaros")

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def init_db():
    try:
        async with engine.begin() as conn:
            # Create tables
            await conn.run_sync(Base.metadata.create_all)
    except Exception as e:
        print(f"Database initialization error: {str(e)}")
        raise

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
