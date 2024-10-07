from typing import Optional

from pydantic import BaseModel, ConfigDict


class SKittenAdd(BaseModel):
    name: str
    breed_id: int
    color: str
    age_in_months: int
    description: str


class SKittenUpdate(BaseModel):
    name: Optional[str] = None
    breed_id: Optional[int] = None
    color: Optional[str] = None
    age_in_months: Optional[int] = None
    description: Optional[str] = None


class SKitten(SKittenAdd):
    id: int
    model_config = ConfigDict(from_attributes=True)


class SKittenId(BaseModel):
    id: int


class SBreedAdd(BaseModel):
    name: str


class SBreed(SBreedAdd):
    id: int
    model_config = ConfigDict(from_attributes=True)


class SBreedId(BaseModel):
    id: int
