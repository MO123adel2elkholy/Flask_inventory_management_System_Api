from datetime import datetime

from flask import request, session
from flask_socketio import emit, join_room, leave_room

from . import socketio
from .config import CHAT_ROOMS

active_users = {}


@socketio.on("connect")
def connect():
    username = session.get("username", "Guest")

    active_users[request.sid] = username

    emit(
        "active_users",
        {"users": list(active_users.values())},
        broadcast=True,
    )


@socketio.on("disconnect")
def disconnect():
    if request.sid in active_users:
        del active_users[request.sid]

    emit(
        "active_users",
        {"users": list(active_users.values())},
        broadcast=True,
    )


@socketio.on("join")
def on_join(data):
    room = data.get("room")

    if room not in CHAT_ROOMS:
        return

    join_room(room)

    emit(
        "status",
        {"msg": f"{session.get('username')} joined {room}"},
        room=room,
    )


@socketio.on("leave")
def on_leave(data):
    room = data.get("room")

    leave_room(room)

    emit(
        "status",
        {"msg": f"{session.get('username')} left {room}"},
        room=room,
    )


@socketio.on("message")
def handle_message(data):
    username = session.get("username", "Guest")
    msg = data.get("msg", "").strip()
    room = data.get("room")

    if not msg:
        return

    # private
    if data.get("type") == "private":
        target = data.get("target")

        for sid, user in active_users.items():
            if user == target:
                emit(
                    "private_message",
                    {"msg": msg, "from": username},
                    room=sid,
                )
                return

    # room message
    if room not in CHAT_ROOMS:
        return

    emit(
        "message",
        {
            "username": username,
            "msg": msg,
            "timestamp": datetime.now().isoformat(),
        },
        room=room,
    )
