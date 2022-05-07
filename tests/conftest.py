import asyncio

from db import Base, engine

from httpx import AsyncClient

import pytest

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from order_service.app import order_app


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="module")
async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="module")
async def test_async_client(event_loop):
    async with AsyncClient(app=order_app, base_url="http://testserver") as client:
        yield client


@pytest.fixture(scope="function")
async def temp_session(init_models) -> AsyncSession:
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False, autocommit=False)
    async with async_session() as session:
        yield session


@pytest.fixture()
def item_juice_in():
    return {
        "name": "Juice",
        "description": "Apple juice",
        "cost": 100,
        "available": 30
    }


@pytest.fixture()
def item_juice():
    return {
        "id": 1,
        "name": "Juice",
        "description": "Apple juice",
        "cost": 100,
        "available": 30
    }


@pytest.fixture()
def item_pepsi_in():
    return {
        "name": "Pepsi",
        "description": "Pepsi lemonade",
        "cost": 99,
        "available": 30
    }


@pytest.fixture()
def item_pepsi():
    return {
        "id": 2,
        "name": "Pepsi",
        "description": "pepsi limonade",
        "cost": 45,
        "available": 30
    }


@pytest.fixture()
def item_bounty_in():
    return {
        "name": "Bounty",
        "description": "Coco choco",
        "cost": 33,
        "available": 20
    }
