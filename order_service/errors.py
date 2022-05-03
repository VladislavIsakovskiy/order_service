class APIError(Exception):
    status_code: int = None  # type: ignore
    message: str = None  # type: ignore

    def __init__(self, message: str = None):
        super().__init__(message)
        if message:
            self.message = message


class ItemAlreadyExistsError(APIError):
    status_code = 409

    def __init__(self, item_name: str):
        super().__init__(f"Item with {item_name} already exists.")


class EntityNotFoundError(APIError):
    status_code = 422

    def __init__(self, object_type: str, object_id: int):
        super().__init__(f"{object_type} with id {object_id} does not exist.")


class WrongCostOrAvailableFieldsFormat(APIError):
    status_code = 422

    def __init__(self):  # type: ignore
        super().__init__("Cost and Available for Item should be more than 0.")


class NoOneFieldWereSpecifiedForUpdate(APIError):
    status_code = 422

    def __init__(self, object_type: str, object_id: int):
        super().__init__(f"No one field were specified for update {object_type} with id {object_id}.")


class APIOrderNotFound(APIError):
    status_code = 422

    def __init__(self, order_name: str):
        super().__init__(f"There is not order {order_name} at server.")


class APIOrderNotDeleted(APIError):
    status_code = 422

    def __init__(self, order_name: str):
        super().__init__(f"Something went wrong with deleting {order_name} order.")
