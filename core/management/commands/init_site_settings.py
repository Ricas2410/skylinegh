from django.core.management.base import BaseCommand
from core.models import SiteSettings


class Command(BaseCommand):
    help = 'Initialize default site settings if none exist'

    def handle(self, *args, **options):
        if not SiteSettings.objects.exists():
            SiteSettings.objects.create(
                site_name='Skyline Ghana Constructions',
                site_tagline='Building Dreams, Creating Futures',
                site_description='Professional construction services in Ghana. From residential homes to commercial buildings, we bring your vision to life with quality craftsmanship and modern techniques.',
                meta_description='Professional construction services in Ghana',
                meta_keywords='construction, Ghana, building, residential, commercial',
                phone_primary='+233 24 123 4567',
                email_primary='info@skylinegh.com',
                address_line_1='123 Construction Avenue',
                city='Accra',
                region='Greater Accra'
            )
            self.stdout.write(
                self.style.SUCCESS('Successfully created default site settings')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Site settings already exist')
            )
