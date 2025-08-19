from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import BlogCategory, BlogTag, BlogPost, BlogComment


@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'color_preview', 'order', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    list_editable = ('order', 'is_active')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('order', 'name')
    list_per_page = 20

    def color_preview(self, obj):
        return format_html(
            '<div style="width: 20px; height: 20px; background-color: {}; border-radius: 50%; display: inline-block;"></div>',
            obj.color
        )
    color_preview.short_description = "Color"

    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }


@admin.register(BlogTag)
class BlogTagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name',)
    list_per_page = 30

    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'status', 'is_featured', 'views_count', 'published_at')
    list_filter = ('status', 'is_featured', 'category', 'author', 'created_at', 'published_at')
    search_fields = ('title', 'excerpt', 'content', 'meta_title')
    list_editable = ('status', 'is_featured')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('tags',)
    date_hierarchy = 'published_at'
    ordering = ('-published_at', '-created_at')
    list_per_page = 20

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'excerpt', 'content')
        }),
        ('Publishing', {
            'fields': ('author', 'status', 'published_at')
        }),
        ('Categorization', {
            'fields': ('category', 'tags')
        }),
        ('Media', {
            'fields': ('featured_image', 'featured_image_alt'),
            'classes': ('collapse',)
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
        ('Display Options', {
            'fields': ('is_featured', 'allow_comments'),
            'classes': ('collapse',)
        }),
        ('Statistics', {
            'fields': ('views_count', 'likes_count'),
            'classes': ('collapse',)
        })
    )

    readonly_fields = ('views_count', 'likes_count')

    def save_model(self, request, obj, form, change):
        if not change:  # If creating new post
            obj.author = request.user
        super().save_model(request, obj, form, change)

    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }


@admin.register(BlogComment)
class BlogCommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'post', 'status', 'created_at', 'moderated_by')
    list_filter = ('status', 'created_at', 'moderated_by')
    search_fields = ('name', 'email', 'content', 'post__title')
    list_editable = ('status',)
    readonly_fields = ('ip_address', 'user_agent', 'created_at', 'updated_at')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    list_per_page = 25

    fieldsets = (
        ('Comment Information', {
            'fields': ('post', 'name', 'email', 'website', 'content')
        }),
        ('Moderation', {
            'fields': ('status', 'moderated_by', 'moderated_at')
        }),
        ('Threading', {
            'fields': ('parent',),
            'classes': ('collapse',)
        }),
        ('Technical', {
            'fields': ('ip_address', 'user_agent', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

    actions = ['approve_comments', 'reject_comments']

    def approve_comments(self, request, queryset):
        for comment in queryset:
            comment.approve(request.user)
        self.message_user(request, f"{queryset.count()} comments approved.")
    approve_comments.short_description = "Approve selected comments"

    def reject_comments(self, request, queryset):
        for comment in queryset:
            comment.reject(request.user)
        self.message_user(request, f"{queryset.count()} comments rejected.")
    reject_comments.short_description = "Reject selected comments"

    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }
