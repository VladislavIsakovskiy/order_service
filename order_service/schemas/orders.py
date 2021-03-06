from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel
from pydantic.schema import datetime


class OrderItem(BaseModel):
    id: int
    order_id: int
    item_id: int
    quantity: int
    order_item_amount: Decimal
    closed_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class ItemIn(BaseModel):
    id: int
    quantity: int


class OrderIn(BaseModel):
    customer_id: int
    items: List[ItemIn]


class OrderUpdateIn(BaseModel):
    id: int
    items: List[ItemIn]


class OrderOut(BaseModel):
    id: int
    status: str
    created_at: datetime
    total_amount: Decimal
    items: List[OrderItem]

    class Config:
        orm_mode = True


class Order(BaseModel):
    id: int
    customer_id: int
    status: str
    created_at: datetime
    closed_at: Optional[datetime] = None
    total_amount: Decimal
    items: List[OrderItem]

    class Config:
        orm_mode = True
