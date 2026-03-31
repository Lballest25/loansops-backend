from typing import Any, Dict

from shared.constants import ALL_ROLES
from shared.decorators.user_permission import user_permission
from shared.decorators.user_session import user_session
from shared.utils import get_response_handler
from src.documents.get_document_url.src.entity import GetDocumentUrl


@user_session
@user_permission(*ALL_ROLES)
def lambda_handler(request: Dict[str, Any], ctx: object) -> Dict[str, Any]:
    loan_id = request["pathParameters"]["loan_id"]
    document_id = request["pathParameters"]["document_id"]
    conn = ctx.conn  # type: ignore[attr-defined]
    use_case = GetDocumentUrl(conn, ctx)
    status_code, response = use_case.generate_download_url(
        loan_id, document_id
    )
    return get_response_handler(status_code, response)
