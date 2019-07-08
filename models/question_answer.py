from models.user import User
from models.base_model import SQLMixin, db
from routes.route_user import current_user
from sqlalchemy import String, Integer, Column, Text, UnicodeText, Unicode
from utils import log
import json
# from flask import escape

views = Column(Integer, nullable=False, default=0)
title = Column(Unicode(50), nullable=False)
content = Column(UnicodeText, nullable=False)
user_id = Column(Integer, nullable=False)
board_id = Column(Integer, nullable=False)


class Question(SQLMixin, db.Model):
    __tablename__ = 'Question'
    author = Column(String(20), nullable=False)
    title = Column(Unicode(50), nullable=False)
    content = Column(UnicodeText, nullable=False)
    count_answer = Column(Integer, nullable=False, default=0)

    @classmethod
    def new(cls, form):
        # form['content'] = json.dumps(form['content'])
        form['author'] = current_user().username

        a = super().new(form)
        return a

    def all_answer(self):
        all = Answer.all(question_id=self.id)
        return all


class Answer(SQLMixin, db.Model):
    __tablename__ = 'Answer'

    author = Column(String(20), nullable=False)
    content = Column(UnicodeText, nullable=False)
    question_id = Column(Integer, nullable=False)
    # 赞
    agree = Column(Integer, nullable=False, default=0)
    # 反对
    disagree = Column(Integer, nullable=False, default=0)

    @classmethod
    def new(cls, form):
        form['content'] = json.dumps(form['content'])
        form['author'] = current_user().username
        # log('answer in new', form['content'], type(form['content']))
        a = super().new(form)
        return a

    @classmethod
    def api_new(cls, form):
        a = cls.new(form).json()
        a['image'] = User.one(username=a['author']).image
        return a

    @classmethod
    def manual_new(cls, form):
        form['content'] = str(form['content'])
        return super().new(form)

    def question(self):
        q = Question.one(id=self.question_id)
        return q

    # 返回答主这个user对象
    def user(self):
        u = User.one(username=self.author)
        return u

    @classmethod
    def api_all(cls, **kwargs):
        all = cls.all(**kwargs)
        all = [e.json() for e in all]

        for e in all:
            log('api author', e)
            e['image'] = User.one(username=e['author']).image

        return all


class AnswerComment(SQLMixin, db.Model):
    __tablename__ = 'AnswerComment'
    author = Column(String(20), nullable=False)
    content = Column(UnicodeText, nullable=False)
    answer_id = Column(Integer, nullable=False)

    def answer(self):
        q = Answer.one(id=self.answer_id)
        return q

    # 返回答主这个user对象
    def user(self):
        u = User.one(username=self.author)
        return u
