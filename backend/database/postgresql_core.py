import os
from typing import AsyncGenerator, Annotated

from fastapi import Depends, FastAPI

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

__all__ = ["DatabaseSession", "get_db", "CustomBase", "lifespan", "Base"]

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(DATABASE_URL)
SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)

Base = declarative_base()


class CustomBase(Base):
    """ Custom base class to add custom methods """
    __abstract__ = True

    def model_dump(self) -> dict:
        """ Method to dump model to dictionary """
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


async def check_db_connection():
    try:
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        print("✅ Successfully connected to database")
    except Exception as e:
        print(f"❌ Failed to connect to database: {e}")


async def lifespan(app: FastAPI):
    await check_db_connection()
    yield
    await engine.dispose()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """ Dependency to get a database session """

    async with SessionLocal() as session:
        yield session


DatabaseSession = Annotated[AsyncSession, Depends(get_db)]
