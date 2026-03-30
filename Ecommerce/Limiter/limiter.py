from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from .config import DEFAULT_LIMITS, REDIS_URI

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=DEFAULT_LIMITS,
    storage_uri=REDIS_URI,  # Redis storage لو multi-server
)


def init_app(app):
    """
    Function to initialize limiter with Flask app
    """
    limiter.init_app(app)
    return limiter
