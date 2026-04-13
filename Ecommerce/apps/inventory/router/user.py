from apifairy import body, response
from flask import request

# filepath: e:\YouTubeDownloads\Downloads\Video\Flask_Course\Master_Flask_api\Ecommerce\apps\inventory\routes.py
from flask.json import jsonify

# Add these imports for authentication
from flask_httpauth import HTTPBasicAuth
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from werkzeug.security import check_password_hash, generate_password_hash

from Ecommerce.apps import database as db
from Ecommerce.apps.models.inventory_models import User
from Ecommerce.apps.schema.new_schema import UserSchemaAuto
from Ecommerce.tasks.models_Email_notification import send_email_task
from Ecommerce.utils.token import generate_token

# from Ecommerce.Exceptions import APIException
from .. import inventory_user_api_blueprint

# ...existing code...

# Move Basic auth setup here for the blueprint
basic_auth = HTTPBasicAuth()


@basic_auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        return user
    return None


# ...existing code...


# Add authentication routes to the blueprint
@inventory_user_api_blueprint.route("/login/basic", methods=["GET"])
@basic_auth.login_required
def basic_login():
    user = basic_auth.current_user()
    return jsonify({"message": f"Logged in as {user.username}"})


@inventory_user_api_blueprint.route("/login/jwt", methods=["POST"])
def jwt_login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token)
    return jsonify({"error": "Invalid credentials"}), 401


@inventory_user_api_blueprint.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify({"message": f"Hello, {current_user}"})


# ...existing code...


@inventory_user_api_blueprint.route("/user", methods=["POST"])
@body(UserSchemaAuto(many=False))
@response(UserSchemaAuto(many=False))
def create_user(data):
    data = request.get_json()
    print("user data =>", data)
    password = data["password"]
    username = data["username"]
    email = data["email"]
    hashed_password = generate_password_hash(password)
    user = User()
    user.email = email
    user.username = username
    user.password = hashed_password
    db.session.add(user)
    db.session.commit()
    db.session.refresh(user)
    token = generate_token(email=email)
    send_email_task.delay(
        subject="Email verivication",
        recipients=[email],
        body=f"http://127.0.0.1:5000/api/verify-email/{token}",
    )
    return user
