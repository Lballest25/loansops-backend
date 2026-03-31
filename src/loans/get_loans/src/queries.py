import os
from typing import Optional

from shared.db_config import DatabaseConnection
from shared.decorators.query_reader import sql_query_reader

base_dir = os.path.dirname(os.path.abspath(__file__))


class GetLoansQueries:

    @sql_query_reader(base_dir, "get_loans.sql")
    def get_loans(
        self,
        user_id: Optional[str],
        status: Optional[str],
        limit: int,
        offset: int,
        conn: DatabaseConnection,
    ) -> Optional[list]:
        query: str = self.get_loans.query
        params = {
            "user_id": user_id,
            "status": status,
            "limit": limit,
            "offset": offset,
        }
        return conn.execute_query(query, params)
