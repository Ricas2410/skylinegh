from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.http import Http404
from core.views import BaseContextMixin
from .models import ServiceCategory, Service

class ServiceListView(BaseContextMixin, ListView):
    """List all service categories"""
    model = ServiceCategory
    template_name = 'services/service_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return ServiceCategory.objects.filter(is_active=True)

class ServiceCategoryDetailView(BaseContextMixin, DetailView):
    """Service category detail page"""
    model = ServiceCategory
    template_name = 'services/category_detail.html'
    context_object_name = 'category'

    def get_queryset(self):
        return ServiceCategory.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add category page images
        context['category_images'] = self.object.page_images.all()[:12]

        # Add related projects from the same service category
        from projects.models import Project
        context['related_projects'] = Project.objects.filter(
            service_category=self.object,
            is_published=True
        ).select_related('service_category', 'project_type')[:6]

        return context

    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except Http404:
            # Fallback to service list if category not found/inactive
            return redirect('services:service_list')

class ServiceDetailView(BaseContextMixin, DetailView):
    """Individual service detail page"""
    model = Service
    template_name = 'services/service_detail.html'
    context_object_name = 'service'
    slug_url_kwarg = 'service_slug'

    def get_queryset(self):
        return Service.objects.filter(
            is_active=True,
            category__slug=self.kwargs['category_slug'],
            category__is_active=True
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add related projects from the same service category
        from projects.models import Project
        context['related_projects'] = Project.objects.filter(
            service_category=self.object.category,
            is_published=True
        ).select_related('service_category', 'project_type')[:6]

        # Add service page images (from the category)
        context['service_images'] = self.object.category.page_images.all()[:8]

        return context

    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except Http404:
            # Fallback to service list if service or category missing
            return redirect('services:service_list')
