from functools import wraps
from shared.constants import STATUS_BAD_REQUEST
from shared.db_config import DatabaseConnection
from shared.queries.queries import SharedQueries
from shared.utils import get_response_handler


def user_session(func):
    @wraps(func)
    def wrapper(request, context, *args, **kwargs):
        claims = request["requestContext"]["authorizer"]["claims"]
        email = claims.get("email")

        if not email:
            return get_response_handler(
                STATUS_BAD_REQUEST, {"message": "email missing from claims"}
            )

        conn = DatabaseConnection()
        user_data = SharedQueries().get_user(email, conn)

        if not user_data:
            return get_response_handler(STATUS_BAD_REQUEST, {"message": "User not found"})

        setattr(context, "user", user_data)
        setattr(context, "conn", conn)
        return func(request, context, *args, **kwargs)

    return wrapper
