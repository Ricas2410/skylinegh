from django import template
from django.utils.safestring import mark_safe
from django.conf import settings

register = template.Library()


@register.inclusion_tag('core/seo_meta.html', takes_context=True)
def seo_meta(context, obj=None):
    """
    Simplified SEO meta tag inclusion
    Usage: {% seo_meta object %}
    """
    request = context.get('request')
    site_settings = context.get('site_settings')
    
    # Enhanced default values with comprehensive construction keywords
    default_keywords = 'construction Ghana, building contractors Ghana, skyline construction, skyline Ghana, skyline construction company, construction company Accra, residential construction Ghana, commercial construction Ghana, building services Ghana, construction contractors, Ghana builders, skyline GH, construction projects Ghana, building renovation Ghana, property development Ghana, construction management Ghana, architectural services Ghana, civil engineering Ghana, building materials Ghana, construction consultancy Ghana'

    meta_data = {
        'title': getattr(site_settings, 'site_name', 'Skyline Ghana Constructions - Premier Building Contractors'),
        'description': getattr(site_settings, 'site_description', 'Leading construction company in Ghana specializing in residential, commercial, and industrial building projects. Expert contractors delivering quality construction services across Accra and Ghana.'),
        'keywords': getattr(site_settings, 'meta_keywords', default_keywords),
        'og_title': getattr(site_settings, 'site_name', 'Skyline Ghana Constructions - Premier Building Contractors'),
        'og_description': getattr(site_settings, 'site_description', 'Leading construction company in Ghana specializing in residential, commercial, and industrial building projects. Expert contractors delivering quality construction services across Accra and Ghana.'),
        'og_image': '',
        'canonical_url': request.build_absolute_uri() if request else '',
    }
    
    # Override with object data if provided
    if obj and hasattr(obj, 'get_meta_title'):
        meta_data.update({
            'title': obj.get_meta_title(),
            'description': obj.get_meta_description(),
            'keywords': obj.get_meta_keywords(),
            'og_title': obj.get_og_title(),
            'og_description': obj.get_og_description(),
        })
        
        # Add object-specific image if available
        if hasattr(obj, 'featured_image') and obj.featured_image:
            meta_data['og_image'] = obj.featured_image.url
        elif hasattr(obj, 'image') and obj.image:
            meta_data['og_image'] = obj.image.url
    
    # Add site settings image as fallback
    if not meta_data['og_image'] and site_settings:
        if hasattr(site_settings, 'hero_card_image') and site_settings.hero_card_image:
            meta_data['og_image'] = site_settings.hero_card_image.url
        elif hasattr(site_settings, 'logo') and site_settings.logo:
            meta_data['og_image'] = site_settings.logo.url
    
    return meta_data


@register.simple_tag
def structured_data(obj=None, obj_type='WebPage'):
    """
    Generate JSON-LD structured data
    Usage: {% structured_data object "Article" %}
    """
    data = {
        "@context": "https://schema.org",
        "@type": obj_type,
    }

    # Add construction company specific data for homepage
    if obj_type == 'WebPage' and not obj:
        data.update({
            "@type": "Organization",
            "name": "Skyline Ghana Constructions",
            "alternateName": ["Skyline GH", "Skylink Construction", "Skyline Ghana"],
            "url": "https://skylinegh.com",
            "logo": "https://skylinegh.com/static/images/logo.png",
            "description": "Leading construction company in Ghana specializing in residential, commercial, and industrial building projects.",
            "address": {
                "@type": "PostalAddress",
                "addressCountry": "Ghana",
                "addressLocality": "Accra",
                "addressRegion": "Greater Accra"
            },
            "contactPoint": {
                "@type": "ContactPoint",
                "telephone": "+233-24-123-4567",
                "contactType": "customer service",
                "email": "info@skylinegh.com"
            },
            "sameAs": [
                "https://www.facebook.com/skylineghana",
                "https://www.linkedin.com/company/skyline-ghana",
                "https://www.instagram.com/skylineghana"
            ],
            "serviceArea": {
                "@type": "Country",
                "name": "Ghana"
            },
            "hasOfferCatalog": {
                "@type": "OfferCatalog",
                "name": "Construction Services",
                "itemListElement": [
                    {
                        "@type": "Offer",
                        "itemOffered": {
                            "@type": "Service",
                            "name": "Residential Construction",
                            "description": "Custom home building and residential construction services"
                        }
                    },
                    {
                        "@type": "Offer",
                        "itemOffered": {
                            "@type": "Service",
                            "name": "Commercial Construction",
                            "description": "Office buildings, retail spaces, and commercial construction"
                        }
                    }
                ]
            }
        })

    if obj:
        if hasattr(obj, 'get_meta_title'):
            data["name"] = obj.get_meta_title()
        if hasattr(obj, 'get_meta_description'):
            data["description"] = obj.get_meta_description()
        if hasattr(obj, 'created_at'):
            data["datePublished"] = obj.created_at.isoformat()
        if hasattr(obj, 'updated_at'):
            data["dateModified"] = obj.updated_at.isoformat()

        # Add image if available
        if hasattr(obj, 'featured_image') and obj.featured_image:
            data["image"] = obj.featured_image.url
        elif hasattr(obj, 'image') and obj.image:
            data["image"] = obj.image.url
    
    # Add organization data
    data["publisher"] = {
        "@type": "Organization",
        "name": "Skyline Ghana Constructions",
        "url": "https://skylinegh.com"
    }
    
    import json
    return mark_safe(f'<script type="application/ld+json">{json.dumps(data, indent=2)}</script>')


@register.simple_tag
def breadcrumb_schema(breadcrumbs):
    """
    Generate breadcrumb structured data
    Usage: {% breadcrumb_schema breadcrumb_list %}
    """
    if not breadcrumbs:
        return ''
    
    items = []
    for i, (name, url) in enumerate(breadcrumbs, 1):
        items.append({
            "@type": "ListItem",
            "position": i,
            "name": name,
            "item": url
        })
    
    data = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": items
    }
    
    import json
    return mark_safe(f'<script type="application/ld+json">{json.dumps(data, indent=2)}</script>')
