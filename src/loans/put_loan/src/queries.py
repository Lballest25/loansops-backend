import os
from typing import Optional

from shared.db_config import DatabaseConnection
from shared.decorators.query_reader import sql_query_reader

base_dir = os.path.dirname(os.path.abspath(__file__))


class PutLoanQueries:

    @sql_query_reader(base_dir, "get_loan.sql")
    def get_loan(
        self, loan_id: str, conn: DatabaseConnection
    ) -> Optional[list]:
        query: str = self.get_loan.query
        return conn.execute_query(query, {"loan_id": loan_id})

    def update_loan(self, payload: dict, conn: DatabaseConnection) -> bool:
        updatable = {k: v for k, v in payload.items() if k != "loan_id"}
        set_clause = ", ".join(f"{col} = %({col})s" for col in updatable)
        query = f"""
            UPDATE loans
            SET    {set_clause}
            WHERE  loan_id = %(loan_id)s;
        """
        return conn.execute_update(query, payload)
