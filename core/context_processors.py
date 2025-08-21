from .models import SiteSettings
from django.core.cache import cache
from django.conf import settings as django_settings


def site_settings(request):
    """Expose SiteSettings as `site_settings` globally in templates with caching."""
    # Use cache to avoid database hits on every request
    cache_key = 'site_settings_v2'
    settings_obj = cache.get(cache_key)

    if settings_obj is None:
        try:
            settings_obj = SiteSettings.objects.first()
            if not settings_obj:
                # Create default settings if none exist
                settings_obj = SiteSettings.objects.create(
                    site_name="Skyline Ghana Constructions",
                    site_tagline="Building Dreams, Creating Futures",
                    site_description="Professional construction services in Ghana. From residential homes to commercial buildings, we bring your vision to life with quality craftsmanship and modern techniques.",
                    phone_primary="+233 24 123 4567",
                    email_primary="info@skylinegh.com",
                    address_line_1="123 Construction Avenue",
                    city="Accra",
                    region="Greater Accra"
                )

            # Cache for 1 hour (3600 seconds)
            cache.set(cache_key, settings_obj, 3600)
        except Exception as e:
            # Fallback to a minimal object with default values
            class DefaultSettings:
                site_name = "Skyline Ghana Constructions"
                site_tagline = "Building Dreams, Creating Futures"
                site_description = "Professional construction services in Ghana"
                meta_description = "Professional construction services in Ghana"
                meta_keywords = "construction, Ghana, building, residential, commercial"
                phone_primary = "+233 24 123 4567"
                email_primary = "info@skylinegh.com"
                logo = None
                projects_completed = 500
                square_feet_built = 1000000
                client_satisfaction = 98
                years_experience = 25

            settings_obj = DefaultSettings()
            # Cache the fallback for a shorter time (5 minutes)
            cache.set(cache_key, settings_obj, 300)

    return {"site_settings": settings_obj}
