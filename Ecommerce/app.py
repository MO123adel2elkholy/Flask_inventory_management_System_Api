import logging
import os
import random
from datetime import datetime
from typing import Dict

from ariadne import graphql_sync, load_schema_from_path, make_executable_schema
from flask import jsonify, render_template, request, session
from flask_httpauth import HTTPBasicAuth
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO, emit, join_room, leave_room
from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.security import check_password_hash

from Ecommerce.admin.setup import Create_admin
from Ecommerce.apps import create_app
from Ecommerce.apps.models.inventory_models import User
from Ecommerce.Exceptions import APIException
from Ecommerce.graphql.resolvers.inventory_resover import mutation, product_obj, query
from Ecommerce.Limiter.limiter import init_app, limiter

# Initialize Limiter


# Logging


# Load GraphQL types
type_defs = load_schema_from_path("graphql/types")

# Create Flask app
app = create_app()


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


#  handling Websocket

# Config logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# App Configuration Settings


# Handle reverse proxy headers
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Initialize SocketIO with appropriate CORS settings
socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    logger=True,
    engineio_logger=True,
)

# In-memory storage for active users
# In production, consider using Redis or another distributed storage
active_users: Dict[str, dict] = {}


def generate_guest_username() -> str:
    """Generate a unique guest username with timestamp to avoid collisions"""
    timestamp = datetime.now().strftime("%H%M")
    return f"Guest{timestamp}{random.randint(1000, 9999)}"


@app.route("/chatt")
def index():
    if "username" not in session:
        session["username"] = generate_guest_username()
        logger.info(f"New user session created: {session['username']}")

    return render_template(
        "chatt.html", username=session["username"], rooms=app.config["CHATT_ROOMS"]
    )


@socketio.event
def connect():
    try:
        if "username" not in session:
            session["username"] = generate_guest_username()

        active_users[request.sid] = {
            "username": session["username"],
            "connected_at": datetime.now().isoformat(),
        }

        emit(
            "active_users",
            {"users": [user["username"] for user in active_users.values()]},
            broadcast=True,
        )

        logger.info(f"User connected: {session['username']}")

    except Exception as e:
        logger.error(f"Connection error: {str(e)}")
        return False


@socketio.event
def disconnect():
    try:
        if request.sid in active_users:
            username = active_users[request.sid]["username"]
            del active_users[request.sid]

            emit(
                "active_users",
                {"users": [user["username"] for user in active_users.values()]},
                broadcast=True,
            )

            logger.info(f"User disconnected: {username}")

    except Exception as e:
        logger.error(f"Disconnection error: {str(e)}")


@socketio.on("join")
def on_join(data: dict):
    try:
        username = session["username"]
        room = data["room"]

        if room not in app.config["CHATT_ROOMS"]:
            logger.warning(f"Invalid room join attempt: {room}")
            return

        join_room(room)
        active_users[request.sid]["room"] = room

        emit(
            "status",
            {
                "msg": f"{username} has joined the room.",
                "type": "join",
                "timestamp": datetime.now().isoformat(),
            },
            room=room,
        )

        logger.info(f"User {username} joined room: {room}")

    except Exception as e:
        logger.error(f"Join room error: {str(e)}")


@socketio.on("leave")
def on_leave(data: dict):
    try:
        username = session["username"]
        room = data["room"]

        leave_room(room)
        if request.sid in active_users:
            active_users[request.sid].pop("room", None)

        emit(
            "status",
            {
                "msg": f"{username} has left the room.",
                "type": "leave",
                "timestamp": datetime.now().isoformat(),
            },
            room=room,
        )

        logger.info(f"User {username} left room: {room}")

    except Exception as e:
        logger.error(f"Leave room error: {str(e)}")


@socketio.on("message")
def handle_message(data: dict):
    try:
        username = session["username"]
        room = data.get("room", "General")
        msg_type = data.get("type", "message")
        message = data.get("msg", "").strip()

        if not message:
            return

        timestamp = datetime.now().isoformat()

        if msg_type == "private":
            # Handle private messages
            target_user = data.get("target")
            if not target_user:
                return

            for sid, user_data in active_users.items():
                if user_data["username"] == target_user:
                    emit(
                        "private_message",
                        {
                            "msg": message,
                            "from": username,
                            "to": target_user,
                            "timestamp": timestamp,
                        },
                        room=sid,
                    )
                    logger.info(f"Private message sent: {username} -> {target_user}")
                    return

            logger.warning(f"Private message failed - user not found: {target_user}")

        else:
            # Regular room message
            if room not in app.config["CHATT_ROOMS"]:
                logger.warning(f"Message to invalid room: {room}")
                return

            emit(
                "message",
                {
                    "msg": message,
                    "username": username,
                    "room": room,
                    "timestamp": timestamp,
                },
                room=room,
            )

            logger.info(f"Message sent in {room} by {username}")

    except Exception as e:
        logger.error(f"Message handling error: {str(e)}")


# In production, use gunicorn or uwsgi instead
port = int(os.environ.get("PORT", 5000))
socketio.run(
    app,
    host="0.0.0.0",
    port=port,
    debug=app.config["DEBUG"],
    use_reloader=app.config["DEBUG"],
)
