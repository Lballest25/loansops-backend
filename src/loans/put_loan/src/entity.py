from shared.constants import (
    STATUS_BAD_REQUEST,
    STATUS_NOT_FOUND,
    STATUS_OK,
    STATUS_SERVER_ERROR,
)
from shared.db_config import DatabaseConnection
from src.loans.put_loan.src.queries import PutLoanQueries

UPDATABLE_FIELDS = {
    "amount",
    "interest_rate",
    "start_date",
    "due_date",
    "next_payment_date",
}


class PutLoan:
    def __init__(self, conn: DatabaseConnection, ctx: object):
        self.queries = PutLoanQueries()
        self.conn = conn
        self.session_user = getattr(ctx, "user", {})

    def update_loan(self, loan_id: str, body: dict) -> tuple:
        payload = {k: v for k, v in body.items() if k in UPDATABLE_FIELDS}

        if not payload:
            return STATUS_BAD_REQUEST, {
                "message": "No valid fields provided for update"
            }

        existing = self.queries.get_loan(loan_id=loan_id, conn=self.conn)

        if existing is None:
            return STATUS_SERVER_ERROR, {
                "message": "An error occurred while fetching the loan"
            }

        if not existing:
            return STATUS_NOT_FOUND, {"message": "Loan not found"}

        payload["updated_by"] = self.session_user.get("user_id")
        payload["loan_id"] = loan_id

        success = self.queries.update_loan(payload=payload, conn=self.conn)

        if not success:
            return STATUS_SERVER_ERROR, {
                "message": "An error occurred while updating the loan"
            }

        return STATUS_OK, {"message": "Loan updated successfully"}
