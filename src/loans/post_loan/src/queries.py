import os
from typing import Optional

from shared.db_config import DatabaseConnection
from shared.decorators.query_reader import sql_query_reader

base_dir = os.path.dirname(os.path.abspath(__file__))


class PostLoanQueries:

    @sql_query_reader(base_dir, "get_user.sql")
    def get_user(
        self, user_id: str, conn: DatabaseConnection
    ) -> Optional[list]:
        query: str = self.get_user.query
        return conn.execute_query(query, {"user_id": user_id})

    @sql_query_reader(base_dir, "insert_loan.sql")
    def insert_loan(
        self,
        loan_id: str,
        user_id: str,
        amount: float,
        interest_rate: float,
        start_date: str,
        due_date: str,
        next_payment_date: str,
        created_by: str,
        updated_by: str,
        conn: DatabaseConnection,
    ) -> bool:
        query: str = self.insert_loan.query
        params = {
            "loan_id": loan_id,
            "user_id": user_id,
            "amount": amount,
            "interest_rate": interest_rate,
            "start_date": start_date,
            "due_date": due_date,
            "next_payment_date": next_payment_date,
            "created_by": created_by,
            "updated_by": updated_by,
        }
        return conn.execute_update(query, params)

    @sql_query_reader(base_dir, "get_loan.sql")
    def get_loan(
        self, loan_id: str, conn: DatabaseConnection
    ) -> Optional[list]:
        query: str = self.get_loan.query
        return conn.execute_query(query, {"loan_id": loan_id})
