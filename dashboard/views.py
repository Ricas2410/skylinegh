from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponse
from django.core.management import call_command
from django.conf import settings
import io, os, zipfile, datetime
from django.db.models import Count, Q, Sum
from django.utils import timezone
from datetime import datetime, timedelta

from projects.models import Project, ProjectImage
from services.models import Service, ServiceCategory, ServicePageImage
from core.models import ContactInquiry, SiteSettings, Testimonial
from .models import ActivityLog, SystemMetrics
from careers.models import JobPosition, JobApplication
from blog.models import BlogPost
from django.contrib.auth.models import User
from .forms import SiteSettingsForm

class DashboardHomeView(LoginRequiredMixin, TemplateView):
    """Dashboard home page with analytics"""
    template_name = 'dashboard/home.html'
    login_url = '/my-admin/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get statistics
        context['total_projects'] = Project.objects.count()
        context['active_projects'] = Project.objects.filter(is_published=True).count()
        context['completed_projects'] = Project.objects.filter(is_published=True).count()
        context['total_inquiries'] = ContactInquiry.objects.count()
        context['new_inquiries'] = ContactInquiry.objects.filter(
            created_at__gte=timezone.now() - timedelta(days=7)
        ).count()
        context['total_jobs'] = JobPosition.objects.filter(status='active').count()
        context['total_applications'] = JobApplication.objects.count()
        context['new_applications'] = JobApplication.objects.filter(
            created_at__gte=timezone.now() - timedelta(days=7)
        ).count()

        # Visitor metrics
        today = timezone.localdate()
        context['visitors_today'] = SystemMetrics.objects.filter(
            metric_name='visitors', metric_date=today
        ).aggregate(total=Sum('metric_value'))['total'] or 0
        context['visitors_7d'] = SystemMetrics.objects.filter(
            metric_name='visitors', metric_date__gte=today - timedelta(days=6)
        ).aggregate(total=Sum('metric_value'))['total'] or 0
        context['visitors_30d'] = SystemMetrics.objects.filter(
            metric_name='visitors', metric_date__gte=today - timedelta(days=29)
        ).aggregate(total=Sum('metric_value'))['total'] or 0
        context['visitors_365d'] = SystemMetrics.objects.filter(
            metric_name='visitors', metric_date__gte=today - timedelta(days=364)
        ).aggregate(total=Sum('metric_value'))['total'] or 0
        series = []
        for i in range(13, -1, -1):
            d = today - timedelta(days=i)
            val = SystemMetrics.objects.filter(metric_name='visitors', metric_date=d).aggregate(total=Sum('metric_value'))['total'] or 0
            series.append({'date': d.isoformat(), 'value': int(val)})
        context['visitors_series'] = series

        # 180-day daily series for interactive ranges (14d/30d/90d)
        series_180 = []
        for i in range(179, -1, -1):
            d = today - timedelta(days=i)
            val = SystemMetrics.objects.filter(metric_name='visitors', metric_date=d).aggregate(total=Sum('metric_value'))['total'] or 0
            series_180.append({'date': d.isoformat(), 'value': int(val)})
        context['visitors_series_180d'] = series_180

        # Recent projects
        context['recent_projects'] = Project.objects.filter(
            is_published=True
        ).order_by('-created_at')[:5]

        # Recent inquiries
        context['recent_inquiries'] = ContactInquiry.objects.order_by('-created_at')[:5]

        # Recent applications
        context['recent_applications'] = JobApplication.objects.order_by('-created_at')[:5]

        # Categories
        context['total_services'] = Service.objects.count()
        context['active_services'] = Service.objects.filter(is_active=True).count()
        context['categories'] = ServiceCategory.objects.filter(is_active=True).order_by('order', 'name')
        context['selected_category'] = self.request.GET.get('category')

        return context

class DashboardLoginView(LoginView):
    """Dashboard login page"""
    template_name = 'dashboard/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return '/my-admin/'

    def form_valid(self, form):
        response = super().form_valid(form)
        try:
            ActivityLog.objects.create(
                user=self.request.user,
                action='login',
                model_name='User',
                object_id=str(self.request.user.pk),
                message='User logged in'
            )
        except Exception:
            pass
        return response

