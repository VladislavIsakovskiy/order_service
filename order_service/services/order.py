from datetime import datetime
from typing import List

from models.order import Order, OrderItem

from sqlalchemy.ext.asyncio import AsyncSession

from order_service.schemas.orders import ItemIn
from order_service.services.base import BaseService
from order_service.services.item import ItemService


class OrderService(BaseService):

    def __init__(self, db_session: AsyncSession):
        super().__init__(db_session)
        self.item_service = ItemService(db_session)

    async def create_order(self, customer_id: int, items: List[ItemIn]) -> Order:
        """
        Create new order and return Order object in case of success
        :param customer_id: int
        :param items: List[Item]
        :return: Order
        """
        new_order = await self._create_order_instance(customer_id)
        for item in items:
            await self._create_order_item(new_order.id, item)
        await self.save_transaction()
        return new_order

    async def _create_order_instance(self, customer_id: int) -> Order:
        new_order = Order()
        new_order.customer_id = customer_id
        new_order.status = Order.Statuses.created
        new_order.created_at = datetime.utcnow()
        self.db_session.add(new_order)
        await self.db_session.flush()
        return new_order

    async def _create_order_item(self, order_id: int, item_in: ItemIn):
        new_order_item = OrderItem()
        new_order_item.order_id = order_id
        new_order_item.item_id = item_in.id
        await self.item_service.update_item_availability(item_in.id, item_in.quantity)
        new_order_item.quantity = item_in.quantity
        self.db_session.add(new_order_item)
        await self.db_session.flush()

    async def get_orders(self) -> List[Order]:
        """
        Returns info about all orders that server contains
        :return: List[Order]
        """
        return

    async def get_order(self, order_id: int) -> Order:
        """
        Returns info about particular order
        If order doesn't exist raise APIOrderNotFound exception
        :param order_id: int
        :return: Order
        """
        return

    async def update_order(self, order_id: int) -> Order:
        """
        Update particular order and return message in case of success
        If order does not exist raise APIOrderNotFound exception
        If existed order didn't updated raise APIOrderNotUpdated exception
        :param order_id:  int
        :return: Order
        """
        return

    async def delete_order(self, order_id: int) -> str:
        """
        Delete particular order and return message in case of success
        If order does not exist raise APIOrderNotFound exception
        If existed order didn't deleted raise APIOrderNotDeleted exception
        :param order_id:  int
        :return: str
        """
        return
