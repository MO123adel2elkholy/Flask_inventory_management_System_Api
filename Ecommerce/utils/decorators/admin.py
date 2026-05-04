from functools import wraps

from flask import abort, redirect, request, session, url_for

from Ecommerce.apps.models.inventory_models import User


def get_user_by_id(user_id):
    return User.query.get(user_id)


def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):

        user_session = session.get("user")
        print(f"user session => {user_session} ")

        if not user_session:
            print("Decorator Hits see login")
            return redirect(
                url_for("inventory_auth_api_blueprint.login", next=request.url)
            )

        db_user = get_user_by_id(user_session["id"])

        if not db_user or not db_user.is_admin:
            return abort(403)

        return f(*args, **kwargs)

    return wrapper