class DashboardLogoutView(LogoutView):
    """Dashboard logout"""
    next_page = '/my-admin/login/'

    def dispatch(self, request, *args, **kwargs):
        user = request.user if request.user.is_authenticated else None
        try:
            ActivityLog.objects.create(
                user=user,
                action='logout',
                model_name='User',
                object_id=str(user.pk) if user else '',
                message='User logged out'
            )
        except Exception:
            pass
        return super().dispatch(request, *args, **kwargs)

# Project Management Views
class ProjectListView(LoginRequiredMixin, ListView):
    """List all projects in dashboard"""
    model = Project
    template_name = 'dashboard/projects/list.html'
    context_object_name = 'projects'
    paginate_by = 20
    login_url = '/my-admin/login/'

    def get_queryset(self):
        queryset = Project.objects.all().order_by('-created_at')
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(location__icontains=search)
            )
        return queryset

class ProjectCreateView(LoginRequiredMixin, CreateView):
    """Create new project"""
    model = Project
    template_name = 'dashboard/projects/form.html'
    fields = [
        'title', 'short_description', 'description', 'location', 'client_name', 'project_type',
        'service_category', 'start_date', 'featured_image', 'is_featured', 'is_published'
    ]
    login_url = '/my-admin/login/'
    success_url = reverse_lazy('dashboard:project_list')

    def form_valid(self, form):
        messages.success(self.request, 'Project created successfully!')
        return super().form_valid(form)

class ServiceToggleActiveView(LoginRequiredMixin, TemplateView):
    """Toggle a service's active state and redirect back to list"""
    login_url = '/my-admin/login/'

    def post(self, request, *args, **kwargs):
        service = get_object_or_404(Service, pk=kwargs.get('pk'))
        service.is_active = not service.is_active
        service.save(update_fields=['is_active'])
        messages.success(request, f"Service '{service.name}' is now {'active' if service.is_active else 'inactive'}.")
        return redirect('dashboard:service_list')

class ServiceDeleteView(LoginRequiredMixin, DeleteView):
    """Delete a service"""
    model = Service
    template_name = 'dashboard/services/delete.html'
    login_url = '/my-admin/login/'
    success_url = reverse_lazy('dashboard:service_list')

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(request, f"Service '{obj.name}' deleted successfully!")
        return super().delete(request, *args, **kwargs)

class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    """Update existing project"""
    model = Project
    template_name = 'dashboard/projects/form.html'
    fields = [
        'title', 'short_description', 'description', 'location', 'client_name', 'project_type',
        'service_category', 'start_date', 'featured_image', 'is_featured', 'is_published'
    ]
    login_url = '/my-admin/login/'
    success_url = reverse_lazy('dashboard:project_list')

    def form_valid(self, form):
        messages.success(self.request, 'Project updated successfully!')
        return super().form_valid(form)

class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    """Delete project"""
    model = Project
    template_name = 'dashboard/projects/delete.html'
    login_url = '/my-admin/login/'
    success_url = reverse_lazy('dashboard:project_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Project deleted successfully!')
        return super().delete(request, *args, **kwargs)

# Service Management Views
class ServiceListView(LoginRequiredMixin, ListView):
    """List all services in dashboard"""
    model = Service
    template_name = 'dashboard/services/list.html'
    context_object_name = 'services'
    paginate_by = 20
    login_url = '/my-admin/login/'

    def get_queryset(self):
        qs = Service.objects.select_related('category').prefetch_related('category__project_set').all()
        category_id = self.request.GET.get('category')
        search = self.request.GET.get('q')
        if category_id:
            qs = qs.filter(category_id=category_id)
        if search:
            qs = qs.filter(Q(name__icontains=search) | Q(short_description__icontains=search) | Q(description__icontains=search))
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = Service.objects.all()
        context['total_services'] = qs.count()
        context['active_services'] = qs.filter(is_active=True).count()
        context['categories'] = ServiceCategory.objects.filter(is_active=True).order_by('order', 'name')
        context['selected_category'] = self.request.GET.get('category')
        return context

class ServiceCreateView(LoginRequiredMixin, CreateView):
    """Create new service"""
    model = Service
    template_name = 'dashboard/services/form.html'
    fields = [
        'name', 'category', 'short_description', 'description', 'detailed_description',
        'features', 'benefits', 'process_steps',
        'image', 'banner_image', 'hero_image',
        'starting_price', 'price_unit',
        'meta_title', 'meta_description', 'meta_keywords',
        'is_featured', 'is_active', 'order'
    ]
    login_url = '/my-admin/login/'
    success_url = reverse_lazy('dashboard:service_list')

    def form_valid(self, form):
        messages.success(self.request, 'Service created successfully!')
        return super().form_valid(form)

