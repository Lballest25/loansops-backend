import os
from typing import Optional

from shared.db_config import DatabaseConnection
from shared.decorators.query_reader import sql_query_reader

base_dir = os.path.dirname(os.path.abspath(__file__))


class PatchLoanStatusQueries:

    @sql_query_reader(base_dir, "get_loan.sql")
    def get_loan(
        self, loan_id: str, conn: DatabaseConnection
    ) -> Optional[list]:
        query: str = self.get_loan.query  # type: ignore[attr-defined]
        params = (loan_id,)
        return conn.execute_query(query, params)

    @sql_query_reader(base_dir, "patch_loan_status.sql")
    def update_status(
        self,
        loan_id: str,
        status: str,
        updated_by: str,
        conn: DatabaseConnection,
    ) -> bool:
        query: str = self.update_status.query  # type: ignore[attr-defined]
        params = (loan_id, status, updated_by)
        return conn.execute_update(query, params)
