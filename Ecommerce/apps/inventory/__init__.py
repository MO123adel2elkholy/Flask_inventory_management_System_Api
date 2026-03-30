# Run pip install flask-blueprint
from flask import Blueprint

inventory_category_api_blueprint = Blueprint(
    "inventory_category_api_blueprint", __name__
)

inventory_prodcut_api_blueprint = Blueprint("inventory_prodcut_api_blueprint", __name__)


inventory_user_api_blueprint = Blueprint("inventory_user_api_blueprint", __name__)

from .router import category, user  # noqa: F401
