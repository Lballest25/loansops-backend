import os
from typing import Optional

from shared.db_config import DatabaseConnection
from shared.decorators.query_reader import sql_query_reader

base_dir = os.path.dirname(os.path.abspath(__file__))


class GetUserQueries:

    @sql_query_reader(base_dir, "get_user.sql")
    def get_user(
        self, user_id: str, conn: DatabaseConnection
    ) -> Optional[list]:
        query: str = self.get_user.query  # type: ignore[attr-defined]
        params = (user_id,)
        return conn.execute_query(query, params)
