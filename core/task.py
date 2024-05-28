from celery import shared_task

from core.utils import send_mail_to_user


@shared_task
def send_mail_task(*args, **kwargs):
    return send_mail_to_user(email=args[0])
