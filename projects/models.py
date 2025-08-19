from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from core.models import TimeStampedModel
from core.mixins import SEOMixin, TimestampMixin, SlugMixin, StatusMixin
from services.models import ServiceCategory
from PIL import Image
import os

class ProjectCategory(TimeStampedModel):
    """Project categories for filtering"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=7, default='#0ea5e9', help_text="Hex color code")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Project Category"
        verbose_name_plural = "Project Categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Project(SEOMixin, TimeStampedModel):
    """Portfolio projects"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField()
    short_description = models.CharField(max_length=300, help_text="Brief description for listings")

    # Project details
    client_name = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=200)
    project_type = models.ForeignKey(ProjectCategory, on_delete=models.SET_NULL, null=True, blank=True)
    service_category = models.ForeignKey(ServiceCategory, on_delete=models.SET_NULL, null=True, blank=True)

    # Timeline
    start_date = models.DateField(null=True, blank=True)
    completion_date = models.DateField(null=True, blank=True)
    duration_months = models.PositiveIntegerField(null=True, blank=True, help_text="Project duration in months")

    # Project specifications
    area_sqft = models.PositiveIntegerField(null=True, blank=True, help_text="Area in square feet")
    budget_range = models.CharField(max_length=50, blank=True, help_text="e.g., $50K - $100K")
    team_size = models.PositiveIntegerField(null=True, blank=True)

    # Content
    challenges = models.TextField(blank=True, help_text="Challenges faced during the project")
    solutions = models.TextField(blank=True, help_text="Solutions implemented")
    technologies_used = models.TextField(blank=True, help_text="Technologies/materials used")
    client_testimonial = models.TextField(blank=True)

    # Media
    featured_image = models.ImageField(upload_to='projects/featured/')
    before_image = models.ImageField(upload_to='projects/before/', blank=True)
    after_image = models.ImageField(upload_to='projects/after/', blank=True)

    # Display options
    is_featured = models.BooleanField(default=False, help_text="Show on homepage")
    is_published = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0, help_text="Display order")

    # Stats
    views_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-is_featured', 'order', '-completion_date', '-created_at']
        verbose_name = "Project"
        verbose_name_plural = "Projects"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('projects:project_detail', kwargs={'slug': self.slug})

    def increment_views(self):
        """Increment view count"""
        self.views_count += 1
        self.save(update_fields=['views_count'])

    @property
    def status(self):
        """Get project status based on dates"""
        if not self.start_date:
            return "Planning"
        elif not self.completion_date:
            return "In Progress"
        else:
            return "Completed"

    @property
    def has_before_after(self):
        """Check if project has before/after images"""
        return bool(self.before_image and self.after_image)

class ProjectImage(TimeStampedModel):
    """Project gallery images"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='projects/gallery/')
    caption = models.CharField(max_length=200, blank=True)
    alt_text = models.CharField(max_length=200, blank=True)
    is_before_image = models.BooleanField(default=False)
    is_after_image = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Project Image"
        verbose_name_plural = "Project Images"

    def __str__(self):
        return f"{self.project.title} - Image {self.id}"

class ProjectTag(TimeStampedModel):
    """Tags for projects"""
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True)
    color = models.CharField(max_length=7, default='#6b7280', help_text="Hex color code")

    class Meta:
        ordering = ['name']
        verbose_name = "Project Tag"
        verbose_name_plural = "Project Tags"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

# Many-to-many relationship for project tags
Project.add_to_class('tags', models.ManyToManyField(ProjectTag, blank=True, related_name='projects'))
