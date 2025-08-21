# Generated manually to add default project categories

from django.db import migrations, models


def create_default_project_categories(apps, schema_editor):
    ProjectCategory = apps.get_model('projects', 'ProjectCategory')
    from django.utils.text import slugify

    default_categories = [
        {
            'name': 'Residential Construction',
            'slug': 'residential-construction',
            'description': 'Single-family homes, apartments, condominiums, and other residential buildings',
            'color': '#10b981',
            'order': 1
        },
        {
            'name': 'Commercial Construction',
            'slug': 'commercial-construction',
            'description': 'Office buildings, retail spaces, warehouses, and commercial facilities',
            'color': '#3b82f6',
            'order': 2
        },
        {
            'name': 'Industrial Construction',
            'slug': 'industrial-construction',
            'description': 'Factories, manufacturing plants, and industrial facilities',
            'color': '#f59e0b',
            'order': 3
        },
        {
            'name': 'Infrastructure Projects',
            'slug': 'infrastructure-projects',
            'description': 'Roads, bridges, utilities, and public infrastructure',
            'color': '#8b5cf6',
            'order': 4
        },
        {
            'name': 'Renovation & Remodeling',
            'slug': 'renovation-remodeling',
            'description': 'Home improvements, office renovations, and building upgrades',
            'color': '#ef4444',
            'order': 5
        },
        {
            'name': 'Specialized Services',
            'slug': 'specialized-services',
            'description': 'Custom projects, architectural design, and specialized construction',
            'color': '#06b6d4',
            'order': 6
        }
    ]

    for category_data in default_categories:
        # Check if category already exists by name or slug
        if not ProjectCategory.objects.filter(
            models.Q(name=category_data['name']) | models.Q(slug=category_data['slug'])
        ).exists():
            ProjectCategory.objects.create(**category_data)


def remove_default_project_categories(apps, schema_editor):
    ProjectCategory = apps.get_model('projects', 'ProjectCategory')
    
    default_names = [
        'Residential Construction',
        'Commercial Construction', 
        'Industrial Construction',
        'Infrastructure Projects',
        'Renovation & Remodeling',
        'Specialized Services'
    ]
    
    ProjectCategory.objects.filter(name__in=default_names).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_auto_20250821_1301'),
    ]

    operations = [
        migrations.RunPython(
            create_default_project_categories,
            remove_default_project_categories
        ),
    ]
