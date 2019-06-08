from flask import (
    Flask,
)
from flask_socketio import SocketIO

from models import MongoModel
from models.user import User
import config
from utils import log

# 初始化数据库
MongoModel.init_db()
# User 设置索引
User.init_db()

# socketio
socketio = SocketIO()


def create_app():
    app = Flask(__name__)

    from routes.route_zhihu import main as route_zhihu
    from routes.route_user import main as route_user
    from routes.route_chat import main as route_chat
    from routes.route_root import main as route_root

    app.register_blueprint(route_zhihu, url_prefix='/zhihu')
    app.register_blueprint(route_user, url_prefix='/user')
    app.register_blueprint(route_chat, url_prefix='/chat')
    app.register_blueprint(route_root, url_prefix='/')

    app.secret_key = config.secret_key

    socketio.init_app(app)
    log('real socketio', socketio)

    return app
