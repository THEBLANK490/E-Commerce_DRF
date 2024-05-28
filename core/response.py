from rest_framework import exceptions


def get_success(code: int, message: str, data=None) -> dict:
    """
    Utility function to generate a success response dictionary.

    Args:
        code (int): The status code of the response.
        message (str): The message associated with the response.
        data (optional): Additional data to include in the response. Defaults to None.

    Returns:
        dict: A dictionary containing the success response.
    """
    context = {"code": code, "message": message, "data": data, "error": {}}
    return context


def get_error(qs: object, message: str) -> exceptions:
    """
    Utility function to raise a validation error if queryset is not empty.

    Args:
        qs (object): The queryset to check.
        message (str): The error message to include in the exception.

    Raises:
        exceptions.ValidationError: If the queryset is not empty.
    """
    if qs:
        raise exceptions.ValidationError(message)
