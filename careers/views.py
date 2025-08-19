from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, FormView, TemplateView
from django.contrib import messages
from django.db.models import Q
from core.views import BaseContextMixin
from .models import JobPosition, JobApplication, Department
from .forms import JobApplicationForm

class JobListView(BaseContextMixin, ListView):
    """List all active job positions"""
    model = JobPosition
    template_name = 'careers/job_list.html'
    context_object_name = 'jobs'
    paginate_by = 10

    def get_queryset(self):
        qs = JobPosition.objects.filter(status='active')
        params = self.request.GET

        # Search
        q = params.get('q')
        if q:
            qs = qs.filter(
                Q(title__icontains=q)
                | Q(summary__icontains=q)
                | Q(description__icontains=q)
                | Q(department__name__icontains=q)
                | Q(location__icontains=q)
            )

        # Department
        dept = params.get('department')
        if dept:
            qs = qs.filter(department__slug=dept)

        # Job type
        job_type = params.get('job_type')
        if job_type:
            qs = qs.filter(job_type=job_type)

        # Experience level
        experience = params.get('experience')
        if experience:
            qs = qs.filter(experience_level=experience)

        # Location
        location = params.get('location')
        if location:
            qs = qs.filter(location__icontains=location)

        # Remote allowed
        remote = params.get('remote')
        if remote == '1':
            qs = qs.filter(remote_allowed=True)

        # Featured first already handled by model Meta ordering
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        params = self.request.GET.copy()
        params.pop('page', None)
        querystring = params.urlencode()

        context.update({
            'departments': Department.objects.filter(is_active=True).order_by('name'),
            'job_types': JobPosition.JOB_TYPES,
            'experience_levels': JobPosition.EXPERIENCE_LEVELS,
            'current_filters': {
                'q': self.request.GET.get('q', ''),
                'department': self.request.GET.get('department', ''),
                'job_type': self.request.GET.get('job_type', ''),
                'experience': self.request.GET.get('experience', ''),
                'location': self.request.GET.get('location', ''),
                'remote': self.request.GET.get('remote', ''),
            },
            'querystring': querystring,
        })
        return context

class JobDetailView(BaseContextMixin, DetailView):
    """Job position detail page"""
    model = JobPosition
    template_name = 'careers/job_detail.html'
    context_object_name = 'job'

    def get_queryset(self):
        return JobPosition.objects.filter(status='active')

    def get_object(self):
        obj = super().get_object()
        obj.increment_views()
        return obj

class JobApplicationView(BaseContextMixin, FormView):
    """Job application form"""
    template_name = 'careers/job_apply.html'
    form_class = JobApplicationForm

    def get_success_url(self):
        return '/careers/application-success/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['job'] = JobPosition.objects.get(slug=self.kwargs['slug'])
        return context

    def form_valid(self, form):
        job = JobPosition.objects.get(slug=self.kwargs['slug'])
        application = form.save(commit=False)
        application.position = job
        application.save()

        job.increment_applications()
        messages.success(self.request, 'Your application has been submitted successfully!')
        return super().form_valid(form)

class ApplicationSuccessView(BaseContextMixin, TemplateView):
    """Application success page"""
    template_name = 'careers/application_success.html'
