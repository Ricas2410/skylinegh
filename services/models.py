from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from core.models import TimeStampedModel
from PIL import Image
import os

class ServiceCategory(TimeStampedModel):
    """Main service categories as defined in overview.md"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField()
    short_description = models.CharField(max_length=200, help_text="Brief description for cards")
    icon = models.CharField(max_length=50, blank=True, help_text="CSS class for icon")
    image = models.ImageField(upload_to='services/categories/', blank=True)
    banner_image = models.ImageField(upload_to='services/banners/', blank=True)
    hero_image = models.ImageField(upload_to='services/heroes/', blank=True, help_text="Hero image for category page")

    # SEO fields
    meta_title = models.CharField(max_length=60, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    meta_keywords = models.TextField(blank=True)

    # Display options
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0, help_text="Display order")

    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Service Category"
        verbose_name_plural = "Service Categories"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('services:category_detail', kwargs={'slug': self.slug})


class ServicePageImage(models.Model):
    """Images for service category pages - allows admin to upload custom images for each service category"""
    category = models.ForeignKey('ServiceCategory', on_delete=models.CASCADE, related_name='page_images')
    title = models.CharField(max_length=200, help_text="Title/caption for the image")
    image = models.ImageField(upload_to='services/page_images/', help_text="Image for the service category page")
    description = models.TextField(blank=True, help_text="Optional description of the project/image")
    location = models.CharField(max_length=100, blank=True, help_text="Project location (optional)")
    completion_year = models.PositiveIntegerField(blank=True, null=True, help_text="Year completed (optional)")
    is_featured = models.BooleanField(default=False, help_text="Show this image prominently")
    order = models.PositiveIntegerField(default=0, help_text="Display order (lower numbers first)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = "Service Category Image"
        verbose_name_plural = "Service Category Images"

    def __str__(self):
        return f"{self.category.name} - {self.title}"

class Service(TimeStampedModel):
    """Individual services within categories"""
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, related_name='services')
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, blank=True)
    description = models.TextField()
    short_description = models.CharField(max_length=200, help_text="Brief description for listings")

    # Content for dedicated service pages
    detailed_description = models.TextField(blank=True, help_text="Detailed content for service page")
    features = models.TextField(blank=True, help_text="Key features, one per line")
    benefits = models.TextField(blank=True, help_text="Benefits, one per line")
    process_steps = models.TextField(blank=True, help_text="Process steps, one per line")

    # Media
    image = models.ImageField(upload_to='services/', blank=True)
    banner_image = models.ImageField(upload_to='services/banners/', blank=True)
    hero_image = models.ImageField(upload_to='services/heroes/', blank=True, help_text="Hero image for service page")

    # Pricing (optional)
    starting_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_unit = models.CharField(max_length=50, blank=True, help_text="e.g., per sq ft, per project")

    # SEO fields
    meta_title = models.CharField(max_length=60, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    meta_keywords = models.TextField(blank=True)

    # Display options
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0, help_text="Display order within category")

    class Meta:
        ordering = ['category', 'order', 'name']
        unique_together = ['category', 'slug']
        verbose_name = "Service"
        verbose_name_plural = "Services"

    def __str__(self):
        return f"{self.category.name} - {self.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('services:service_detail', kwargs={
            'category_slug': self.category.slug,
            'service_slug': self.slug
        })

    def get_features_list(self):
        """Return features as a list"""
        if self.features:
            return [feature.strip() for feature in self.features.split('\n') if feature.strip()]
        return []

    def get_benefits_list(self):
        """Return benefits as a list"""
        if self.benefits:
            return [benefit.strip() for benefit in self.benefits.split('\n') if benefit.strip()]
        return []

    def get_process_steps_list(self):
        """Return process steps as a list"""
        if self.process_steps:
            return [step.strip() for step in self.process_steps.split('\n') if step.strip()]
        return []

class ServiceImage(TimeStampedModel):
    """Additional images for services"""
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='services/gallery/')
    caption = models.CharField(max_length=200, blank=True)
    alt_text = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Service Image"
        verbose_name_plural = "Service Images"

    def __str__(self):
        return f"{self.service.name} - Image {self.id}"

class ServiceHighlight(TimeStampedModel):
    """Highlight boxes for service categories (admin configurable)"""
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, related_name='highlights')
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50, blank=True, help_text="CSS class for icon")
    image = models.ImageField(upload_to='services/highlights/', blank=True)
    link_url = models.URLField(blank=True, help_text="Optional link URL")
    link_text = models.CharField(max_length=50, blank=True, help_text="Link button text")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'title']
        verbose_name = "Service Highlight"
        verbose_name_plural = "Service Highlights"

    def __str__(self):
        return f"{self.category.name} - {self.title}"
