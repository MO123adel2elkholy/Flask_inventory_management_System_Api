from redis import Redis

redis_client = Redis(host="localhost", port=6379, decode_responses=True)


def rate_limit(key, limit, window=60):
    """
    key: unique identifier (user/IP + resolver name)
    limit: max requests
    window: time in seconds
    """
    current = redis_client.get(key)

    if current is None:
        redis_client.set(key, 1, ex=window)
        return True

    if int(current) < limit:
        redis_client.incr(key)
        return True

    return False
