from typing import Any
import logging
from rest_framework import status

# status.

take_log = logging.getLogger("take_log")


class DemoMiddleware:
    def __init__(self, get_response) -> None:
        self.get_response = get_response

    def __call__(self, request) -> Any:
        response = self.get_response(request)

        if request.method == "GET":
            if request.user:
                take_log.info(
                    "User:{}, Method:{}, url:{}, view:{}".format(
                        request.user,
                        request.method,
                        request.path,
                        request.resolver_match.view_name,
                    )
                )
            else:
                take_log.info(
                    "Method:{}, url:{}, view:{}".format(
                        request.method, request.path, request.resolver_match.view_name
                    )
                )

        if request.method in ["POST", "PATCH"] and response.status_code in [
            200,
            201,
            202,
        ]:
            take_log.info(
                "User:{}, Method:{}, url:{}, view:{}".format(
                    request.user,
                    request.method,
                    request.path,
                    request.resolver_match.view_name,
                )
            )

        if request.method == "DELETE" and response.status_code in [200, 201, 202]:
            take_log.warning(
                "User:{}, Method:{}, url:{}, view:{}".format(
                    request.user,
                    request.method,
                    request.path,
                    request.resolver_match.view_name,
                )
            )

        return response

    def process_exception(self, request, exception):
        try:
            raise exception
        except Exception as e:
            take_log.critical(
                "Method:{}, url:{}, view:{} Unhandled Exception:{} ".format(
                    request.method,
                    request.path,
                    request.resolver_match.view_name,
                    str(e),
                )
            )
        return exception
