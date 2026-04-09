import os
import random

from ariadne import graphql_sync, load_schema_from_path, make_executable_schema
from flask import jsonify, render_template, request, session
from flask_httpauth import HTTPBasicAuth
from flask_jwt_extended import JWTManager
from werkzeug.security import check_password_hash

from Ecommerce.admin.setup import Create_admin
from Ecommerce.apps import create_app
from Ecommerce.apps.models.inventory_models import User
from Ecommerce.chat import socketio
from Ecommerce.chat.config import CHAT_ROOMS
from Ecommerce.Exceptions import APIException
from Ecommerce.graphql.resolvers.inventory_resover import mutation, product_obj, query
from Ecommerce.Limiter.limiter import init_app, limiter

# Initialize Limiter


# Logging


# Load GraphQL types
type_defs = load_schema_from_path("graphql/types")

# Create Flask app
app = create_app()


# handling Websocket connections


app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

# initialize socket
socketio.init_app(app, cors_allowed_origins="*")


def generate_username():
    return f"Guest{random.randint(1000, 9999)}"


@app.route("/chatt")
def chatt():
    if "username" not in session:
        session["username"] = generate_username()

    return render_template(
        "chatt.html",
        username=session["username"],
        rooms=CHAT_ROOMS,
    )


socketio.run(app, debug=True)
# intialize limiter
init_app(app)


# JWT and Auth
app.config["JWT_SECRET_KEY"] = os.getenv("SECRET_KEY")
jwt = JWTManager(app)
basic_auth = HTTPBasicAuth()


@basic_auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password_hash, password):
        return user
    return None


# Admin setup
Create_admin(app)


# Error handler
@app.errorhandler(APIException)
def handle_api_exception(e):
    return jsonify({"error": str(e)}), getattr(e, "status_code", 500)


# Routes
@app.route("/")
@limiter.limit("10/minute")
def hello():
    return "<h1>Welcome To Flask Development</h1>"


# GraphQL
schema = make_executable_schema(type_defs, query, mutation, product_obj)


@app.route("/graphql", methods=["POST"])
@limiter.limit("10/minute")
def graphql_server():
    data = request.get_json()
    success, result = graphql_sync(schema, data, context_value=request, debug=True)
    return jsonify(result)
