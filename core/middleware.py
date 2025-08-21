from __future__ import annotations

from django.utils import timezone
from django.conf import settings
from django.urls import resolve
from django.http import HttpResponsePermanentRedirect
from dashboard.models import SystemMetrics


class VisitorTrackingMiddleware:
    """
    Lightweight visitor tracking.
    - Increments a daily "visitors" counter stored in `dashboard.models.SystemMetrics`.
    - Skips admin, dashboard, static, media, and staff-auth paths.
    """

    EXCLUDED_PREFIXES = (
        "/admin/",
        "/my-admin/",
        settings.STATIC_URL or "/static/",
        getattr(settings, "MEDIA_URL", "/media/"),
        "/__debug__",
        "/favicon.ico",
        "/robots.txt",
        "/sitemap.xml",
        "/api/auth/",
    )

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self._maybe_track(request)
        return self.get_response(request)

    def _maybe_track(self, request):
        try:
            path = request.path or "/"

            # Exclude prefixes
            if any(path.startswith(p) for p in self.EXCLUDED_PREFIXES):
                return

            # Only track GET requests for normal pages
            if request.method != "GET":
                return

            # Skip AJAX requests
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return

            # Skip bots and crawlers (basic detection)
            user_agent = request.headers.get("user-agent", "").lower()
            bot_indicators = ["bot", "crawler", "spider", "scraper", "curl", "wget"]
            if any(indicator in user_agent for indicator in bot_indicators):
                return

            # Count unique session per day to reduce inflation
            session = getattr(request, "session", None)
            today_key = f"visited:{timezone.localdate().isoformat()}"

            if session is not None:
                # Check if this session already visited today
                if session.get(today_key):
                    return

                # Mark session as visited today
                session[today_key] = True
                session.modified = True
            else:
                # If no session available, still track but this might cause some inflation
                pass

            # Increment daily counter
            metric_date = timezone.localdate()
            obj, created = SystemMetrics.objects.get_or_create(
                metric_name="visitors",
                metric_date=metric_date,
                defaults={"metric_value": 0},
            )

            # Use F() expression for atomic increment to avoid race conditions
            from django.db.models import F
            obj.metric_value = F('metric_value') + 1
            obj.save(update_fields=["metric_value"])

            # Refresh from database to get actual value for logging
            obj.refresh_from_db()

        except Exception as e:
            # Log error in development but don't interrupt requests
            if settings.DEBUG:
                print(f"Visitor tracking error: {e}")
            return


class WWWRedirectMiddleware:
    """
    Middleware to redirect www.domain.com to domain.com (or vice versa)
    This ensures consistent canonical URLs for SEO
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only apply redirects in production
        if not settings.DEBUG:
            host = request.get_host().lower()

            # Redirect www.skylinegh.com to skylinegh.com (preferred canonical)
            if host.startswith('www.'):
                new_host = host[4:]  # Remove 'www.'
                new_url = f"{request.scheme}://{new_host}{request.get_full_path()}"
                return HttpResponsePermanentRedirect(new_url)

        response = self.get_response(request)
        return response


class CacheControlMiddleware:
    """
    Middleware to add cache control headers for better performance
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Add cache headers for static files
        if request.path.startswith('/static/'):
            # Cache static files for 1 year
            response['Cache-Control'] = 'public, max-age=31536000, immutable'
            response['Expires'] = 'Thu, 31 Dec 2025 23:59:59 GMT'
        elif request.path.startswith('/media/'):
            # Cache media files for 1 week
            response['Cache-Control'] = 'public, max-age=604800'
        elif request.path.endswith(('.css', '.js', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico', '.woff', '.woff2')):
            # Cache other assets for 1 month
            response['Cache-Control'] = 'public, max-age=2592000'
        else:
            # Cache HTML pages for 1 hour
            response['Cache-Control'] = 'public, max-age=3600'

        return response
