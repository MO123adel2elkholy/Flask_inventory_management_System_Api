from functools import wraps

from flask import request
from flask_jwt_extended import get_jwt_identity
from graphql import GraphQLError

from .graphql_limiter import rate_limit


def graphql_rate_limit(limit=5, window=60):  # five requse per Second
    def decorator(func):
        @wraps(func)
        def wrapper(obj, info, **kwargs):
            try:
                user = get_jwt_identity()  # getting user IP address
            except:
                user = request.remote_addr  # getting user Ip

            key = f"rate_limit:{user}:{func.__name__}"

            if not rate_limit(key, limit, window):
                extensions = {
                    "code": "RATE_LIMIT_EXCEEDED",
                    "retry_after": f"  {window // 60} Minutes",
                    "limit": limit,
                }
                raise GraphQLError(
                    message="Too many requests. Please try again later.",
                    extensions=extensions,
                )
            # mo
            return func(obj, info, **kwargs)

        return wrapper

    return decorator


print("hello")
