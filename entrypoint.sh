#!/bin/bash

set -euo pipefail

# Ensure we have the correct PATH for appuser
export PATH="/home/appuser/.local/bin:$PATH"

echo "🚀 Starting Skyline Ghana Constructions..."

# Function to check database connectivity
check_db() {
    python -c "
import django
django.setup()
from django.db import connections
try:
    connections['default'].cursor()
    print('✅ Database connected')
    exit(0)
except Exception as e:
    print(f'❌ Database error: {e}')
    exit(1)
"
}

# Wait for database with faster retries
echo "⏳ Waiting for database..."
RETRIES=15
until check_db; do
  RETRIES=$((RETRIES-1)) || true
  if [ "$RETRIES" -le 0 ]; then
    echo "❌ Database not ready after multiple attempts" >&2
    exit 1
  fi
  echo "🔄 DB not ready, retrying... ($RETRIES left)"
  sleep 1
done

# Run migrations only if needed
echo "🔄 Checking migrations..."
if python manage.py showmigrations --plan | grep -q '\[ \]'; then
    echo "📦 Applying migrations..."
    python manage.py migrate --noinput
else
    echo "✅ Migrations up to date"
fi

# Create cache table if needed
echo "🗄️ Setting up cache..."
python manage.py createcachetable 2>/dev/null || echo "✅ Cache table exists"

# Initialize site settings (only if needed)
echo "⚙️ Initializing site settings..."
python manage.py init_site_settings 2>/dev/null || echo "✅ Site settings exist"

# Update site statistics if they're zero (for new deployments)
echo "📊 Checking site statistics..."
python -c "
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skylinegh.production_settings')
django.setup()
from core.models import SiteSettings
try:
    s = SiteSettings.objects.first()
    if s and hasattr(s, 'projects_completed'):
        if s.projects_completed == 0:
            s.projects_completed = 500
            s.square_feet_built = 1000000
            s.client_satisfaction = 98
            s.years_experience = 25
            s.save()
            print('✅ Statistics updated with default values')
        else:
            print('✅ Statistics already configured')
    else:
        print('⚠️ Statistics fields not found - migration may be needed')
except Exception as e:
    print(f'⚠️ Statistics check failed: {e}')
" 2>/dev/null || echo "⚠️ Statistics check skipped"

# Skip sample data in production to save startup time
if [ "${POPULATE_SAMPLE_DATA:-false}" = "true" ]; then
    echo "📊 Populating sample data..."
    python manage.py populate_sample_data
else
    echo "⏭️ Skipping sample data (set POPULATE_SAMPLE_DATA=true to enable)"
fi

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput --clear

# Calculate optimal worker count
WORKERS=${WEB_CONCURRENCY:-2}
echo "🔧 Starting with $WORKERS workers"

echo "🌟 Starting Gunicorn server..."
exec gunicorn skylinegh.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers $WORKERS \
  --worker-class gthread \
  --threads 2 \
  --worker-connections 1000 \
  --max-requests 1000 \
  --max-requests-jitter 100 \
  --timeout 30 \
  --keep-alive 2 \
  --access-logfile '-' \
  --error-logfile '-' \
  --log-level info \
  --preload
