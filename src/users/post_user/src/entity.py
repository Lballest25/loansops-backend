import os
import boto3
import json
from shared.constants import (
    KEYS_USER,
    STATUS_CREATED_SUCCESS,
    STATUS_BAD_REQUEST,
    STATUS_SERVER_ERROR,
)
from src.users.post_user.src.queries import PostUserQueries
from shared.db_config import DatabaseConnection
from dotenv import load_dotenv


class PostUser:
    def __init__(self, conn: DatabaseConnection, ctx: object):
        self.user_queries = PostUserQueries()
        self.conn = conn
        self.ctx = ctx
        self.session_user = getattr(ctx, "user", {})
        load_dotenv()

    def insert_user(self, user_data: dict) -> tuple:
        """
        This method will insert a new user into the database.

        args:
            user_data (dict): The user data to be inserted.

        Returns:
            tuple: The status code and response message.
        """
        current_data = (user_data[key] for key in KEYS_USER)
        user_name, email, role, identification = current_data
        created_by = self.session_user.get("user_id")
        validate_user = self.user_queries.get_user(email=email, conn=self.conn)

        if validate_user:
            return STATUS_BAD_REQUEST, {"message": "User already exists"}

        self.user_queries.insert_user(
            user_name=user_name,
            email=email,
            identification=identification,
            role=role,
            created_by=created_by,
            updated_by=created_by,
            conn=self.conn,
        )
        validate_user = self.user_queries.get_user(email=email, conn=self.conn)

        if not validate_user:
            return STATUS_SERVER_ERROR, {
                "message": "An error occurred while creating the user"
            }

        user_id_created = validate_user[0].get("user_id")

        status, message = self.publish_user_cognito(user_data, user_id_created)

        if status != STATUS_CREATED_SUCCESS:
            return status, message

        return STATUS_CREATED_SUCCESS, {"message": "User created successfully"}

    def publish_user_cognito(self, data: dict, user_id_created: int) -> tuple:
        """
        This method will publish the user data to the cognito lambda function.

        args:
            data (dict): The user data to be published.

        Returns:
            tuple: The status code and response message.
        """
        lambda_client = boto3.client("lambda")
        function_name = os.getenv("FUNCTION_NAME_COGNITO")
        payload = json.dumps(
            {
                "email": data.get("email"),
                "user_name": data.get("user_name"),
                "password": data.get("identification"),
                "user_id": str(user_id_created),
            }
        )

        try:
            response = lambda_client.invoke(
                FunctionName=function_name,
                InvocationType="RequestResponse",
                Payload=json.dumps({"body": payload}),
            )
            response_payload = json.load(response["Payload"])
            return STATUS_CREATED_SUCCESS, response_payload
        except Exception as e:
            return STATUS_SERVER_ERROR, {
                "message": (
                    (
                        "An error occurred while publishing the user data: "
                        f"{str(e)}"
                    )
                )
            }
