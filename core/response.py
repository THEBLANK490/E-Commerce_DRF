from rest_framework import exceptions


def get_success(code: int, message: str, data=None) -> dict:
    context = {"code": code, "message": message, "data": data, "error": {}}
    return context


def get_error(qs: object, message: str) -> exceptions:
    if qs:
        raise exceptions.ValidationError(message)
