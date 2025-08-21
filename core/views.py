from django.shortcuts import render, redirect
from django.views.generic import TemplateView, FormView, DetailView, View
from django.contrib import messages
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from .models import SiteSettings, ContactInquiry, Newsletter, TeamMember, Testimonial
from .forms import ContactForm, NewsletterForm

class BaseContextMixin:
    """Mixin to add common context to all views"""
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['site_settings'] = SiteSettings.objects.first()
        except SiteSettings.DoesNotExist:
            context['site_settings'] = None
        return context

class HomeView(BaseContextMixin, TemplateView):
    """Homepage view"""
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add featured testimonials for the homepage
        try:
            context['testimonials'] = Testimonial.objects.filter(is_active=True).order_by('-is_featured', '-created_at')[:8]
        except Exception:
            context['testimonials'] = []
        return context

class AboutView(BaseContextMixin, TemplateView):
    """About page view"""
    template_name = 'core/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['team_members'] = TeamMember.objects.filter(is_active=True)
        # Add testimonials same as homepage
        try:
            context['testimonials'] = Testimonial.objects.filter(is_active=True).order_by('-is_featured', '-created_at')[:8]
        except Exception:
            context['testimonials'] = []
        return context


class TeamMemberDetailView(BaseContextMixin, DetailView):
    """Team member detail page"""
    model = TeamMember
    template_name = 'core/team_member_detail.html'
    context_object_name = 'member'

    def get_queryset(self):
        return TeamMember.objects.filter(is_active=True)

class ContactView(BaseContextMixin, FormView):
    """Contact page view"""
    template_name = 'core/contact.html'
    form_class = ContactForm
    success_url = '/contact/#contact-form'

    def form_valid(self, form):
        # Save the inquiry
        inquiry = form.save(commit=False)
        inquiry.ip_address = self.get_client_ip()
        inquiry.user_agent = self.request.META.get('HTTP_USER_AGENT', '')
        inquiry.save()

        # Send notification email
        try:
            send_mail(
                subject=f'New Contact Inquiry: {inquiry.subject}',
                message=f'Name: {inquiry.name}\nEmail: {inquiry.email}\nPhone: {inquiry.phone}\n\nMessage:\n{inquiry.message}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.DEFAULT_FROM_EMAIL],
                fail_silently=True,
            )
        except Exception:
            pass

        messages.success(
            self.request,
            f'Thank you for your message, {inquiry.name}! We have received your inquiry about "{inquiry.subject}" and will get back to you within 24 hours at {inquiry.email}.'
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        """Handle form validation errors"""
        messages.error(
            self.request,
            'There was an error with your submission. Please check the form and try again.'
        )
        return super().form_invalid(form)

    def get_client_ip(self):
        """Get client IP address"""
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip

class NewsletterSignupView(BaseContextMixin, FormView):
    """Newsletter signup view"""
    form_class = NewsletterForm

    def form_valid(self, form):
        email = form.cleaned_data['email']
        newsletter, created = Newsletter.objects.get_or_create(
            email=email,
            defaults={'is_active': True}
        )

        if created:
            messages.success(self.request, 'Successfully subscribed to our newsletter!')
        else:
            if newsletter.is_active:
                messages.info(self.request, 'You are already subscribed to our newsletter.')
            else:
                newsletter.is_active = True
                newsletter.save()
                messages.success(self.request, 'Successfully resubscribed to our newsletter!')

        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'message': 'Successfully subscribed!'})

        return redirect(self.request.META.get('HTTP_REFERER', '/'))

    def form_invalid(self, form):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'errors': form.errors})

        for error in form.errors.values():
            messages.error(self.request, error[0])
        return redirect(self.request.META.get('HTTP_REFERER', '/'))

class PrivacyPolicyView(BaseContextMixin, TemplateView):
    """Privacy policy page"""
    template_name = 'core/privacy_policy.html'

class TermsOfServiceView(BaseContextMixin, TemplateView):
    """Terms of service page"""
    template_name = 'core/terms_of_service.html'

class SitemapView(BaseContextMixin, TemplateView):
    """Sitemap page"""
    template_name = 'core/sitemap.html'


class WebManifestView(View):
    """Web App Manifest for PWA support and better search results"""

    def get(self, request, *args, **kwargs):
        from django.http import JsonResponse
        from django.conf import settings

        try:
            site_settings = SiteSettings.objects.first()
        except SiteSettings.DoesNotExist:
            site_settings = None

        manifest = {
            "name": site_settings.site_name if site_settings else "Skyline Ghana Constructions",
            "short_name": "Skyline Ghana",
            "description": site_settings.site_tagline if site_settings else "Building Dreams, Creating Futures",
            "start_url": "/",
            "display": "standalone",
            "background_color": "#ffffff",
            "theme_color": "#4f46e5",
            "orientation": "portrait-primary",
            "scope": "/",
            "lang": "en",
            "categories": ["business", "construction", "architecture"],
            "icons": []
        }

        # Add icons if logo is available
        if site_settings and site_settings.logo:
            logo_url = request.build_absolute_uri(site_settings.logo.url)
            manifest["icons"] = [
                {
                    "src": logo_url,
                    "sizes": "192x192",
                    "type": "image/png",
                    "purpose": "any maskable"
                },
                {
                    "src": logo_url,
                    "sizes": "512x512",
                    "type": "image/png",
                    "purpose": "any maskable"
                }
            ]

        response = JsonResponse(manifest)
        response['Content-Type'] = 'application/manifest+json'
        return response
