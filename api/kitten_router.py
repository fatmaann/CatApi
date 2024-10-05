from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from db.database import SessionLocal, KittenOrm
from db.repository import KittenRepository

router = APIRouter(
    prefix="/kitten",
    tags=["kittens"]
)


async def get_session() -> AsyncSession:
    async with SessionLocal() as session:
        yield session


@router.get("")
async def get_all_cats(session: AsyncSession = Depends(get_session)) -> List[KittenOrm]:
    cats = await KittenRepository.get_all_cats(session)
    return cats


@router.get("/breed/{breed_id}", response_model=List[KittenOrm])
async def get_cats_by_breed(breed_id: int, session: AsyncSession = Depends(get_session)):
    cats = await KittenRepository.get_cats_by_breed(session, breed_id)
    return cats


@router.get("/{kitten_id}", response_model=KittenOrm)
async def get_cat_details(kitten_id: int, session: AsyncSession = Depends(get_session)):
    cat = await KittenRepository.get_cat_details(session, kitten_id)
    if cat is None:
        raise HTTPException(status_code=404, detail="Kitten not found")
    return cat


@router.post("")
async def add_cat(
    name: str,
    breed_id: int,
    color: str,
    age_in_months: int,
    description: str,
    session: AsyncSession = Depends(get_session)
) -> KittenOrm:
    new_cat = await KittenRepository.add_cat(
        session,
        name=name,
        breed_id=breed_id,
        color=color,
        age_in_months=age_in_months,
        description=description
    )
    return new_cat


@router.put("/{kitten_id}", response_model=KittenOrm)
async def update_cat(
    kitten_id: int,
    name: Optional[str] = None,
    breed_id: Optional[int] = None,
    color: Optional[str] = None,
    age_in_months: Optional[int] = None,
    description: Optional[str] = None,
    session: AsyncSession = Depends(get_session)
):
    updated_cat = await KittenRepository.update_cat(
        session,
        kitten_id,
        name=name,
        breed_id=breed_id,
        color=color,
        age_in_months=age_in_months,
        description=description
    )
    if updated_cat is None:
        raise HTTPException(status_code=404, detail="Kitten not found")
    return updated_cat


@router.delete("/{kitten_id}", response_model=dict)
async def delete_cat(kitten_id: int, session: AsyncSession = Depends(get_session)):
    success = await KittenRepository.delete_cat(session, kitten_id)
    if not success:
        raise HTTPException(status_code=404, detail="Kitten not found")
    return {"detail": "Kitten deleted successfully"}
