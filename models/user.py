from models import MongoModel
import time
from pymongo import ASCENDING
from models.user_role import UserRole
import hashlib
import config
import urllib


class User(MongoModel):
    def __init__(self, form):
        super().__init__(form)
        self._id = form.get('_id', None)
        self.username = form.get('username')
        self.password = form.get('password')
        # 用户角色
        self.role = form.get('role', UserRole.normal)
        # 注册时间
        self.time = int(time.time())
        # 用户的头像图片
        # 注意，一定要用 form.get，而不能直接赋值，否则从数据库转成model时
        # 会有数据没有办法导出来
        self.user_image = form.get('user_image', self.default_img())

    @staticmethod
    def default_img():
        return 'default.png'

    @classmethod
    def guest(cls):
        '''
        生成一个游客对象，给未登录状态的访客使用
        '''
        form = dict(
            username='游客',
            password='',
            role=UserRole.guest,
        )
        u = cls(form)
        return u

    def is_guest(self):
        """
        判断当前用户是否是游客
        """
        return self.role == UserRole.guest

    @classmethod
    def init_db(cls):
        username = urllib.parse.quote_plus(config.mongo_user)
        password = urllib.parse.quote_plus(config.mongo_passwd)
        cls.db.authenticate(username, password)
        cls.db[cls.collection_name()].create_index([
            ('username', ASCENDING),
        ],
            unique=True)

    # 检查表单是否合法
    @staticmethod
    def validate(form):
        return len(form['username']) > 2 and len(form['password']) > 2

    @staticmethod
    def salted_password(password, salt=config.user_salt):
        # 加盐
        salted = password + salt
        # hash 后以 16 进制保存
        hash = hashlib.sha256(salted.encode()).hexdigest()
        return hash

    @classmethod
    def register(cls, form):
        # 检查表单是否合法
        valid = cls.validate(form)
        # 如果用户名和密码合法
        if valid is True:
            # 给密码加盐hash
            form['password'] = cls.salted_password(form['password'])
            # 存入数据库
            u = cls.new(form)
            result = ''
        else:
            u = None()
            result = '用户名或密码长度需要大于2'
        return u, result

    @classmethod
    def login(cls, form):
        # 给密码加密
        form['password'] = cls.salted_password(form['password'])
        # 验证用户名与密码是否存在
        u = User.find_one(**form)
        if u is None:
            result = '登录失败'
        else:
            result = ''
        return u, result
