from shared.constants import (
    CLIENT_ROLE,
    STATUS_FORBIDDEN,
    STATUS_NOT_FOUND,
    STATUS_OK,
    STATUS_SERVER_ERROR,
)
from shared.db_config import DatabaseConnection
from src.users.get_user.src.queries import GetUserQueries


class GetUser:
    def __init__(self, conn: DatabaseConnection, ctx: object):
        self.queries = GetUserQueries()
        self.conn = conn
        self.session_user = getattr(ctx, "user", {})

    def get_user(self, user_id: str) -> tuple:
        """
        Returns a single user by user_id.
        A CLIENT can only view their own profile.
        """
        session_role = self.session_user.get("role")
        session_user_id = self.session_user.get("user_id")

        if session_role == CLIENT_ROLE and session_user_id != user_id:
            return STATUS_FORBIDDEN, {
                "message": "Clients can only view their own profile"
            }

        user = self.queries.get_user(user_id=user_id, conn=self.conn)

        if user is None:
            return STATUS_SERVER_ERROR, {
                "message": "An error occurred while fetching the user"
            }

        if not user:
            return STATUS_NOT_FOUND, {"message": "User not found"}

        return STATUS_OK, {"user": user[0]}
