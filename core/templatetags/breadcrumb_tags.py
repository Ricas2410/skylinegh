from django import template
from django.urls import reverse

register = template.Library()


@register.inclusion_tag('partials/breadcrumbs.html', takes_context=True)
def breadcrumbs(context, *args):
    """
    Generate breadcrumbs for the current page
    Usage: {% breadcrumbs "Services" "Residential Construction" %}
    """
    request = context.get('request')
    breadcrumb_list = []
    
    # Convert args to breadcrumb objects
    for i, breadcrumb in enumerate(args):
        if isinstance(breadcrumb, str):
            breadcrumb_list.append({
                'name': breadcrumb,
                'url': None  # Last item typically has no URL
            })
        elif isinstance(breadcrumb, dict):
            breadcrumb_list.append(breadcrumb)
    
    return {
        'breadcrumbs': breadcrumb_list,
        'request': request
    }


@register.simple_tag(takes_context=True)
def auto_breadcrumbs(context):
    """
    Automatically generate breadcrumbs based on the current URL
    """
    request = context.get('request')
    if not request:
        return []
    
    path = request.path.strip('/')
    if not path:
        return []
    
    breadcrumbs = []
    path_parts = path.split('/')
    
    # Build breadcrumbs based on URL structure
    current_path = ''
    for i, part in enumerate(path_parts):
        current_path += f'/{part}'
        
        # Skip if it's a slug/ID (contains numbers or is last part)
        if i == len(path_parts) - 1:
            # Last part - no URL
            breadcrumbs.append({
                'name': part.replace('-', ' ').replace('_', ' ').title(),
                'url': None
            })
        else:
            # Intermediate parts
            name = part.replace('-', ' ').replace('_', ' ').title()
            breadcrumbs.append({
                'name': name,
                'url': current_path + '/'
            })
    
    return breadcrumbs


@register.simple_tag
def service_breadcrumbs(service=None, category=None):
    """
    Generate breadcrumbs for service pages
    """
    breadcrumbs = [
        {'name': 'Services', 'url': reverse('services:service_list')}
    ]
    
    if category:
        breadcrumbs.append({
            'name': category.name,
            'url': category.get_absolute_url() if hasattr(category, 'get_absolute_url') else None
        })
    
    if service:
        breadcrumbs.append({
            'name': service.name,
            'url': None  # Current page
        })
    
    return breadcrumbs


@register.simple_tag
def project_breadcrumbs(project=None):
    """
    Generate breadcrumbs for project pages
    """
    breadcrumbs = [
        {'name': 'Projects', 'url': reverse('projects:project_list')}
    ]
    
    if project:
        breadcrumbs.append({
            'name': project.title,
            'url': None  # Current page
        })
    
    return breadcrumbs


@register.simple_tag
def blog_breadcrumbs(post=None, category=None):
    """
    Generate breadcrumbs for blog pages
    """
    breadcrumbs = [
        {'name': 'Blog', 'url': reverse('blog:post_list')}
    ]
    
    if category:
        breadcrumbs.append({
            'name': category.name,
            'url': category.get_absolute_url() if hasattr(category, 'get_absolute_url') else None
        })
    
    if post:
        breadcrumbs.append({
            'name': post.title,
            'url': None  # Current page
        })
    
    return breadcrumbs
