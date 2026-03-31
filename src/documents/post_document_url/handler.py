import json
from typing import Any, Dict

from shared.constants import ALL_ROLES
from shared.decorators.user_permission import user_permission
from shared.decorators.user_session import user_session
from shared.utils import get_response_handler
from src.documents.post_document_url.src.entity import PostDocumentUrl


@user_session
@user_permission(*ALL_ROLES)
def lambda_handler(request: Dict[str, Any], ctx: object) -> Dict[str, Any]:
    loan_id = request["pathParameters"]["loan_id"]
    body: Dict[str, Any] = json.loads(request.get("body", "{}"))
    conn = ctx.conn  # type: ignore[attr-defined]
    use_case = PostDocumentUrl(conn, ctx)
    status_code, response = use_case.generate_upload_url(loan_id, body)
    return get_response_handler(status_code, response)
