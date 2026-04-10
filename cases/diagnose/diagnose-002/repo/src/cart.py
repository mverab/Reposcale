"""Shopping cart management."""

from dataclasses import dataclass, field


@dataclass
class CartItem:
    product_id: str
    quantity: int
    unit_price: float


@dataclass
class Cart:
    user_id: str
    items: list[CartItem] = field(default_factory=list)

    def add_item(self, product_id: str, quantity: int, unit_price: float):
        for item in self.items:
            if item.product_id == product_id:
                item.quantity += quantity
                return
        self.items.append(CartItem(product_id, quantity, unit_price))

    def remove_item(self, product_id: str):
        self.items = [i for i in self.items if i.product_id != product_id]

    def total(self) -> float:
        return sum(i.quantity * i.unit_price for i in self.items)

    def checkout(self, inventory, payment_client):
        """Validate inventory and initiate payment."""
        for item in self.items:
            if not inventory.check_stock(item.product_id, item.quantity):
                raise ValueError(f"Insufficient stock for {item.product_id}")

        for item in self.items:
            inventory.decrement(item.product_id, item.quantity)

        return payment_client.create_charge(self.user_id, self.total())
