import os
from typing import Optional

from shared.db_config import DatabaseConnection
from shared.decorators.query_reader import sql_query_reader

base_dir = os.path.dirname(os.path.abspath(__file__))


class PostDocumentUrlQueries:

    @sql_query_reader(base_dir, "get_loan.sql")
    def get_loan(
        self, loan_id: str, conn: DatabaseConnection
    ) -> Optional[list]:
        query: str = self.get_loan.query  # type: ignore[attr-defined]
        params = (loan_id,)
        return conn.execute_query(query, params)

    @sql_query_reader(base_dir, "insert_document.sql")
    def insert_document(
        self,
        document_id: str,
        loan_id: str,
        uploaded_by: str,
        s3_key: str,
        document_type: str,
        conn: DatabaseConnection,
    ) -> bool:
        query: str = self.insert_document.query  # type: ignore[attr-defined]
        params = (document_id, loan_id, uploaded_by, s3_key, document_type)
        return conn.execute_update(query, params)
