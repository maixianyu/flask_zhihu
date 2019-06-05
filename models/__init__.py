from pymongo import (
    MongoClient,
)
from utils import log
from models.user_role import userrole_codec
from bson import ObjectId
import json


class MongoModel(object):
    client = None
    db = None
    # 这里是为了encode一些自定义类型，比如 UserRole
    from bson.codec_options import TypeRegistry, CodecOptions
    type_registry = TypeRegistry([userrole_codec])
    codec_options = CodecOptions(type_registry=type_registry)

    @classmethod
    def init_db(cls):
        cls.client = MongoClient()
        cls.db = cls.client['BJudeLab']

    def __init__(self, form):
        self._id = str(form.get('_id', ''))

    @classmethod
    def collection_name(cls):
        return '{}'.format(cls.__name__)

    @classmethod
    def new(cls, form):
        # cls(form) 相当于 User(form)
        m = cls(form)
        _id = cls.insert(m.__dict__)
        m._id = str(_id)
        return m

    # 插入
    @classmethod
    def insert(cls, form):
        # get a collection
        collection = cls.db.get_collection(cls.collection_name(),
                                           codec_options=cls.codec_options)
        # _id 不允许写入
        form.pop('_id')
        _id = collection.insert_one(form).inserted_id
        return _id

    # 删除
    @classmethod
    def delete(cls, id):
        collection = cls.db[cls.collection_name()]
        result = collection.delete_one({"_id": id})
        # result 是删除的数目
        return result

    @classmethod
    def update(cls, id, **kwargs):
        if '_id' in kwargs:
            kwargs.pop('_id')
        # id 必须是 _id
        collection = cls.db[cls.collection_name()]
        log('update', id, kwargs)
        res = collection.update(
            {"_id": id},
            kwargs,
        )
        log('update res', res)

    # 查找
    @classmethod
    def find_one(cls, **kwargs):
        collection = cls.db[cls.collection_name()]
        r = collection.find_one(kwargs)
        if r is not None:
            m = cls(r)
            return m
        return None

    @classmethod
    def all(cls, **kwargs):
        collection = cls.db[cls.collection_name()]
        rs = collection.find(kwargs)
        all = [cls(r) for r in rs]
        return all

    def save(self):
        self.update(ObjectId(self._id), **self.__dict__)

    def __repr__(self):
        """
        __repr__ 是一个魔法方法
        简单来说, 它的作用是得到类的 字符串表达 形式
        比如 print(u) 实际上是 print(u.__repr__())
        不明白就看书或者 搜
        """
        name = self.__class__.__name__
        properties = ['{}: ({})'.format(k, v)
                      for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '< {}\n{} >\n'.format(name, s)

    def json(self):
        return json.dumps(self.__dict__)
