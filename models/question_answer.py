from models import MongoModel
from models.user import User
import time
from routes.route_user import current_user


class Question(MongoModel):
    def __init__(self, form):
        super().__init__(form)
        author = current_user().username
        self.author = author
        self.title = form.get('title')
        self.content = form.get('content')
        self.time = int(time.time())
        self.count_answer = 0

    def all_answer(self):
        all = Answer.all(question_id=self._id)
        return all


class Answer(MongoModel):
    def __init__(self, form):
        super().__init__(form)
        u = current_user()
        self.author = form.get('author', u.username)
        self.content = form.get('content')
        self.question_id = form.get('question_id')
        self.time = int(time.time())
        # 赞
        self.agree = form.get('agree', 0)
        # 反对
        self.disagree = form.get('disagree', 0)

    def question(self):
        q = Question.find_one(_id=self.question_id)
        return q

    # 返回答主这个user对象
    def user(self):
        u = User.find_one(username=self.author)
        return u

    # 返回 all，同时加上 user_image
    @classmethod
    def all(cls, **kwargs):
        all = super().all(**kwargs)
        # 将用户的图片关联到answer中
        for ans in all:
            ans.user_image = ans.user().user_image
        return all


class AnswerComment(MongoModel):
    def __init__(self, form):
        super().__init__(form)
        u = current_user()
        self.author = form.get('author', u.username)
        self.content = form.get('content')
        self.answer_id = form.get('answer_id')
        self.time = int(time.time())

    def answer(self):
        q = Answer.find_one(_id=self.answer_id)
        return q

    # 返回答主这个user对象
    def user(self):
        u = User.find_one(username=self.author)
        return u
