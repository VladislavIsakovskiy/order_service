# type: ignore[no-untyped-def]
from db import get_session

from fastapi import APIRouter, Depends

from fastapi_pagination import Page, add_pagination, paginate

from sqlalchemy.ext.asyncio import AsyncSession

from order_service.schemas.items import Item, ItemIn, ItemOut, ItemUpdateIn
from order_service.services.item import ItemService

router = APIRouter(
    prefix="/items",
    tags=["items"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=ItemOut)
async def upload_item(item_data: ItemIn, session: AsyncSession = Depends(get_session)):
    new_item = await ItemService(session).create_item(item_data.name, item_data.description, item_data.cost,
                                                      item_data.available)
    return ItemOut.from_orm(new_item)


@router.get("/", response_model=Page[Item])
async def read_items(session: AsyncSession = Depends(get_session)):
    items = await ItemService(session).get_items()
    return paginate([Item.from_orm(item) for item in items])


@router.get("/{item_id}/", response_model=Item)
async def read_item(item_id: int, session: AsyncSession = Depends(get_session)):
    item = await ItemService(session).get_item(item_id)
    return Item.from_orm(item)


@router.put("/{item_id}/", response_model=Item)
async def update_item(item_data: ItemUpdateIn, session: AsyncSession = Depends(get_session)):
    item = await ItemService(session).update_item(item_data.id, item_data.name, item_data.description, item_data.cost,
                                                  item_data.available)
    return Item.from_orm(item)


@router.delete("/{item_id}/", response_model=str)
async def remove_item(item_id: int, session: AsyncSession = Depends(get_session)):
    deleted_item_status_message = await ItemService(session).delete_item(item_id)
    return deleted_item_status_message


add_pagination(router)
