"""Order API — synchronous notification and report calls block responses."""

from app.models.order import Order, save_order
from app.models.user import get_user
from app.services.notifications import send_order_confirmation
from app.services.reports import generate_daily_report


def create_order(user_id: str, items: list[dict]) -> dict:
    user = get_user(user_id)
    if not user:
        return {"error": "User not found", "status": 404}

    order = Order(user_id=user_id, items=items)
    save_order(order)

    # Blocks response — sends email synchronously
    send_order_confirmation(user["email"], order)

    return {"order_id": order.id, "status": 201}


def get_daily_report(date: str) -> dict:
    # Blocks response — report generation can take 30+ seconds
    report = generate_daily_report(date)
    return {"report": report, "status": 200}
