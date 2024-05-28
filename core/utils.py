from django.conf import settings
from django.core.mail import send_mail
from rest_framework import exceptions


def get_or_not_found(qs: object, **kwargs):
    """
    Utility function to get an object from queryset or raise NotFound exception if not found.

    Args:
        qs (object): The queryset to search for the object.
        **kwargs: Keyword arguments for filtering the queryset.

    Returns:
        object: The object retrieved from the queryset.

    Raises:
        exceptions.NotFound: If the object is not found in the queryset.
    """
    try:
        return qs.get(**kwargs)
    except:
        raise exceptions.NotFound("{} instance not found".format(qs.model.__name__))


def send_mail_to_user(email: str):
    """
    Utility function to send a welcome email to the user.

    Args:
        email (str): The email address of the user.
    """
    subject = "welcome to ECommerce website"
    message = f"Hi {email}, thank you for registering."
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
