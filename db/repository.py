from typing import Optional, List
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import KittenOrm, BreedOrm
from api.shemas import SKitten, SKittenId, SKittenAdd, SKittenUpdate, SBreed, SBreedId, SBreedAdd


class KittenRepository:
    @classmethod
    async def get_all_kittens(cls, session: AsyncSession) -> List[SKitten]:
        result = await session.execute(select(KittenOrm))
        kittens = [SKitten.model_validate(model) for model in result.scalars().all()]
        return kittens

    @classmethod
    async def get_kittens_by_breed(cls, breed_id: SBreedId, session: AsyncSession) -> List[SKitten]:
        query = select(KittenOrm).where(KittenOrm.breed_id == breed_id.id)
        result = await session.execute(query)
        kittens = [SKitten.model_validate(model) for model in result.scalars().all()]
        return kittens

    @classmethod
    async def get_kittens_by_id(cls, kitten_id: SKittenId, session: AsyncSession) -> List[SKitten]:
        query = select(KittenOrm).where(KittenOrm.id == kitten_id.id)
        result = await session.execute(query)
        kittens = [SKitten.model_validate(model) for model in result.scalars().all()]
        return kittens

    @classmethod
    async def add_kitten(cls, session: AsyncSession, new_kitten: SKittenAdd) -> int:
        new_kitten_dict = new_kitten.model_dump()
        kitten = KittenOrm(**new_kitten_dict)
        session.add(kitten)
        await session.commit()
        await session.refresh(kitten)
        return kitten.id

    @classmethod
    async def add_kitten_description(cls, kitten_id: SKittenId, extra_description: str,
                                     session: AsyncSession, ) -> Optional[SKittenId]:
        result = await session.execute(select(KittenOrm.description).where(KittenOrm.id == kitten_id.id))
        current_description = result.scalar()

        if current_description is None:
            return None

        new_description = current_description + " " + extra_description
        await session.execute(
            update(KittenOrm)
            .where(KittenOrm.id == kitten_id.id)
            .values(description=new_description)
        )
        await session.commit()
        return kitten_id

    @classmethod
    async def update_kitten_data(cls, kitten_id: SKittenId, updated_data: SKittenUpdate,
                                 session: AsyncSession) -> Optional[int]:
        updated_kitten_dict = updated_data.model_dump(exclude_unset=True)
        updated_kitten_dict = {k: v for k, v in updated_kitten_dict.items() if v is not None}
        result = await session.execute(
            update(KittenOrm)
            .where(KittenOrm.id == kitten_id.id)
            .values(**updated_kitten_dict)
            .returning(KittenOrm.id)
        )

        await session.commit()
        updated_kitten_id = result.scalar_one_or_none()
        return updated_kitten_id

    @classmethod
    async def delete_kitten(cls, kitten_id: SKittenId, session: AsyncSession) -> Optional[int]:
        result = await session.execute(delete(KittenOrm).where(KittenOrm.id == kitten_id.id).returning(KittenOrm.id))
        deleted_kitten_id = result.scalar()
        if not deleted_kitten_id:
            return None
        await session.commit()
        return deleted_kitten_id


class BreedRepository:
    @classmethod
    async def get_all_breeds(cls, session: AsyncSession) -> List[SBreed]:
        result = await session.execute(select(BreedOrm))
        breeds = [SBreed.model_validate(model) for model in result.scalars().all()]
        return breeds

    @classmethod
    async def add_breed(cls, session: AsyncSession, new_breed: SBreedAdd) -> int:
        new_breed_dict = new_breed.model_dump()
        breed = BreedOrm(**new_breed_dict)
        session.add(breed)
        await session.commit()
        await session.refresh(breed)
        return breed.id
