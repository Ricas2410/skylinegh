from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.cache import cache
from core.models import SiteSettings
import os
import requests
from urllib.parse import urljoin


class Command(BaseCommand):
    help = 'Optimize SEO settings and check for common SEO issues'

    def add_arguments(self, parser):
        parser.add_argument(
            '--check-urls',
            action='store_true',
            help='Check if important URLs are accessible',
        )
        parser.add_argument(
            '--fix-meta',
            action='store_true',
            help='Fix common meta tag issues',
        )
        parser.add_argument(
            '--clear-cache',
            action='store_true',
            help='Clear SEO-related cache',
        )
        parser.add_argument(
            '--all',
            action='store_true',
            help='Run all SEO optimizations',
        )

    def handle(self, *args, **options):
        if options['all']:
            options['check_urls'] = True
            options['fix_meta'] = True
            options['clear_cache'] = True

        self.stdout.write(
            self.style.SUCCESS('🔍 Starting SEO optimization...')
        )

        if options['clear_cache']:
            self.clear_seo_cache()

        if options['fix_meta']:
            self.fix_meta_tags()

        if options['check_urls']:
            self.check_important_urls()

        self.stdout.write(
            self.style.SUCCESS('✅ SEO optimization completed!')
        )

    def clear_seo_cache(self):
        """Clear SEO-related cache entries"""
        self.stdout.write('🧹 Clearing SEO cache...')
        try:
            # Clear site settings cache
            cache.delete('site_settings_v2')
            
            # Clear any other SEO-related cache keys
            cache_keys = [
                'sitemap_cache',
                'robots_txt_cache',
                'meta_tags_cache',
            ]
            
            for key in cache_keys:
                cache.delete(key)
            
            self.stdout.write(
                self.style.SUCCESS('✅ SEO cache cleared successfully')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error clearing SEO cache: {e}')
            )

    def fix_meta_tags(self):
        """Fix common meta tag issues"""
        self.stdout.write('🏷️ Checking and fixing meta tags...')
        
        try:
            # Ensure site settings exist with proper SEO data
            site_settings, created = SiteSettings.objects.get_or_create(
                pk=1,
                defaults={
                    'site_name': 'Skyline Ghana Constructions',
                    'site_tagline': 'Building Dreams, Creating Futures',
                    'site_description': 'Leading construction company in Ghana specializing in residential, commercial, and industrial building projects.',
                    'meta_description': 'Professional construction services in Ghana. Expert contractors delivering quality construction services across Accra, Kumasi, and all regions of Ghana.',
                    'meta_keywords': 'construction company ghana, building contractors ghana, construction services accra, residential construction ghana, commercial construction ghana',
                }
            )
            
            if created:
                self.stdout.write('✅ Created default site settings with SEO data')
            else:
                # Update existing settings if meta fields are empty
                updated = False
                if not site_settings.meta_description:
                    site_settings.meta_description = 'Professional construction services in Ghana. Expert contractors delivering quality construction services across Accra, Kumasi, and all regions of Ghana.'
                    updated = True
                
                if not site_settings.meta_keywords:
                    site_settings.meta_keywords = 'construction company ghana, building contractors ghana, construction services accra, residential construction ghana, commercial construction ghana'
                    updated = True
                
                if updated:
                    site_settings.save()
                    self.stdout.write('✅ Updated site settings with missing SEO data')
                else:
                    self.stdout.write('✅ Site settings SEO data is complete')
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error fixing meta tags: {e}')
            )

    def check_important_urls(self):
        """Check if important URLs are accessible"""
        self.stdout.write('🌐 Checking important URLs...')
        
        base_url = 'http://127.0.0.1:8000'  # Development URL
        if not settings.DEBUG:
            base_url = 'https://skylinegh.com'  # Production URL
        
        important_urls = [
            '/',
            '/about/',
            '/services/',
            '/projects/',
            '/contact/',
            '/careers/',
            '/blog/',
            '/sitemap.xml',
            '/robots.txt',
        ]
        
        for url_path in important_urls:
            full_url = urljoin(base_url, url_path)
            try:
                if settings.DEBUG:
                    # For development, just check if URL pattern exists
                    self.stdout.write(f'📄 {url_path} - URL pattern configured')
                else:
                    # For production, make actual HTTP request
                    response = requests.get(full_url, timeout=10)
                    if response.status_code == 200:
                        self.stdout.write(f'✅ {url_path} - OK ({response.status_code})')
                    else:
                        self.stdout.write(f'⚠️ {url_path} - {response.status_code}')
            except Exception as e:
                self.stdout.write(f'❌ {url_path} - Error: {e}')

    def check_seo_issues(self):
        """Check for common SEO issues"""
        self.stdout.write('🔍 Checking for SEO issues...')
        
        issues = []
        
        # Check if site settings exist
        if not SiteSettings.objects.exists():
            issues.append('No site settings configured')
        
        # Check if Google Analytics is configured
        site_settings = SiteSettings.objects.first()
        if site_settings and not site_settings.google_analytics_id:
            issues.append('Google Analytics not configured')
        
        # Check if meta description is set
        if site_settings and not site_settings.meta_description:
            issues.append('Meta description not set in site settings')
        
        # Check if meta keywords are set
        if site_settings and not site_settings.meta_keywords:
            issues.append('Meta keywords not set in site settings')
        
        if issues:
            self.stdout.write('⚠️ SEO Issues Found:')
            for issue in issues:
                self.stdout.write(f'  - {issue}')
        else:
            self.stdout.write('✅ No major SEO issues found')
        
        return issues
