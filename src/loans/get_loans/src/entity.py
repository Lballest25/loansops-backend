from shared.constants import (
    CLIENT_ROLE,
    STATUS_OK,
    STATUS_SERVER_ERROR,
)
from shared.db_config import DatabaseConnection
from src.loans.get_loans.src.queries import GetLoansQueries


class GetLoans:
    def __init__(self, conn: DatabaseConnection, ctx: object):
        self.queries = GetLoansQueries()
        self.conn = conn
        self.session_user = getattr(ctx, "user", {})

    def get_loans(self, query_params: dict) -> tuple:
        """
        Returns a paginated list of loans.
        CLIENTs only see their own loans.

        Supported query params:
            status – filter by loan status
            limit  – max rows, default 50
            offset – pagination offset, default 0
        """
        session_role = self.session_user.get("role")
        session_user_id = self.session_user.get("user_id")

        status = query_params.get("status")
        limit = int(query_params.get("limit", 50))
        offset = int(query_params.get("offset", 0))

        # CLIENTs are restricted to their own loans
        user_id_filter = (
            session_user_id if session_role == CLIENT_ROLE else None
        )

        loans = self.queries.get_loans(
            user_id=user_id_filter,
            status=status,
            limit=limit,
            offset=offset,
            conn=self.conn,
        )

        if loans is None:
            return STATUS_SERVER_ERROR, {
                "message": "An error occurred while fetching loans"
            }

        return STATUS_OK, {"loans": loans, "count": len(loans)}
