import os
import random

from ariadne import graphql_sync, load_schema_from_path, make_executable_schema
from dotenv import load_dotenv
from flask import jsonify, redirect, render_template, request, session, url_for
from flask_dance.contrib.github import github, make_github_blueprint
from flask_dance.contrib.google import google, make_google_blueprint
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

load_dotenv()
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
@app.route("/", endpoint="index")
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


os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"


@app.route("/me/email")
def me_email():
    if not github.authorized:
        return {"error": "Not logged in"}

    resp = github.get("/user/emails")
    print("user respnse =>> ", resp.json())
    return jsonify(resp.json())


google_bp = make_google_blueprint(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    scope=["profile", "email"],
    redirect_to="google_login",
)

app.register_blueprint(google_bp, url_prefix="/login")


@app.route("/google")
def google_login():
    if not google.authorized:
        return redirect(url_for("google.login"))

    resp = google.get("/oauth2/v2/userinfo")
    user_info = resp.json()

    return user_info


os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

github_bp = make_github_blueprint(
    client_id=os.getenv("client_id"),
    client_secret=os.getenv("client_secret"),
    scope="user:email",
)

app.register_blueprint(github_bp, url_prefix="/login")


@app.route("/github")
def github_login():
    if not github.authorized:
        return redirect(url_for("github.login"))

    resp = github.get("/user")
    print("user data =>", resp.json())
    return resp.json()


# {"avatar_url":"https://avatars.githubusercontent.com/u/100943707?v=4","bio":"python backend developer  (Django - fastapi -flask) ","blog":"","company":"monufia university","created_at":"2022-03-04T12:58:09Z","email":null,"events_url":"https://api.github.com/users/MO123adel2elkholy/events{/privacy}","followers":0,"followers_url":"https://api.github.com/users/MO123adel2elkholy/followers","following":2,"following_url":"https://api.github.com/users/MO123adel2elkholy/following{/other_user}","gists_url":"https://api.github.com/users/MO123adel2elkholy/gists{/gist_id}","gravatar_id":"","hireable":true,"html_url":"https://github.com/MO123adel2elkholy","id":100943707,"location":"Cairo ","login":"MO123adel2elkholy","name":"mahmoud adel","node_id":"U_kgDOBgRHWw","notification_email":null,"organizations_url":"https://api.github.com/users/MO123adel2elkholy/orgs","public_gists":0,"public_repos":26,"received_events_url":"https://api.github.com/users/MO123adel2elkholy/received_events","repos_url":"https://api.github.com/users/MO123adel2elkholy/repos","site_admin":false,"starred_url":"https://api.github.com/users/MO123adel2elkholy/starred{/owner}{/repo}","subscriptions_url":"https://api.github.com/users/MO123adel2elkholy/subscriptions","twitter_username":null,"type":"User","updated_at":"2026-03-24T02:57:42Z","url":"https://api.github.com/users/MO123adel2elkholy","user_view_type":"public"}


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


print("End of file ")
