#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skylinegh.settings')
django.setup()

from django.test import RequestFactory
from core.context_processors import site_settings
from core.models import SiteSettings

def main():
    print("🔍 Debugging context processor...")
    
    # Check if SiteSettings exists
    try:
        site_settings_obj = SiteSettings.objects.first()
        if site_settings_obj:
            print(f"✅ SiteSettings found in database:")
            print(f"   ID: {site_settings_obj.id}")
            print(f"   Projects: {getattr(site_settings_obj, 'projects_completed', 'MISSING')}")
            print(f"   Sq Ft: {getattr(site_settings_obj, 'square_feet_built', 'MISSING')}")
            print(f"   Satisfaction: {getattr(site_settings_obj, 'client_satisfaction', 'MISSING')}")
            print(f"   Experience: {getattr(site_settings_obj, 'years_experience', 'MISSING')}")
        else:
            print("❌ No SiteSettings found in database")
            return False
    except Exception as e:
        print(f"❌ Error accessing SiteSettings: {e}")
        return False
    
    # Test context processor
    try:
        factory = RequestFactory()
        request = factory.get('/')
        
        context = site_settings(request)
        print(f"\n🔧 Context processor result:")
        print(f"   Context keys: {list(context.keys())}")
        
        if 'site_settings' in context:
            settings = context['site_settings']
            print(f"   site_settings type: {type(settings)}")
            print(f"   Projects: {getattr(settings, 'projects_completed', 'MISSING')}")
            print(f"   Sq Ft: {getattr(settings, 'square_feet_built', 'MISSING')}")
            print(f"   Satisfaction: {getattr(settings, 'client_satisfaction', 'MISSING')}")
            print(f"   Experience: {getattr(settings, 'years_experience', 'MISSING')}")
        else:
            print("   ❌ 'site_settings' not in context")
            
    except Exception as e:
        print(f"❌ Error testing context processor: {e}")
        return False
    
    # Test template rendering
    try:
        from django.template import Template, Context
        from django.template.loader import get_template
        
        print(f"\n🎨 Testing template rendering...")
        
        # Create a simple test template
        template_content = """
        Projects: {{ site_settings.projects_completed|default:"NOT_FOUND" }}
        Sq Ft: {{ site_settings.square_feet_built|default:"NOT_FOUND" }}
        Satisfaction: {{ site_settings.client_satisfaction|default:"NOT_FOUND" }}
        Experience: {{ site_settings.years_experience|default:"NOT_FOUND" }}
        """
        
        template = Template(template_content)
        context = Context(site_settings(request))
        rendered = template.render(context)
        
        print("   Rendered template:")
        print(rendered)
        
    except Exception as e:
        print(f"❌ Error testing template: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n❌ Debug failed - there are issues to fix")
    else:
        print("\n✅ Debug completed - check results above")
