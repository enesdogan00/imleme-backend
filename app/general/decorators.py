from functools import wraps

from starlette_context import context

from app.general.exceptions import PermissionDeniedException


def check_role(*roles: str):
    def decorator_check(func):
        @wraps(func)
        async def wrapper_check(*args, **kwargs):
            if context["role"] not in roles:
                raise PermissionDeniedException
            return await func(*args, **kwargs)

        return wrapper_check

    return decorator_check
