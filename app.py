from flask import (
    Flask,
)

from routes.route_root import main as route_root
from routes.route_zhihu import main as route_zhihu
from routes.route_user import main as route_user

from models import MongoModel
from models.user import User
import config

app = Flask(__name__)
app.register_blueprint(route_zhihu, url_prefix='/zhihu')
app.register_blueprint(route_user, url_prefix='/user')
app.register_blueprint(route_root, url_prefix='/')

app.secret_key = config.secret_key

# 初始化数据库
MongoModel.init_db()
# User 设置索引
User.init_db()

# 运行代码
if __name__ == '__main__':
    # debug 模式可以自动加载你对代码的变动, 所以不用重启程序
    # host 参数指定为 '0.0.0.0' 可以让别的机器访问你的代码
    config = dict(
        debug=True,
        host='0.0.0.0',
        port=2000,
    )

    # 启动
    app.run(**config)
