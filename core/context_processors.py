from .models import SiteSettings


def site_settings(request):
    """Expose SiteSettings as `site_settings` globally in templates."""
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
            
        settings_obj = DefaultSettings()
    
    return {"site_settings": settings_obj}
