import os
from typing import Optional

from shared.db_config import DatabaseConnection
from shared.decorators.query_reader import sql_query_reader

base_dir = os.path.dirname(os.path.abspath(__file__))


class GetDocumentUrlQueries:

    @sql_query_reader(base_dir, "get_document.sql")
    def get_document(
        self, document_id: str, loan_id: str, conn: DatabaseConnection
    ) -> Optional[list]:
        query: str = self.get_document.query
        return conn.execute_query(
            query, {"document_id": document_id, "loan_id": loan_id}
        )
