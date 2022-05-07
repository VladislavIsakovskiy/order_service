# type: ignore[no-untyped-def]
from db import get_session

from fastapi import APIRouter, Depends

from fastapi_pagination import Page, add_pagination, paginate

from sqlalchemy.ext.asyncio import AsyncSession

from order_service.schemas.orders import Order, OrderIn, OrderOut, OrderUpdateIn
from order_service.services.order import OrderService

router = APIRouter(
    prefix="/orders",
    tags=["orders"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=OrderOut)
async def upload_order(order_data: OrderIn, session: AsyncSession = Depends(get_session)):
    new_order = await OrderService(session).create_order(order_data.customer_id, order_data.items)
    return OrderOut.from_orm(new_order)


@router.get("/", response_model=Page[Order])
async def read_orders(session: AsyncSession = Depends(get_session)):
    orders = await OrderService(session).get_orders()
    return paginate([Order.from_orm(order) for order in orders])


@router.get("/{order_id}/", response_model=Order)
async def read_order(order_id: int, session: AsyncSession = Depends(get_session)):
    order = await OrderService(session).get_order(order_id)
    return Order.from_orm(order)


@router.put("/{order_id}/", response_model=Order)
async def update_order(order_data: OrderUpdateIn, session: AsyncSession = Depends(get_session)):
    order = await OrderService(session).update_order(order_data.id, order_data.items)
    return Order.from_orm(order)


@router.delete("/{order_id}/", response_model=str)
async def delete_order(order_id: int, session: AsyncSession = Depends(get_session)):
    deleted_order_status_message = await OrderService(session).delete_order(order_id)
    return deleted_order_status_message


add_pagination(router)
