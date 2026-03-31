from shared.constants import STATUS_OK, STATUS_SERVER_ERROR
from shared.db_config import DatabaseConnection
from src.users.get_users.src.queries import GetUsersQueries


class GetUsers:
    def __init__(self, conn: DatabaseConnection, ctx: object):
        self.queries = GetUsersQueries()
        self.conn = conn
        self.ctx = ctx

    def get_users(self, query_params: dict) -> tuple:
        """
        Returns a paginated list of users.

        Supported query params:
            role   – filter by role (ADMIN | ANALYST | CLIENT)
            active – filter by is_active (1 | 0), default 1
            limit  – max rows to return, default 50
            offset – pagination offset, default 0
        """
        role = query_params.get("role")
        is_active = query_params.get("active", "1")
        limit = int(query_params.get("limit", 50))
        offset = int(query_params.get("offset", 0))

        users = self.queries.get_users(
            role=role,
            is_active=int(is_active),
            limit=limit,
            offset=offset,
            conn=self.conn,
        )

        if users is None:
            return STATUS_SERVER_ERROR, {
                "message": "An error occurred while fetching users"
            }

        return STATUS_OK, {"users": users, "count": len(users)}
