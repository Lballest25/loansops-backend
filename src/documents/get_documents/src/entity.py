from shared.constants import (
    CLIENT_ROLE,
    STATUS_FORBIDDEN,
    STATUS_NOT_FOUND,
    STATUS_OK,
    STATUS_SERVER_ERROR,
)
from shared.db_config import DatabaseConnection
from src.documents.get_documents.src.queries import GetDocumentsQueries


class GetDocuments:
    def __init__(self, conn: DatabaseConnection, ctx: object):
        self.queries = GetDocumentsQueries()
        self.conn = conn
        self.session_user = getattr(ctx, "user", {})

    def get_documents(self, loan_id: str) -> tuple:
        """
        Returns all documents for a loan.
        CLIENTs can only list documents from their own loans.
        """
        loan = self.queries.get_loan(loan_id=loan_id, conn=self.conn)

        if loan is None:
            return STATUS_SERVER_ERROR, {
                "message": "An error occurred while fetching the loan"
            }

        if not loan:
            return STATUS_NOT_FOUND, {"message": "Loan not found"}

        session_role = self.session_user.get("role")
        session_user_id = self.session_user.get("user_id")

        if (
            session_role == CLIENT_ROLE
            and loan[0]["user_id"] != session_user_id
        ):
            return STATUS_FORBIDDEN, {
                "message": "Clients can only view documents from their own loans"
            }

        documents = self.queries.get_documents(
            loan_id=loan_id, conn=self.conn
        )

        if documents is None:
            return STATUS_SERVER_ERROR, {
                "message": "An error occurred while fetching documents"
            }

        return STATUS_OK, {"documents": documents, "count": len(documents)}
