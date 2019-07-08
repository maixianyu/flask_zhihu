from sqlalchemy import Column, String, Enum
from models.base_model import SQLMixin, db

from models.user_role import UserRole
import hashlib
import config
import secret
from utils import log


class User(SQLMixin, db.Model):
    __tablename__ = 'User'
    default_img = 'default.png'

    username = Column(String(20), nullable=False)
    password = Column(String(100), nullable=False)
    image = Column(String(100), nullable=False,
                   default=default_img)
    email = Column(String(50), nullable=False)
    role = Column(Enum(UserRole), nullable=False)

    @staticmethod
    def guest():
        form = dict()
        form['username'] = '游客'
        form['role'] = UserRole.guest
        form['image'] = __class__.default_img
        u = __class__()
        for k, v in form.items():
            setattr(u, k, v)
        return u

    def is_guest(self):
        """
        判断当前用户是否是游客
        """
        return self.role == UserRole.guest

    @staticmethod
    def salted_password(password, salt=secret.user_salt):
        # 加盐
        salted = password + salt
        # hash 后以 16 进制保存
        hash = hashlib.sha256(salted.encode()).hexdigest()
        return hash

    @classmethod
    def register(cls, form):
        name = form.get('username', '')
        if len(name) > 2 and User.one(username=name) is None:
            form['password'] = User.salted_password(form['password'])
            form['role'] = UserRole.normal
            u = User.new(form)
            return u
        else:
            return None

    @classmethod
    def validate_login(cls, form):
        query = dict(
            username=form['username'],
            password=User.salted_password(form['password']),
        )
        print('validate_login', form, query)
        return User.one(**query)
