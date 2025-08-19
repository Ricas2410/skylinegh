from django.urls import path
from . import views

app_name = 'careers'

urlpatterns = [
    path('', views.JobListView.as_view(), name='job_list'),
    path('jobs/<slug:slug>/', views.JobDetailView.as_view(), name='job_detail'),
    path('jobs/<slug:slug>/apply/', views.JobApplicationView.as_view(), name='job_apply'),
    path('application-success/', views.ApplicationSuccessView.as_view(), name='application_success'),
]
