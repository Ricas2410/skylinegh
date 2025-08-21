#!/usr/bin/env python
import os
import sys
import django
from datetime import datetime, timedelta

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skylinegh.settings')
django.setup()

from django.utils import timezone
from dashboard.models import SystemMetrics
from django.test import RequestFactory
from core.middleware import VisitorTrackingMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.sessions.backends.db import SessionStore

def main():
    print("🔍 Debugging Visitor Tracking...")
    
    # Check current visitor metrics
    print("\n📊 Current Visitor Metrics:")
    today = timezone.localdate()
    yesterday = today - timedelta(days=1)
    week_ago = today - timedelta(days=7)
    
    try:
        # Today's visitors
        today_metric = SystemMetrics.objects.filter(
            metric_name="visitors",
            metric_date=today
        ).first()
        print(f"   Today ({today}): {today_metric.metric_value if today_metric else 0}")
        
        # Yesterday's visitors
        yesterday_metric = SystemMetrics.objects.filter(
            metric_name="visitors", 
            metric_date=yesterday
        ).first()
        print(f"   Yesterday ({yesterday}): {yesterday_metric.metric_value if yesterday_metric else 0}")
        
        # All visitor metrics
        all_metrics = SystemMetrics.objects.filter(metric_name="visitors").order_by('-metric_date')[:10]
        print(f"\n📈 Recent visitor metrics:")
        for metric in all_metrics:
            print(f"   {metric.metric_date}: {metric.metric_value}")
            
    except Exception as e:
        print(f"❌ Error reading metrics: {e}")
        return False
    
    # Test the middleware directly
    print(f"\n🧪 Testing Visitor Tracking Middleware...")
    
    try:
        # Create a test request
        factory = RequestFactory()
        request = factory.get('/')
        
        # Add session middleware
        session_middleware = SessionMiddleware(lambda r: None)
        session_middleware.process_request(request)
        request.session.save()
        
        # Create visitor tracking middleware
        visitor_middleware = VisitorTrackingMiddleware(lambda r: None)
        
        print(f"   Request path: {request.path}")
        print(f"   Request method: {request.method}")
        print(f"   Session key: {request.session.session_key}")
        
        # Check if path would be excluded
        excluded = any(request.path.startswith(p) for p in visitor_middleware.EXCLUDED_PREFIXES)
        print(f"   Path excluded: {excluded}")
        
        # Get current count before
        before_metric = SystemMetrics.objects.filter(
            metric_name="visitors",
            metric_date=today
        ).first()
        before_count = before_metric.metric_value if before_metric else 0
        print(f"   Visitors before: {before_count}")
        
        # Test the tracking
        visitor_middleware._maybe_track(request)
        
        # Get count after
        after_metric = SystemMetrics.objects.filter(
            metric_name="visitors",
            metric_date=today
        ).first()
        after_count = after_metric.metric_value if after_metric else 0
        print(f"   Visitors after: {after_count}")
        print(f"   Increment: {after_count - before_count}")
        
        # Test session tracking (should not increment again)
        print(f"\n🔄 Testing session tracking (should not increment)...")
        visitor_middleware._maybe_track(request)
        
        final_metric = SystemMetrics.objects.filter(
            metric_name="visitors",
            metric_date=today
        ).first()
        final_count = final_metric.metric_value if final_metric else 0
        print(f"   Final count: {final_count}")
        print(f"   Second increment: {final_count - after_count} (should be 0)")
        
        # Check session data
        today_key = f"visited:{today.isoformat()}"
        print(f"   Session key '{today_key}': {request.session.get(today_key)}")
        
    except Exception as e:
        print(f"❌ Error testing middleware: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test with different paths
    print(f"\n🛣️ Testing different paths...")
    test_paths = [
        '/',
        '/projects/',
        '/about/',
        '/admin/',  # Should be excluded
        '/static/css/style.css',  # Should be excluded
        '/my-admin/',  # Should be excluded
    ]
    
    for path in test_paths:
        try:
            request = factory.get(path)
            session_middleware.process_request(request)
            request.session.save()
            
            excluded = any(path.startswith(p) for p in visitor_middleware.EXCLUDED_PREFIXES)
            print(f"   {path}: {'EXCLUDED' if excluded else 'TRACKED'}")
            
        except Exception as e:
            print(f"   {path}: ERROR - {e}")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n❌ Debug failed - there are issues to fix")
    else:
        print("\n✅ Debug completed - check results above")
