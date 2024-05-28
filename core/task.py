from celery import shared_task

from core.utils import send_mail_to_user


@shared_task
def send_mail_task(*args, **kwargs):
    """
    This is a task which is used to queue the
    sending email task in the celery.
    """
    return send_mail_to_user(email=args[0])
