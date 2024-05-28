from django.conf import settings
from django.core.mail import send_mail
from rest_framework import exceptions


def get_or_not_found(qs: object, **kwargs):
    try:
        return qs.get(**kwargs)
    except:
        raise exceptions.NotFound("{} instance not found".format(qs.model.__name__))


def send_mail_to_user(email: str):
    subject = "welcome to ECommerce website"
    message = f"Hi {email}, thank you for registering."
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
