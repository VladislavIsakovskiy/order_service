from typing import List, Optional

from pydantic import BaseModel  # pylint: disable=no-name-in-module
from pydantic.schema import datetime  # pylint: disable=no-name-in-module

from order_service.schemas.items import Item


class OrderIn(BaseModel):  # pylint: disable=too-few-public-methods
    customer_id: Optional[int]
    order_status_code: int
    order_date: datetime
    items: List[Item]


class OrderOut(BaseModel):  # pylint: disable=too-few-public-methods
    order_id: int
    order_date: datetime
    items: List[Item]


class Order(BaseModel):  # pylint: disable=too-few-public-methods
    order_id: int
    customer_id: Optional[int]
    order_status_code: int
    order_date: datetime
    total_amount: int
    items: List[Item]
