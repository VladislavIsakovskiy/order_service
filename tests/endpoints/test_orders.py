import json
from datetime import datetime, timedelta

from models.order import Item, Order

import pytest


@pytest.mark.asyncio
async def test_create_order_success(temp_session, test_async_client, item_juice_in, item_pepsi_in, item_bounty_in):
    await test_async_client.post("/v1/items/", json=item_juice_in)
    await test_async_client.post("/v1/items/", json=item_pepsi_in)
    await test_async_client.post("/v1/items/", json=item_bounty_in)
    new_order = {
        "customer_id": 1,
        "items": [
            {
                "id": 1,
                "quantity": 3
            },
            {
                "id": 2,
                "quantity": 2
            }
        ]
    }

    response = await test_async_client.post("/v1/orders/", json=new_order)
    assert response.status_code == 200

    new_order = await temp_session.get(ident=1, entity=Order)
    assert new_order.customer_id == 1
    assert new_order.status == "created"
    assert new_order.total_amount == 498
    assert ((datetime.utcnow() - timedelta(minutes=1)) < new_order.created_at < datetime.utcnow())
    assert len(new_order.items) == 2
    juice_item = await temp_session.get(ident=1, entity=Item)
    assert juice_item.available == 27
    pepsi_item = await temp_session.get(ident=2, entity=Item)
    assert pepsi_item.available == 28


@pytest.mark.asyncio
async def test_create_order_exceeded_quantity_raise_exception(temp_session, test_async_client):
    order_with_incorrect_item_quantity = {
        "customer_id": 1,
        "items": [
            {
                "id": 1,
                "quantity": 0
            }
        ]
    }
    response = await test_async_client.post("/v1/orders/", json=order_with_incorrect_item_quantity)
    assert response.status_code == 422
    assert json.loads(response.content)["message"] == "Quantity for Item with id 1 should be greater than 0."

    order_with_exceeded_item_quantity = {
        "customer_id": 1,
        "items": [
            {
                "id": 1,
                "quantity": 999
            }
        ]
    }
    response = await test_async_client.post("/v1/orders/", json=order_with_exceeded_item_quantity)
    assert response.status_code == 422
    assert json.loads(response.content)["message"] == "There are only 27 available Items with id 1."


@pytest.mark.asyncio
async def test_create_order_wrong_item_id_raise_exception(temp_session, test_async_client):
    incorrect_order = {
        "customer_id": 1,
        "items": [
            {
                "id": 999,
                "quantity": 12
            }
        ]
    }
    response = await test_async_client.post("/v1/orders/", json=incorrect_order)
    assert response.status_code == 422
    assert json.loads(response.content)["message"] == "Item with id 999 does not exist."


@pytest.mark.asyncio
async def test_get_orders_success(temp_session, test_async_client):
    response = await test_async_client.get("/v1/orders/")
    assert response.status_code == 200
    assert len(json.loads(response.content)["items"]) == 1
    order = json.loads(response.content)["items"][0]
    assert order["id"] == 1
    assert order["customer_id"] == 1
    assert order["status"] == "created"
    assert order["total_amount"] == 498
    assert len(order["items"]) == 2


@pytest.mark.asyncio
async def test_get_order_success(temp_session, test_async_client):
    response = await test_async_client.get("/v1/orders/1/")
    assert response.status_code == 200
    order = json.loads(response.content)
    assert order["id"] == 1
    assert order["customer_id"] == 1
    assert order["status"] == "created"
    assert order["total_amount"] == 498
    assert len(order["items"]) == 2


@pytest.mark.asyncio
async def test_get_order_with_wrong_id_raise_exception(temp_session, test_async_client):
    response = await test_async_client.get("/v1/orders/999/")
    assert response.status_code == 422
    assert json.loads(response.content)["message"] == "Order with id 999 does not exist."


@pytest.mark.asyncio
async def test_update_order_success(temp_session, test_async_client):
    order = {
        "id": 1,
        "items": [
            {
                "id": 1,
                "quantity": 1
            },
            {
                "id": 2,
                "quantity": 4
            },
            {
                "id": 3,
                "quantity": 3
            }
        ]
    }

    response = await test_async_client.put("/v1/orders/1/", json=order)
    assert response.status_code == 200

    new_order = await temp_session.get(ident=1, entity=Order)
    assert new_order.customer_id == 1
    assert new_order.status == "created"
    assert new_order.total_amount == 595
    assert ((datetime.utcnow() - timedelta(seconds=5)) < new_order.created_at < datetime.utcnow())
    assert len(new_order.items) == 3
    juice_item = await temp_session.get(ident=1, entity=Item)
    assert juice_item.available == 29
    pepsi_item = await temp_session.get(ident=2, entity=Item)
    assert pepsi_item.available == 26
    bounty_item = await temp_session.get(ident=3, entity=Item)
    assert bounty_item.available == 17


@pytest.mark.asyncio
async def test_delete_order_success(temp_session, test_async_client):
    response = await test_async_client.delete("/v1/orders/1/")
    assert response.status_code == 200
    assert json.loads(response.content) == "Order with id 1 successfully deleted."
