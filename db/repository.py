from typing import Optional, List
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound
from db.database import KittenOrm, BreedOrm


class KittenRepository:
    @classmethod
    async def get_all_cats(cls, session: AsyncSession) -> List[KittenOrm]:
        result = await session.execute(select(KittenOrm))
        cats = result.scalars().all()
        return cats

    @classmethod
    async def get_cats_by_breed(cls, session: AsyncSession, breed_id: int) -> List[KittenOrm]:
        result = await session.execute(
            select(KittenOrm).where(KittenOrm.breed_id == breed_id)
        )
        kittens = result.scalars().all()
        return kittens

    @classmethod
    async def get_cat_details(cls, session: AsyncSession, kitten_id: int) -> Optional[KittenOrm]:
        try:
            result = await session.execute(
                select(KittenOrm).where(KittenOrm.id == kitten_id)
            )
            kitten = result.scalar_one()
            return kitten
        except NoResultFound:
            return None

    @classmethod
    async def add_cat(cls, session: AsyncSession, name: str, breed_id: int, color: str, age_in_months: int,
                      description: str):
        new_kitten = KittenOrm(
            name=name,
            breed_id=breed_id,
            color=color,
            age_in_months=age_in_months,
            description=description
        )
        session.add(new_kitten)
        await session.commit()
        await session.refresh(new_kitten)
        return new_kitten

    @classmethod
    async def update_cat(cls, session: AsyncSession, kitten_id: int, name: Optional[str] = None,
                         breed_id: Optional[int] = None, color: Optional[str] = None,
                         age_in_months: Optional[int] = None, description: Optional[str] = None) -> Optional[KittenOrm]:
        try:
            result = await session.execute(
                select(KittenOrm).where(KittenOrm.id == kitten_id)
            )
            kitten = result.scalar_one()

            if name:
                kitten.name = name
            if breed_id:
                kitten.breed_id = breed_id
            if color:
                kitten.color = color
            if age_in_months:
                kitten.age_in_months = age_in_months
            if description:
                kitten.description = description

            await session.commit()
            await session.refresh(kitten)
            return kitten
        except NoResultFound:
            return None

    @classmethod
    async def delete_cat(cls, session: AsyncSession, kitten_id: int) -> bool:
        try:
            result = await session.execute(
                select(KittenOrm).where(KittenOrm.id == kitten_id)
            )
            kitten = result.scalar_one()
            await session.delete(kitten)
            await session.commit()
            return True
        except NoResultFound:
            return False


class BreedRepository:
    @classmethod
    async def get_all_breeds(cls, session: AsyncSession) -> List[BreedOrm]:
        result = await session.execute(select(BreedOrm))
        breeds = result.scalars().all()
        return breeds
