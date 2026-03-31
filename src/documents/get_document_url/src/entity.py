from shared.constants import (
    CLIENT_ROLE,
    STATUS_FORBIDDEN,
    STATUS_NOT_FOUND,
    STATUS_OK,
    STATUS_SERVER_ERROR,
)
from shared.db_config import DatabaseConnection
from shared.utils import generate_presigned_get_url
from src.documents.get_document_url.src.queries import GetDocumentUrlQueries


class GetDocumentUrl:
    def __init__(self, conn: DatabaseConnection, ctx: object):
        self.queries = GetDocumentUrlQueries()
        self.conn = conn
        self.session_user = getattr(ctx, "user", {})

    def generate_download_url(
        self, loan_id: str, document_id: str
    ) -> tuple:
        """
        Validates document ownership, then returns a presigned GET URL.
        CLIENTs can only download documents from their own loans.
        """
        document = self.queries.get_document(
            document_id=document_id, loan_id=loan_id, conn=self.conn
        )

        if document is None:
            return STATUS_SERVER_ERROR, {
                "message": "An error occurred while fetching the document"
            }

        if not document:
            return STATUS_NOT_FOUND, {"message": "Document not found"}

        record = document[0]
        session_role = self.session_user.get("role")
        session_user_id = self.session_user.get("user_id")

        if (
            session_role == CLIENT_ROLE
            and record["uploaded_by"] != session_user_id
        ):
            return STATUS_FORBIDDEN, {
                "message": "Clients can only download their own documents"
            }

        status, result = generate_presigned_get_url(s3_key=record["s3_key"])

        if status != STATUS_OK:
            return status, result

        return STATUS_OK, {
            "document_id": document_id,
            "download_url": result["download_url"],
            "document_type": record["document_type"],
            "expires_in": result["expires_in"],
        }
