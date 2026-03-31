import json
from typing import Any, Dict

from shared.constants import ADMIN_ROLE
from shared.decorators.user_permission import user_permission
from shared.decorators.user_session import user_session
from shared.utils import get_response_handler
from src.users.put_user.src.entity import PutUser


@user_session
@user_permission(ADMIN_ROLE)
def lambda_handler(request: Dict[str, Any], ctx: object) -> Dict[str, Any]:
    user_id = request["pathParameters"]["user_id"]
    body: Dict[str, Any] = json.loads(request.get("body", "{}"))
    conn = ctx.conn  # type: ignore[attr-defined]
    use_case = PutUser(conn, ctx)
    status_code, response = use_case.update_user(user_id, body)
    return get_response_handler(status_code, response)
