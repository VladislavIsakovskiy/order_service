from decimal import Decimal

from pydantic import BaseModel


class ItemIn(BaseModel):
    name: str
    description: str
    cost: Decimal
    quantity: int
    available: int


class ItemOut(BaseModel):
    item_id: int


class Item(BaseModel):
    item_id: str
    name: str
    description: str
    cost: Decimal
    quantity: int
    available: int

    class Config:
        orm_mode = True
