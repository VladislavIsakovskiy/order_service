# type: ignore[no-untyped-def]
from typing import List

from fastapi import APIRouter

from order_service.schemas.items import Item, ItemIn
from order_service.services.item import ItemService

router = APIRouter(
    prefix="/items",
    tags=["items"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=Item)
async def upload_item(item_data: ItemIn):
    new_item = await ItemService().create_item(item_data)
    return new_item


@router.get("/", response_model=List[Item])
async def read_items():
    items = await ItemService().get_items()
    return items


@router.get("/{item_id}/", response_model=Item)
async def read_item(item_id: int):
    item = await ItemService().get_item(item_id)
    return item


@router.put("/{item_id}/", response_model=Item)
async def update_order(item_id: int):
    item = await ItemService().update_item(item_id)
    return item


@router.delete("/{item_id}/", response_model=str)
async def delete_order(item_id: int):
    deleted_item_status_message = await ItemService().delete_item(item_id)
    return deleted_item_status_message
