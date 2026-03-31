import uuid

from shared.constants import (
    DOCUMENT_TYPES,
    STATUS_BAD_REQUEST,
    STATUS_CREATED_SUCCESS,
    STATUS_NOT_FOUND,
    STATUS_SERVER_ERROR,
)
from shared.db_config import DatabaseConnection
from shared.utils import generate_presigned_put_url
from src.documents.post_document_url.src.queries import PostDocumentUrlQueries


class PostDocumentUrl:
    def __init__(self, conn: DatabaseConnection, ctx: object):
        self.queries = PostDocumentUrlQueries()
        self.conn = conn
        self.session_user = getattr(ctx, "user", {})

    def generate_upload_url(self, loan_id: str, body: dict) -> tuple:
        """
        1. Validates loan exists.
        2. Generates a presigned PUT URL — the client uploads directly to S3.
        3. Saves document metadata (s3_key, type, etc.) in MySQL.
        4. Returns the presigned URL + document_id to the client.

        Body params:
            document_type – one of DOCUMENT_TYPES
            file_name     – original file name (used to build the s3_key)
            content_type  – MIME type, e.g. 'application/pdf'
        """
        document_type = body.get("document_type")
        file_name = body.get("file_name")
        content_type = body.get("content_type", "application/octet-stream")

        if not document_type or not file_name:
            return STATUS_BAD_REQUEST, {
                "message": "Fields 'document_type' and 'file_name' are required"
            }

        if document_type not in DOCUMENT_TYPES:
            return STATUS_BAD_REQUEST, {
                "message": f"Invalid document_type. Allowed: {DOCUMENT_TYPES}"
            }

        loan = self.queries.get_loan(loan_id=loan_id, conn=self.conn)
        if loan is None:
            return STATUS_SERVER_ERROR, {
                "message": "An error occurred while validating the loan"
            }
        if not loan:
            return STATUS_NOT_FOUND, {"message": "Loan not found"}

        document_id = str(uuid.uuid4())
        uploaded_by = self.session_user.get("user_id")
        # s3_key pattern: documents/{loan_id}/{document_type}/{document_id}_{file_name}
        s3_key = (
            f"documents/{loan_id}/{document_type}/"
            f"{document_id}_{file_name}"
        )

        status, result = generate_presigned_put_url(
            s3_key=s3_key, content_type=content_type
        )
        if status != STATUS_CREATED_SUCCESS:
            return status, result

        saved = self.queries.insert_document(
            document_id=document_id,
            loan_id=loan_id,
            uploaded_by=uploaded_by,
            s3_key=s3_key,
            document_type=document_type,
            conn=self.conn,
        )

        if not saved:
            return STATUS_SERVER_ERROR, {
                "message": "An error occurred while saving document metadata"
            }

        return STATUS_CREATED_SUCCESS, {
            "document_id": document_id,
            "upload_url": result["upload_url"],
            "s3_key": s3_key,
            "expires_in": result["expires_in"],
        }
