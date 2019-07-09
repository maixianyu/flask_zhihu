# from time import sleep
from sqlalchemy import Column, Unicode, UnicodeText, Integer

from config import admin_mail

from models.base_model import SQLMixin, db
from models.user import User
from tasks import send_async


class Messages(SQLMixin, db.Model):
    title = Column(Unicode(50), nullable=False)
    content = Column(UnicodeText, nullable=False)
    sender_id = Column(Integer, nullable=False)
    receiver_id = Column(Integer, nullable=False)

    @staticmethod
    def send(title: str, content: str, sender_id: int, receiver_id: int):
        form = dict(
            title=title,
            content=content,
            sender_id=sender_id,
            receiver_id=receiver_id
        )
        Messages.new(form)

        receiver: User = User.one(id=receiver_id)

        send_async.delay(
            subject=form['title'],
            author=admin_mail,
            to=receiver.email,
            content=form['content']
        )
