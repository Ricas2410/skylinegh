from django.contrib import admin
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import SiteSettings, ContactInquiry, Testimonial, TeamMember, AboutSectionImage, HomepageCarouselImage
from dashboard.models import ActivityLog


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    class AboutSectionImageInline(admin.TabularInline):
        model = AboutSectionImage
        extra = 0
        max_num = 10
        fields = ("image_preview", "image", "order", "is_active")
        readonly_fields = ("image_preview",)
        ordering = ("order", "id")
        verbose_name = "About Section Image"
        verbose_name_plural = "About Section Images"

        def image_preview(self, obj):
            if obj.image:
                return mark_safe(f'<img src="{obj.image.url}" style="max-height: 60px; max-width: 100px; border-radius: 4px;" />')
            return "No image"
        image_preview.short_description = "Preview"

    class HomepageCarouselImageInline(admin.TabularInline):
        model = HomepageCarouselImage
        extra = 0
        max_num = 10
        fields = ("image_preview", "image", "caption", "order", "is_active")
        readonly_fields = ("image_preview",)
        ordering = ("order", "id")
        verbose_name = "Homepage Carousel Image"
        verbose_name_plural = "Homepage Carousel Images"

        def image_preview(self, obj):
            if obj.image:
                return mark_safe(f'<img src="{obj.image.url}" style="max-height: 60px; max-width: 100px; border-radius: 4px;" />')
            return "No image"
        image_preview.short_description = "Preview"

    list_display = ('site_name', 'site_tagline', 'phone_primary', 'email_primary', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    search_fields = ('site_name', 'site_tagline', 'phone_primary', 'email_primary')

    fieldsets = (
        ('Basic Information', {
            'fields': ('site_name', 'site_tagline')
        }),
        ('Contact Information', {
            'fields': ('phone_primary', 'phone_secondary', 'email_primary', 'email_secondary',
                      'address_line_1', 'address_line_2', 'city', 'region', 'postal_code', 'country')
        }),
        ('Top Navbar', {
            'fields': ('top_navbar_email', 'top_navbar_phone')
        }),
        ('Branding', {
            'fields': ('logo', 'favicon')
        }),
        ('Hero Images', {
            'fields': ('hero_background', 'hero_card_image', 'services_hero_image', 'about_hero_image',
                      'contact_hero_image', 'projects_hero_image', 'careers_hero_image', 'blog_hero_image'),
            'description': 'Upload custom hero background images for different pages. If not uploaded, default fallback images will be used.'
        }),
        ('Featured Service Images', {
            'fields': ('featured_service_1_image', 'featured_service_2_image', 'featured_service_3_image'),
            'description': 'Background images for the three featured service cards on the homepage.'
        }),
        ('Content Images', {
            'fields': ('about_company_image', 'why_choose_us_image'),
            'description': 'Images used in various content sections throughout the site.'
        }),
        ('Default Images', {
            'fields': ('default_testimonial_image', 'default_team_member_image'),
            'description': 'Fallback images used when testimonials or team members don\'t have photos uploaded.'
        }),
        ('Hero Content', {
            'fields': ('hero_title', 'hero_subtitle')
        }),
        ('Social Media', {
            'fields': ('linkedin_url', 'facebook_url', 'instagram_url', 'twitter_url')
        }),
        ('Navigation', {
            'fields': ('blog_url', 'show_blog_in_top_nav', 'get_in_touch_text')
        }),
        ('Analytics', {
            'fields': ('google_analytics_id',)
        }),
        ('Other', {
            'fields': ('business_hours',)
        })
    )

    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }

    fieldsets = (
        ('Basic Information', {
            'fields': ('site_name', 'site_tagline')
        }),
        ('Contact Information', {
            'fields': ('phone_primary', 'phone_secondary', 'email_primary', 'email_secondary')
        }),
        ('Address', {
            'fields': ('address_line_1', 'address_line_2', 'city', 'region', 'postal_code')
        }),
        ('Logo & Branding', {
            'fields': ('logo', 'favicon'),
            'description': 'Upload site logos and icons'
        }),
        ('Hero Section', {
            'fields': ('hero_title', 'hero_subtitle', 'hero_background', 'hero_card_image'),
            'description': 'Manage homepage hero content and images'
        }),
        ('Top Navigation Bar', {
            'fields': ('top_navbar_email', 'top_navbar_phone', 'blog_url', 'show_blog_in_top_nav', 'get_in_touch_text'),
            'description': 'Configure top navigation bar content',
            'classes': ('collapse',)
        }),
        ('Social Media', {
            'fields': ('linkedin_url', 'facebook_url', 'instagram_url', 'twitter_url', 'youtube_url'),
            'description': 'Social media profile URLs',
            'classes': ('collapse',)
        }),
        ('Page Hero Images', {
            'fields': ('services_hero_image', 'about_hero_image', 'contact_hero_image', 'projects_hero_image', 'careers_hero_image', 'blog_hero_image'),
            'description': 'Upload hero images for different pages',
            'classes': ('collapse',)
        }),
        ('Company Statistics', {
            'fields': ('projects_completed', 'square_feet_built', 'client_satisfaction', 'years_experience'),
            'description': 'Statistics displayed on the website (projects page, about page, etc.)',
        }),
        ('Analytics', {
            'fields': ('google_analytics_id',),
            'classes': ('collapse',)
        }),
        ('Business Information', {
            'fields': ('business_hours',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    inlines = [AboutSectionImageInline, HomepageCarouselImageInline]


@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'inquiry_type', 'subject', 'status', 'created_at')
    list_filter = ('inquiry_type', 'status', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('created_at', 'updated_at')
    list_editable = ('status',)
    list_per_page = 25
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }

    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone', 'company')
        }),
        ('Inquiry Details', {
            'fields': ('inquiry_type', 'subject', 'message')
        }),
        ('Status', {
            'fields': ('status', 'admin_response', 'responded_by', 'responded_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'rating', 'image_preview', 'is_featured', 'is_active', 'created_at')
    list_filter = ('rating', 'is_featured', 'is_active', 'created_at')
    search_fields = ('name', 'company', 'content')
    list_editable = ('is_featured', 'is_active')
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 20
    ordering = ('-is_featured', '-created_at')

    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'company', 'content', 'rating')
        }),
        ('Image', {
            'fields': ('image',)
        }),
        ('Display Options', {
            'fields': ('is_featured', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 4px;" />', obj.image.url)
        return "No image"
    image_preview.short_description = "Image"


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'years_experience', 'photo_preview', 'is_featured', 'is_active', 'order')
    list_filter = ('is_featured', 'is_active', 'years_experience', 'created_at')
    search_fields = ('name', 'position', 'bio', 'specializations')
    list_editable = ('is_featured', 'is_active', 'order')
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 20
    ordering = ('order', 'name')

    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'position', 'bio', 'detailed_bio')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone', 'linkedin_url'),
            'classes': ('collapse',)
        }),
        ('Images', {
            'fields': ('photo', 'cover_image'),
            'description': 'Upload professional photos'
        }),
        ('Professional Details', {
            'fields': ('years_experience', 'specializations', 'education', 'certifications'),
            'description': 'Enter each item on a new line'
        }),
        ('Display Options', {
            'fields': ('is_featured', 'is_active', 'order')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

    def photo_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 50%;" />', obj.photo.url)
        return "No photo"
    photo_preview.short_description = "Photo"


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'user', 'action', 'content_type', 'object_id', 'object_repr')
    list_filter = ('action', 'content_type', 'created_at')
    search_fields = ('user__username', 'content_type', 'object_repr', 'description', 'ip_address', 'user_agent')
    readonly_fields = ('created_at', 'updated_at')
