from django.contrib import admin
from django.utils.html import format_html
from .models import ServiceCategory, Service, ServiceImage, ServicePageImage, ServiceHighlight


class ServiceImageInline(admin.TabularInline):
    model = ServiceImage
    extra = 1
    fields = ('image', 'caption', 'alt_text', 'order')


class ServiceHighlightInline(admin.TabularInline):
    model = ServiceHighlight
    extra = 1
    fields = ('title', 'description', 'icon', 'image', 'link_url', 'link_text', 'order', 'is_active')


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'short_description', 'image_preview', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description', 'short_description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')
    inlines = [ServiceHighlightInline]

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description', 'short_description', 'icon', 'is_active')
        }),
        ('Images', {
            'fields': ('image', 'banner_image', 'hero_image'),
            'description': 'Upload images for different sections of the category page'
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords'),
            'classes': ('collapse',)
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


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'short_description', 'starting_price', 'image_preview', 'is_featured', 'is_active')
    list_filter = ('category', 'is_featured', 'is_active', 'created_at')
    search_fields = ('name', 'description', 'short_description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')
    inlines = [ServiceImageInline]

    fieldsets = (
        ('Basic Information', {
            'fields': ('category', 'name', 'slug', 'description', 'short_description', 'detailed_description')
        }),
        ('Service Details', {
            'fields': ('features', 'benefits', 'process_steps'),
            'description': 'Enter each item on a new line'
        }),
        ('Images', {
            'fields': ('image', 'banner_image', 'hero_image'),
            'description': 'Upload images for different sections of the service page'
        }),
        ('Pricing', {
            'fields': ('starting_price', 'price_unit'),
            'classes': ('collapse',)
        }),
        ('Display Options', {
            'fields': ('is_featured', 'is_active', 'order')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords'),
            'classes': ('collapse',)
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


@admin.register(ServiceImage)
class ServiceImageAdmin(admin.ModelAdmin):
    list_display = ('service', 'caption', 'image_preview', 'order')
    list_filter = ('service__category', 'created_at')
    search_fields = ('service__name', 'caption', 'alt_text')

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 4px;" />', obj.image.url)
        return "No image"
    image_preview.short_description = "Image"


@admin.register(ServicePageImage)
class ServicePageImageAdmin(admin.ModelAdmin):
    list_display = ('category', 'title', 'image_preview', 'location', 'completion_year', 'is_featured', 'order')
    list_filter = ('category', 'is_featured', 'completion_year', 'created_at')
    search_fields = ('category__name', 'title', 'description', 'location')
    list_editable = ('order', 'is_featured')

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 4px;" />', obj.image.url)
        return "No image"
    image_preview.short_description = "Image"


@admin.register(ServiceHighlight)
class ServiceHighlightAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'image_preview', 'order', 'is_active')
    list_filter = ('category', 'is_active', 'created_at')
    search_fields = ('title', 'description')

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 4px;" />', obj.image.url)
        return "No image"
    image_preview.short_description = "Image"
