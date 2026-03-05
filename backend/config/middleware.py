import time
import logging
from django.db import connection
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)


class RateLimitHeadersMiddleware(MiddlewareMixin):
    """
    Adds rate limit headers to responses when available.
    """

    def process_response(self, request, response):
        if hasattr(request, 'rate_limit'):
            response['X-RateLimit-Limit'] = str(request.rate_limit.get('limit', ''))
            response['X-RateLimit-Remaining'] = str(request.rate_limit.get('remaining', ''))
            response['X-RateLimit-Reset'] = str(request.rate_limit.get('reset', ''))
        return response


class QueryCountDebugMiddleware(MiddlewareMixin):
    """
    Middleware to log the number of database queries and total time.
    Only active when DEBUG = True.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        super().__init__(get_response)

    def __call__(self, request):
        if not connection.queries:
            return self.get_response(request)

        # Reset query log
        connection.queries_log.clear()

        # Process request
        start_time = time.time()
        response = self.get_response(request)
        total_time = time.time() - start_time

        # Log query count
        num_queries = len(connection.queries)

        if num_queries > 20:  # Alert if too many queries
            logger.warning(
                f"High query count: {num_queries} queries in {total_time:.2f}s "
                f"for {request.method} {request.path}"
            )

            # Log the actual queries for debugging
            for i, query in enumerate(connection.queries):
                logger.debug(f"Query {i + 1}: {query['sql']} ({query['time']}s)")
        else:
            logger.debug(
                f"Query count: {num_queries} queries in {total_time:.2f}s "
                f"for {request.method} {request.path}"
            )

        # Add headers for debugging
        if hasattr(response, '__setitem__'):
            response['X-Query-Count'] = str(num_queries)
            response['X-Query-Time'] = str(round(total_time, 3))

        return response


class CacheControlMiddleware(MiddlewareMixin):
    """
    Adds appropriate cache control headers based on content type.
    """

    def process_response(self, request, response):
        # Don't cache authenticated responses
        if request.user.is_authenticated:
            response['Cache-Control'] = 'private, no-cache, no-store, must-revalidate'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
            return response

        # Cache static-like endpoints
        if request.path.startswith('/api/v1/products/featured'):
            response['Cache-Control'] = 'public, max-age=300'  # 5 minutes
        elif request.path.startswith('/api/v1/leagues/'):
            response['Cache-Control'] = 'public, max-age=86400'  # 24 hours
        elif request.path.startswith('/api/v1/collections/'):
            response['Cache-Control'] = 'public, max-age=86400'  # 24 hours
        elif request.path.startswith('/api/v1/products/') and '?' not in request.get_full_path():
            response['Cache-Control'] = 'public, max-age=3600'  # 1 hour

        return response