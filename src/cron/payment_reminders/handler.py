from typing import Any, Dict

from shared.db_config import DatabaseConnection
from shared.utils import get_response_handler
from src.cron.payment_reminders.src.entity import PaymentReminders


def lambda_handler(
    event: Dict[str, Any], context: object  # pylint: disable=unused-argument
) -> Dict[str, Any]:  # pylint: disable=unused-argument
    """
    Triggered daily by EventBridge (cron).
    Finds loans whose next_payment_date is exactly 7 days away
    and sends email + WhatsApp reminders to each borrower.
    """
    conn = DatabaseConnection()
    use_case = PaymentReminders(conn)
    status_code, response = use_case.run()
    return get_response_handler(status_code, response)
