from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class ItemIn(BaseModel):
    name: str
    description: str
    cost: Decimal
    available: int


class ItemOut(BaseModel):
    id: int

    class Config:
        orm_mode = True


class Item(BaseModel):
    id: str
    name: str
    description: str
    cost: Decimal
    available: int

    class Config:
        orm_mode = True


class ItemUpdateIn(BaseModel):
    id: int
    name: Optional[str] = None
    description: Optional[str] = None
    cost: Optional[Decimal] = None
    available: Optional[int] = None
