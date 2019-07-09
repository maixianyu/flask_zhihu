from tasks import send_async
from config import test_mail, admin_mail

if __name__ == '__main__':
    subject = 'celery的测试'
    content = '如果收到，说明测试成功'
    send_async.delay(subject,
                     author=admin_mail,
                     to=test_mail,
                     content=content)
