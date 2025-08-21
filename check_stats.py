#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skylinegh.settings')
django.setup()

from core.models import SiteSettings

def main():
    print("Checking site statistics...")
    
    try:
        site_settings = SiteSettings.objects.first()
        
        if site_settings:
            print(f"✅ Site settings found:")
            print(f"   Projects Completed: {getattr(site_settings, 'projects_completed', 'Field not found')}")
            print(f"   Square Feet Built: {getattr(site_settings, 'square_feet_built', 'Field not found')}")
            print(f"   Client Satisfaction: {getattr(site_settings, 'client_satisfaction', 'Field not found')}%")
            print(f"   Years Experience: {getattr(site_settings, 'years_experience', 'Field not found')}")
            
            # Check if fields exist but are zero
            if hasattr(site_settings, 'projects_completed'):
                if site_settings.projects_completed == 0:
                    print("⚠️ Projects completed is 0 - updating to default value")
                    site_settings.projects_completed = 500
                    site_settings.save()
                    
            if hasattr(site_settings, 'square_feet_built'):
                if site_settings.square_feet_built == 0:
                    print("⚠️ Square feet built is 0 - updating to default value")
                    site_settings.square_feet_built = 1000000
                    site_settings.save()
                    
            if hasattr(site_settings, 'client_satisfaction'):
                if site_settings.client_satisfaction == 0:
                    print("⚠️ Client satisfaction is 0 - updating to default value")
                    site_settings.client_satisfaction = 98
                    site_settings.save()
                    
            if hasattr(site_settings, 'years_experience'):
                if site_settings.years_experience == 0:
                    print("⚠️ Years experience is 0 - updating to default value")
                    site_settings.years_experience = 25
                    site_settings.save()
                    
        else:
            print("❌ No site settings found - creating default settings")
            site_settings = SiteSettings.objects.create(
                site_name="Skyline Ghana Constructions",
                site_tagline="Building Dreams, Creating Futures",
                projects_completed=500,
                square_feet_built=1000000,
                client_satisfaction=98,
                years_experience=25
            )
            print("✅ Default site settings created")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
        
    # Clear cache
    try:
        from django.core.cache import cache
        cache.delete('site_settings_v2')
        print("✅ Cache cleared")
    except Exception as e:
        print(f"⚠️ Cache clear warning: {e}")
        
    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎯 Next steps:")
        print("1. Check your local development site: http://127.0.0.1:8000/projects/")
        print("2. If working locally, deploy to production using the deployment guide")
        print("3. Update statistics in admin panel: /my-admin/settings/")
    else:
        print("\n❌ Please fix the errors above and try again")
