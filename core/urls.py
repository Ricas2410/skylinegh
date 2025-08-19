from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('team/<int:pk>/', views.TeamMemberDetailView.as_view(), name='team_member_detail'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('newsletter-signup/', views.NewsletterSignupView.as_view(), name='newsletter_signup'),
    path('privacy-policy/', views.PrivacyPolicyView.as_view(), name='privacy_policy'),
    path('terms-of-service/', views.TermsOfServiceView.as_view(), name='terms_of_service'),
    path('sitemap/', views.SitemapView.as_view(), name='sitemap'),
]
