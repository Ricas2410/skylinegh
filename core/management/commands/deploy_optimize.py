from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings
from django.core.cache import cache
from core.models import SiteSettings
import os
import time


class Command(BaseCommand):
    help = 'Comprehensive deployment optimization for production'

    def add_arguments(self, parser):
        parser.add_argument(
            '--skip-static',
            action='store_true',
            help='Skip static file collection',
        )
        parser.add_argument(
            '--skip-cache',
            action='store_true',
            help='Skip cache setup',
        )
        parser.add_argument(
            '--skip-seo',
            action='store_true',
            help='Skip SEO optimization',
        )

    def handle(self, *args, **options):
        start_time = time.time()
        
        self.stdout.write(
            self.style.SUCCESS('🚀 Starting deployment optimization...')
        )

        # 1. Database migrations
        if not options.get('skip_migrations', False):
            self.run_migrations()

        # 2. Static files collection
        if not options['skip_static']:
            self.collect_static()

        # 3. Cache setup
        if not options['skip_cache']:
            self.setup_cache()

        # 4. SEO optimization
        if not options['skip_seo']:
            self.optimize_seo()

        # 5. Performance optimization
        self.optimize_performance()

        # 6. Final checks
        self.run_final_checks()

        end_time = time.time()
        duration = end_time - start_time
        
        self.stdout.write(
            self.style.SUCCESS(f'✅ Deployment optimization completed in {duration:.2f} seconds')
        )

    def run_migrations(self):
        """Run database migrations"""
        self.stdout.write('📊 Running database migrations...')
        try:
            call_command('migrate', verbosity=0)
            self.stdout.write(
                self.style.SUCCESS('✅ Database migrations completed')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Migration error: {e}')
            )

    def collect_static(self):
        """Collect static files"""
        self.stdout.write('📦 Collecting static files...')
        try:
            call_command('collectstatic', '--noinput', verbosity=0)
            self.stdout.write(
                self.style.SUCCESS('✅ Static files collected')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Static collection error: {e}')
            )

    def setup_cache(self):
        """Setup cache system"""
        self.stdout.write('🗄️ Setting up cache...')
        try:
            # Create cache table if using database cache
            cache_backend = settings.CACHES['default']['BACKEND']
            if 'DatabaseCache' in cache_backend:
                call_command('createcachetable', verbosity=0)
                self.stdout.write('✅ Cache table created')
            
            # Clear existing cache
            cache.clear()
            self.stdout.write('✅ Cache cleared')
            
            # Warm up cache with site settings
            site_settings = SiteSettings.objects.first()
            if site_settings:
                cache.set('site_settings_v2', site_settings, 3600)
                self.stdout.write('✅ Cache warmed up')
            
        except Exception as e:
            self.stdout.write(
                self.style.WARNING(f'⚠️ Cache setup warning: {e}')
            )

    def optimize_seo(self):
        """Run SEO optimization"""
        self.stdout.write('🔍 Optimizing SEO...')
        try:
            call_command('optimize_seo', '--all', verbosity=0)
            self.stdout.write(
                self.style.SUCCESS('✅ SEO optimization completed')
            )
        except Exception as e:
            self.stdout.write(
                self.style.WARNING(f'⚠️ SEO optimization warning: {e}')
            )

    def optimize_performance(self):
        """Run performance optimization"""
        self.stdout.write('⚡ Optimizing performance...')
        try:
            # Clear any old cache entries
            cache_keys = [
                'sitemap_staticviewsitemap',
                'sitemap_projectsitemap',
                'sitemap_servicesitemap',
                'sitemap_blogsitemap',
                'sitemap_jobsitemap',
            ]
            
            for key in cache_keys:
                cache.delete(key)
            
            self.stdout.write(
                self.style.SUCCESS('✅ Performance optimization completed')
            )
        except Exception as e:
            self.stdout.write(
                self.style.WARNING(f'⚠️ Performance optimization warning: {e}')
            )

    def run_final_checks(self):
        """Run final deployment checks"""
        self.stdout.write('🔍 Running final checks...')
        
        checks = []
        
        # Check if site settings exist
        if SiteSettings.objects.exists():
            checks.append('✅ Site settings configured')
        else:
            checks.append('❌ Site settings missing')
        
        # Check if static files directory exists
        if os.path.exists(settings.STATIC_ROOT):
            checks.append('✅ Static files directory exists')
        else:
            checks.append('❌ Static files directory missing')
        
        # Check if media directory exists
        if os.path.exists(settings.MEDIA_ROOT):
            checks.append('✅ Media files directory exists')
        else:
            checks.append('❌ Media files directory missing')
        
        # Check cache functionality
        try:
            cache.set('test_key', 'test_value', 60)
            if cache.get('test_key') == 'test_value':
                checks.append('✅ Cache system working')
                cache.delete('test_key')
            else:
                checks.append('❌ Cache system not working')
        except Exception:
            checks.append('❌ Cache system error')
        
        # Display results
        for check in checks:
            if '✅' in check:
                self.stdout.write(check)
            else:
                self.stdout.write(self.style.WARNING(check))

    def create_superuser_if_needed(self):
        """Create superuser if none exists"""
        from django.contrib.auth.models import User
        
        if not User.objects.filter(is_superuser=True).exists():
            self.stdout.write('👤 Creating superuser...')
            try:
                User.objects.create_superuser(
                    username='admin',
                    email='admin@skylinegh.com',
                    password='admin123'  # Change this in production!
                )
                self.stdout.write(
                    self.style.SUCCESS('✅ Superuser created (username: admin, password: admin123)')
                )
                self.stdout.write(
                    self.style.WARNING('⚠️ Please change the default password immediately!')
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'❌ Superuser creation error: {e}')
                )
        else:
            self.stdout.write('✅ Superuser already exists')

    def setup_site_settings(self):
        """Ensure site settings are properly configured"""
        self.stdout.write('⚙️ Setting up site settings...')
        
        site_settings, created = SiteSettings.objects.get_or_create(
            pk=1,
            defaults={
                'site_name': 'Skyline Ghana Constructions',
                'site_tagline': 'Building Dreams, Creating Futures',
                'site_description': 'Leading construction company in Ghana specializing in residential, commercial, and industrial building projects.',
                'meta_description': 'Professional construction services in Ghana. Expert contractors delivering quality construction services across Accra, Kumasi, and all regions of Ghana.',
                'meta_keywords': 'construction company ghana, building contractors ghana, construction services accra, residential construction ghana, commercial construction ghana',
                'phone_primary': '+233 24 123 4567',
                'email_primary': 'info@skylinegh.com',
                'address_line_1': '123 Construction Avenue',
                'city': 'Accra',
                'region': 'Greater Accra',
                'projects_completed': 500,
                'square_feet_built': 1000000,
                'client_satisfaction': 98,
                'years_experience': 25,
            }
        )
        
        if created:
            self.stdout.write('✅ Site settings created with default values')
        else:
            self.stdout.write('✅ Site settings already exist')
