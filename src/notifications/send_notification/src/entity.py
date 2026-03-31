from shared.constants import (
    STATUS_BAD_REQUEST,
    STATUS_CREATED_SUCCESS,
    STATUS_NOT_FOUND,
    STATUS_SERVER_ERROR,
)
from shared.db_config import DatabaseConnection
from shared.utils import send_email, send_whatsapp
from src.notifications.send_notification.src.queries import (
    SendNotificationQueries,
)

TEMPLATE_PATH = "shared/templates/notification_email.html"
CHANNELS = ("email", "whatsapp", "both")


class SendNotification:
    def __init__(self, conn: DatabaseConnection, ctx: object):
        self.queries = SendNotificationQueries()
        self.conn = conn

    def send(self, body: dict) -> tuple:
        """
        Sends a manual notification to a user via email, WhatsApp, or both.

        Body params:
            user_id  – target user
            message  – notification text
            subject  – email subject (optional, defaults to 'Notificación LoanOps')
            channel  – 'email' | 'whatsapp' | 'both'  (default 'both')
        """
        user_id = body.get("user_id")
        message = body.get("message")
        subject = body.get("subject", "Notificación – LoanOps")
        channel = body.get("channel", "both")

        if not user_id or not message:
            return STATUS_BAD_REQUEST, {
                "message": "Fields 'user_id' and 'message' are required"
            }

        if channel not in CHANNELS:
            return STATUS_BAD_REQUEST, {
                "message": f"Invalid channel. Allowed: {CHANNELS}"
            }

        user = self.queries.get_user(user_id=user_id, conn=self.conn)

        if user is None:
            return STATUS_SERVER_ERROR, {
                "message": "An error occurred while fetching the user"
            }

        if not user:
            return STATUS_NOT_FOUND, {"message": "User not found"}

        record = user[0]
        results = {}

        if channel in ("email", "both"):
            email_status, email_result = send_email(
                recipients=[record["email"]],
                subject=subject,
                template_path=TEMPLATE_PATH,
                data={
                    "user_name": record["user_name"],
                    "message": message,
                },
            )
            results["email"] = email_result

        if channel in ("whatsapp", "both") and record.get("phone"):
            wa_status, wa_result = send_whatsapp(
                to_number=record["phone"], body=message
            )
            results["whatsapp"] = wa_result

        return STATUS_CREATED_SUCCESS, {
            "message": "Notification sent",
            "results": results,
        }
