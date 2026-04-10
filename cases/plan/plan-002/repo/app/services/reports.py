"""Report generation — expensive synchronous computation."""

from app.models.order import get_orders_by_date


def generate_daily_report(date: str) -> dict:
    """Generate daily summary — scans all orders, no caching."""
    orders = get_orders_by_date(date)

    total_revenue = 0
    item_counts: dict[str, int] = {}

    for order in orders:
        for item in order.items:
            price = item.get("price", 0) * item.get("quantity", 1)
            total_revenue += price
            name = item.get("name", "unknown")
            item_counts[name] = item_counts.get(name, 0) + item.get("quantity", 1)

    return {
        "date": date,
        "total_orders": len(orders),
        "total_revenue": total_revenue,
        "top_items": sorted(item_counts.items(), key=lambda x: -x[1])[:10],
    }
