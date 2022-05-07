import json

from models.order import Item

import pytest


@pytest.mark.asyncio
async def test_create_items_success(temp_session, test_async_client, item_juice_in, item_pepsi_in):
    response = await test_async_client.post("/v1/items/", json=item_juice_in)
    assert response.status_code == 200

    item_juice_item = await temp_session.get(ident=1, entity=Item)
    assert item_juice_item.name == item_juice_in["name"]
    assert item_juice_item.description == item_juice_in["description"]
    assert item_juice_item.cost == item_juice_in["cost"]
    assert item_juice_item.available == item_juice_in["available"]

    response = await test_async_client.post("/v1/items/", json=item_pepsi_in)
    assert response.status_code == 200
    item_pepsi_item = await temp_session.get(ident=2, entity=Item)
    assert item_pepsi_item.name == item_pepsi_in["name"]
    assert item_pepsi_item.description == item_pepsi_in["description"]
    assert item_pepsi_item.cost == item_pepsi_in["cost"]
    assert item_pepsi_item.available == item_pepsi_in["available"]


@pytest.mark.asyncio
async def test_create_item_with_similar_item_raise_exception(temp_session, test_async_client):
    similar_juice = {
        "name": "Juice",
        "description": "Apple juice",
        "cost": 120,
        "available": 30
    }
    response = await test_async_client.post("/v1/items/", json=similar_juice)
    assert response.status_code == 409
    assert json.loads(response.content)["message"] == f"Item with name {similar_juice['name']} already exists."


@pytest.mark.asyncio
async def test_create_items_incorrect_cost_available_raise_exception(temp_session, test_async_client):
    incorrect_juice = {
        "name": "Another Juice",
        "description": "Apple juice",
        "cost": 0,
        "available": 30
    }
    incorrect_pepsi = {
        "name": "Another Pepsi",
        "description": "pepsi limonade",
        "cost": 150,
        "available": -1
    }
    response = await test_async_client.post("/v1/items/", json=incorrect_juice)
    assert response.status_code == 422
    assert json.loads(response.content)["message"] == "Cost for Item should be greater than 0."
    response = await test_async_client.post("/v1/items/", json=incorrect_pepsi)
    assert response.status_code == 422
    assert json.loads(response.content)["message"] == "Available for Item should be greater than 0."


@pytest.mark.asyncio
async def test_update_item_success(temp_session, test_async_client, item_pepsi):
    response = await test_async_client.put("/v1/items/2/", json=item_pepsi)
    assert response.status_code == 200
    pepsi_item = await temp_session.get(ident=2, entity=Item)
    assert pepsi_item.name == item_pepsi["name"]
    assert pepsi_item.description == item_pepsi["description"]
    assert pepsi_item.cost == item_pepsi["cost"]
    assert pepsi_item.available == item_pepsi["available"]


@pytest.mark.asyncio
async def test_update_item_with_non_specified_fields_raise_exception(temp_session, test_async_client):
    incorrect_pepsi = {
        "id": 2
    }
    response = await test_async_client.put("/v1/items/2/", json=incorrect_pepsi)
    assert response.status_code == 422
    assert json.loads(response.content)["message"] == "No one field were specified for update Item with id 2."


@pytest.mark.asyncio
async def test_get_items_success(temp_session, test_async_client, item_juice, item_pepsi):
    expected_result = {
        "items": [item_juice, item_pepsi],
        "total": 2,
        "page": 1,
        "size": 50
    }
    response = await test_async_client.get("/v1/items/")
    assert response.status_code == 200
    assert json.loads(response.content) == expected_result


@pytest.mark.asyncio
async def test_get_item_success(temp_session, test_async_client):
    expected_result = {
        "id": 1,
        "name": "Juice",
        "description": "Apple juice",
        "cost": 100,
        "available": 30
    }
    response = await test_async_client.get("/v1/items/1/")
    assert response.status_code == 200
    assert json.loads(response.content) == expected_result


@pytest.mark.asyncio
async def test_get_non_existed_item_raise_exception(temp_session, test_async_client):
    response = await test_async_client.get("/v1/items/999/")
    assert response.status_code == 422
    assert json.loads(response.content)["message"] == "Item with id 999 does not exist."


@pytest.mark.asyncio
async def test_delete_item_success(temp_session, test_async_client):
    response = await test_async_client.delete("/v1/items/2/")
    assert response.status_code == 200
    assert json.loads(response.content) == "Item with id 2 successfully deleted."


@pytest.mark.asyncio
async def test_delete_non_existed_item_raise_exception(temp_session, test_async_client):
    response = await test_async_client.delete("/v1/items/2/")
    assert response.status_code == 422
    assert json.loads(response.content)["message"] == "Item with id 2 does not exist."
