import time

import pymysql

import config
import secret
from utils import log


class SQLModel(object):
    connection = None

    @classmethod
    def init_db(cls):
        cls.connection = pymysql.connect(
            host='localhost',
            user='root',
            password=secret.mysql_password,
            db=config.db_name,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

    def __init__(self, form):
        # 因为 id 是数据库给的，所以最开始初始化的时候必须是 None
        self.id = form.get('id', None)

    @classmethod
    def table_name(cls):
        return '`{}`'.format(cls.__name__.lower())

    @classmethod
    def new(cls, form):
        m = cls(form)
        id = cls.insert(m.__dict__)
        m.id = id
        return m

    @classmethod
    def insert(cls, form):
        form.pop('id')

        sql_keys = ', '.join(['`{}`'.format(k) for k in form.keys()])
        sql_values = ', '.join(['%s'] * len(form))
        sql_insert = 'INSERT INTO {} ({}) VALUES ({})'.format(
            cls.table_name(),
            sql_keys,
            sql_values,
        )
        log('ORM insert <{}>'.format(sql_insert))

        values = tuple(form.values())

        with cls.connection.cursor() as cursor:
            cursor.execute(sql_insert, values)
            _id = cursor.lastrowid
        cls.connection.commit()

        return _id

    @classmethod
    def delete(cls, id):
        sql_delete = 'DELETE FROM {} WHERE `id`=%s'.format(cls.table_name())
        log('ORM delete <{}>'.format(sql_delete.replace('\n', ' ')))

        with cls.connection.cursor() as cursor:
            cursor.execute(sql_delete, (id,))
        cls.connection.commit()

    @classmethod
    def update(cls, id, **kwargs):
        sql_set = ', '.join(
            ['`{}`=%s'.format(k) for k in kwargs.keys()]
        )
        sql_update = 'UPDATE {} SET {} WHERE `id`=%s'.format(
            cls.table_name(),
            sql_set,
        )
        log('ORM update <{}>'.format(sql_update.replace('\n', ' ')))

        values = list(kwargs.values())
        values.append(id)
        values = tuple(values)

        with cls.connection.cursor() as cursor:
            cursor.execute(sql_update, values)
        cls.connection.commit()

    @classmethod
    def all(cls, **kwargs):
        # SELECT * FROM User WHERE username='xxx' AND password='xxx'
        sql_select = 'SELECT * FROM \n\t{}'.format(cls.table_name())

        if len(kwargs) > 0:
            sql_where = ' AND '.join(
                ['`{}`=%s'.format(k) for k in kwargs.keys()]
            )
            sql_where = '\nWHERE\n\t{}'.format(sql_where)
            sql_select = '{}{}'.format(sql_select, sql_where)
        log('ORM all <{}>'.format(sql_select.replace('\n', ' ')))

        values = tuple(kwargs.values())

        ms = []
        with cls.connection.cursor() as cursor:
            cursor.execute(sql_select, values)
            result = cursor.fetchall()
            for row in result:
                m = cls(row)
                ms.append(m)
            return ms

    @classmethod
    def one(cls, **kwargs):
        sql_select = 'SELECT * FROM \n' \
                     '\t{} \n' \
                     '{}\n' \
                     'LIMIT 1'

        sql_where = ' AND '.join(
            ['`{}`=%s'.format(k) for k in kwargs.keys()]
        )
        sql_where = '\nWHERE\n\t{}'.format(sql_where)
        sql_select = sql_select.format(
            cls.table_name(),
            sql_where
        )

        log('ORM one <{}>'.format(sql_select.replace('\n', ' ')))

        values = tuple(kwargs.values())

        with cls.connection.cursor() as cursor:
            cursor.execute(sql_select, values)
            result = cursor.fetchone()
            if result is None:
                return None
            else:
                return cls(result)

    def __repr__(self):
        """
        """
        name = self.__class__.__name__
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '< {}\n{} >\n'.format(name, s)

    def json(self):
        return self.__dict__


class SQLModelPro(object):

    def __init__(self, form):
        # 因为 id 是数据库给的，所以最开始初始化的时候必须是 None
        self.id = form.get('id', None)

    @classmethod
    def table_name(cls):
        return '`{}`'.format(cls.__name__)

    def __repr__(self):
        """
        """
        name = self.__class__.__name__
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '< {}\n{} >\n'.format(name, s)

    @classmethod
    def select(cls, connection):
        # SELECT * FROM user
        sql_select = 'SELECT * FROM {}'.format(cls.table_name())
        return Query(sql_select, connection, cls)


class Query(object):
    def __init__(self, raw, connection, model):
        self.query = raw
        self.values = tuple()
        self.connection = connection
        self.model = model

    def where(self, **kwargs):
        if len(kwargs) > 0:
            sql_where = ' AND '.join(
                ['`{}`=%s'.format(k) for k in kwargs.keys()]
            )
            sql_where = '\tWHERE\t{}'.format(sql_where)
            self.query = '{}{}'.format(self.query, sql_where)
        log('ORM where <{}>'.format(self.query))

        self.values = tuple(kwargs.values())

        return self

    def all(self):
        log('ORM all <{}> <{}>'.format(self.query, self.values))

        ms = []
        with self.connection.cursor() as cursor:
            log('ORM execute all <{}>'.format(cursor.mogrify(self.query, self.values)))
            cursor.execute(self.query, self.values)
            result = cursor.fetchall()
            for row in result:
                if self.join_exit():
                    m = row
                else:
                    m = self.model(row)
                ms.append(m)
            return ms

    def one(self):
        self.query = '{} LIMIT 1'.format(self.query)
        log('ORM one <{}> <{}>'.format(self.query, self.values))

        with self.connection.cursor() as cursor:
            log('ORM execute one <{}>'.format(cursor.mogrify(self.query, self.values)))
            cursor.execute(self.query, self.values)
            result = cursor.fetchone()
            if result is None:
                return None
            else:
                if self.join_exit():
                    return result
                else:
                    return self.model(result)

    def join(self, target_model, field, target_field):
        # JOIN topic on user.id=topic.user_id
        target_table = target_model.table_name()
        table = self.model.table_name()
        sql_join = 'JOIN {} on {}.{}={}.{}'.format(
            target_table, table, field, target_table, target_field
        )
        self.query = '{}\t{}'.format(self.query, sql_join)
        return self

    def join_exit(self):
        exist = 'JOIN' in self.query
        return exist
