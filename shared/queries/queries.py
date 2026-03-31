from typing import Optional

from shared.db_config import DatabaseConnection
from shared.decorators.query_reader import sql_query_reader
import os

base_dir = os.path.dirname(os.path.abspath(__file__))


class SharedQueries:

    @sql_query_reader(base_dir, "get_user.sql")
    def get_user(self, email: str, conn: DatabaseConnection) -> Optional[dict]:
        """
        This method will get a user from the database.

        args:
            email (str): The email of the user.
            conn (DatabaseConnection): The database connection object.

        Returns:
            dict: The user details if found.
            None: If the user is not found.
        """
        query: str = self.get_user.query  # type: ignore[attr-defined]
        params = (email,)
        resp = conn.execute_query(query, params)
        if resp and len(resp) > 0:
            return resp[0]
        return None
