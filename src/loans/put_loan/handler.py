import json
from typing import Any, Dict

from shared.constants import ADMIN_ROLE, ANALYST_ROLE
from shared.decorators.user_permission import user_permission
from shared.decorators.user_session import user_session
from shared.utils import get_response_handler
from src.loans.put_loan.src.entity import PutLoan


@user_session
@user_permission(ADMIN_ROLE, ANALYST_ROLE)
def lambda_handler(request: Dict[str, Any], ctx: object) -> Dict[str, Any]:
    loan_id = request["pathParameters"]["loan_id"]
    body: Dict[str, Any] = json.loads(request.get("body", "{}"))
    conn = ctx.conn  # type: ignore[attr-defined]
    use_case = PutLoan(conn, ctx)
    status_code, response = use_case.update_loan(loan_id, body)
    return get_response_handler(status_code, response)
