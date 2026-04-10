"""Payment processing with webhook handler."""

import logging

logger = logging.getLogger(__name__)


class PaymentClient:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def create_charge(self, user_id: str, amount: float) -> dict:
        # Simulated charge creation
        return {"charge_id": f"ch_{user_id}_{amount}", "status": "pending"}


def handle_webhook(payload: dict):
    """Process payment webhook — silently swallows errors."""
    try:
        event_type = payload["type"]
        charge_id = payload["data"]["charge_id"]

        if event_type == "charge.succeeded":
            logger.info(f"Charge {charge_id} succeeded")
            # TODO: update order status
        elif event_type == "charge.failed":
            logger.info(f"Charge {charge_id} failed")
            # TODO: restore inventory
    except Exception:
        # BUG: silently discards all errors including KeyError, TypeError
        pass
