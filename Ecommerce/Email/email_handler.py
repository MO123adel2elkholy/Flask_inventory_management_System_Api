# Ecommerce/apps/email_handler.py
from threading import Thread

from flask import current_app
from flask_mail import Message

from Ecommerce.apps import mail
from Ecommerce.tasks.models_Email_notification import send_email_task


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, recipients, body):
    app = current_app._get_current_object()
    msg = Message(subject=subject, recipients=recipients, body=body)
    Thread(
        target=send_async_email, args=(app, msg)
    ).start()  # this the to prvent request blocking and time out latter we we use celery as backgroud tasks processor


# مثال لإيميل تلقائي عند إضافة منتج جديد
def notify_new_product(product):
    subject = f"New Product Added: {product.name}"
    body = f"A new product has been added to the inventory:\n\nName: {product.name}\nPrice: 90$ \nCategory:Electronics "
    # send_email(subject, ["adel333mahmoud@gmail.com",], body)
    send_email_task.delay(
        subject,
        [
            "adel333mahmoud@gmail.com",
        ],
        body,
    )
