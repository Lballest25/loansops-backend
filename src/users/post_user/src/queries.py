from typing import Optional

from shared.db_config import DatabaseConnection
from shared.decorators.query_reader import sql_query_reader
import os

base_dir = os.path.dirname(os.path.abspath(__file__))


class PostUserQueries:

    @sql_query_reader(base_dir, "insert_user.sql")
    def insert_user(
        self,
        user_name: str,
        email: str,
        identification: str,
        role: str,
        created_by: str,
        updated_by: str,
        conn: DatabaseConnection,
    ) -> Optional[int]:
        """
        This method will insert a new user into the database.

        args:
            user_name (str): The name of the user.
            email (str): The email of the user.
            identification (str): The identification of the user.
            role (str): The role of the user.
            created_by (str): The user who created the user.
            updated_by (str): The user who updated the user.
            conn (DatabaseConnection): The database connection object.

        Returns:
            int: The id of the newly created user.
            None: If an error occurs
        """
        query: str = self.insert_user.query
        params = {
            "user_name": user_name,
            "email": email,
            "identification": identification,
            "role": role,
            "created_by": created_by,
            "updated_by": updated_by,
        }
        resp = conn.execute_update(query, params)
        return resp

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
        query: str = self.get_user.query
        params = {"email": email}
        resp = conn.execute_query(query, params)
        return resp
