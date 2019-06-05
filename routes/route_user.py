from flask import (
    render_template,
    redirect,
    url_for,
    Blueprint,
    request,
    session,
    escape,

)
from models.user import User
from utils import log
from werkzeug.utils import secure_filename
from config import imgDir
import os

main = Blueprint('user', __name__)


def login_required(func):
    '''
    权限检查的装饰器，要求必须用户已登录
    '''
    def f(*args, **kwargs):
        u = current_user()
        if u.is_guest():
            log('用户身份是游客')
            return redirect(url_for('user.login_view'))
        else:
            return func(*args, **kwargs)
    return f


@main.route("/")
def index():
    # 查看session是否存在
    if 'username' in session:
        username = escape(session['username'])
        u = User.find_one(username=username)
        if u is not None:
            # 用户存在
            return render_template("user/index.html", user=u)
        else:
            # 用户不存在
            return render_template("user/index.html")
    else:
        return render_template("user/index.html")


@main.route("/login_view")
def login_view():
    return render_template("user/login.html", message='')


@main.route("/login", methods=["POST"])
def login():
    # request.form 不是 dict，所以需要转换一下
    form = request.form.to_dict()
    u, result = User.login(form)
    if u is not None:
        # 设置客户端session
        session['username'] = request.form['username']
        # 跳转到用户主页
        return redirect(url_for('.index'))
    else:
        return redirect(url_for('.login_view', message=result))


@main.route("/logout", methods=["GET"])
def logout():
    # remove the username from the session if it's there
    log('session before pop', session)
    session.pop('username', None)
    log('session after pop', session)
    return redirect(url_for('root.index'))


@main.route("/register_view")
def register_view():
    msg = request.args.get('msg', '')
    return render_template("user/register.html", message=msg)


@main.route("/register", methods=["POST"])
def register():
    form = request.form
    u, msg = User.register(form.to_dict())
    if u is None:
        return redirect(url_for('.register_view', msg=msg))
    else:
        return redirect(url_for('.login_view'))


def allow_file(filename):
    suffix = filename.split('.')[-1]
    from config import accept_user_file_type
    return suffix in accept_user_file_type


@main.route('/addimg', methods=["POST"])
def add_img():
    u = current_user()

    if u is None:
        return redirect(url_for(".profile"))

    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)

    if allow_file(file.filename):
        # 检查文件名的合法性
        filename = secure_filename(file.filename)
        # log('imgDir', imgDir)
        file.save(os.path.join(imgDir, filename))
        # 将头像的文件名绑定到用户的属性上
        u.user_image = filename
        log('u', u)
        u.save()

    return redirect(url_for(".index"))


def current_user():
    '''
    获取当前用户，如果没有登录，则返回 None
    '''
    # 查看session是否存在
    if 'username' in session:
        username = escape(session['username'])
        u = User.find_one(username=username)
        if u is not None:
            return u
    return User.guest()