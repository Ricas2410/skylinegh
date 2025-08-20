from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.utils import timezone
from datetime import datetime
from projects.models import Project
from services.models import Service, ServiceCategory
from blog.models import BlogPost
from careers.models import JobPosition

class StaticViewSitemap(Sitemap):
    """Sitemap for static pages"""
    priority = 0.9
    changefreq = 'weekly'
    protocol = 'https'

    def items(self):
        return [
            'core:home',
            'core:about',
            'core:contact',
            'projects:project_list',
            'projects:gallery',
            'careers:job_list',
            'blog:post_list',
            'services:service_list',
        ]

    def location(self, item):
        return reverse(item)

    def lastmod(self, item):
        # Return more specific last modified dates for different pages
        if item == 'core:home':
            return timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        return timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)

    def priority(self, item):
        # Set different priorities for different pages
        priorities = {
            'core:home': 1.0,
            'services:service_list': 0.9,
            'projects:project_list': 0.9,
            'core:about': 0.8,
            'core:contact': 0.8,
            'blog:post_list': 0.7,
            'careers:job_list': 0.6,
            'projects:gallery': 0.6,
        }
        return priorities.get(item, 0.5)

class ProjectSitemap(Sitemap):
    """Sitemap for project pages"""
    changefreq = 'monthly'
    priority = 0.8
    protocol = 'https'

    def items(self):
        return Project.objects.filter(is_published=True).order_by('-updated_at')

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return obj.get_absolute_url()

    def priority(self, obj):
        # Featured projects get higher priority
        return 0.9 if getattr(obj, 'is_featured', False) else 0.8

class ServiceSitemap(Sitemap):
    """Sitemap for service pages"""
    changefreq = 'monthly'
    priority = 0.9
    protocol = 'https'
    
    def items(self):
        return Service.objects.filter(is_active=True)
    
    def lastmod(self, obj):
        return obj.updated_at
    
    def location(self, obj):
        return obj.get_absolute_url()

class ServiceCategorySitemap(Sitemap):
    """Sitemap for service category pages"""
    changefreq = 'monthly'
    priority = 0.8
    protocol = 'https'
    
    def items(self):
        return ServiceCategory.objects.filter(is_active=True)
    
    def lastmod(self, obj):
        return obj.updated_at
    
    def location(self, obj):
        return obj.get_absolute_url()

class BlogSitemap(Sitemap):
    """Sitemap for blog posts"""
    changefreq = 'weekly'
    priority = 0.6
    
    def items(self):
        # BlogPost has 'status' and optional 'published_at' (no boolean 'is_published' field)
        # Only include posts actually published and with a publish timestamp
        return BlogPost.objects.filter(status='published', published_at__isnull=False)
    
    def lastmod(self, obj):
        return obj.updated_at
    
    def location(self, obj):
        return obj.get_absolute_url()

class JobSitemap(Sitemap):
    """Sitemap for job postings"""
    changefreq = 'weekly'
    priority = 0.7
    
    def items(self):
        # Use status field defined on JobPosition; 'active' means currently open
        return JobPosition.objects.filter(status='active')
    
    def lastmod(self, obj):
        return obj.updated_at
    
    def location(self, obj):
        return obj.get_absolute_url()
