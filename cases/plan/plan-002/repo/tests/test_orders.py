from app.models.user import create_user
from app.api.orders import create_order


def test_create_order():
    user = create_user("Alice", "alice@test.com")
    result = create_order(user["id"], [{"name": "Widget", "price": 10, "quantity": 2}])
    assert result["status"] == 201
    assert "order_id" in result
