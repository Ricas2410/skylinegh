from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('gallery/', views.GalleryView.as_view(), name='gallery'),
    path('', views.ProjectListView.as_view(), name='project_list'),
    path('<slug:slug>/', views.ProjectDetailView.as_view(), name='project_detail'),
]
