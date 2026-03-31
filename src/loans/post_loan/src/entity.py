import uuid

from shared.constants import (
    STATUS_BAD_REQUEST,
    STATUS_CREATED_SUCCESS,
    STATUS_NOT_FOUND,
    STATUS_SERVER_ERROR,
)
from shared.db_config import DatabaseConnection
from src.loans.post_loan.src.queries import PostLoanQueries

REQUIRED_FIELDS = (
    "user_id",
    "amount",
    "interest_rate",
    "start_date",
    "due_date",
    "next_payment_date",
)


class PostLoan:
    def __init__(self, conn: DatabaseConnection, ctx: object):
        self.queries = PostLoanQueries()
        self.conn = conn
        self.session_user = getattr(ctx, "user", {})

    def create_loan(self, body: dict) -> tuple:
        """
        Validates required fields, verifies the target user exists,
        inserts the loan, and returns the created record.
        """
        missing = [f for f in REQUIRED_FIELDS if f not in body]
        if missing:
            return STATUS_BAD_REQUEST, {
                "message": f"Missing required fields: {missing}"
            }

        user_exists = self.queries.get_user(
            user_id=body["user_id"], conn=self.conn
        )
        if user_exists is None:
            return STATUS_SERVER_ERROR, {
                "message": "An error occurred while validating the user"
            }
        if not user_exists:
            return STATUS_NOT_FOUND, {"message": "User not found"}

        loan_id = str(uuid.uuid4())
        created_by = self.session_user.get("user_id")

        success = self.queries.insert_loan(
            loan_id=loan_id,
            user_id=body["user_id"],
            amount=body["amount"],
            interest_rate=body["interest_rate"],
            start_date=body["start_date"],
            due_date=body["due_date"],
            next_payment_date=body["next_payment_date"],
            created_by=created_by,
            updated_by=created_by,
            conn=self.conn,
        )

        if not success:
            return STATUS_SERVER_ERROR, {
                "message": "An error occurred while creating the loan"
            }

        loan = self.queries.get_loan(loan_id=loan_id, conn=self.conn)

        return STATUS_CREATED_SUCCESS, {
            "message": "Loan created successfully",
            "loan": loan[0] if loan else {},
        }
