from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from PIL import Image
import os

class TimeStampedModel(models.Model):
    """Abstract base model with created and updated timestamps"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class SiteSettings(models.Model):
    """Site-wide settings and configuration"""
    site_name = models.CharField(max_length=100, default="Skyline Ghana Constructions")
    site_tagline = models.CharField(max_length=200, default="Building Dreams, Creating Futures")
    site_description = models.TextField(default="Professional construction services in Ghana")

    # Contact Information
    phone_primary = models.CharField(max_length=20, blank=True)
    phone_secondary = models.CharField(max_length=20, blank=True)
    email_primary = models.EmailField(blank=True)
    email_secondary = models.EmailField(blank=True)

    # Address
    address_line_1 = models.CharField(max_length=200, blank=True)
    address_line_2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=100, blank=True)
    region = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)

    # GPS Coordinates for map
    latitude = models.DecimalField(max_digits=10, decimal_places=8, blank=True, null=True, help_text="Latitude for Google Maps")
    longitude = models.DecimalField(max_digits=11, decimal_places=8, blank=True, null=True, help_text="Longitude for Google Maps")

    # Social Media
    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)

    # SEO
    meta_keywords = models.TextField(blank=True, help_text="Comma-separated keywords")
    meta_description = models.TextField(max_length=160, blank=True)

    # Business Hours
    business_hours = models.TextField(blank=True, help_text="Business hours information")

    # Logo and Images
    logo = models.ImageField(upload_to='site/', blank=True)
    favicon = models.ImageField(upload_to='site/', blank=True)

    # Hero Images
    hero_background = models.ImageField(upload_to='site/heroes/', blank=True, help_text="Main hero background image")
    hero_card_image = models.ImageField(upload_to='site/heroes/', blank=True, help_text="Hero section card image")
    services_hero_image = models.ImageField(upload_to='site/heroes/', blank=True, help_text="Hero image for services page")
    about_hero_image = models.ImageField(upload_to='site/heroes/', blank=True, help_text="Hero image for about page")
    contact_hero_image = models.ImageField(upload_to='site/heroes/', blank=True, help_text="Hero image for contact page")
    projects_hero_image = models.ImageField(upload_to='site/heroes/', blank=True, help_text="Hero image for projects page")
    careers_hero_image = models.ImageField(upload_to='site/heroes/', blank=True, help_text="Hero image for careers page")
    blog_hero_image = models.ImageField(upload_to='site/heroes/', blank=True, help_text="Hero image for blog page")

    # Featured Service Images (Homepage)
    featured_service_1_image = models.ImageField(upload_to='site/services/', blank=True, help_text="Background image for first featured service card (Construction)")
    featured_service_2_image = models.ImageField(upload_to='site/services/', blank=True, help_text="Background image for second featured service card (Design)")
    featured_service_3_image = models.ImageField(upload_to='site/services/', blank=True, help_text="Background image for third featured service card (Materials)")

    # Content Section Images
    about_company_image = models.ImageField(upload_to='site/content/', blank=True, help_text="Company image for About page content section")
    why_choose_us_image = models.ImageField(upload_to='site/content/', blank=True, help_text="Image for 'Why Choose Us' section on homepage")
    join_team_left_image = models.ImageField(upload_to='site/content/', blank=True, help_text="Left side image for 'Join the Team' section on homepage")

    # Default Fallback Images
    default_testimonial_image = models.ImageField(upload_to='site/defaults/', blank=True, help_text="Default image for testimonials without photos")
    default_team_member_image = models.ImageField(upload_to='site/defaults/', blank=True, help_text="Default image for team members without photos")

    # Top Navbar Contact Information
    top_navbar_email = models.EmailField(blank=True, default="info@skylineghana.com", help_text="Email displayed in top navbar")
    top_navbar_phone = models.CharField(max_length=20, blank=True, default="+233 24 123 4567", help_text="Phone number displayed in top navbar")

    # Social Media Links
    linkedin_url = models.URLField(blank=True, help_text="LinkedIn profile URL")
    facebook_url = models.URLField(blank=True, help_text="Facebook page URL")
    instagram_url = models.URLField(blank=True, help_text="Instagram profile URL")
    twitter_url = models.URLField(blank=True, help_text="Twitter/X profile URL")

    # Navigation Content
    blog_url = models.URLField(blank=True, help_text="Blog URL (can be external)")
    show_blog_in_top_nav = models.BooleanField(default=True, help_text="Show blog link in top navigation")
    get_in_touch_text = models.CharField(max_length=50, default="Get in Touch", help_text="Text for the get in touch button")

    # Hero Content
    hero_title = models.CharField(max_length=200, default="Building the Future, Block by Block.", help_text="Main hero title")
    hero_subtitle = models.TextField(default="Skyline Ghana Constructions is a leading name in construction and design, transforming visions into reality with precision, innovation, and a commitment to quality.", help_text="Hero subtitle/description")

    # Analytics
    google_analytics_id = models.CharField(max_length=50, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return self.site_name

    def save(self, *args, **kwargs):
        # Resize logo and favicon if we have a local filesystem path (FileSystemStorage).
        # Remote storages (e.g., ImageKit) may not support .path; in that case we skip resizing.
        super().save(*args, **kwargs)

        def _resize_image_field(field, size):
            try:
                if not field:
                    return
                storage = field.storage
                # Some storages implement .path(name); others raise NotImplementedError
                if hasattr(storage, 'path'):
                    try:
                        path = storage.path(field.name)
                    except Exception:
                        return
                    if path and os.path.exists(path):
                        try:
                            img = Image.open(path)
                            img.thumbnail(size)
                            img.save(path)
                        except Exception:
                            # If PIL fails for any reason, just skip silently
                            pass
            except Exception:
                # Be defensive: never let media resizing break model save()
                pass

        _resize_image_field(self.logo, (600, 600))
        _resize_image_field(self.favicon, (128, 128))


class AboutSectionImage(TimeStampedModel):
    """Additional images for the About section tall image area"""
    site_settings = models.ForeignKey(SiteSettings, on_delete=models.CASCADE, related_name='about_images')
    image = models.ImageField(upload_to='site/about/')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "About Section Image"
        verbose_name_plural = "About Section Images"

    def __str__(self):
        return f"About Image #{self.pk} (order {self.order})"


class HomepageCarouselImage(TimeStampedModel):
    """Images for the homepage carousel section"""
    site_settings = models.ForeignKey(SiteSettings, on_delete=models.CASCADE, related_name='homepage_carousel_images')
    image = models.ImageField(upload_to='site/homepage_carousel/')
    caption = models.CharField(max_length=200, blank=True, help_text="Optional caption for the image")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Homepage Carousel Image"
        verbose_name_plural = "Homepage Carousel Images"

    def __str__(self):
        return f"Homepage Carousel Image #{self.pk} (order {self.order})"


class ContactInquiry(TimeStampedModel):
    """Contact form submissions"""
    INQUIRY_TYPES = [
        ('general', 'General Inquiry'),
        ('quote', 'Request Quote'),
        ('service', 'Service Information'),
        ('career', 'Career Inquiry'),
        ('complaint', 'Complaint'),
        ('other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    inquiry_type = models.CharField(max_length=20, choices=INQUIRY_TYPES, default='general')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')

    # Admin response
    admin_response = models.TextField(blank=True)
    responded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    responded_at = models.DateTimeField(null=True, blank=True)

    # Additional fields
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Contact Inquiry"
        verbose_name_plural = "Contact Inquiries"

    def __str__(self):
        return f"{self.name} - {self.subject}"

    def mark_as_responded(self, user, response):
        """Mark inquiry as responded with admin response"""
        self.admin_response = response
        self.responded_by = user
        self.responded_at = timezone.now()
        self.status = 'in_progress'
        self.save()

class Newsletter(TimeStampedModel):
    """Newsletter subscriptions"""
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    unsubscribed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-subscribed_at']
        verbose_name = "Newsletter Subscription"
        verbose_name_plural = "Newsletter Subscriptions"

    def __str__(self):
        return self.email

    def unsubscribe(self):
        """Unsubscribe from newsletter"""
        self.is_active = False
        self.unsubscribed_at = timezone.now()
        self.save()

class Testimonial(TimeStampedModel):
    """Client testimonials"""
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100, blank=True)
    company = models.CharField(max_length=100, blank=True)
    content = models.TextField()
    rating = models.PositiveIntegerField(default=5, help_text="Rating out of 5")
    image = models.ImageField(upload_to='testimonials/', blank=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-is_featured', '-created_at']
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"

    def __str__(self):
        return f"{self.name} - {self.rating}/5"


class TeamMember(TimeStampedModel):
    """Team member information"""
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    bio = models.TextField(help_text="Brief biography")
    detailed_bio = models.TextField(blank=True, help_text="Detailed biography for profile page")

    # Contact information
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    linkedin_url = models.URLField(blank=True)

    # Images
    photo = models.ImageField(upload_to='team/', help_text="Professional headshot")
    cover_image = models.ImageField(upload_to='team/covers/', blank=True, help_text="Cover image for profile page")

    # Professional details
    years_experience = models.PositiveIntegerField(default=0, help_text="Years of experience")
    specializations = models.TextField(blank=True, help_text="Areas of specialization, one per line")
    education = models.TextField(blank=True, help_text="Educational background")
    certifications = models.TextField(blank=True, help_text="Professional certifications, one per line")

    # Display options
    is_featured = models.BooleanField(default=False, help_text="Show on homepage")
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0, help_text="Display order")

    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Team Member"
        verbose_name_plural = "Team Members"

    def __str__(self):
        return f"{self.name} - {self.position}"

    def get_specializations_list(self):
        """Return specializations as a list"""
        if self.specializations:
            return [spec.strip() for spec in self.specializations.split('\n') if spec.strip()]
        return []

    def get_certifications_list(self):
        """Return certifications as a list"""
        if self.certifications:
            return [cert.strip() for cert in self.certifications.split('\n') if cert.strip()]
        return []
