"""Notification service — synchronous, blocks caller."""

import time


def send_order_confirmation(email: str, order):
    """Send order confirmation email — simulates 2-5 second SMTP call."""
    # In production this blocks the request handler
    time.sleep(0)  # Simulated — real latency is 2-5 seconds
    print(f"[NOTIFY] Order {order.id} confirmation sent to {email}")
    return True


def send_shipping_update(email: str, order_id: str, status: str):
    time.sleep(0)
    print(f"[NOTIFY] Shipping update for {order_id}: {status}")
    return True
