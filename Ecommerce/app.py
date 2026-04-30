import os
import random

from ariadne import graphql_sync, load_schema_from_path, make_executable_schema
from dotenv import load_dotenv
from flask import jsonify, render_template, request, session
from flask_httpauth import HTTPBasicAuth
from flask_jwt_extended import JWTManager
from werkzeug.security import check_password_hash

from Ecommerce.apps import cache, create_app
from Ecommerce.apps.models.inventory_models import User
from Ecommerce.chat import socketio
from Ecommerce.chat.config import CHAT_ROOMS
from Ecommerce.Exceptions import APIException
from Ecommerce.graphql.resolvers.inventory_resover import mutation, product_obj, query
from Ecommerce.Limiter.limiter import init_app, limiter

load_dotenv()

# Load GraphQL types
type_defs = load_schema_from_path("graphql/types")

# Create Flask app
app = create_app()

# ADD THIS - Session configuration for Flask-Login
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SECURE"] = False  # Set to True in production (HTTPS only)
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["PERMANENT_SESSION_LIFETIME"] = 86400  # 24 hours

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

# initialize socket
socketio.init_app(app, cors_allowed_origins="*")

# Limiter
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


# Error handler
@app.errorhandler(APIException)
def handle_api_exception(e):
    return jsonify({"error": str(e)}), getattr(e, "status_code", 500)


# Routes
@app.route("/", endpoint="index")
@limiter.limit("10/minute")
@cache.cached(timeout=10)
def hello():
    return f"<h1>Welcome To Flask Development {random.randint(1, 1000)}</h1>"


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


# GraphQL
schema = make_executable_schema(type_defs, query, mutation, product_obj)


@app.route("/graphql", methods=["POST"])
@limiter.limit("10/minute")
def graphql_server():
    data = request.get_json()
    success, result = graphql_sync(schema, data, context_value=request, debug=True)
    return jsonify(result)


# ONLY RUN SOCKETIO AT THE END
if __name__ == "__main__":
    socketio.run(app, debug=True)
