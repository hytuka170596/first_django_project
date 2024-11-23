from http import HTTPStatus

from django.http import HttpRequest, HttpResponse

from time import time
from colorama import Fore, Back
from django.shortcuts import render
from loguru import logger as log
from typing import Callable


def set_useragent_on_request_middleware(get_response):
    """
    Middleware to set the user agent on the request object.

    Args:
        get_response (Callable): The next middleware or view in the chain.

    Returns:
        Callable: The middleware function.
    """
    log.info(Fore.RED + "\n\n --------------- Initial call middleware\n")

    def middleware(request: HttpRequest):
        log.info(Fore.BLUE + " ------  Before get response middleware")
        request.user_agent = request.META.get("HTTP_USER_AGENT", "unknown")
        response = get_response(request)
        log.info(Fore.CYAN + " ------  After get response middleware")

        return response

    return middleware


class CountRequestsMiddleware:
    """Middleware to count the number of requests, responses, and exceptions."""

    def __init__(self, get_response: Callable) -> None:
        """
        Initialize the middleware.

        Args:
            get_response (Callable): The next middleware or view in the chain.
        """
        self.get_response = get_response
        self.requests_count = 0
        self.response_count = 0
        self.exceptions_count = 0

    def __call__(self, request: HttpRequest) -> HttpResponse:
        """
        Process the request and count the number of requests.

        Args:
            request (HttpRequest): The incoming request.

        Returns:
            HttpResponse: The response from the next middleware or view.
        """
        self.requests_count += 1
        log.info(
            Fore.GREEN
            + "requests count: ({current_request_count})".format(
                current_request_count=self.requests_count
            )
        )
        response = self.get_response(request)

        self.response_count += 1
        log.info(
            Fore.YELLOW
            + "responses count: ({current_response_count})".format(
                current_response_count=self.response_count
            )
        )

        return response

    def process_exception(self, request: HttpRequest, exception: Exception) -> None:
        """
        Process an exception and count the number of exceptions.

        Args:
            request (HttpRequest): The incoming request.
            exception (Exception): The exception that occurred.
        """
        self.exceptions_count += 1
        log.info(
            Fore.RED
            + Back.LIGHTWHITE_EX
            + "\n\n\tgot ({current_exception_count}) exceptions so far".format(
                current_exception_count=self.exceptions_count
            ).upper()
        )


class ThrottlingMiddleware:
    """Middleware to throttle requests from a single IP address."""

    def __init__(self, get_response: Callable, reset_time: int = 40) -> None:
        """
        Initialize the middleware.

        Args:
            get_response (Callable): The next middleware or view in the chain.
            reset_time (int, optional): The time in seconds to reset the request count. Defaults to 40.
        """
        self.get_response = get_response
        self.limit_requests = 30
        self.reset_time = reset_time
        self.ip_requests = dict()

    def get_ip_client(self, request: HttpRequest) -> str:
        """
        Get the IP address of the client.

        Args:
            request (HttpRequest): The incoming request.

        Returns:
            str: The IP address of the client.
        """
        ip = request.META.get("REMOTE_ADDR")
        return ip

    def __call__(self, request: HttpRequest) -> HttpResponse:
        """
        Process the request and check if the request limit has been exceeded.

        Args:
            request (HttpRequest): The incoming request.

        Returns:
            HttpResponse: The response from the next middleware
            or view, or a 429 response if the limit has been exceeded.
        """
        user_ip = self.get_ip_client(request)
        current_time = time()

        info_requests = self.ip_requests.get(
            user_ip, {"count": 0, "timestamp": current_time}
        )

        if current_time - info_requests["timestamp"] > self.reset_time:
            info_requests = {"count": 0, "timestamp": current_time}

        info_requests["count"] += 1
        self.ip_requests[user_ip] = info_requests

        if info_requests["count"] > self.limit_requests:
            request.is_rate_limited = True

        response = self.get_response(request)

        return response
