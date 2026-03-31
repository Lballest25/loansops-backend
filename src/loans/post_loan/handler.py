import json
from typing import Any, Dict

from shared.constants import ADMIN_ROLE, ANALYST_ROLE
from shared.decorators.user_permission import user_permission
from shared.decorators.user_session import user_session
from shared.utils import get_response_handler
from src.loans.post_loan.src.entity import PostLoan


@user_session
@user_permission(ADMIN_ROLE, ANALYST_ROLE)
def lambda_handler(request: Dict[str, Any], ctx: object) -> Dict[str, Any]:
    body: Dict[str, Any] = json.loads(request.get("body", "{}"))
    conn = ctx.conn  # type: ignore[attr-defined]
    use_case = PostLoan(conn, ctx)
    status_code, response = use_case.create_loan(body)
    return get_response_handler(status_code, response)
