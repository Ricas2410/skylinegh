from django.contrib import admin
from .models import Project, ProjectCategory, ProjectImage, ProjectTag


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1
    max_num = 20
    fields = ("image", "caption", "alt_text", "is_before_image", "is_after_image", "order")
    ordering = ("order", "id")
    verbose_name = "Project Image"
    verbose_name_plural = "Project Images"


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "project_type",
        "service_category",
        "location",
        "is_featured",
        "is_published",
        "order",
        "created_at"
    )
    list_filter = ("is_published", "is_featured", "project_type", "service_category", "created_at")
    search_fields = ("title", "description", "location", "client_name")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ProjectImageInline]
    list_editable = ("is_featured", "is_published", "order")
    list_per_page = 20
    date_hierarchy = 'created_at'
    ordering = ('-is_featured', 'order', '-created_at')

    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }
    fieldsets = (
        ("Basic Info", {"fields": ("title", "slug", "short_description", "description")}),
        (
            "Classification",
            {"fields": ("project_type", "service_category", "location", "client_name")},
        ),
        (
            "Timeline",
            {"fields": ("start_date", "completion_date", "duration_months")},
        ),
        (
            "Specifications",
            {"fields": ("area_sqft", "budget_range", "team_size")},
        ),
        (
            "Content",
            {"fields": ("challenges", "solutions", "technologies_used", "client_testimonial")},
        ),
        ("Media", {"fields": ("featured_image", "before_image", "after_image")}),
        (
            "SEO",
            {"fields": ("meta_title", "meta_description", "meta_keywords")},
        ),
        (
            "Display",
            {"fields": ("is_featured", "is_published", "order")},
        ),
    )


@admin.register(ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "is_active", "order")
    list_filter = ("is_active",)
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(ProjectImage)
class ProjectImageAdmin(admin.ModelAdmin):
    list_display = (
        "project",
        "caption",
        "is_before_image",
        "is_after_image",
        "order",
    )
    list_filter = ("is_before_image", "is_after_image", "project")
    search_fields = ("project__title", "caption", "alt_text")
    ordering = ("project", "order", "id")


@admin.register(ProjectTag)
class ProjectTagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}

# Register your models here.
