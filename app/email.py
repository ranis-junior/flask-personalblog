from threading import Thread

from flask import current_app
from flask_mail import Message

from app import mail


def send_email(subject, sender, recipients, text_body, html_body, attachments=None, sync=False):
    msg = Message(subject, recipients, text_body, html_body, sender)
    if attachments:
        for attach in attachments:
            msg.attach(*attach)

    if sync:
        mail.send(msg)
    else:
        Thread(target=send_async_mail, args=(current_app._get_current_object(), msg)).start()


def send_async_mail(app, msg):
    with app.app_context():
        mail.send(msg)
