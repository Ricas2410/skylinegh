from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.cache import cache
from django.db import connection
import os
import subprocess
import time

class Command(BaseCommand):
    help = 'Optimize site performance by clearing cache, optimizing database, and checking static files'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear-cache',
            action='store_true',
            help='Clear all cache entries',
        )
        parser.add_argument(
            '--optimize-db',
            action='store_true',
            help='Run database optimization commands',
        )
        parser.add_argument(
            '--check-static',
            action='store_true',
            help='Check static file sizes and suggest optimizations',
        )
        parser.add_argument(
            '--all',
            action='store_true',
            help='Run all optimization tasks',
        )

    def handle(self, *args, **options):
        start_time = time.time()
        
        if options['all']:
            options['clear_cache'] = True
            options['optimize_db'] = True
            options['check_static'] = True

        self.stdout.write(
            self.style.SUCCESS('🚀 Starting performance optimization...')
        )

        if options['clear_cache']:
            self.clear_cache()

        if options['optimize_db']:
            self.optimize_database()

        if options['check_static']:
            self.check_static_files()

        end_time = time.time()
        duration = end_time - start_time
        
        self.stdout.write(
            self.style.SUCCESS(f'✅ Performance optimization completed in {duration:.2f} seconds')
        )

    def clear_cache(self):
        """Clear all cache entries"""
        self.stdout.write('🧹 Clearing cache...')
        try:
            cache.clear()

            # Also clear specific cache keys
            cache_keys = [
                'site_settings_v2',
                'sitemap_cache',
                'robots_txt_cache',
                'meta_tags_cache',
            ]

            for key in cache_keys:
                cache.delete(key)

            self.stdout.write(
                self.style.SUCCESS('✅ Cache cleared successfully')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error clearing cache: {e}')
            )

    def optimize_database(self):
        """Run database optimization commands"""
        self.stdout.write('🗄️ Optimizing database...')
        try:
            with connection.cursor() as cursor:
                # Analyze tables for PostgreSQL
                if 'postgresql' in settings.DATABASES['default']['ENGINE']:
                    cursor.execute("ANALYZE;")
                    self.stdout.write('✅ Database tables analyzed')
                
                # Get database size info
                cursor.execute("""
                    SELECT 
                        schemaname,
                        tablename,
                        attname,
                        n_distinct,
                        correlation
                    FROM pg_stats 
                    WHERE schemaname = 'public'
                    ORDER BY tablename, attname
                    LIMIT 10;
                """)
                
                self.stdout.write('📊 Database statistics updated')
                
        except Exception as e:
            self.stdout.write(
                self.style.WARNING(f'⚠️ Database optimization skipped: {e}')
            )

    def check_static_files(self):
        """Check static file sizes and suggest optimizations"""
        self.stdout.write('📁 Checking static files...')
        
        static_root = getattr(settings, 'STATIC_ROOT', None)
        if not static_root or not os.path.exists(static_root):
            self.stdout.write(
                self.style.WARNING('⚠️ STATIC_ROOT not found or does not exist')
            )
            return

        large_files = []
        total_size = 0
        
        for root, dirs, files in os.walk(static_root):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    size = os.path.getsize(file_path)
                    total_size += size
                    
                    # Flag files larger than 500KB
                    if size > 500 * 1024:
                        relative_path = os.path.relpath(file_path, static_root)
                        large_files.append((relative_path, size))
                except OSError:
                    continue

        # Convert total size to MB
        total_size_mb = total_size / (1024 * 1024)
        
        self.stdout.write(f'📊 Total static files size: {total_size_mb:.2f} MB')
        
        if large_files:
            self.stdout.write('⚠️ Large files found (>500KB):')
            for file_path, size in sorted(large_files, key=lambda x: x[1], reverse=True):
                size_kb = size / 1024
                self.stdout.write(f'  • {file_path}: {size_kb:.1f} KB')
                
                # Suggest optimizations based on file type
                if file_path.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                    self.stdout.write(f'    💡 Consider optimizing image: {file_path}')
                elif file_path.endswith('.css'):
                    self.stdout.write(f'    💡 Consider minifying CSS: {file_path}')
                elif file_path.endswith('.js'):
                    self.stdout.write(f'    💡 Consider minifying JavaScript: {file_path}')
        else:
            self.stdout.write('✅ No large static files found')

        # Check for common performance issues
        self.check_performance_issues()

    def check_performance_issues(self):
        """Check for common performance issues"""
        self.stdout.write('🔍 Checking for performance issues...')
        
        issues = []
        
        # Check if DEBUG is enabled
        if getattr(settings, 'DEBUG', False):
            issues.append('DEBUG is enabled - should be False in production')
        
        # Check cache configuration
        cache_backend = settings.CACHES['default']['BACKEND']
        if 'dummy' in cache_backend.lower():
            issues.append('Using dummy cache backend - consider Redis or Memcached')
        
        # Check database connection pooling
        db_config = settings.DATABASES['default']
        if 'CONN_MAX_AGE' not in db_config or db_config.get('CONN_MAX_AGE', 0) == 0:
            issues.append('Database connection pooling not configured')
        
        # Check static file serving
        if not hasattr(settings, 'STATICFILES_STORAGE'):
            issues.append('Static file compression not configured')
        
        if issues:
            self.stdout.write('⚠️ Performance issues found:')
            for issue in issues:
                self.stdout.write(f'  • {issue}')
        else:
            self.stdout.write('✅ No obvious performance issues found')
