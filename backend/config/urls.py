from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from django.db import connection
from django.core.cache import cache
from django.utils import timezone
import os


def health_check(request):
    """Comprehensive health check endpoint"""
    health_status = {
        'status': 'healthy',
        'timestamp': timezone.now().isoformat(),
        'version': '1.0.0',
        'checks': {}
    }

    # Database check
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        health_status['checks']['database'] = {
            'status': 'ok',
            'message': 'Database connection successful'
        }
    except Exception as e:
        health_status['status'] = 'unhealthy'
        health_status['checks']['database'] = {
            'status': 'error',
            'message': str(e)
        }

    # Cache/Redis check
    try:
        cache.set('health_check', 'ok', 5)
        if cache.get('health_check') == 'ok':
            health_status['checks']['cache'] = {
                'status': 'ok',
                'message': 'Redis cache working'
            }
        else:
            health_status['checks']['cache'] = {
                'status': 'error',
                'message': 'Cache write/read failed'
            }
    except Exception as e:
        health_status['status'] = 'unhealthy'
        health_status['checks']['cache'] = {
            'status': 'error',
            'message': str(e)
        }

    # Disk space check
    try:
        stat = os.statvfs('.')
        free_space = stat.f_frsize * stat.f_bavail / (1024 * 1024)  # MB
        total_space = stat.f_frsize * stat.f_blocks / (1024 * 1024)  # MB
        used_percent = (1 - stat.f_bavail / stat.f_blocks) * 100

        health_status['checks']['disk'] = {
            'status': 'ok' if used_percent < 90 else 'warning',
            'total_mb': round(total_space, 2),
            'free_mb': round(free_space, 2),
            'used_percent': round(used_percent, 2)
        }
    except Exception as e:
        health_status['checks']['disk'] = {
            'status': 'error',
            'message': str(e)
        }

    status_code = 200 if health_status['status'] == 'healthy' else 503
    return JsonResponse(health_status, status=status_code)


urlpatterns = [
    path('health/', health_check, name='health-check'),
    path('admin/', admin.site.urls),
    path('api/v1/', include('store.urls')),
    path('api/v1/auth/', include('accounts.urls')),
]

# Prometheus metrics endpoint
if settings.DEBUG:
    urlpatterns += [path('metrics/', include('django_prometheus.urls'))]

# Serve static AND media files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
