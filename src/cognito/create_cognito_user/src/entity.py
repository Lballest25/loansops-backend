import os
import logging

import boto3
from botocore.exceptions import ClientError

from shared.constants import (
    STATUS_BAD_REQUEST,
    STATUS_CREATED_SUCCESS,
    STATUS_SERVER_ERROR,
)

logger = logging.getLogger(__name__)


class CreateCognitoUser:
    def __init__(self):
        self.client = boto3.client("cognito-idp")
        self.user_pool_id = os.environ["COGNITO_USER_POOL_ID"]

    def create(self, body: dict) -> tuple:
        """
        Creates a user in Cognito User Pool with a permanent password.
        Sets 'custom:user_id' attribute so downstream services can
        map Cognito sub → internal user_id.

        Body params:
            email     – user email (also the Cognito username)
            user_name – display name
            password  – temporary/permanent password
            user_id   – internal UUID from the users table
        """
        email = body.get("email")
        user_name = body.get("user_name")
        password = body.get("password")
        user_id = body.get("user_id")

        if not all([email, user_name, password, user_id]):
            return STATUS_BAD_REQUEST, {
                "message": "Fields 'email', 'user_name', 'password', 'user_id' are required"
            }

        try:
            self.client.admin_create_user(
                UserPoolId=self.user_pool_id,
                Username=email,
                TemporaryPassword=password,
                MessageAction="SUPPRESS",
                UserAttributes=[
                    {"Name": "email", "Value": email},
                    {"Name": "email_verified", "Value": "true"},
                    {"Name": "name", "Value": user_name},
                    {"Name": "custom:user_id", "Value": str(user_id)},
                ],
            )

            self.client.admin_set_user_password(
                UserPoolId=self.user_pool_id,
                Username=email,
                Password=password,
                Permanent=True,
            )

            logger.info("Cognito user created for email: %s", email)
            return STATUS_CREATED_SUCCESS, {
                "message": "Cognito user created successfully"
            }

        except self.client.exceptions.UsernameExistsException:
            return STATUS_BAD_REQUEST, {
                "message": "A Cognito user with this email already exists"
            }
        except ClientError as exc:
            logger.error("Cognito error: %s", exc)
            return STATUS_SERVER_ERROR, {"message": str(exc)}
