from functools import wraps
from typing import Any, Union

from sanic import json
from sanic.exceptions import Unauthorized


def with_token(func):
    @wraps(func)
    async def wrapper(request, *args, **kwargs):
        token = request.args.get("token")

        if not token:
            raise Unauthorized("No token provided")

        return await func(request, *args, **kwargs, token=token)

    return wrapper


def _jsonable(v: Any = None):
    if isinstance(v, dict):
        f = {}

        for x, y in v.items():
            f[x] = _jsonable(y)

        return f
    elif isinstance(v, list) or isinstance(v, tuple) or isinstance(v, set):
        return [_jsonable(x) for x in v]

    if isinstance(v, int):
        if v > (2 ^ 53 - 1):
            return str(v)

    return v


def jsonify(data: Union[list, dict] = {}):
    """JSONify a dict"""
    jsonified = type(data)()

    if isinstance(data, dict):
        for k, v in data.items():
            jsonified[k] = _jsonable(v)
    else:
        for i in data:
            jsonified.append(_jsonable(i))

    return json(jsonified)
