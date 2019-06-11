from flask_socketio import emit
from app import socketio
from routes.route_user import current_user
from utils import log

log('event_chat is imported')
log('socketio:', socketio)


class OnlineCount():
    count = 0

    @classmethod
    def add(cls):
        cls.count += 1

    @classmethod
    def get(cls):
        return cls.count

    @classmethod
    def minus(cls):
        cls.count -= 1


@socketio.on('connect', namespace='/chat')
def event_connect():
    OnlineCount.add()
    # log('connect event', OnlineCount.get())
    emit('event_online_count', {'online_count': OnlineCount.get()},
         broadcast=True)


@socketio.on('disconnect', namespace='/chat')
def event_disconnect():
    OnlineCount.minus()
    # log('disconnect event', OnlineCount.get())
    emit('event_online_count', {'online_count': OnlineCount.get()},
         broadcast=True)


@socketio.on('event_text', namespace='/chat')
def text(data):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    # log('message from client', data)
    u = current_user()
    username = u.username
    emit('event_text',
         {'text': username + ':' + data['text']},
         broadcast=True)
