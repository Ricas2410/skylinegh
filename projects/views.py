from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.db.models import Q
from core.views import BaseContextMixin
from .models import Project, ProjectCategory, ProjectImage
from django.shortcuts import redirect
from django.http import Http404

class ProjectListView(BaseContextMixin, ListView):
    """List all projects with filtering"""
    model = Project
    template_name = 'projects/project_list.html'
    context_object_name = 'projects'
    paginate_by = 12

    def get_queryset(self):
        queryset = Project.objects.filter(is_published=True).select_related('project_type', 'service_category')

        # Filter by category
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(project_type__slug=category_slug)

        # Search functionality
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(location__icontains=search_query) |
                Q(client_name__icontains=search_query)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ProjectCategory.objects.filter(is_active=True)
        context['current_category'] = self.request.GET.get('category', '')
        context['search_query'] = self.request.GET.get('search', '')
        return context

class ProjectDetailView(BaseContextMixin, DetailView):
    """Project detail page"""
    model = Project
    template_name = 'projects/project_detail.html'
    context_object_name = 'project'

    def get_queryset(self):
        return Project.objects.filter(is_published=True)

    def get_object(self):
        obj = super().get_object()
        obj.increment_views()
        return obj

    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except Http404:
            return redirect('projects:project_list')


class GalleryView(BaseContextMixin, ListView):
    """Public gallery of finished work samples (project images)."""
    model = ProjectImage
    template_name = 'projects/gallery.html'
    context_object_name = 'images'
    paginate_by = 24

    def get_queryset(self):
        qs = (
            ProjectImage.objects
            .select_related('project')
            .filter(project__is_published=True)
            .order_by('project__order', 'order', 'id')
        )
        # Optional filtering by project or category via query params
        project_slug = self.request.GET.get('project')
        category_slug = self.request.GET.get('category')
        if project_slug:
            qs = qs.filter(project__slug=project_slug)
        if category_slug:
            qs = qs.filter(project__project_type__slug=category_slug)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ProjectCategory.objects.filter(is_active=True)
        context['current_category'] = self.request.GET.get('category', '')
        context['current_project'] = self.request.GET.get('project', '')
        return context