class ServiceUpdateView(LoginRequiredMixin, UpdateView):
    """Update existing service"""
    model = Service
    template_name = 'dashboard/services/form.html'
    fields = [
        'name', 'category', 'short_description', 'description', 'detailed_description',
        'features', 'benefits', 'process_steps',
        'image', 'banner_image', 'hero_image',
        'starting_price', 'price_unit',
        'meta_title', 'meta_description', 'meta_keywords',
        'is_featured', 'is_active', 'order'
    ]
    login_url = '/my-admin/login/'
    success_url = reverse_lazy('dashboard:service_list')

    def form_valid(self, form):
        messages.success(self.request, 'Service updated successfully!')
        return super().form_valid(form)

# Category Management (Dashboard)
class ServiceCategoryListView(LoginRequiredMixin, ListView):
    model = ServiceCategory
    template_name = 'dashboard/services/categories/list.html'
    context_object_name = 'categories'
    login_url = '/my-admin/login/'

    def get_queryset(self):
        qs = ServiceCategory.objects.all()
        search = self.request.GET.get('q')
        if search:
            qs = qs.filter(Q(name__icontains=search) | Q(short_description__icontains=search))
        return qs.order_by('order', 'name')

class ServiceCategoryCreateView(LoginRequiredMixin, CreateView):
    model = ServiceCategory
    fields = ['name', 'short_description', 'description', 'icon', 'image', 'banner_image', 'hero_image', 'is_featured', 'is_active', 'order', 'meta_title', 'meta_description', 'meta_keywords']
    template_name = 'dashboard/services/categories/form.html'
    login_url = '/my-admin/login/'
    success_url = reverse_lazy('dashboard:service_category_list')

    def form_valid(self, form):
        messages.success(self.request, 'Category created successfully!')
        return super().form_valid(form)

class ServiceCategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = ServiceCategory
    fields = ['name', 'short_description', 'description', 'icon', 'image', 'banner_image', 'hero_image', 'is_featured', 'is_active', 'order', 'meta_title', 'meta_description', 'meta_keywords']
    template_name = 'dashboard/services/categories/form.html'
    login_url = '/my-admin/login/'
    success_url = reverse_lazy('dashboard:service_category_list')

    def form_valid(self, form):
        messages.success(self.request, 'Category updated successfully!')
        return super().form_valid(form)

# Notifications (simple recent activity)
class NotificationsView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/partials/notifications.html'
    login_url = '/my-admin/login/'

    def get(self, request, *args, **kwargs):
        logs = ActivityLog.objects.select_related('user').order_by('-created_at')[:8]
        context = {'logs': logs}
        return self.render_to_response(context)

