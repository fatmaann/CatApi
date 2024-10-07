from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from db.database import SessionLocal
from db.repository import BreedRepository
from api.shemas import SBreed, SBreedAdd, SBreedId
from typing import Annotated

router = APIRouter(
    prefix="/breed",
    tags=["Breeds"]
)


async def get_session() -> AsyncSession:
    async with SessionLocal() as session:
        yield session


@router.get("")
async def get_all_breeds(session: AsyncSession = Depends(get_session)) -> List[SBreed]:
    breeds = await BreedRepository.get_all_breeds(session)
    return breeds


@router.post("")
async def add_breed(cat: Annotated[SBreedAdd, Depends()], session: AsyncSession = Depends(get_session)) -> SBreedId:
    new_breed_id = await BreedRepository.add_breed(session, cat)
    return {"id": new_breed_id}
