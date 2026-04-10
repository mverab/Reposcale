"""Inventory management — non-atomic stock operations."""

_stock: dict[str, int] = {}


def load_stock(data: dict[str, int]):
    global _stock
    _stock = dict(data)


def check_stock(product_id: str, quantity: int) -> bool:
    return _stock.get(product_id, 0) >= quantity


def decrement(product_id: str, quantity: int):
    # BUG: not atomic — race condition under concurrent access
    current = _stock.get(product_id, 0)
    _stock[product_id] = current - quantity


def get_stock(product_id: str) -> int:
    return _stock.get(product_id, 0)
