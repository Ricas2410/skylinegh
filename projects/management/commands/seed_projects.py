import random
from datetime import date, timedelta
from io import BytesIO

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from projects.models import Project, ProjectCategory
from services.models import ServiceCategory
from PIL import Image, ImageDraw, ImageFont


SAMPLE_PROJECTS = [
    ("Modern Residential Build", "A contemporary residence featuring open spaces and sustainable materials."),
    ("Office Complex Renovation", "Full interior renovation with modern finishes and energy-efficient lighting."),
    ("Retail Fit-Out", "Turnkey retail space delivery with custom joinery and branding elements."),
    ("Warehouse Construction", "Large-span structural build with optimized logistics flow."),
    ("Healthcare Facility Upgrade", "Compliance-driven refurbishment with patient-first design."),
    ("School Classroom Block", "New classroom block with improved ventilation and natural light."),
    ("Road Drainage Works", "Improved surface drainage and culvert installations to reduce flooding."),
    ("Luxury Apartment Finishing", "High-end interior finishing with bespoke cabinetry and stonework."),
]

COLORS = ["#6366F1", "#22C55E", "#F59E0B", "#EF4444", "#06B6D4", "#84CC16"]


def generate_placeholder_image(text: str, size=(1200, 720), bg=None) -> ContentFile:
    """Generate a simple placeholder image with text and return as ContentFile."""
    if bg is None:
        bg = tuple(int(COLORS[random.randrange(len(COLORS))].lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
    img = Image.new('RGB', size, bg)
    draw = ImageDraw.Draw(img)
    # Try to load a common font; fallback to default if not found
    try:
        font = ImageFont.truetype("arial.ttf", 48)
    except Exception:
        font = ImageFont.load_default()
    x1, y1, x2, y2 = draw.textbbox((0,0), text, font=font)
    w = x2 - x1
    h = y2 - y1
    draw.text(((size[0]-w)//2, (size[1]-h)//2), text, fill=(255, 255, 255), font=font)
    buf = BytesIO()
    img.save(buf, format='JPEG', quality=85)
    return ContentFile(buf.getvalue(), name=f"{slugify(text)}.jpg")


class Command(BaseCommand):
    help = "Seed the database with sample Project data for testing."

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING("Seeding sample projects..."))

        # Ensure some ProjectCategories exist
        default_categories = [
            ("Residential", "Homes, apartments, and villas"),
            ("Commercial", "Offices, retail, and warehouses"),
            ("Infrastructure", "Roads, drainage, and utilities"),
            ("Healthcare", "Hospitals and clinics"),
            ("Education", "Schools and universities"),
        ]
        cat_objs = []
        for idx, (name, desc) in enumerate(default_categories):
            cat, _ = ProjectCategory.objects.get_or_create(
                name=name,
                defaults={
                    'description': desc,
                    'color': COLORS[idx % len(COLORS)],
                    'order': idx,
                    'is_active': True,
                }
            )
            cat_objs.append(cat)

        service_categories = list(ServiceCategory.objects.all())

        created = 0
        for i, (title, short_desc) in enumerate(SAMPLE_PROJECTS, start=1):
            if Project.objects.filter(slug=slugify(title)).exists():
                continue

            start_delta = random.randint(30, 400)
            start_date = date.today() - timedelta(days=start_delta)
            completion_date = start_date + timedelta(days=random.randint(20, 250)) if random.choice([True, False]) else None

            project = Project(
                title=title,
                short_description=short_desc,
                description=f"{short_desc}\n\nThis is a seeded project used for testing listings, detail pages, and admin forms.",
                client_name=random.choice(["Skyline Client", "Acme Corp", "Globex", "Wayne Holdings", "Stark Industries", ""]),
                location=random.choice(["Accra", "Kumasi", "Tema", "Takoradi", "Tamale"]),
                project_type=random.choice(cat_objs),
                service_category=random.choice(service_categories) if service_categories else None,
                start_date=start_date,
                completion_date=completion_date,
                duration_months=None,
                is_featured=random.choice([True, False, False]),
                is_published=True,
                order=i,
            )
            # featured image
            project.featured_image = generate_placeholder_image(title)
            project.save()
            created += 1

        self.stdout.write(self.style.SUCCESS(f"Created {created} sample projects."))
