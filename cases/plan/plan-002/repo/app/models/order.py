"""Order model — in-memory store."""

import uuid
from dataclasses import dataclass, field


@dataclass
class Order:
    user_id: str
    items: list[dict]
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    status: str = "pending"


_orders: dict[str, Order] = {}


def save_order(order: Order):
    _orders[order.id] = order


def get_order(order_id: str) -> Order | None:
    return _orders.get(order_id)


def get_orders_by_date(date: str) -> list[Order]:
    # No date filtering — returns all orders
    return list(_orders.values())
