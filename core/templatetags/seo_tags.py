from django import template
from django.utils.safestring import mark_safe
from django.conf import settings

register = template.Library()


@register.inclusion_tag('core/seo_meta.html', takes_context=True)
def seo_meta(context, obj=None):
    """
    Code-based SEO meta tag inclusion - all settings handled in code
    Usage: {% seo_meta object %}
    """
    request = context.get('request')

    # Code-based SEO settings - not editable via admin to prevent accidental changes
    SITE_NAME = "Skyline Ghana Constructions - Premier Building Contractors"
    SITE_DESCRIPTION = "Leading construction company in Ghana specializing in residential, commercial, and industrial building projects. Expert contractors delivering quality construction services across Accra and Ghana."

    # Comprehensive construction keywords with your specified additions
    DEFAULT_KEYWORDS = 'skylinegh, skyline GH, Skylink GH, Skylink, construction Ghana, building contractors Ghana, skyline construction, skyline Ghana, skyline construction company, construction company Accra, residential construction Ghana, commercial construction Ghana, building services Ghana, construction contractors, Ghana builders, construction projects Ghana, building renovation Ghana, property development Ghana, construction management Ghana, architectural services Ghana, civil engineering Ghana, building materials Ghana, construction consultancy Ghana, construction company near me, best construction company Ghana, reliable builders Ghana, quality construction services, affordable construction Ghana, modern construction techniques, sustainable building Ghana, green construction, project management Ghana'

    # Generate canonical URL (always use non-www version)
    canonical_url = ''
    if request:
        canonical_url = request.build_absolute_uri()
        # Ensure canonical URL uses non-www version
        if '://www.' in canonical_url:
            canonical_url = canonical_url.replace('://www.', '://')

    meta_data = {
        'title': SITE_NAME,
        'description': SITE_DESCRIPTION,
        'keywords': DEFAULT_KEYWORDS,
        'og_title': SITE_NAME,
        'og_description': SITE_DESCRIPTION,
        'og_image': '',
        'canonical_url': canonical_url,
        'site_name': 'Skyline Ghana Constructions',
        'company_name': 'Skyline Ghana Constructions',
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
    
    # Add default logo/image as fallback
    if not meta_data['og_image']:
        # Use a default logo/image path - you can update this path to your actual logo
        meta_data['og_image'] = '/static/images/skyline-logo-og.png'
    
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
            "@type": ["Organization", "LocalBusiness", "GeneralContractor"],
            "name": "Skyline Ghana Constructions",
            "alternateName": ["Skyline GH", "Skylink GH", "Skylink", "SkylineGH", "Skyline Ghana"],
            "url": "https://skylinegh.com",
            "logo": "https://skylinegh.com/static/images/skyline-logo.png",
            "image": "https://skylinegh.com/static/images/skyline-logo-og.png",
            "description": "Leading construction company in Ghana specializing in residential, commercial, and industrial building projects. Expert contractors delivering quality construction services across Accra and Ghana.",
            "slogan": "Building Dreams, Creating Futures",
            "foundingDate": "2015",
            "keywords": "skylinegh, skyline GH, Skylink GH, Skylink, construction Ghana, building contractors Ghana",
            "address": {
                "@type": "PostalAddress",
                "streetAddress": "Construction Avenue",
                "addressLocality": "Accra",
                "addressRegion": "Greater Accra",
                "postalCode": "00233",
                "addressCountry": "GH"
            },
            "geo": {
                "@type": "GeoCoordinates",
                "latitude": "5.6037",
                "longitude": "-0.1870"
            },
            "contactPoint": [{
                "@type": "ContactPoint",
                "telephone": "+233-24-123-4567",
                "contactType": "customer service",
                "email": "info@skylinegh.com",
                "availableLanguage": ["English"]
            }],
            "areaServed": {
                "@type": "Country",
                "name": "Ghana"
            },
            "serviceArea": {
                "@type": "GeoCircle",
                "geoMidpoint": {
                    "@type": "GeoCoordinates",
                    "latitude": "5.6037",
                    "longitude": "-0.1870"
                },
                "geoRadius": "200000"
            },
            "priceRange": "$$",
            "paymentAccepted": ["Cash", "Credit Card", "Bank Transfer"],
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
                    },
                    {
                        "@type": "Offer",
                        "itemOffered": {
                            "@type": "Service",
                            "name": "Industrial Construction",
                            "description": "Warehouses, factories, and industrial facility construction"
                        }
                    },
                    {
                        "@type": "Offer",
                        "itemOffered": {
                            "@type": "Service",
                            "name": "Renovation Services",
                            "description": "Building renovation and remodeling services"
                        }
                    }
                ]
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
