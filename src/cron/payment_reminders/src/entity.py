import logging

from shared.constants import (
    REMINDER_DAYS_BEFORE,
    STATUS_OK,
    STATUS_SERVER_ERROR,
)
from shared.db_config import DatabaseConnection
from shared.utils import send_email, send_whatsapp
from src.cron.payment_reminders.src.queries import PaymentRemindersQueries

logger = logging.getLogger(__name__)

TEMPLATE_PATH = "shared/templates/payment_reminder_email.html"
CURRENCY = "USD"


class PaymentReminders:
    def __init__(self, conn: DatabaseConnection):
        self.queries = PaymentRemindersQueries()
        self.conn = conn

    def run(self) -> tuple:
        """
        Fetches all active loans whose next_payment_date is
        REMINDER_DAYS_BEFORE days from today, then sends
        email + WhatsApp to each borrower.
        """
        loans = self.queries.get_loans_due_soon(
            days_before=REMINDER_DAYS_BEFORE, conn=self.conn
        )

        if loans is None:
            return STATUS_SERVER_ERROR, {
                "message": "Failed to fetch loans for reminders"
            }

        if not loans:
            logger.info(
                "No loans due in %d days. Nothing to send.",
                REMINDER_DAYS_BEFORE,
            )
            return STATUS_OK, {"message": "No reminders to send", "sent": 0}

        sent = 0
        errors = []

        for loan in loans:
            try:
                self._notify(loan)
                sent += 1
            except Exception as exc:  # pylint: disable=broad-except
                logger.error(
                    "Failed to notify loan %s: %s", loan.get("loan_id"), exc
                )
                errors.append(
                    {"loan_id": loan.get("loan_id"), "error": str(exc)}
                )

        return STATUS_OK, {
            "message": (
                f"Reminders processed. Sent: {sent}, " f"Errors: {len(errors)}"
            ),
            "sent": sent,
            "errors": errors,
        }

    def _notify(self, loan: dict) -> None:
        """Send email and WhatsApp notification for a loan reminder."""
        template_data = {
            "user_name": loan["user_name"],
            "days_before": REMINDER_DAYS_BEFORE,
            "currency": CURRENCY,
            "amount": loan["amount"],
            "loan_id": loan["loan_id"],
            "interest_rate": loan["interest_rate"],
            "next_payment_date": str(loan["next_payment_date"]),
            "due_date": str(loan["due_date"]),
        }

        send_email(
            recipients=[loan["email"]],
            subject=f"Recordatorio de pago – {REMINDER_DAYS_BEFORE} días",
            template_path=TEMPLATE_PATH,
            data=template_data,
        )

        if loan.get("phone"):
            whatsapp_body = (
                f"Hola {loan['user_name']}, te recordamos que tienes un pago "
                f"de {CURRENCY} {loan['amount']} programado para el "
                f"{loan['next_payment_date']} "
                f"(en {REMINDER_DAYS_BEFORE} días). "
                f"Préstamo ID: {loan['loan_id']}."
            )
            send_whatsapp(to_number=loan["phone"], body=whatsapp_body)