# Backup creation (DB JSON + media zip)
class CreateBackupView(LoginRequiredMixin, TemplateView):
    login_url = '/my-admin/login/'

    def get(self, request, *args, **kwargs):
        dt = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
            # dumpdata
            data_io = io.StringIO()
            call_command('dumpdata', '--natural-foreign', '--natural-primary', '--indent', '2', stdout=data_io)
            zf.writestr(f'db_dump_{dt}.json', data_io.getvalue())
            # media
            media_root = getattr(settings, 'MEDIA_ROOT', None)
            if media_root and os.path.isdir(media_root):
                for root, dirs, files in os.walk(media_root):
                    for f in files:
                        full_path = os.path.join(root, f)
                        arcname = os.path.relpath(full_path, media_root)
                        zf.write(full_path, f'media/{arcname}')
        zip_buffer.seek(0)
        response = HttpResponse(zip_buffer.getvalue(), content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename="skylinegh_backup_{dt}.zip"'
        return response


# Advanced Backup Management API Views
class AdminBackupAPIView(UserPassesTestMixin, View):
    """API view to trigger data backup"""

    def test_func(self):
        return self.request.user.is_staff

    def post(self, request):
        try:
            from django.core.management import call_command
            from django.http import JsonResponse
            import io
            import sys

            # Capture output
            old_stdout = sys.stdout
            redirect_output = io.StringIO()
            sys.stdout = redirect_output

            try:
                # Parse request data
                import json
                data = json.loads(request.body) if request.body else {}
                include_media = data.get('include_media', True)
                compress = data.get('compress', True)

                # Build command arguments
                args = ['backup_data', '--include-media', '--compress']

                call_command(*args)
                output = redirect_output.getvalue()
                sys.stdout = old_stdout # Restore stdout
                return JsonResponse({'success': True, 'message': 'Backup created successfully with media files included!', 'output': output})
            except Exception as e:
                sys.stdout = old_stdout # Restore stdout
                return JsonResponse({'success': False, 'error': f'Backup failed: {str(e)}'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': f'Server error: {str(e)}'})


class AdminRestoreAPIView(UserPassesTestMixin, View):
    """API view to trigger data restore"""

    def test_func(self):
        return self.request.user.is_staff

    def post(self, request):
        try:
            import tempfile
            import os
            from django.core.management import call_command
            from django.http import JsonResponse
            import io
            import sys

            # Get uploaded backup file
            backup_file = request.FILES.get('backup_file')
            if not backup_file:
                return JsonResponse({'success': False, 'error': 'No backup file provided'})

            # Save uploaded file to temporary location
            temp_file_path = os.path.join(tempfile.gettempdir(), backup_file.name)

            try:
                with open(temp_file_path, 'wb+') as destination:
                    for chunk in backup_file.chunks():
                        destination.write(chunk)

                # Capture output
                old_stdout = sys.stdout
                redirect_output = io.StringIO()
                sys.stdout = redirect_output

                try:
                    # Call restore command with the backup file path
                    call_command('restore_data', temp_file_path, '--include-media', '--clear-existing', '--force')
                    output = redirect_output.getvalue()
                    sys.stdout = old_stdout # Restore stdout
                    return JsonResponse({
                        'success': True,
                        'message': 'Backup restored successfully! The page will reload to reflect changes.',
                        'output': output
                    })
                except Exception as e:
                    sys.stdout = old_stdout # Restore stdout
                    return JsonResponse({'success': False, 'error': f'Restore failed: {str(e)}'})

            finally:
                # Clean up temporary file
                if os.path.exists(temp_file_path):
                    os.remove(temp_file_path)

        except Exception as e:
            return JsonResponse({'success': False, 'error': f'Server error: {str(e)}'})


class AdminBackupHistoryAPIView(UserPassesTestMixin, View):
    """API view to get backup history"""

    def test_func(self):
        return self.request.user.is_staff

    def get(self, request):
        try:
            import os
            from datetime import datetime
            from django.conf import settings

            backup_dir = os.path.join(settings.BASE_DIR, 'backups')
            backups = []

            if os.path.exists(backup_dir):
                for item in os.listdir(backup_dir):
                    item_path = os.path.join(backup_dir, item)
                    if os.path.isfile(item_path) and (item.endswith('.zip') or item.endswith('.json')):
                        # Get file stats
                        stat = os.stat(item_path)
                        size = self.format_file_size(stat.st_size)
                        date = datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M')

                        backups.append({
                            'name': item,
                            'path': item_path,
                            'size': size,
                            'date': date,
                            'timestamp': stat.st_mtime
                        })
                    elif os.path.isdir(item_path) and item.startswith('Skyline_backup_'):
                        # Directory backup
                        stat = os.stat(item_path)
                        size = self.get_directory_size(item_path)
                        date = datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M')

                        backups.append({
                            'name': item,
                            'path': item_path,
                            'size': self.format_file_size(size),
                            'date': date,
                            'timestamp': stat.st_mtime
                        })

            # Sort by timestamp (newest first)
            backups.sort(key=lambda x: x['timestamp'], reverse=True)

            return JsonResponse({'success': True, 'backups': backups})

        except Exception as e:
            return JsonResponse({'success': False, 'error': f'Error loading backup history: {str(e)}'})

    def format_file_size(self, size_bytes):
        """Format file size in human readable format"""
        if size_bytes == 0:
            return "0B"
        size_names = ["B", "KB", "MB", "GB", "TB"]
        import math
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return f"{s} {size_names[i]}"

    def get_directory_size(self, directory):
        """Get total size of directory"""
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(directory):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                if os.path.exists(filepath):
                    total_size += os.path.getsize(filepath)
        return total_size


class AdminDownloadBackupAPIView(UserPassesTestMixin, View):
    """API view to download backup files"""

    def test_func(self):
        return self.request.user.is_staff

    def get(self, request):
        try:
            from django.http import FileResponse, Http404
            import os
            from urllib.parse import unquote

            backup_path = request.GET.get('path')
            if not backup_path:
                return JsonResponse({'success': False, 'error': 'No backup path specified'})

            # Decode URL-encoded path
            backup_path = unquote(backup_path)

            # Security check - ensure path is within backup directory
            from django.conf import settings
            backup_dir = os.path.join(settings.BASE_DIR, 'backups')
            if not backup_path.startswith(backup_dir):
                return JsonResponse({'success': False, 'error': 'Invalid backup path'})

            if not os.path.exists(backup_path):
                raise Http404("Backup file not found")

            if os.path.isfile(backup_path):
                response = FileResponse(
                    open(backup_path, 'rb'),
                    as_attachment=True,
                    filename=os.path.basename(backup_path)
                )
                return response

        except Exception as e:
            return JsonResponse({'success': False, 'error': f'Download failed: {str(e)}'})


class AdminDeleteBackupAPIView(UserPassesTestMixin, View):
    """API view to delete backup files"""

    def test_func(self):
        return self.request.user.is_staff

    def post(self, request):
        try:
            import json
            import os
            import shutil
            from django.conf import settings

            data = json.loads(request.body)
            backup_path = data.get('path')

            if not backup_path:
                return JsonResponse({'success': False, 'error': 'No backup path specified'})

            # Security check - ensure path is within backup directory
            backup_dir = os.path.join(settings.BASE_DIR, 'backups')
            if not backup_path.startswith(backup_dir):
                return JsonResponse({'success': False, 'error': 'Invalid backup path'})

            if not os.path.exists(backup_path):
                return JsonResponse({'success': False, 'error': 'Backup file not found'})

            # Delete file or directory
            if os.path.isfile(backup_path):
                os.remove(backup_path)
            elif os.path.isdir(backup_path):
                shutil.rmtree(backup_path)

            return JsonResponse({'success': True, 'message': 'Backup deleted successfully'})

        except Exception as e:
            return JsonResponse({'success': False, 'error': f'Error deleting backup: {str(e)}'})


# Service Page Image Management Views
class ServicePageImageListView(LoginRequiredMixin, ListView):
    """List all service page images"""
    model = ServicePageImage
    template_name = 'dashboard/service_images/list.html'
    context_object_name = 'images'
    login_url = '/my-admin/login/'
    paginate_by = 20

    def get_queryset(self):
        qs = ServicePageImage.objects.select_related('category').all()
        category_id = self.request.GET.get('category')
        search = self.request.GET.get('q')

        if category_id:
            qs = qs.filter(category_id=category_id)
        if search:
            qs = qs.filter(Q(title__icontains=search) | Q(description__icontains=search) | Q(category__name__icontains=search))

        return qs.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ServiceCategory.objects.filter(is_active=True).order_by('name')
        context['current_category'] = self.request.GET.get('category')
        context['search_query'] = self.request.GET.get('q', '')
        return context


class ServicePageImageCreateView(LoginRequiredMixin, CreateView):
    """Create new service page image"""
    model = ServicePageImage
    template_name = 'dashboard/service_images/form.html'
    fields = ['category', 'title', 'image', 'description', 'location', 'completion_year', 'is_featured', 'order']
    login_url = '/my-admin/login/'
    success_url = reverse_lazy('dashboard:service_image_list')

    def form_valid(self, form):
        messages.success(self.request, 'Service category image added successfully!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add Service Category Image'
        return context


class ServicePageImageUpdateView(LoginRequiredMixin, UpdateView):
    """Update existing service page image"""
    model = ServicePageImage
    template_name = 'dashboard/service_images/form.html'
    fields = ['category', 'title', 'image', 'description', 'location', 'completion_year', 'is_featured', 'order']
    login_url = '/my-admin/login/'
    success_url = reverse_lazy('dashboard:service_image_list')

    def form_valid(self, form):
        messages.success(self.request, 'Service category image updated successfully!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Service Category Image'
        return context


class ServicePageImageDeleteView(LoginRequiredMixin, DeleteView):
    """Delete service page image"""
    model = ServicePageImage
    template_name = 'dashboard/service_images/confirm_delete.html'
    login_url = '/my-admin/login/'
    success_url = reverse_lazy('dashboard:service_image_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Service category image deleted successfully!')
        return super().delete(request, *args, **kwargs)

# Inquiry Management Views
class InquiryListView(LoginRequiredMixin, ListView):
    """List all inquiries in dashboard"""
    model = ContactInquiry
    template_name = 'dashboard/inquiries/list.html'
    context_object_name = 'inquiries'
    paginate_by = 20
    login_url = '/my-admin/login/'

    def get_queryset(self):
        return ContactInquiry.objects.all().order_by('-created_at')

# Career Management Views
class CareerListView(LoginRequiredMixin, ListView):
    """List all job positions in dashboard"""
    model = JobPosition
    template_name = 'dashboard/careers/list.html'
    context_object_name = 'jobs'
    paginate_by = 20
    login_url = '/my-admin/login/'

    def get_queryset(self):
        queryset = JobPosition.objects.all().order_by('-created_at')
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(department__name__icontains=search)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = JobPosition.objects.all()
        context['total_jobs'] = qs.count()
        context['active_jobs'] = qs.filter(status='active').count()
        context['applications_total'] = JobApplication.objects.count()
        return context

class CareerCreateView(LoginRequiredMixin, CreateView):
    """Create new job position"""
    model = JobPosition
    template_name = 'dashboard/careers/form.html'
    fields = [
        'title', 'department', 'job_type', 'experience_level', 'location',
        'summary', 'description', 'responsibilities', 'requirements', 'qualifications',
        'status', 'application_deadline', 'is_featured', 'is_urgent'
    ]
    login_url = '/my-admin/login/'
    success_url = reverse_lazy('dashboard:career_list')

    def form_valid(self, form):
        messages.success(self.request, 'Job position created successfully!')
        return super().form_valid(form)

class CareerUpdateView(LoginRequiredMixin, UpdateView):
    """Update existing job position"""
    model = JobPosition
    template_name = 'dashboard/careers/form.html'
    fields = [
        'title', 'department', 'job_type', 'experience_level', 'location',
        'summary', 'description', 'responsibilities', 'requirements', 'qualifications',
        'status', 'application_deadline', 'is_featured', 'is_urgent'
    ]
    login_url = '/my-admin/login/'
    success_url = reverse_lazy('dashboard:career_list')

    def form_valid(self, form):
        messages.success(self.request, 'Job position updated successfully!')
        return super().form_valid(form)

class CareerDeleteView(LoginRequiredMixin, DeleteView):
    """Delete job position"""
    model = JobPosition
    template_name = 'dashboard/careers/delete.html'
    login_url = '/my-admin/login/'
    success_url = reverse_lazy('dashboard:career_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Job position deleted successfully!')
        return super().delete(request, *args, **kwargs)

# Project Image Management Views
class ProjectImageManageView(LoginRequiredMixin, TemplateView):
    """Manage project images"""
    template_name = 'dashboard/projects/images.html'
    login_url = '/my-admin/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_id = kwargs.get('pk')
        context['project'] = get_object_or_404(Project, pk=project_id)
        context['images'] = ProjectImage.objects.filter(project=context['project']).order_by('order')
        return context

    def post(self, request, *args, **kwargs):
        project_id = kwargs.get('pk')
        project = get_object_or_404(Project, pk=project_id)

        # Handle image upload
        if 'image' in request.FILES:
            image_file = request.FILES['image']
            caption = request.POST.get('caption', '')

            # Get the next order number
            last_image = ProjectImage.objects.filter(project=project).order_by('-order').first()
            order = (last_image.order + 1) if last_image else 1

            ProjectImage.objects.create(
                project=project,
                image=image_file,
                caption=caption,
                order=order
            )
            messages.success(request, 'Image uploaded successfully!')

        # Handle image deletion
        elif 'delete_image' in request.POST:
            image_id = request.POST.get('delete_image')
            try:
                image = ProjectImage.objects.get(id=image_id, project=project)
                image.delete()
                messages.success(request, 'Image deleted successfully!')
            except ProjectImage.DoesNotExist:
                messages.error(request, 'Image not found!')

        return redirect('dashboard:project_images', pk=project_id)


# ==========================
# Testimonials Management
# ==========================
class TestimonialListView(LoginRequiredMixin, ListView):
    """List all testimonials"""
    model = Testimonial
    template_name = 'dashboard/testimonials/list.html'
    context_object_name = 'testimonials'
    paginate_by = 20
    login_url = '/my-admin/login/'

    def get_queryset(self):
        qs = Testimonial.objects.all().order_by('-is_featured', '-created_at')
        search = self.request.GET.get('search')
        if search:
            qs = qs.filter(Q(name__icontains=search) | Q(company__icontains=search) | Q(content__icontains=search))
        return qs

class TestimonialCreateView(LoginRequiredMixin, CreateView):
    """Create testimonial"""
    model = Testimonial
    template_name = 'dashboard/testimonials/form.html'
    fields = ['name', 'position', 'company', 'content', 'rating', 'image', 'is_featured', 'is_active']
    login_url = '/my-admin/login/'
    success_url = reverse_lazy('dashboard:testimonial_list')

    def form_valid(self, form):
        messages.success(self.request, 'Testimonial created successfully!')
        response = super().form_valid(form)
        try:
            ActivityLog.objects.create(
                user=self.request.user,
                action='create',
                model_name='Testimonial',
                object_id=str(self.object.pk),
                message=f"Created testimonial for {self.object.name}"
            )
        except Exception:
            pass
        return response

class BlogDeleteView(LoginRequiredMixin, DeleteView):
    """Delete blog post"""
    model = BlogPost
    template_name = 'dashboard/blog/delete.html'
    login_url = '/my-admin/login/'
    success_url = reverse_lazy('dashboard:blog_list')

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        title = obj.title
        pk = obj.pk
        messages.success(request, 'Blog post deleted successfully!')
        response = super().delete(request, *args, **kwargs)
        try:
            ActivityLog.objects.create(
                user=request.user,
                action='delete',
                model_name='BlogPost',
                object_id=str(pk),
                message=f"Deleted blog post '{title}'"
            )
        except Exception:
            pass
        return response

class TestimonialUpdateView(LoginRequiredMixin, UpdateView):
    """Update testimonial"""
    model = Testimonial
    template_name = 'dashboard/testimonials/form.html'
    fields = ['name', 'position', 'company', 'content', 'rating', 'image', 'is_featured', 'is_active']
    login_url = '/my-admin/login/'
    success_url = reverse_lazy('dashboard:testimonial_list')

    def form_valid(self, form):
        messages.success(self.request, 'Testimonial updated successfully!')
        response = super().form_valid(form)
        try:
            ActivityLog.objects.create(
                user=self.request.user,
                action='update',
                model_name='Testimonial',
                object_id=str(self.object.pk),
                message=f"Updated testimonial for {self.object.name}"
            )
        except Exception:
            pass
        return response

class TestimonialDeleteView(LoginRequiredMixin, DeleteView):
    """Delete testimonial"""
    model = Testimonial
    template_name = 'dashboard/testimonials/delete.html'
    login_url = '/my-admin/login/'
    success_url = reverse_lazy('dashboard:testimonial_list')

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(request, 'Testimonial deleted successfully!')
        try:
            pk = obj.pk
            name = obj.name
        except Exception:
            pk = ''
            name = ''
        response = super().delete(request, *args, **kwargs)
        try:
            ActivityLog.objects.create(
                user=request.user,
                action='delete',
                model_name='Testimonial',
                object_id=str(pk),
                message=f"Deleted testimonial for {name}"
            )
        except Exception:
            pass
        return response


# ==========================
# Blog Admin (basic)
# ==========================
class BlogListView(LoginRequiredMixin, ListView):
    """List blog posts"""
    model = BlogPost
    template_name = 'dashboard/blog/list.html'
    context_object_name = 'posts'
    paginate_by = 20
    login_url = '/my-admin/login/'

    def get_queryset(self):
        qs = BlogPost.objects.all().order_by('-published_at', '-created_at')
        search = self.request.GET.get('search')
        if search:
            qs = qs.filter(Q(title__icontains=search) | Q(excerpt__icontains=search) | Q(content__icontains=search))
        return qs

class BlogCreateView(LoginRequiredMixin, CreateView):
    """Create blog post"""
    model = BlogPost
    template_name = 'dashboard/blog/form.html'
    fields = ['title', 'excerpt', 'content', 'author', 'status', 'category', 'tags', 'featured_image', 'featured_image_alt', 'is_featured', 'allow_comments']
    login_url = '/my-admin/login/'
    success_url = reverse_lazy('dashboard:blog_list')

    def form_valid(self, form):
        messages.success(self.request, 'Blog post created successfully!')
        response = super().form_valid(form)
        try:
            ActivityLog.objects.create(
                user=self.request.user,
                action='create',
                model_name='BlogPost',
                object_id=str(self.object.pk),
                message=f"Created blog post '{self.object.title}'"
            )
        except Exception:
            pass
        return response

class BlogUpdateView(LoginRequiredMixin, UpdateView):
    """Update blog post"""
    model = BlogPost
    template_name = 'dashboard/blog/form.html'
    fields = ['title', 'excerpt', 'content', 'author', 'status', 'category', 'tags', 'featured_image', 'featured_image_alt', 'is_featured', 'allow_comments']
    login_url = '/my-admin/login/'
    success_url = reverse_lazy('dashboard:blog_list')

    def form_valid(self, form):
        messages.success(self.request, 'Blog post updated successfully!')
        response = super().form_valid(form)
        try:
            ActivityLog.objects.create(
                user=self.request.user,
                action='update',
                model_name='BlogPost',
                object_id=str(self.object.pk),
                message=f"Updated blog post '{self.object.title}'"
            )
        except Exception:
            pass
        return response


# ==========================
# Analytics & Settings
# ==========================
class AnalyticsView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/analytics.html'
    login_url = '/my-admin/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['inquiries_count'] = ContactInquiry.objects.count()
        context['projects_count'] = Project.objects.count()
        context['posts_count'] = BlogPost.objects.filter(status='published').count()
        # Visitor analytics
        today = timezone.localdate()
        context['visitors_today'] = SystemMetrics.objects.filter(
            metric_name='visitors', metric_date=today
        ).aggregate(total=Sum('metric_value'))['total'] or 0
        context['visitors_7d'] = SystemMetrics.objects.filter(
            metric_name='visitors', metric_date__gte=today - timedelta(days=6)
        ).aggregate(total=Sum('metric_value'))['total'] or 0
        context['visitors_30d'] = SystemMetrics.objects.filter(
            metric_name='visitors', metric_date__gte=today - timedelta(days=29)
        ).aggregate(total=Sum('metric_value'))['total'] or 0
        context['visitors_365d'] = SystemMetrics.objects.filter(
            metric_name='visitors', metric_date__gte=today - timedelta(days=364)
        ).aggregate(total=Sum('metric_value'))['total'] or 0

        # Build simple timeseries for last 14 days
        series = []
        for i in range(13, -1, -1):
            d = today - timedelta(days=i)
            val = SystemMetrics.objects.filter(metric_name='visitors', metric_date=d).aggregate(total=Sum('metric_value'))['total'] or 0
            series.append({'date': d.isoformat(), 'value': int(val)})
        context['visitors_series'] = series
        return context

class SettingsView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/settings.html'
    login_url = '/my-admin/login/'

    def get_object(self):
        obj = SiteSettings.objects.first()
        if not obj:
            obj = SiteSettings.objects.create()
        return obj

    def get(self, request, *args, **kwargs):
        form = SiteSettingsForm(instance=self.get_object())
        context = self.get_context_data(form=form)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        form = SiteSettingsForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            obj = form.save()
            messages.success(request, 'Settings updated successfully!')
            try:
                ActivityLog.objects.create(
                    user=request.user,
                    action='settings',
                    model_name='SiteSettings',
                    object_id=str(obj.pk),
                    message='Updated site settings'
                )
            except Exception:
                pass
            return redirect('dashboard:settings')
        context = self.get_context_data(form=form)
        return self.render_to_response(context)


class UsersListView(LoginRequiredMixin, ListView):
    """Read-only list of users"""
    model = User
    template_name = 'dashboard/users/list.html'
    context_object_name = 'users'
    paginate_by = 25
    login_url = '/my-admin/login/'

    def get_queryset(self):
        qs = User.objects.all().order_by('-date_joined')
        search = self.request.GET.get('search')
        if search:
            qs = qs.filter(Q(username__icontains=search) | Q(email__icontains=search) | Q(first_name__icontains=search) | Q(last_name__icontains=search))
        return qs


class ActivityLogListView(LoginRequiredMixin, ListView):
    """Audit log list"""
    model = ActivityLog
    template_name = 'dashboard/activity/list.html'
    context_object_name = 'logs'
    paginate_by = 25
    login_url = '/my-admin/login/'

    def get_queryset(self):
        qs = ActivityLog.objects.select_related('user').all()
        search = self.request.GET.get('search')
        if search:
            qs = qs.filter(
                Q(user__username__icontains=search) |
                Q(action__icontains=search) |
                Q(model_name__icontains=search) |
                Q(message__icontains=search)
            )
        return qs.order_by('-created_at')
