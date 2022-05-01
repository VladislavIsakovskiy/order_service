from datetime import datetime
from decimal import Decimal

from db import Base, engine

import sqlalchemy
from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

metadata = sqlalchemy.MetaData()


class Order(Base):
    __tablename__ = "orders"

    class Statuses:
        created = "created"
        processing_fee = "paid"
        processed = "processed"

    id = Column("id", Integer, autoincrement=True, primary_key=True, nullable=False, index=True)
    customer_id = Column(Integer, nullable=False)
    status = Column(String, default=Statuses.created, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    closed_at = Column(DateTime)
    _items = relationship("OrderItem", back_populates="order")

    @hybrid_property
    def items(self):
        return [i for i in self._items]  # noqa

    @hybrid_property
    def total_amount(self):
        total_amount = sum(
            [
                Decimal(order_item.total_item_amount)
                for order_item in self._items
            ]
        )
        return total_amount


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column("id", Integer, autoincrement=True, primary_key=True, nullable=False, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    order = relationship("Order", back_populates="_items", uselist=False)
    item_id = Column(Integer, ForeignKey("items.id"))
    item = relationship("Item", back_populates="order_item", uselist=False)
    quantity = Column(Integer, nullable=False)

    @hybrid_property
    def total_item_amount(self):
        return Decimal(self.item.cost * self.quantity)


class Item(Base):
    __tablename__ = "items"

    id = Column("id", Integer, autoincrement=True, primary_key=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    cost = Column(Numeric(12, 2), nullable=False)
    available = Column("available", Integer, nullable=False)
    order_item = relationship("OrderItem", back_populates="item", uselist=False)


async def init_models():
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)  # Uncomment this if you want to clear existed tables
        await conn.run_sync(Base.metadata.create_all)
