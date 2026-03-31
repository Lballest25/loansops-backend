from functools import wraps
from shared.constants import STATUS_FORBIDDEN
from shared.utils import get_response_handler


from typing import Callable, Any


def user_permission(*allowed_roles: str) -> Callable[[Any], Callable]:
    """
    Decorator factory that validates the session user's role.

    Usage:
        @user_permission(ADMIN_ROLE)
        @user_permission(ADMIN_ROLE, ANALYST_ROLE)
        @user_permission(*STAFF_ROLES)
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(
            request: Any, context: Any, *args: Any, **kwargs: Any
        ) -> Any:
            session_user = getattr(context, "user", {})
            role = session_user.get("role")

            if role not in allowed_roles:
                return get_response_handler(
                    STATUS_FORBIDDEN,
                    {
                        "message": "User role not allowed "
                        "to access this resource"
                    },
                )

            return func(request, context, *args, **kwargs)

        return wrapper

    return decorator
