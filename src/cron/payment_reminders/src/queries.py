import os
from typing import Optional

from shared.db_config import DatabaseConnection
from shared.decorators.query_reader import sql_query_reader

base_dir = os.path.dirname(os.path.abspath(__file__))


class PaymentRemindersQueries:

    @sql_query_reader(base_dir, "get_loans_due_soon.sql")
    def get_loans_due_soon(
        self, days_before: int, conn: DatabaseConnection
    ) -> Optional[list]:
        query: str = (
            self.get_loans_due_soon.query  # type: ignore[attr-defined]
        )
        params = (days_before,)
        return conn.execute_query(query, params)
