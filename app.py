from flask import (
    Flask,
)
from flask_socketio import SocketIO

from models.base_model import db

import config
import secret
from utils import log


# socketio
socketio = SocketIO()


def register_routes(app):
    """
    注册路由
    """
    from routes.route_message import main as route_message
    from routes.route_zhihu import main as route_zhihu
    from routes.route_user import main as route_user
    from routes.route_chat import main as route_chat
    from routes.route_root import main as route_root

    app.register_blueprint(route_message, url_prefix='/mail')
    app.register_blueprint(route_zhihu, url_prefix='/zhihu')
    app.register_blueprint(route_user, url_prefix='/user')
    app.register_blueprint(route_chat, url_prefix='/chat')
    app.register_blueprint(route_root, url_prefix='/')


def db_init(app):
    """
    初始化数据库
    """
    uri = 'mysql+pymysql://root:{}@localhost/{}?charset=utf8mb4'.format(
        secret.database_password,
        config.database_name,
    )
    app.config['SQLALCHEMY_DATABASE_URI'] = uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)


def register_jinja_func(app):
    from jinja_func import count, format_time
    app.template_filter()(count)
    app.template_filter()(format_time)


def configured_app():
    app = Flask(__name__)

    register_routes(app)
    db_init(app)
    from . import event_chat
    socketio.init_app(app)
    register_jinja_func(app)

    app.secret_key = secret.secret_key

    # log('real socketio', socketio)

    return app
