from django.shortcuts import render
from django.views.generic import ListView, DetailView
from core.views import BaseContextMixin
from .models import BlogPost, BlogCategory, BlogTag

class BlogPostListView(BaseContextMixin, ListView):
    """List all published blog posts"""
    model = BlogPost
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        return BlogPost.objects.filter(status='published')

class BlogPostDetailView(BaseContextMixin, DetailView):
    """Blog post detail page"""
    model = BlogPost
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_queryset(self):
        return BlogPost.objects.filter(status='published')

    def get_object(self):
        obj = super().get_object()
        obj.increment_views()
        return obj

class BlogCategoryView(BaseContextMixin, ListView):
    """Blog posts by category"""
    model = BlogPost
    template_name = 'blog/category.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        return BlogPost.objects.filter(
            status='published',
            category__slug=self.kwargs['slug']
        )

class BlogTagView(BaseContextMixin, ListView):
    """Blog posts by tag"""
    model = BlogPost
    template_name = 'blog/tag.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        return BlogPost.objects.filter(
            status='published',
            tags__slug=self.kwargs['slug']
        )
