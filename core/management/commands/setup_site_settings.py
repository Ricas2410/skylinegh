from django.core.management.base import BaseCommand
from core.models import SiteSettings


class Command(BaseCommand):
    help = 'Setup default site settings for the new design'

    def handle(self, *args, **options):
        self.stdout.write('Setting up site settings...')

        # Get or create the site settings instance
        site_settings, created = SiteSettings.objects.get_or_create(pk=1)
        
        # Update with default values for new fields
        site_settings.hero_title = "Building the Future, Block by Block."
        site_settings.hero_subtitle = "Skyline Ghana Constructions is a leading name in construction and design, transforming visions into reality with precision, innovation, and a commitment to quality."
        site_settings.top_navbar_email = "info@skylineghana.com"
        site_settings.top_navbar_phone = "+233 24 123 4567"
        site_settings.get_in_touch_text = "Get in Touch"
        site_settings.show_blog_in_top_nav = True
        site_settings.blog_url = "#"
        
        # Social media URLs (you can update these with real URLs)
        site_settings.linkedin_url = "https://linkedin.com/company/skyline-ghana"
        site_settings.facebook_url = "https://facebook.com/skylineghana"
        site_settings.instagram_url = "https://instagram.com/skylineghana"
        site_settings.twitter_url = "https://twitter.com/skylineghana"
        
        site_settings.save()
        
        if created:
            self.stdout.write(self.style.SUCCESS('Created new site settings with default values'))
        else:
            self.stdout.write(self.style.SUCCESS('Updated existing site settings with new default values'))
        
        self.stdout.write('Site settings setup complete!')
