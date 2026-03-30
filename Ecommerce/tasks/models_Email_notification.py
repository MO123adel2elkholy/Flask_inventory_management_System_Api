from celery import shared_task
from flask_mail import Message

from Ecommerce.apps import mail


@shared_task
def send_email_task(subject, recipients, body):
    msg = Message(
        subject=subject,
        recipients=recipients,
        body=body,
        sender="adel333mahmoud@gmail.com",
    )
    mail.send(msg)
