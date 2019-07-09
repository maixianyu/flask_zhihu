from marrow.mailer import Mailer
import secret
from celery import Celery
from config import admin_mail

app = Celery('tasks', broker='redis://localhost:6379/2')


def configured_mailer():
    config = {
        # 'manager.use': 'futures',
        'transport.debug': True,
        'transport.timeout': 1,
        'transport.use': 'smtp',
        'transport.host': 'smtp.exmail.qq.com',
        'transport.port': 465,
        'transport.tls': 'ssl',
        'transport.username': admin_mail,
        'transport.password': secret.mail_password,
    }
    m = Mailer(config)
    m.start()
    return m


mailer = configured_mailer()


@app.task
def send_async(subject, author, to, content):
    m = mailer.new(
        subject=subject,
        author=author,
        to=to,
    )
    m.plain = content

    mailer.send(m)


@app.task
def add(x, y):
    return x + y
