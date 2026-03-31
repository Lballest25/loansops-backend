import os
from typing import List, Optional

from shared.db_config import DatabaseConnection
from shared.decorators.query_reader import sql_query_reader

base_dir = os.path.dirname(os.path.abspath(__file__))


class GetUsersQueries:

    @sql_query_reader(base_dir, "get_users.sql")
    def get_users(
        self,
        role: Optional[str],
        is_active: int,
        limit: int,
        offset: int,
        conn: DatabaseConnection,
    ) -> Optional[List[dict]]:
        query: str = self.get_users.query
        params = {
            "role": role,
            "is_active": is_active,
            "limit": limit,
            "offset": offset,
        }
        return conn.execute_query(query, params)
