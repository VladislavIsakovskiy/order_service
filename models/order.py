from datetime import datetime
from decimal import Decimal

from db import Base

import sqlalchemy
from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

metadata = sqlalchemy.MetaData()


class Order(Base):
    __tablename__ = "orders"

    class Statuses:
        created = "created"
        processed = "processed"

    id = Column("id", Integer, autoincrement=True, primary_key=True, nullable=False, index=True)
    customer_id = Column(Integer, nullable=False)
    status = Column(String, default=Statuses.created, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    closed_at = Column(DateTime)
    order_items = relationship("OrderItem", back_populates="order", lazy='selectin')

    @hybrid_property
    def items(self):
        return [i for i in self.order_items]  # noqa

    @hybrid_property
    def total_amount(self):
        total_amount = sum(
            [
                Decimal(order_item.order_item_amount)
                for order_item in self.order_items
            ]
        )
        return total_amount


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column("id", Integer, autoincrement=True, primary_key=True, nullable=False, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    order = relationship("Order", back_populates="order_items", uselist=False)
    item_id = Column(Integer, ForeignKey("items.id"))
    item = relationship("Item", back_populates="order_item", uselist=False, lazy='selectin')
    quantity = Column(Integer, nullable=False)

    @hybrid_property
    def order_item_amount(self):
        return Decimal(self.item.cost * self.quantity)


class Item(Base):
    __tablename__ = "items"

    id = Column("id", Integer, primary_key=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    cost = Column(Numeric(12, 2), nullable=False)
    available = Column("available", Integer, nullable=False)
    order_item = relationship("OrderItem", back_populates="item", uselist=False, lazy='selectin')
