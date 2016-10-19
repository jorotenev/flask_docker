from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
from . import mail
from app.utils import logException


def send_email(to, subject, template, attachments=None, **kwargs):
    try:
        app = current_app._get_current_object()
        msg = Message(subject,
                      sender=app.config['DEFAULT_MAIL_SENDER'], recipients=[to])
        msg.body = render_template(template + '.txt', **kwargs)
        msg.html = render_template(template + '.html', **kwargs)

        if attachments is not None:
            for attachment in attachments.keys():
                msg.attach(attachment, "application/pdf", attachments[attachment])
        thr = Thread(target=_send_async_email, args=[app, msg])
        thr.start()
        return msg
    except Exception as ex:
        logException()
        print(str(ex))

def bulk_send_email(tos, *args, **kwargs):
    with mail.connect():
        for to in tos:
            send_email(*args,to=to, **kwargs)

def _send_async_email(app, msg):
    with app.app_context():
        try:
            mail.send(msg)
        except Exception as ex:
            logException()

