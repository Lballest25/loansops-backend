import os
from typing import Optional

from shared.db_config import DatabaseConnection
from shared.decorators.query_reader import sql_query_reader

base_dir = os.path.dirname(os.path.abspath(__file__))


class GetLoanQueries:

    @sql_query_reader(base_dir, "get_loan.sql")
    def get_loan(
        self, loan_id: str, conn: DatabaseConnection
    ) -> Optional[list]:
        query: str = self.get_loan.query
        return conn.execute_query(query, {"loan_id": loan_id})
