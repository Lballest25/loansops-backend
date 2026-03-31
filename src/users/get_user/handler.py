from typing import Any, Dict

from shared.constants import ALL_ROLES
from shared.decorators.user_permission import user_permission
from shared.decorators.user_session import user_session
from shared.utils import get_response_handler
from src.users.get_user.src.entity import GetUser


@user_session
@user_permission(*ALL_ROLES)
def lambda_handler(request: Dict[str, Any], ctx: object) -> Dict[str, Any]:
    user_id = request["pathParameters"]["user_id"]
    conn = ctx.conn  # type: ignore[attr-defined]
    use_case = GetUser(conn, ctx)
    status_code, response = use_case.get_user(user_id)
    return get_response_handler(status_code, response)
