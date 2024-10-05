from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from db.database import SessionLocal, BreedOrm
from db.repository import BreedRepository

router = APIRouter(
    prefix="/breed",
    tags=["breeds"]
)


async def get_session() -> AsyncSession:
    async with SessionLocal() as session:
        yield session


@router.get("")
async def get_all_breeds(session: AsyncSession = Depends(get_session)) -> List[BreedOrm]:
    breeds = await BreedRepository.get_all_breeds(session)
    return breeds
