from typing import Any, Dict

from shared.constants import ALL_ROLES
from shared.decorators.user_permission import user_permission
from shared.decorators.user_session import user_session
from shared.utils import get_response_handler
from src.loans.get_loan.src.entity import GetLoan


@user_session
@user_permission(*ALL_ROLES)
def lambda_handler(request: Dict[str, Any], ctx: object) -> Dict[str, Any]:
    loan_id = request["pathParameters"]["loan_id"]
    conn = ctx.conn  # type: ignore[attr-defined]
    use_case = GetLoan(conn, ctx)
    status_code, response = use_case.get_loan(loan_id)
    return get_response_handler(status_code, response)
