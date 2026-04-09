from flask_socketio import SocketIO

socketio = SocketIO()

# مهم جدًا عشان يسجل events
from . import chats  # noqa: F401
