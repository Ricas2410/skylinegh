from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Count, Q
from django.utils import timezone
from datetime import datetime, timedelta

from projects.models import Project, ProjectImage
from services.models import Service, ServiceCategory
from core.models import ContactInquiry, SiteSettings
from careers.models import JobPosition, JobApplication
from blog.models import BlogPost

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

        # Recent projects
        context['recent_projects'] = Project.objects.filter(
            is_published=True
        ).order_by('-created_at')[:5]

        # Recent inquiries
        context['recent_inquiries'] = ContactInquiry.objects.order_by('-created_at')[:5]

        # Recent applications
        context['recent_applications'] = JobApplication.objects.order_by('-created_at')[:5]

        return context

class DashboardLoginView(LoginView):
    """Dashboard login page"""
    template_name = 'dashboard/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return '/my-admin/'

class DashboardLogoutView(LogoutView):
    """Dashboard logout"""
    next_page = '/my-admin/login/'

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
        'title', 'description', 'location', 'client_name', 'project_type',
        'service_category', 'start_date', 'end_date', 'budget',
        'featured_image', 'is_featured', 'is_published'
    ]
    login_url = '/my-admin/login/'
    success_url = reverse_lazy('dashboard:project_list')

    def form_valid(self, form):
        messages.success(self.request, 'Project created successfully!')
        return super().form_valid(form)

class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    """Update existing project"""
    model = Project
    template_name = 'dashboard/projects/form.html'
    fields = [
        'title', 'description', 'location', 'client_name', 'project_type',
        'service_category', 'start_date', 'end_date', 'budget',
        'featured_image', 'is_featured', 'is_published'
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
        messages.success(self.request, 'Project deleted successfully!')
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
        return Service.objects.all().order_by('name')

class ServiceCreateView(LoginRequiredMixin, CreateView):
    """Create new service"""
    model = Service
    template_name = 'dashboard/services/form.html'
    fields = [
        'name', 'category', 'short_description', 'description',
        'starting_price', 'price_unit', 'features', 'is_active'
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
        'name', 'category', 'short_description', 'description',
        'starting_price', 'price_unit', 'features', 'is_active'
    ]
    login_url = '/my-admin/login/'
    success_url = reverse_lazy('dashboard:service_list')

    def form_valid(self, form):
        messages.success(self.request, 'Service updated successfully!')
        return super().form_valid(form)

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

# Project Image Management Views
class ProjectImageManageView(LoginRequiredMixin, TemplateView):
    """Manage project images"""
    template_name = 'dashboard/projects/images.html'
    login_url = '/my-admin/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_id = self.kwargs.get('pk')
        context['project'] = get_object_or_404(Project, id=project_id)
        context['images'] = context['project'].images.all()
        return context

    def post(self, request, *args, **kwargs):
        project = get_object_or_404(Project, id=kwargs.get('pk'))
        
        # Handle image uploads
        images = request.FILES.getlist('images')
        for image in images:
            ProjectImage.objects.create(
                project=project,
                image=image,
                caption=request.POST.get('caption', '')
            )
        
        # Handle image deletion
        delete_ids = request.POST.getlist('delete_images')
        if delete_ids:
            ProjectImage.objects.filter(id__in=delete_ids, project=project).delete()
        
        messages.success(request, 'Images updated successfully!')
        return redirect('dashboard:project_images', pk=project.id)
