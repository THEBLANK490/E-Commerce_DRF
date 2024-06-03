from typing import Any
import logging

take_log = logging.getLogger("take_log")


class LoggingMiddleware:
    def __init__(self, get_response) -> None:
        # Initialize the middleware with a reference to the get_response function
        self.get_response = get_response

    def __call__(self, request) -> Any:
        # Execute this middleware when a request is received

        # Get the response by passing the request to the next middleware or view
        response = self.get_response(request)

        # Log information for GET requests
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
        # Handle any unhandled exceptions(500) that occur during request processing
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
