from __future__ import annotations

from django.utils import timezone
from django.conf import settings
from django.urls import resolve
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

            # Optionally skip AJAX
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return

            # Count unique session per day to reduce inflation
            session = getattr(request, "session", None)
            today_key = f"visited:{timezone.localdate().isoformat()}"
            if session is not None:
                if session.get(today_key):
                    return
                session[today_key] = True
                session.modified = True

            # Increment daily counter
            metric_date = timezone.localdate()
            obj, _ = SystemMetrics.objects.get_or_create(
                metric_name="visitors",
                metric_date=metric_date,
                defaults={"metric_value": 0},
            )
            obj.metric_value = (obj.metric_value or 0) + 1
            obj.save(update_fields=["metric_value"])
        except Exception:
            # Do not interrupt requests if tracking fails
            return
