from decimal import Decimal
from typing import List

from pydantic import BaseModel
from pydantic.schema import datetime


class OrderItem(BaseModel):
    id: int
    order_id: int
    item_id: int
    quantity: int
    order_item_amount: Decimal
    closed_at: datetime

    class Config:
        orm_mode = True


class OrderIn(BaseModel):
    customer_id: int
    status: str
    created_at: datetime
    closed_at: datetime
    items: List[OrderItem]


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
    closed_at: datetime
    total_amount: Decimal
    items: List[OrderItem]

    class Config:
        orm_mode = True
