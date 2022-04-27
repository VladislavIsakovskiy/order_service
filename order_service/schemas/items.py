from typing import Optional

from pydantic import BaseModel  # pylint: disable=no-name-in-module


class ItemIn(BaseModel):  # pylint: disable=too-few-public-methods
    name: str
    description: str
    price: int
    quantity: int
    upc: Optional[int]


class ItemOut(BaseModel):  # pylint: disable=too-few-public-methods
    order_id: int


class Item(BaseModel):  # pylint: disable=too-few-public-methods
    item_id: str
    name: str
    description: str
    price: int
    quantity: int
    upc: Optional[int]
