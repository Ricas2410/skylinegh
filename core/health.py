from django.http import JsonResponse, HttpResponse
from django.db import connections
from django.core.cache import cache
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

def health_check(request):
    """
    Health check endpoint for Fly.io load balancer.
    Checks database connectivity and basic app functionality.
    """
    try:
        # Check database connection
        db_conn = connections['default']
        db_conn.cursor()
        
        # Check cache (optional, don't fail if cache is down)
        try:
            cache.set('health_check', 'ok', 10)
            cache.get('health_check')
        except Exception as e:
            logger.warning(f"Cache check failed: {e}")
        
        return HttpResponse('ok', content_type='text/plain')
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return HttpResponse('unhealthy', status=503, content_type='text/plain')
