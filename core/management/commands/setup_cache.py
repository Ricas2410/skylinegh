from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings

class Command(BaseCommand):
    help = 'Set up cache table for database caching'

    def handle(self, *args, **options):
        """Create cache table if using database cache"""
        cache_backend = settings.CACHES['default']['BACKEND']
        
        if 'DatabaseCache' in cache_backend:
            self.stdout.write('Creating cache table...')
            try:
                call_command('createcachetable')
                self.stdout.write(
                    self.style.SUCCESS('Successfully created cache table')
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error creating cache table: {e}')
                )
        else:
            self.stdout.write(
                self.style.WARNING('Not using database cache, skipping cache table creation')
            )
