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
    SITE_NAME = "Skyline Ghana Constructions - Premier Building Contractors in Ghana"
    SITE_DESCRIPTION = "Leading construction company in Ghana specializing in residential, commercial, and industrial building projects. Expert contractors delivering quality construction services across Accra, Kumasi, and all regions of Ghana. Get free quotes for your construction project today."

    # Comprehensive construction keywords with your specified additions - optimized for Ghana market
    DEFAULT_KEYWORDS = 'skylinegh, skyline ghana, skyline GH, skylink GH, skylink, construction company ghana, building contractors ghana, construction services accra, residential construction ghana, commercial construction ghana, industrial construction ghana, building contractors accra, construction company accra, ghana construction, building services ghana, construction contractors ghana, ghana builders, construction projects ghana, building renovation ghana, property development ghana, construction management ghana, architectural services ghana, civil engineering ghana, building materials ghana, construction consultancy ghana, construction company near me, best construction company ghana, reliable builders ghana, quality construction services, affordable construction ghana, modern construction techniques, sustainable building ghana, green construction ghana, project management ghana, home construction ghana, office construction ghana, warehouse construction ghana, construction quotes ghana, building permits ghana, construction financing ghana'

    # Generate canonical URL (always use non-www version)
    canonical_url = 'https://skylinegh.com/'  # Default fallback
    if request:
        try:
            canonical_url = request.build_absolute_uri()
            # Ensure canonical URL uses non-www version
            if '://www.' in canonical_url:
                canonical_url = canonical_url.replace('://www.', '://')
            # For localhost development, use production URL
            if 'localhost' in canonical_url or '127.0.0.1' in canonical_url:
                path = request.get_full_path()
                canonical_url = f'https://skylinegh.com{path}'
        except Exception:
            # Fallback if request processing fails
            canonical_url = 'https://skylinegh.com/'

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
                "streetAddress": "123 Independence Avenue",
                "addressLocality": "East Legon",
                "addressRegion": "Greater Accra",
                "postalCode": "GA-123-4567",
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
                "availableLanguage": ["English"],
                "hoursAvailable": {
                    "@type": "OpeningHoursSpecification",
                    "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
                    "opens": "08:00",
                    "closes": "18:00"
                }
            }],
            "areaServed": [
                {
                    "@type": "City",
                    "name": "Accra"
                },
                {
                    "@type": "City",
                    "name": "Kumasi"
                },
                {
                    "@type": "City",
                    "name": "Tamale"
                },
                {
                    "@type": "City",
                    "name": "Cape Coast"
                },
                {
                    "@type": "Country",
                    "name": "Ghana"
                }
            ],
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
            "paymentAccepted": ["Cash", "Credit Card", "Bank Transfer", "Mobile Money"],
            "currenciesAccepted": "GHS",
            "openingHours": "Mo-Fr 08:00-18:00, Sa 09:00-16:00",
            "aggregateRating": {
                "@type": "AggregateRating",
                "ratingValue": "4.8",
                "reviewCount": "127",
                "bestRating": "5",
                "worstRating": "1"
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
