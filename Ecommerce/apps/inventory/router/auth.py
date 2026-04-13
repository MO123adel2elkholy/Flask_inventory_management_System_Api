import os

from flask import jsonify, redirect, request, session, url_for
from flask_dance.contrib.github import github, make_github_blueprint
from flask_dance.contrib.google import google, make_google_blueprint
from werkzeug.security import generate_password_hash

from Ecommerce.apps import database as db
from Ecommerce.apps.models.inventory_models import User
from Ecommerce.tasks.models_Email_notification import send_email_task
from Ecommerce.utils.token import generate_token, verify_token

from .. import inventory_auth_api_blueprint  # noqa: F401


@inventory_auth_api_blueprint.route("/auth", methods=["GET"])
def auth():
    return "auth endpoint called "


os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"


@inventory_auth_api_blueprint.route("/me/email")
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

inventory_auth_api_blueprint.register_blueprint(google_bp, url_prefix="/api")


@inventory_auth_api_blueprint.route("/google")
def google_login():
    if not google.authorized:
        return redirect(url_for("inventory_auth_api_blueprint.google.login"))

    resp = google.get("/oauth2/v2/userinfo")
    user_info = resp.json()

    return user_info


os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

github_bp = make_github_blueprint(
    client_id=os.getenv("client_id"),
    client_secret=os.getenv("client_secret"),
    scope="user:email",
)

inventory_auth_api_blueprint.register_blueprint(github_bp, url_prefix="/login")


@inventory_auth_api_blueprint.route("/github")
def github_login():
    if not github.authorized:
        return redirect(url_for("inventory_auth_api_blueprint.github.login"))

    resp = github.get("/user")
    print("user data =>", resp.json())
    return resp.json()


# {"avatar_url":"https://avatars.githubusercontent.com/u/100943707?v=4","bio":"python backend developer  (Django - fastapi -flask) ","blog":"","company":"monufia university","created_at":"2022-03-04T12:58:09Z","email":null,"events_url":"https://api.github.com/users/MO123adel2elkholy/events{/privacy}","followers":0,"followers_url":"https://api.github.com/users/MO123adel2elkholy/followers","following":2,"following_url":"https://api.github.com/users/MO123adel2elkholy/following{/other_user}","gists_url":"https://api.github.com/users/MO123adel2elkholy/gists{/gist_id}","gravatar_id":"","hireable":true,"html_url":"https://github.com/MO123adel2elkholy","id":100943707,"location":"Cairo ","login":"MO123adel2elkholy","name":"mahmoud adel","node_id":"U_kgDOBgRHWw","notification_email":null,"organizations_url":"https://api.github.com/users/MO123adel2elkholy/orgs","public_gists":0,"public_repos":26,"received_events_url":"https://api.github.com/users/MO123adel2elkholy/received_events","repos_url":"https://api.github.com/users/MO123adel2elkholy/repos","site_admin":false,"starred_url":"https://api.github.com/users/MO123adel2elkholy/starred{/owner}{/repo}","subscriptions_url":"https://api.github.com/users/MO123adel2elkholy/subscriptions","twitter_username":null,"type":"User","updated_at":"2026-03-24T02:57:42Z","url":"https://api.github.com/users/MO123adel2elkholy","user_view_type":"public"}


@inventory_auth_api_blueprint.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


@inventory_auth_api_blueprint.route(
    "/verify-email/<token>", methods=["GET"], endpoint="Email-vervication"
)
def verify_email(token):
    email = verify_token(token)

    if not email:
        return {"message": "Invalid or expired token"}

    # هنا update user in DB → is_verified = True
    return {"message": f"Email verified: {email}"}


@inventory_auth_api_blueprint.route("/forgot-password", methods=["POST"])
def forgot_password():
    email = request.json["email"]
    token = generate_token(email)
    reset_link = f"http://127.0.0.1:5000/api/reset-password/{token}"
    send_email_task.delay(
        subject="Reset Password",
        recipients=[email],
        body=f"Click here to reset password: {reset_link}",
    )
    return {"reset_link": f"http://127.0.0.1:5000/api/reset-password/{token}"}


@inventory_auth_api_blueprint.route("/reset-password/<token>", methods=["POST"])
def reset_password(token):
    email = verify_token(token)

    if not email:
        return {"message": "Invalid or expired token"}, 400

    user = User.query.filter_by(email=email).first()

    if not user:
        return {"message": "User not found"}, 404

    data = request.get_json()

    if not data or "password" not in data:
        return {"message": "Password is required"}, 400

    new_password = data["password"]

    if len(new_password) < 6:
        return {"message": "Password too short"}, 400

    user.password = generate_password_hash(new_password)

    db.session.commit()

    return {"message": "Password updated successfully"}


print("End of file ")
