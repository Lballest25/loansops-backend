import os
from typing import Optional

from shared.db_config import DatabaseConnection
from shared.decorators.query_reader import sql_query_reader

base_dir = os.path.dirname(os.path.abspath(__file__))


class PutUserQueries:

    @sql_query_reader(base_dir, "get_user.sql")
    def get_user(
        self, user_id: str, conn: DatabaseConnection
    ) -> Optional[list]:
        query: str = self.get_user.query  # type: ignore[attr-defined]
        params = (user_id,)
        return conn.execute_query(query, params)

    def update_user(self, payload: dict, conn: DatabaseConnection) -> bool:
        """
        Builds the SET clause dynamically from payload keys,
        excluding 'user_id' and 'updated_by' which are used in WHERE/SET.
        """
        updatable = {k: v for k, v in payload.items() if k not in ("user_id",)}
        set_clause = ", ".join(f"{col} = %s" for col in updatable)
        query = f"""
            UPDATE users
            SET    {set_clause}
            WHERE  user_id = %s
              AND  is_active = 1;
        """
        params = tuple(updatable.values()) + (payload["user_id"],)
        return conn.execute_update(query, params)
