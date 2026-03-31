from shared.constants import (
    STATUS_BAD_REQUEST,
    STATUS_NOT_FOUND,
    STATUS_OK,
    STATUS_SERVER_ERROR,
)
from shared.db_config import DatabaseConnection
from src.users.put_user.src.queries import PutUserQueries

UPDATABLE_FIELDS = {"user_name", "identification", "role", "is_active"}


class PutUser:
    def __init__(self, conn: DatabaseConnection, ctx: object):
        self.queries = PutUserQueries()
        self.conn = conn
        self.session_user = getattr(ctx, "user", {})

    def update_user(self, user_id: str, body: dict) -> tuple:
        """
        Updates allowed fields of a user.
        Only fields present in UPDATABLE_FIELDS are applied.
        """
        payload = {k: v for k, v in body.items() if k in UPDATABLE_FIELDS}

        if not payload:
            return STATUS_BAD_REQUEST, {
                "message": "No valid fields provided for update"
            }

        existing = self.queries.get_user(user_id=user_id, conn=self.conn)

        if existing is None:
            return STATUS_SERVER_ERROR, {
                "message": "An error occurred while fetching the user"
            }

        if not existing:
            return STATUS_NOT_FOUND, {"message": "User not found"}

        payload["updated_by"] = self.session_user.get("user_id")
        payload["user_id"] = user_id

        success = self.queries.update_user(payload=payload, conn=self.conn)

        if not success:
            return STATUS_SERVER_ERROR, {
                "message": "An error occurred while updating the user"
            }

        return STATUS_OK, {"message": "User updated successfully"}
