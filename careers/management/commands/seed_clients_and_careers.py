from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta

from core.models import Testimonial
from careers.models import Department, JobPosition


class Command(BaseCommand):
    help = "Seed the database with client testimonials and career positions"

    def handle(self, *args, **options):
        self.stdout.write("Seeding testimonials and careers...")
        self._seed_testimonials()
        self._seed_departments()
        self._seed_jobs()
        self.stdout.write(self.style.SUCCESS("Seeding complete."))

    # --- Helpers ---
    def _seed_testimonials(self):
        samples = [
            {
                'name': 'Kwame Mensah',
                'company': 'Accra Estates',
                'position': 'Project Director',
                'content': 'Skyline Ghana delivered exceptional quality and kept to our tight schedule. Highly recommended!',
                'rating': 5,
                'is_featured': True,
                'is_active': True,
            },
            {
                'name': 'Akosua Boateng',
                'company': 'Prime Retail',
                'position': 'Operations Manager',
                'content': 'Professional team with great communication. Our retail space transformation was outstanding.',
                'rating': 5,
                'is_featured': True,
                'is_active': True,
            },
            {
                'name': 'Nana Owusu',
                'company': 'GreenBuild Africa',
                'position': 'CEO',
                'content': 'Their attention to sustainable building practices impressed our entire board.',
                'rating': 4,
                'is_featured': False,
                'is_active': True,
            },
            {
                'name': 'Yaa Asantewaa',
                'company': 'Royal Residences',
                'position': 'Homeowner',
                'content': 'From design to finish, the process was smooth and the results are beautiful.',
                'rating': 5,
                'is_featured': False,
                'is_active': True,
            },
        ]

        created = 0
        for data in samples:
            _, was_created = Testimonial.objects.get_or_create(
                name=data['name'], company=data['company'], defaults=data
            )
            if was_created:
                created += 1
        self.stdout.write(f"✓ Testimonials added: {created} (idempotent)")

    def _seed_departments(self):
        departments = [
            {'name': 'Construction', 'description': 'Field construction and project management', 'head_of_department': 'John Mensah'},
            {'name': 'Engineering', 'description': 'Structural and civil engineering', 'head_of_department': 'Dr. Sarah Asante'},
            {'name': 'Architecture', 'description': 'Design and architectural planning', 'head_of_department': 'Kwame Osei'},
            {'name': 'Administration', 'description': 'Human resources and administration', 'head_of_department': 'Grace Adjei'},
            {'name': 'Procurement', 'description': 'Materials sourcing and vendor management', 'head_of_department': 'Michael Owusu'},
        ]
        for d in departments:
            Department.objects.get_or_create(name=d['name'], defaults=d)
        self.stdout.write("✓ Departments ensured")

    def _seed_jobs(self):
        jobs = [
            {
                'title': 'Senior Construction Manager',
                'department': 'Construction',
                'job_type': 'full_time',
                'experience_level': 'senior',
                'location': 'Accra, Ghana',
                'summary': 'Lead construction projects from planning to completion, ensuring quality, safety, and timely delivery.',
                'description': 'Oversee residential and commercial construction projects, manage teams and timelines.',
                'responsibilities': 'Plan and manage projects\nCoordinate teams and subcontractors\nMonitor budgets and timelines',
                'requirements': "Bachelor's in Construction Management\n5+ years experience\nStrong leadership",
                'qualifications': 'PMP preferred',
                'benefits': 'Competitive salary\nHealth insurance\nVehicle allowance',
                'salary_min': 8000,
                'salary_max': 12000,
                'status': 'active',
                'is_featured': True,
                'application_deadline': timezone.now() + timedelta(days=30),
            },
            {
                'title': 'Civil Engineer',
                'department': 'Engineering',
                'job_type': 'full_time',
                'experience_level': 'mid',
                'location': 'Accra, Ghana',
                'summary': 'Design and oversee construction of infrastructure projects.',
                'description': 'Design, plan, and oversee roads, bridges, and buildings.',
                'responsibilities': 'Design projects\nPrepare drawings\nConduct site inspections',
                'requirements': "BSc Civil Engineering\n3+ years experience\nAutoCAD proficiency",
                'qualifications': 'Member, GhIE',
                'benefits': 'Salary + bonuses\nHealth insurance',
                'salary_min': 5000,
                'salary_max': 8000,
                'status': 'active',
                'application_deadline': timezone.now() + timedelta(days=45),
            },
            {
                'title': 'Architectural Designer',
                'department': 'Architecture',
                'job_type': 'full_time',
                'experience_level': 'junior',
                'location': 'Accra, Ghana',
                'summary': 'Create innovative architectural designs for diverse projects.',
                'description': 'Develop concepts, drawings and 3D models for projects.',
                'responsibilities': 'Prepare drawings and 3D models\nCollaborate with project teams',
                'requirements': "BSc Architecture\n1-3 years experience\nSketchUp/AutoCAD",
                'qualifications': 'Revit/ArchiCAD a plus',
                'benefits': 'Mentorship\nCareer growth',
                'salary_min': 3500,
                'salary_max': 5500,
                'status': 'active',
                'is_urgent': True,
                'application_deadline': timezone.now() + timedelta(days=20),
            },
            {
                'title': 'Procurement Officer',
                'department': 'Procurement',
                'job_type': 'full_time',
                'experience_level': 'mid',
                'location': 'Accra, Ghana',
                'summary': 'Manage sourcing, vendor relationships, and material quality.',
                'description': 'Source materials, negotiate with vendors, and ensure timely supply.',
                'responsibilities': 'Vendor sourcing\nPrice negotiation\nInventory coordination',
                'requirements': "BSc Supply Chain or related\n2+ years procurement",
                'qualifications': 'CIPS is an advantage',
                'benefits': 'Competitive salary\nHealth insurance',
                'salary_min': 4000,
                'salary_max': 6500,
                'status': 'active',
                'application_deadline': timezone.now() + timedelta(days=35),
            },
            {
                'title': 'HSE Officer',
                'department': 'Construction',
                'job_type': 'full_time',
                'experience_level': 'mid',
                'location': 'Accra, Ghana',
                'summary': 'Ensure site safety and compliance with HSE standards.',
                'description': 'Implement safety protocols, conduct trainings and audits.',
                'responsibilities': 'Develop HSE policies\nSite audits\nIncident reporting',
                'requirements': 'NEBOSH/IOSH certification\n3+ years HSE experience',
                'qualifications': 'Construction industry experience preferred',
                'benefits': 'Health insurance\nAllowances',
                'salary_min': 4200,
                'salary_max': 7000,
                'status': 'active',
                'application_deadline': timezone.now() + timedelta(days=40),
            },
        ]

        created = 0
        for data in jobs:
            dept_name = data.pop('department')
            try:
                department = Department.objects.get(name=dept_name)
            except Department.DoesNotExist:
                department = Department.objects.create(name=dept_name)
            data['department'] = department

            _, was_created = JobPosition.objects.get_or_create(
                title=data['title'], department=department, defaults=data
            )
            if was_created:
                created += 1
        self.stdout.write(f"✓ Job positions added: {created} (idempotent)")
