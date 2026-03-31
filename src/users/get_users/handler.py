from typing import Any, Dict

from shared.constants import ADMIN_ROLE, ANALYST_ROLE
from shared.decorators.user_permission import user_permission
from shared.decorators.user_session import user_session
from shared.utils import get_response_handler
from src.users.get_users.src.entity import GetUsers


@user_session
@user_permission(ADMIN_ROLE, ANALYST_ROLE)
def lambda_handler(request: Dict[str, Any], ctx: object) -> Dict[str, Any]:
    query_params = request.get("queryStringParameters") or {}
    conn = ctx.conn  # type: ignore[attr-defined]
    use_case = GetUsers(conn, ctx)
    status_code, response = use_case.get_users(query_params)
    return get_response_handler(status_code, response)
