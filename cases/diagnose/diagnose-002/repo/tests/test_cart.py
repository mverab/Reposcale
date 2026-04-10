from src.cart import Cart


def test_add_item():
    cart = Cart(user_id="u1")
    cart.add_item("prod-1", 2, 10.0)
    assert len(cart.items) == 1
    assert cart.total() == 20.0


def test_add_same_item_increases_quantity():
    cart = Cart(user_id="u1")
    cart.add_item("prod-1", 1, 5.0)
    cart.add_item("prod-1", 3, 5.0)
    assert cart.items[0].quantity == 4


def test_remove_item():
    cart = Cart(user_id="u1")
    cart.add_item("prod-1", 1, 5.0)
    cart.remove_item("prod-1")
    assert len(cart.items) == 0
