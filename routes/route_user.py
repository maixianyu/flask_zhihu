from flask import (
    render_template,
    redirect,
    url_for,
    Blueprint,
    request,
    session,
    escape,
)
from functools import wraps
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
    @wraps(func)
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
        # username = escape(session['username'])
        username = session['username']
        u = User.one(username=username)
        if u is not None:
            # 用户存在
            return render_template("user/index.html", user=u)
        else:
            # 用户不存在
            return redirect(url_for('.login_view'))
    else:
        return redirect(url_for('.login_view'))


@main.route("/login_view")
def login_view():
    u = current_user()
    if u.is_guest():
        message = request.args.get('message', '')
        return render_template("user/login.html", message=message)
    else:
        return redirect(url_for('.index'))


@main.route("/login", methods=["POST"])
def login():
    # request.form 不是 dict，所以需要转换一下
    form = request.form.to_dict()
    log('login form', form)
    u = User.validate_login(form)
    if u is not None:
        # 设置客户端session
        session['username'] = request.form['username']
        # 跳转至登录前的页面
        ref = form['referrer']
        return redirect(ref)
    else:
        result = "用户名或密码不正确"
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
    msg = request.args.get('message', '')
    return render_template("user/register.html", message=msg)


# 检查表单是否合法的装饰器
def form_validate(fun_next):
    @wraps(fun_next)
    def f():
        form = request.form
        if len(form['username']) > 2 and len(form['password']) > 2:
            return fun_next()
        else:
            message = '用户名和密码长度需要大于2'
            return redirect(url_for('.register_view', message=message))
    return f


# 检查是否具有同用户名的装饰器
def same_username_validate(fun_next):
    @wraps(fun_next)
    def f():
        form = request.form
        u = User.one(username=form['username'])
        if u is not None:
            message = '存在同名用户'
            return redirect(url_for('.register_view', message=message))
        else:
            return fun_next()
    return f


@main.route("/register", methods=["POST"])
@form_validate
@same_username_validate
def register():
    form = request.form
    u, msg = User.register(form.to_dict())
    if u is None:
        return redirect(url_for('.register_view', message=msg))
    else:
        return redirect(url_for('.login_view', message=msg))


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
        u.image = filename
        log('u', u)
        u.save()

    return redirect(url_for(".index"))


def current_user():
    '''
    获取当前用户，如果没有登录，则返回 None
    '''
    # 查看session是否存在
    if 'username' in session:
        # username = escape(session['username'])
        username = session['username']
        log('current user', username, type(username))
        u = User.one(username=username)
        if u is not None:
            return u
    return User.guest()
