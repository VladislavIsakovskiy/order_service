from typing import List

from order_service.schemas.items import Item, ItemIn


class ItemService:
    async def create_item(self, item_data: ItemIn) -> str:
        """
        Create new item and return message in case of success
        :param item_data: ItemIn
        :return: str
        """
        return

    async def get_items(self) -> List[Item]:
        """
        Returns info about all items that server contains
        :return: List[Item]
        """
        return

    async def get_item(self, item_id: int) -> Item:
        """
        Returns info about particular item
        If order doesn't exist raise APIItemNotFound exception
        :param item_id: int
        :return: Item
        """
        return

    async def update_item(self, item_id: int) -> Item:
        """
        Update particular item and return message in case of success
        If item does not exist raise APIItemNotFound exception
        If existed order didn't updated raise APIItemNotUpdated exception
        :param item_id:  int
        :return: Item
        """
        return

    async def delete_item(self, item_id: int) -> str:
        """
        Delete particular item and return message in case of success
        If item does not exist raise APIItemNotFound exception
        If existed item didn't deleted raise APIItemNotDeleted exception
        :param item_id:  int
        :return: str
        """
        return
