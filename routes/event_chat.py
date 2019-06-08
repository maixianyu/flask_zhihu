from flask_socketio import emit
from app import socketio
from routes.route_user import current_user
from utils import log

log('event_chat is imported')
log('socketio:', socketio)


@socketio.on('event_text', namespace='/chat')
def text(data):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    log('message from client', data)
    u = current_user()
    username = u.username
    emit('event_text', {'text': username + ':' + data['text']})
