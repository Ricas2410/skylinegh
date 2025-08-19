from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.BlogPostListView.as_view(), name='post_list'),
    path('<slug:slug>/', views.BlogPostDetailView.as_view(), name='post_detail'),
    path('category/<slug:slug>/', views.BlogCategoryView.as_view(), name='category'),
    path('tag/<slug:slug>/', views.BlogTagView.as_view(), name='tag'),
]
