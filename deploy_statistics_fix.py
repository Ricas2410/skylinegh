#!/usr/bin/env python3
"""
Deployment script to fix statistics display on production site.
Run this script on your production server to apply the statistics fixes.
"""

import os
import sys
import subprocess
import django
from pathlib import Path

# Add the project directory to Python path
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skylinegh.production_settings')

# Setup Django
django.setup()

from django.core.management import execute_from_command_line
from django.core.cache import cache
from core.models import SiteSettings


def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        if isinstance(command, list):
            result = subprocess.run(command, check=True, capture_output=True, text=True)
        else:
            result = subprocess.run(command.split(), check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stdout:
            print(f"STDOUT: {e.stdout}")
        if e.stderr:
            print(f"STDERR: {e.stderr}")
        return False


def main():
    print("🚀 Starting statistics fix deployment...")
    
    # 1. Pull latest changes from git
    print("\n📥 Pulling latest changes...")
    if run_command("git pull origin main", "Git pull"):
        print("✅ Latest changes pulled")
    else:
        print("⚠️ Git pull failed - continuing anyway")
    
    # 2. Install/update dependencies
    print("\n📦 Installing dependencies...")
    run_command("pip install -r requirements.txt", "Dependencies installation")
    
    # 3. Run database migrations
    print("\n📊 Running database migrations...")
    try:
        execute_from_command_line(['manage.py', 'migrate'])
        print("✅ Database migrations completed")
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return False
    
    # 4. Collect static files
    print("\n📦 Collecting static files...")
    try:
        execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])
        print("✅ Static files collected")
    except Exception as e:
        print(f"❌ Static collection failed: {e}")
    
    # 5. Clear cache
    print("\n🧹 Clearing cache...")
    try:
        cache.clear()
        cache.delete('site_settings_v2')
        print("✅ Cache cleared")
    except Exception as e:
        print(f"❌ Cache clearing failed: {e}")
    
    # 6. Update site settings with default statistics
    print("\n⚙️ Setting up site statistics...")
    try:
        site_settings, created = SiteSettings.objects.get_or_create(pk=1)
        
        # Update statistics if they're not set or are zero
        updated = False
        if not hasattr(site_settings, 'projects_completed') or site_settings.projects_completed == 0:
            site_settings.projects_completed = 500
            updated = True
        
        if not hasattr(site_settings, 'square_feet_built') or site_settings.square_feet_built == 0:
            site_settings.square_feet_built = 1000000
            updated = True
        
        if not hasattr(site_settings, 'client_satisfaction') or site_settings.client_satisfaction == 0:
            site_settings.client_satisfaction = 98
            updated = True
        
        if not hasattr(site_settings, 'years_experience') or site_settings.years_experience == 0:
            site_settings.years_experience = 25
            updated = True
        
        if updated:
            site_settings.save()
            print("✅ Site statistics updated with default values")
        else:
            print("✅ Site statistics already configured")
            
        # Display current values
        print(f"📊 Current statistics:")
        print(f"   Projects Completed: {getattr(site_settings, 'projects_completed', 'Not set')}")
        print(f"   Square Feet Built: {getattr(site_settings, 'square_feet_built', 'Not set')}")
        print(f"   Client Satisfaction: {getattr(site_settings, 'client_satisfaction', 'Not set')}%")
        print(f"   Years Experience: {getattr(site_settings, 'years_experience', 'Not set')}")
        
    except Exception as e:
        print(f"❌ Site settings update failed: {e}")
    
    # 7. Restart web server (if using systemd)
    print("\n🔄 Restarting web server...")
    restart_commands = [
        "sudo systemctl restart gunicorn",
        "sudo systemctl restart nginx",
        "sudo service apache2 restart",
        "sudo service nginx restart"
    ]
    
    for cmd in restart_commands:
        if run_command(cmd, f"Restart with {cmd}"):
            break
    else:
        print("⚠️ Could not restart web server automatically")
        print("💡 Please manually restart your web server (gunicorn/apache/nginx)")
    
    print("\n✅ Deployment completed!")
    print("\n📋 Next steps:")
    print("1. Check your website to see if statistics are now showing")
    print("2. Go to /my-admin/settings/ to customize the statistics")
    print("3. Clear browser cache if you still see old values")
    print("4. Check that the web server restarted successfully")


if __name__ == "__main__":
    main()
