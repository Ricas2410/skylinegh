from django.core.management.base import BaseCommand
from django.utils import timezone
from dashboard.models import SystemMetrics
from datetime import timedelta


class Command(BaseCommand):
    help = 'Debug and fix visitor tracking issues'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset-today',
            action='store_true',
            help='Reset today\'s visitor count to 0',
        )
        parser.add_argument(
            '--add-test-data',
            action='store_true',
            help='Add test visitor data for the past week',
        )
        parser.add_argument(
            '--show-stats',
            action='store_true',
            help='Show current visitor statistics',
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('🔍 Visitor Tracking Debug Tool')
        )

        if options['show_stats']:
            self.show_statistics()

        if options['reset_today']:
            self.reset_today()

        if options['add_test_data']:
            self.add_test_data()

        if not any([options['show_stats'], options['reset_today'], options['add_test_data']]):
            self.show_statistics()

    def show_statistics(self):
        """Show current visitor statistics"""
        self.stdout.write("\n📊 Current Visitor Statistics:")
        
        today = timezone.localdate()
        
        # Show recent metrics
        recent_metrics = SystemMetrics.objects.filter(
            metric_name="visitors"
        ).order_by('-metric_date')[:14]  # Last 2 weeks
        
        if not recent_metrics:
            self.stdout.write(
                self.style.WARNING("   ❌ No visitor metrics found!")
            )
            return
        
        total_visitors = 0
        for metric in recent_metrics:
            days_ago = (today - metric.metric_date).days
            if days_ago == 0:
                label = "Today"
            elif days_ago == 1:
                label = "Yesterday"
            else:
                label = f"{days_ago} days ago"
                
            self.stdout.write(f"   {metric.metric_date} ({label}): {int(metric.metric_value)}")
            total_visitors += metric.metric_value
        
        self.stdout.write(f"\n   📈 Total visitors (last {len(recent_metrics)} days): {int(total_visitors)}")
        
        # Check today's metric specifically
        today_metric = SystemMetrics.objects.filter(
            metric_name="visitors",
            metric_date=today
        ).first()
        
        if today_metric:
            self.stdout.write(
                self.style.SUCCESS(f"   ✅ Today's tracking is active: {int(today_metric.metric_value)} visitors")
            )
        else:
            self.stdout.write(
                self.style.WARNING("   ⚠️ No visitors recorded today - tracking may not be working")
            )

    def reset_today(self):
        """Reset today's visitor count"""
        today = timezone.localdate()
        
        metric, created = SystemMetrics.objects.get_or_create(
            metric_name="visitors",
            metric_date=today,
            defaults={"metric_value": 0}
        )
        
        if not created:
            old_value = metric.metric_value
            metric.metric_value = 0
            metric.save()
            self.stdout.write(
                self.style.SUCCESS(f"✅ Reset today's visitors from {int(old_value)} to 0")
            )
        else:
            self.stdout.write(
                self.style.SUCCESS("✅ Created today's visitor metric (set to 0)")
            )

    def add_test_data(self):
        """Add test visitor data for the past week"""
        self.stdout.write("\n🧪 Adding test visitor data...")
        
        today = timezone.localdate()
        test_data = [
            (0, 5),   # Today: 5 visitors
            (1, 12),  # Yesterday: 12 visitors
            (2, 8),   # 2 days ago: 8 visitors
            (3, 15),  # 3 days ago: 15 visitors
            (4, 10),  # 4 days ago: 10 visitors
            (5, 7),   # 5 days ago: 7 visitors
            (6, 9),   # 6 days ago: 9 visitors
        ]
        
        for days_ago, visitor_count in test_data:
            date = today - timedelta(days=days_ago)
            
            metric, created = SystemMetrics.objects.get_or_create(
                metric_name="visitors",
                metric_date=date,
                defaults={"metric_value": visitor_count}
            )
            
            if created:
                self.stdout.write(f"   ✅ Added {visitor_count} visitors for {date}")
            else:
                old_value = metric.metric_value
                metric.metric_value = visitor_count
                metric.save()
                self.stdout.write(f"   🔄 Updated {date}: {int(old_value)} → {visitor_count} visitors")
        
        self.stdout.write(
            self.style.SUCCESS("✅ Test data added successfully!")
        )
