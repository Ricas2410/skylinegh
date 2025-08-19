from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from core.models import TimeStampedModel

class UserProfile(TimeStampedModel):
    """Extended user profile for dashboard users"""
    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('content_manager', 'Content Manager'),
        ('sales_staff', 'Sales Staff'),
        ('hr_manager', 'HR Manager'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='content_manager')
    phone = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to='profiles/', blank=True)
    bio = models.TextField(blank=True)

    # Permissions
    can_manage_projects = models.BooleanField(default=False)
    can_manage_services = models.BooleanField(default=False)
    can_manage_blog = models.BooleanField(default=False)
    can_manage_careers = models.BooleanField(default=False)
    can_manage_inquiries = models.BooleanField(default=False)
    can_manage_users = models.BooleanField(default=False)
    can_view_analytics = models.BooleanField(default=False)

    # Preferences
    email_notifications = models.BooleanField(default=True)
    dashboard_theme = models.CharField(max_length=20, default='light',
                                     choices=[('light', 'Light'), ('dark', 'Dark')])

    # Activity tracking
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    last_activity = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.role})"

    def update_last_activity(self):
        """Update last activity timestamp"""
        self.last_activity = timezone.now()
        self.save(update_fields=['last_activity'])

class DashboardWidget(TimeStampedModel):
    """Configurable dashboard widgets"""
    WIDGET_TYPES = [
        ('stats', 'Statistics'),
        ('chart', 'Chart'),
        ('recent_items', 'Recent Items'),
        ('quick_actions', 'Quick Actions'),
        ('notifications', 'Notifications'),
    ]

    name = models.CharField(max_length=100)
    widget_type = models.CharField(max_length=20, choices=WIDGET_TYPES)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    # Configuration
    config_json = models.JSONField(default=dict, blank=True)

    # Display options
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    width = models.PositiveIntegerField(default=6, help_text="Width in grid columns (1-12)")
    height = models.PositiveIntegerField(default=300, help_text="Height in pixels")

    # Permissions
    required_role = models.CharField(max_length=20, choices=UserProfile.ROLE_CHOICES, blank=True)
    required_permission = models.CharField(max_length=50, blank=True)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Dashboard Widget"
        verbose_name_plural = "Dashboard Widgets"

    def __str__(self):
        return self.title

class ActivityLog(TimeStampedModel):
    """Log of user activities in the dashboard"""
    ACTION_TYPES = [
        ('create', 'Created'),
        ('update', 'Updated'),
        ('delete', 'Deleted'),
        ('view', 'Viewed'),
        ('login', 'Logged In'),
        ('logout', 'Logged Out'),
        ('export', 'Exported'),
        ('import', 'Imported'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activity_logs')
    action = models.CharField(max_length=20, choices=ACTION_TYPES)
    content_type = models.CharField(max_length=50, blank=True, help_text="Type of content affected")
    object_id = models.PositiveIntegerField(null=True, blank=True)
    object_repr = models.CharField(max_length=200, blank=True, help_text="String representation of object")
    description = models.TextField(blank=True)

    # Request details
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Activity Log"
        verbose_name_plural = "Activity Logs"

    def __str__(self):
        return f"{self.user.username} {self.action} {self.content_type} at {self.created_at}"

class Notification(TimeStampedModel):
    """System notifications for dashboard users"""
    NOTIFICATION_TYPES = [
        ('info', 'Information'),
        ('success', 'Success'),
        ('warning', 'Warning'),
        ('error', 'Error'),
        ('inquiry', 'New Inquiry'),
        ('application', 'New Job Application'),
        ('comment', 'New Comment'),
    ]

    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, default='info')
    title = models.CharField(max_length=200)
    message = models.TextField()

    # Related object (optional)
    content_type = models.CharField(max_length=50, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    action_url = models.URLField(blank=True, help_text="URL to navigate when clicked")

    # Status
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"

    def __str__(self):
        return f"{self.title} for {self.recipient.username}"

    def mark_as_read(self):
        """Mark notification as read"""
        self.is_read = True
        self.read_at = timezone.now()
        self.save()

class SystemMetrics(TimeStampedModel):
    """Store system metrics for analytics"""
    metric_name = models.CharField(max_length=100)
    metric_value = models.FloatField()
    metric_date = models.DateField(default=timezone.now)

    # Additional context
    context = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['-metric_date', 'metric_name']
        unique_together = ['metric_name', 'metric_date']
        verbose_name = "System Metric"
        verbose_name_plural = "System Metrics"

    def __str__(self):
        return f"{self.metric_name}: {self.metric_value} ({self.metric_date})"
