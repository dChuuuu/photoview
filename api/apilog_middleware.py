import logging

logger = logging.getLogger(__name__)


class LoggingMiddleware:
    def __init__(self, next_middleware):
        self.next_middleware = next_middleware

    def __call__(self, request):
        logger.info('Request: %s %s', request.method, request.path)
        response = self.next_middleware(request)
        return response
