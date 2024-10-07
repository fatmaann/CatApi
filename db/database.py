import os
from sqlalchemy import ForeignKey
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_async_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, autocommit=False, autoflush=False)

Base = declarative_base()


class BreedOrm(Base):
    __tablename__ = 'breeds'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)


class KittenOrm(Base):
    __tablename__ = 'kittens'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(nullable=False)
    breed_id: Mapped[int] = mapped_column(ForeignKey('breeds.id'))
    color: Mapped[str] = mapped_column(nullable=False)
    age_in_months: Mapped[int] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
