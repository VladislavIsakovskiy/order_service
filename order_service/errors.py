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
        super().__init__(f"Item with name {item_name} already exists.")


class EntityNotFoundError(APIError):
    status_code = 422

    def __init__(self, object_type: str, object_id: int):
        super().__init__(f"{object_type} with id {object_id} does not exist.")


class WrongAmountError(APIError):
    status_code = 422

    def __init__(self, object_type: str, field_name: str):  # type: ignore
        super().__init__(f"{field_name} for {object_type} should be greater than 0.")


class WrongQuantityError(APIError):
    status_code = 422

    def __init__(self, object_id: int):  # type: ignore
        super().__init__(f"Quantity for Item with id {object_id} should be greater than 0.")


class NoOneFieldWereSpecifiedForUpdate(APIError):
    status_code = 422

    def __init__(self, object_type: str, object_id: int):
        super().__init__(f"No one field were specified for update {object_type} with id {object_id}.")


class ItemQuantityMoreThanAvailable(APIError):
    status_code = 422

    def __init__(self, item_id: int, available: int):
        super().__init__(f"There are only {available} available Items with id {item_id}.")
