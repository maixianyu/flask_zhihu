from . import event_chat
# from utils import log
from models.user import User
import redis
import json

from flask import (
    request,
)

# 初始化 session_redis
cache_session = redis.StrictRedis(db=1)


def current_user():
    '''
    获取当前用户，如果没有登录，则返回 None
    '''
    # uid = session.get('user_id', '')
    s = request.cookies.get('session')
    # 从 redis 中找 u.id
    if s is not None and cache_session.exists(s):
        uid = cache_session.get(s)
        uid = json.loads(uid)
        u = User.one(id=uid)
        return u
    else:
        return User.guest()
