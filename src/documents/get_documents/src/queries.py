import os
from typing import Optional

from shared.db_config import DatabaseConnection
from shared.decorators.query_reader import sql_query_reader

base_dir = os.path.dirname(os.path.abspath(__file__))


class GetDocumentsQueries:

    @sql_query_reader(base_dir, "get_loan.sql")
    def get_loan(
        self, loan_id: str, conn: DatabaseConnection
    ) -> Optional[list]:
        query: str = self.get_loan.query  # type: ignore[attr-defined]
        params = (loan_id,)
        return conn.execute_query(query, params)

    @sql_query_reader(base_dir, "get_documents.sql")
    def get_documents(
        self, loan_id: str, conn: DatabaseConnection
    ) -> Optional[list]:
        query: str = self.get_documents.query  # type: ignore[attr-defined]
        params = (loan_id,)
        return conn.execute_query(query, params)
