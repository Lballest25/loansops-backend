from shared.constants import (
    CLIENT_ROLE,
    STATUS_FORBIDDEN,
    STATUS_NOT_FOUND,
    STATUS_OK,
    STATUS_SERVER_ERROR,
)
from shared.db_config import DatabaseConnection
from src.loans.get_loan.src.queries import GetLoanQueries


class GetLoan:
    def __init__(self, conn: DatabaseConnection, ctx: object):
        self.queries = GetLoanQueries()
        self.conn = conn
        self.session_user = getattr(ctx, "user", {})

    def get_loan(self, loan_id: str) -> tuple:
        """
        Returns a single loan.
        CLIENTs can only view loans that belong to them.
        """
        loan = self.queries.get_loan(loan_id=loan_id, conn=self.conn)

        if loan is None:
            return STATUS_SERVER_ERROR, {
                "message": "An error occurred while fetching the loan"
            }

        if not loan:
            return STATUS_NOT_FOUND, {"message": "Loan not found"}

        record = loan[0]
        session_role = self.session_user.get("role")
        session_user_id = self.session_user.get("user_id")

        if (
            session_role == CLIENT_ROLE
            and record["user_id"] != session_user_id
        ):
            return STATUS_FORBIDDEN, {
                "message": "Clients can only view their own loans"
            }

        return STATUS_OK, {"loan": record}
