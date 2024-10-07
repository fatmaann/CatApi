from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from db.database import SessionLocal
from db.repository import KittenRepository
from api.shemas import SKitten, SKittenAdd, SKittenUpdate, SKittenId, SBreedId
from typing import Annotated

router = APIRouter(
    prefix="/kitten",
    tags=["Kittens"]
)


async def get_session() -> AsyncSession:
    async with SessionLocal() as session:
        yield session


@router.get("")
async def get_all_kittens(session: AsyncSession = Depends(get_session)) -> List[SKitten]:
    kittens = await KittenRepository.get_all_kittens(session)
    return kittens


@router.get("/breed_id")
async def get_cats_by_breed(breed_id: Annotated[SBreedId, Depends()],
                            session: AsyncSession = Depends(get_session)) -> List[SKitten]:
    kittens = await KittenRepository.get_kittens_by_breed(breed_id, session)
    return kittens


@router.get("/kitten_id")
async def get_cat_details(kitten_id: Annotated[SKittenId, Depends()],
                          session: AsyncSession = Depends(get_session)) -> List[SKitten]:
    kittens = await KittenRepository.get_kittens_by_id(kitten_id, session)
    return kittens


@router.post("")
async def add_kitten(kitten: Annotated[SKittenAdd, Depends()],
                     session: AsyncSession = Depends(get_session)) -> SKittenId:
    new_cat_id = await KittenRepository.add_kitten(session, kitten)
    return {"id": new_cat_id}


@router.put("/add_desc")
async def add_kitten_description(kitten_id: Annotated[SKittenId, Depends()], description: str,
                                 session: AsyncSession = Depends(get_session)) -> SKittenId:
    updated_desc_id = await KittenRepository.add_kitten_description(kitten_id, description, session)
    if updated_desc_id:
        return updated_desc_id
    raise HTTPException(status_code=404, detail="Kitten not found")


@router.put("/update_data")
async def update_kitten(kitten_id: Annotated[SKittenId, Depends()], updated_data: Annotated[SKittenUpdate, Depends()],
                        session: AsyncSession = Depends(get_session)) -> SKittenId:
    updated_kitten = await KittenRepository.update_kitten_data(kitten_id, updated_data, session)
    if updated_kitten:
        return {"id": updated_kitten}
    raise HTTPException(status_code=500, detail="Internal server error")


@router.delete("/kitten_id")
async def delete_kitten(kitten_id: Annotated[SKittenId, Depends()],
                        session: AsyncSession = Depends(get_session)) -> SKittenId:
    deleted_kitten_id = await KittenRepository.delete_kitten(kitten_id, session)
    if deleted_kitten_id:
        return {"id": deleted_kitten_id}
    raise HTTPException(status_code=404, detail="Kitten not found")
