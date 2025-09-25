import logging
import time
from datetime import datetime

from django.conf import settings
from django.core.exceptions import DisallowedHost
from django.http import HttpResponse

logger = logging.getLogger("django.request")


class IgnoreBadHostMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Get allowed hosts from settings
        self.allowed_hosts = settings.ALLOWED_HOSTS

    def __call__(self, request):
        # Check host before Django's middleware does
        host = request.META.get("HTTP_HOST", "")

        # If host is not in ALLOWED_HOSTS, return a 400 response immediately
        if host and self.allowed_hosts != ["*"] and host not in self.allowed_hosts:
            logger.warning(f"Bad Host: {host} - Path: {request.path}")  # noqa: G004
            return HttpResponse(status=400)

        # Otherwise, proceed with the request
        try:
            return self.get_response(request)
        except DisallowedHost:
            # This is a fallback in case the host check above doesn't catch it
            logger.warning(f"DisallowedHost exception for: {host} - Path: {request.path}")  # noqa: G004
            return HttpResponse(status=400)


class RequestLoggingMiddleware:
    """Middleware to log all requests with detailed information."""

    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger("django.request")

    def __call__(self, request):
        # Log request details before processing
        start_time = time.time()

        # Process the request
        response = self.get_response(request)

        # Calculate request processing time
        duration = time.time() - start_time

        # Get client IP - handle proxy forwarding
        ip = request.META.get('HTTP_X_FORWARDED_FOR', '').split(',')[0].strip() or \
             request.META.get('REMOTE_ADDR', '-')
        
        # Format the log message
        log_message = (
            f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
            f"{ip} {request.method} {request.path} "
            f"- {response.status_code} in {duration:.2f}s "
            f"- {request.META.get('HTTP_USER_AGENT', '-')}"
        )

        # Log at appropriate level based on status code
        if 200 <= response.status_code < 400:
            self.logger.info(log_message)
        elif 400 <= response.status_code < 500:
            self.logger.warning(log_message)
        else:
            self.logger.error(log_message)
        
        return response
