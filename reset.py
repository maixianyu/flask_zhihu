from sqlalchemy import create_engine

import secret
import config
from app import configured_app
from models.base_model import db
from models.user import User
from models.question_answer import Question, Answer, AnswerComment
from models.message import Messages


def reset_database():
    # 现在 mysql root 默认用 socket 来验证而不是密码
    url = 'mysql+pymysql://root:{}@localhost/?charset=utf8mb4'.format(
        secret.database_password,
    )
    e = create_engine(url, echo=True)

    with e.connect() as c:
        c.execute('DROP DATABASE IF EXISTS {}'.format(config.database_name))

        c.execute('CREATE DATABASE {} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci'.format(
            config.database_name))

        c.execute('USE {}'.format(config.database_name))

    db.metadata.create_all(bind=e)


def generate_fake_date(app):
    # 写入用户 maixy
    form = dict(
        username='maixianyu',
        password='123',
        email=config.test_mail,
    )
    u_1 = User.register(form)

    # 写入用户 maixianyu
    form = dict(
        username='maixy',
        password='123',
        email=config.test_mail,
    )
    u_2 = User.register(form)

    # 写入用户 xiandan
    form = dict(
        username='xiandan',
        password='123',
        email=config.test_mail,
    )
    u_3 = User.register(form)

    # 话题模版
    question_form = dict(
        author=u_1.username,
        title='如何看待x事件？',
        content='3天前发生了这件事，你怎么看？',
        count_answer=1,
    )

    # 回答模版
    with open('answer_demo.md', encoding='utf8') as f:
        content = f.read()
        answer_form = dict(
            author=u_1.username,
            question_id=1,
            content=content,
            agree=1,
            disagree=1,
        )

    comment_form = dict(
        author=u_1.username,
        content="说得好。",
        answer_id=0,
    )

    with app.test_request_context():
        for i in range(10):
            print('begin question <{}>'.format(i))
            Question.new(question_form)

            # 每个问题两个回答
            print('begin answer <{}>'.format(i))
            answer_form['question_id'] = i+1
            Answer.manual_new(answer_form)

            print('begin answer <{}>'.format(i))
            answer_form['question_id'] = i+1
            Answer.manual_new(answer_form)

        for i in range(20):
            print('begin AnswerComment <{}>'.format(i))
            comment_form['author'] = u_2.username
            comment_form['answer_id'] = i+1
            AnswerComment.manual_new(comment_form)

            print('begin AnswerComment <{}>'.format(i))
            comment_form['author'] = u_3.username
            comment_form['answer_id'] = i+1
            comment_form['content'] = "同意楼上。"
            AnswerComment.manual_new(comment_form)

    title = '一个请教'
    content = '我的看法是xx。'
    sender_id = u_1.id
    receiver_id = u_2.id
    Messages.send(title, content, sender_id, receiver_id)


if __name__ == '__main__':
    app = configured_app()
    with app.app_context():
        reset_database()
        generate_fake_date(app)
