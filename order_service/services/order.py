from typing import List

from order_service.schemas.orders import Order, OrderIn


class OrderService:
    async def create_order(self, order_data: OrderIn) -> str:
        """
        Create new order and return message in case of success
        :param order_data: OrderIn
        :return: str
        """
        return

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
