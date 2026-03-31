from shared.constants import (
    LOAN_STATUSES,
    STATUS_BAD_REQUEST,
    STATUS_NOT_FOUND,
    STATUS_OK,
    STATUS_SERVER_ERROR,
)
from shared.db_config import DatabaseConnection
from src.loans.patch_loan_status.src.queries import PatchLoanStatusQueries


class PatchLoanStatus:
    def __init__(self, conn: DatabaseConnection, ctx: object):
        self.queries = PatchLoanStatusQueries()
        self.conn = conn
        self.session_user = getattr(ctx, "user", {})

    def patch_status(self, loan_id: str, body: dict) -> tuple:
        new_status = body.get("status")

        if not new_status:
            return STATUS_BAD_REQUEST, {"message": "Field 'status' is required"}

        if new_status not in LOAN_STATUSES:
            return STATUS_BAD_REQUEST, {
                "message": f"Invalid status. Allowed: {LOAN_STATUSES}"
            }

        existing = self.queries.get_loan(loan_id=loan_id, conn=self.conn)

        if existing is None:
            return STATUS_SERVER_ERROR, {
                "message": "An error occurred while fetching the loan"
            }

        if not existing:
            return STATUS_NOT_FOUND, {"message": "Loan not found"}

        updated_by = self.session_user.get("user_id")
        success = self.queries.update_status(
            loan_id=loan_id,
            status=new_status,
            updated_by=updated_by,
            conn=self.conn,
        )

        if not success:
            return STATUS_SERVER_ERROR, {
                "message": "An error occurred while updating the loan status"
            }

        return STATUS_OK, {"message": f"Loan status updated to '{new_status}'"}
