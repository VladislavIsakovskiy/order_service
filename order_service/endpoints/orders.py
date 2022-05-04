# type: ignore[no-untyped-def]
from db import get_session

from fastapi import APIRouter, Depends

from fastapi_pagination import Page

from sqlalchemy.ext.asyncio import AsyncSession

from order_service.schemas.orders import Order, OrderIn, OrderOut
from order_service.services.order import OrderService

router = APIRouter(
    prefix="/orders",
    tags=["orders"],
    responses={404: {"description": "Not found"}},
)


@router.post("/{order_id}/", response_model=OrderOut)
async def upload_order(order_data: OrderIn, session: AsyncSession = Depends(get_session)):
    new_order = await OrderService(session).create_order(order_data.customer_id, order_data.items)
    return OrderOut.from_orm(new_order)


@router.get("/", response_model=Page[Order])
async def read_orders():
    orders = await OrderService().get_orders()
    return orders


@router.get("/{order_id}/", response_model=Order)
async def read_order(order_id: int):
    order = await OrderService().get_order(order_id)
    return order


@router.put("/{order_id}/", response_model=Order)
async def update_order(order_id: int):
    order = await OrderService().update_order(order_id)
    return order


@router.delete("/{order_id}/", response_model=str)
async def delete_order(order_id: int):
    deleted_order_status_message = await OrderService().delete_order(order_id)
    return deleted_order_status_message
