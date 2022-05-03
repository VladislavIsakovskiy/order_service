from decimal import Decimal
from typing import List, Optional

from models.order import Item

from sqlalchemy.future import select

from order_service.errors import EntityNotFoundError, ItemAlreadyExistsError, NoOneFieldWereSpecifiedForUpdate, \
    WrongCostOrAvailableFieldsFormat
from order_service.services.base import BaseService


class ItemService(BaseService):
    async def create_item(self, name: str, description: str, cost: Decimal, available: int) -> Item:
        """
        Create new item and return ItemOut object in case of success
        If item with similar name already exists raise ItemAlreadyExistsError
        :param name: str
        :param description: str
        :param cost: Decimal
        :param available: int
        :return: ItemOut
        """
        existed_item = await self._get_item_by_name(name)
        if existed_item:
            raise ItemAlreadyExistsError(name)
        await self._check_item_fields(cost, available)
        new_item = Item(name=name,
                        description=description,
                        cost=cost,
                        available=available
                        )
        self.db_session.add(new_item)
        await self.save_transaction()
        return new_item

    async def _get_item_by_name(self, name: str) -> Item:
        item_result = await self.db_session.execute(select(Item).where(Item.name == name))
        item = item_result.scalars().first()
        return item

    async def get_items(self) -> List[Item]:
        """
        Returns info about all items that server contains
        :return: List[Item]
        """
        items = await self.db_session.execute(select(Item))
        return items.scalars().all()

    async def _get_item_by_id(self, item_id: int) -> Item:
        item_query = await self.db_session.execute(select(Item).where(Item.id == item_id))
        item = item_query.scalars().first()
        if not item:
            raise EntityNotFoundError(Item.__name__, item_id)
        return item

    async def get_item(self, item_id: int) -> Item:
        """
        Returns info about particular item
        If order doesn't exist raise EntityNotFoundError
        :param item_id: int
        :return: Item
        """
        item = await self._get_item_by_id(item_id)
        return item

    async def update_item(self, item_id: int, name: Optional[str], description: Optional[str], cost: Optional[Decimal],
                          available: Optional[int]) -> Item:
        """
        Update particular item and return message in case of success
        If item does not exist raise EntityNotFoundError exception
        :param item_id:  int
        :param name:  str
        :param description:  str
        :param cost:  Decimal
        :param available:  int
        :return: Item
        """
        if not any([name, description, cost, available]):
            raise NoOneFieldWereSpecifiedForUpdate(Item.__name__, item_id)
        await self._check_item_fields(cost, available)
        item = await self._get_item_by_id(item_id)
        item = await self._update_item_fields(item, name, description, cost, available)
        await self.save_transaction()
        return item

    @staticmethod
    async def _check_item_fields(cost: Optional[Decimal], available: Optional[int]):
        if (cost <= 0) or (available <= 0):
            raise WrongCostOrAvailableFieldsFormat

    @staticmethod
    async def _update_item_fields(item: Item, name: Optional[str], description: Optional[str],
                                  cost: Optional[Decimal],
                                  available: Optional[int]) -> Item:
        if name:
            item.name = name
        if description:
            item.description = description
        if cost:
            item.cost = cost
        if available:
            item.available = available
        return item

    async def delete_item(self, item_id: int) -> str:
        """
        Delete particular item and return message in case of success
        If item does not exist raise APIItemNotFound exception
        If existed item didn't deleted raise APIItemNotDeleted exception
        :param item_id:  int
        :return: str
        """
        item = await self._get_item_by_id(item_id)
        await self.db_session.delete(item)
        await self.save_transaction()
        return f"Item with id {item_id} successfully deleted."
