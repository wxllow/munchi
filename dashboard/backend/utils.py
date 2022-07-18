from functools import wraps

from sanic.exceptions import Unauthorized


def with_token(func):
    @wraps(func)
    async def wrapper(request, *args, **kwargs):
        token = request.args.get("token")

        if not token:
            raise Unauthorized("No token provided")

        return await func(request, *args, **kwargs, token=token)

    return wrapper
