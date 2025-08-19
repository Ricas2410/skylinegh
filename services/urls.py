from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [
    path('', views.ServiceListView.as_view(), name='service_list'),
    path('<slug:slug>/', views.ServiceCategoryDetailView.as_view(), name='category_detail'),
    path('<slug:category_slug>/<slug:service_slug>/', views.ServiceDetailView.as_view(), name='service_detail'),
]
