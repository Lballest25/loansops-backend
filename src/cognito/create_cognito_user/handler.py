import json
from typing import Any, Dict

from shared.utils import get_response_handler
from src.cognito.create_cognito_user.src.entity import CreateCognitoUser


def lambda_handler(
    event: Dict[str, Any], context: object  # pylint: disable=unused-argument
) -> Dict[str, Any]:  # pylint: disable=unused-argument
    """
    Internal Lambda — invoked by post_user, never exposed via API Gateway.
    Expects event body: { email, user_name, password, user_id }
    """
    body: Dict[str, Any] = json.loads(event.get("body", "{}"))
    use_case = CreateCognitoUser()  # type: ignore
    status_code, response = use_case.create(body)
    return get_response_handler(status_code, response)
