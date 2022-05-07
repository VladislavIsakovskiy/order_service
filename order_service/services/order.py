from datetime import datetime
from typing import List

from logger_config import logger

from models.order import Order, OrderItem

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from order_service.errors import EntityNotFoundError, WrongQuantityError
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
        :param items: List[ItemIn]
        :return: Order
        """
        new_order = await self._create_order_instance(customer_id)
        for item in items:
            await self._check_item_quantity(item.id, item.quantity)
            await self._create_order_item(new_order.id, item)
        await self.save_transaction()
        result_order_query = await self.db_session.execute(
            select(Order).where(Order.id == new_order.id))
        result_order = result_order_query.scalars().first()
        return result_order

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
        orders = await self.db_session.execute(select(Order))
        return orders.scalars().all()

    async def get_order(self, order_id: int) -> Order:
        """
        Returns info about particular order
        If order doesn't exist raise EntityNotFoundError
        :param order_id: int
        :return: Order
        """
        order = await self._get_order_by_id(order_id)
        return order

    async def _get_order_by_id(self, order_id: int) -> Order:
        order_query = await self.db_session.execute(select(Order).where(Order.id == order_id))
        order = order_query.scalars().first()
        if not order:
            raise EntityNotFoundError(Order.__name__, order_id)
        return order

    async def update_order(self, order_id: int, items: List[ItemIn]) -> Order:
        """
        Update particular order and return Order object in case of success
        If order doesn't exist raise EntityNotFoundError
        :param order_id: int
        :param items: List[ItemIn]
        :return: Order
        """
        for item in items:
            await self._check_item_quantity(item.id, item.quantity)
        order = await self._get_order_by_id(order_id)
        order_items_for_delete = await self._get_order_items_for_delete(order.items, items)
        order_items_for_update = await self._get_order_items_for_update(order.items, items)
        new_items = await self._get_new_item_ids(order.items, items)
        await self._delete_order_items(order_items_for_delete, order.status)
        for order_item_id, quantity_difference in order_items_for_update.items():
            await self._update_order_item(order_item_id, quantity_difference)
        for new_item in new_items:
            await self._create_order_item(order_id, new_item)
        await self.save_transaction()
        await self.db_session.refresh(order)
        return order

    async def _check_item_quantity(self, item_id: int, quantity: int):
        if quantity <= 0:
            raise WrongQuantityError(item_id)

    async def _get_order_items_for_delete(self, order_items: List[OrderItem], items: List[ItemIn]) -> List[OrderItem]:
        current_item_ids = {item.id for item in items}
        items_for_delete = []
        for order_item in order_items:
            if order_item.item_id not in current_item_ids:
                items_for_delete.append(order_item)
        return items_for_delete

    async def _get_order_items_for_update(self, order_items: List[OrderItem], items: List[ItemIn]) -> dict:
        current_items = {item.id: item.quantity for item in items}
        items_for_update = {}
        for last_item in order_items:
            order_item_id = last_item.id
            item_id = last_item.item_id
            last_quantity = last_item.quantity
            if (item_id in current_items.keys()) and (last_quantity != current_items[item_id]):
                new_quantity = current_items[item_id]
                quantity_difference = new_quantity - last_quantity
                items_for_update[order_item_id] = quantity_difference
        return items_for_update

    async def _get_new_item_ids(self, last_items: List[OrderItem], items_in: List[ItemIn]) -> List[ItemIn]:
        last_item_ids = {order_item.item_id for order_item in last_items}
        new_items = []
        for item in items_in:
            if item.id not in last_item_ids:
                new_items.append(item)
        return new_items

    async def _get_order_item_by_id(self, order_item_id: int) -> OrderItem:
        order_item_query = await self.db_session.execute(select(OrderItem).where(OrderItem.id == order_item_id))
        order_item = order_item_query.scalars().first()
        if not order_item:
            raise EntityNotFoundError(OrderItem.__name__, order_item_id)
        return order_item

    async def _delete_order_items(self, order_items: List[OrderItem], order_status: str):
        for order_item in order_items:
            await self._delete_order_item(order_item.id, order_status)

    async def _delete_order_item(self, order_item_id: int, order_status: str):
        order_item = await self._get_order_item_by_id(order_item_id)
        if order_status != Order.Statuses.processed:
            quantity_difference = - order_item.quantity
            await self.item_service.update_item_availability(order_item.item_id, quantity_difference)
        await self.db_session.delete(order_item)
        await self.db_session.flush()
        logger.info(f"OrderItem with id {order_item} successfully deleted.")

    async def _update_order_item(self, order_item_id: int, quantity_difference: int):
        order_item = await self._get_order_item_by_id(order_item_id)
        await self.item_service.update_item_availability(order_item.item_id, quantity_difference)
        order_item.quantity = order_item.quantity + quantity_difference
        self.db_session.add(order_item)
        await self.db_session.flush()

    async def delete_order(self, order_id: int) -> str:
        """
        Delete particular order and return message in case of success
        If order doesn't exist raise EntityNotFoundError
        :param order_id:  int
        :return: str
        """
        order = await self._get_order_by_id(order_id)
        for order_item in order.items:
            await self._delete_order_item(order_item.id, order.status)
        await self.db_session.delete(order)
        await self.save_transaction()
        return f"Order with id {order_id} successfully deleted."
