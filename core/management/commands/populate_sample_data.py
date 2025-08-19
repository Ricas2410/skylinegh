from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
from core.models import SiteSettings, Testimonial
from careers.models import Department, JobPosition
from services.models import ServiceCategory, Service

class Command(BaseCommand):
    help = 'Populate the database with sample data'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        # Create site settings
        self.create_site_settings()
        
        # Create service categories and services
        self.create_services()
        
        # Create departments and job positions
        self.create_careers()
        
        # Create sample testimonials
        self.create_testimonials()

        self.stdout.write(self.style.SUCCESS('Sample data created successfully!'))

    def create_site_settings(self):
        """Create site settings"""
        site_settings, created = SiteSettings.objects.get_or_create(
            defaults={
                'site_name': 'Skyline Ghana Constructions',
                'site_tagline': 'Building Dreams, Creating Futures',
                'site_description': 'Professional construction services in Ghana. From residential homes to commercial buildings, we bring your vision to life with quality craftsmanship and modern techniques.',
                'phone_primary': '+233 24 123 4567',
                'phone_secondary': '+233 30 987 6543',
                'email_primary': 'info@skylinegh.com',
                'email_secondary': 'projects@skylinegh.com',
                'address_line_1': '123 Independence Avenue',
                'address_line_2': 'East Legon',
                'city': 'Accra',
                'region': 'Greater Accra',
                'postal_code': 'GA-123-4567',
                'facebook_url': 'https://facebook.com/skylineghana',
                'twitter_url': 'https://twitter.com/skylineghana',
                'instagram_url': 'https://instagram.com/skylineghana',
                'linkedin_url': 'https://linkedin.com/company/skylineghana',
                'meta_keywords': 'construction, building, Ghana, residential, commercial, architecture',
                'meta_description': 'Professional construction services in Ghana - residential and commercial building solutions',
                'business_hours': 'Monday - Friday: 8:00 AM - 6:00 PM\nSaturday: 9:00 AM - 4:00 PM\nSunday: Closed',
            }
        )
        if created:
            self.stdout.write('✓ Site settings created')
        else:
            self.stdout.write('✓ Site settings already exist')

    def create_services(self):
        """Create service categories and services"""
        categories_data = [
            {
                'name': 'Residential & Commercial Construction',
                'slug': 'residential-commercial-construction',
                'description': 'Complete building solutions from new construction to renovations and extensions.',
                'short_description': 'New construction, renovations, and building extensions',
                'icon': 'building',
                'services': [
                    {
                        'name': 'New Home Construction',
                        'description': 'Custom home building from foundation to finish',
                        'short_description': 'Build your dream home from the ground up'
                    },
                    {
                        'name': 'Commercial Building',
                        'description': 'Office buildings, retail spaces, and commercial complexes',
                        'short_description': 'Professional commercial construction services'
                    },
                    {
                        'name': 'Home Renovations',
                        'description': 'Complete home makeovers and room additions',
                        'short_description': 'Transform your existing space'
                    }
                ]
            },
            {
                'name': 'Building Materials & Supply',
                'slug': 'building-materials-supply',
                'description': 'High-quality construction materials including cement, blocks, steel, and specialized supplies.',
                'short_description': 'Quality materials for all construction needs',
                'icon': 'cube',
                'services': [
                    {
                        'name': 'Cement & Concrete',
                        'description': 'Premium cement and ready-mix concrete supply',
                        'short_description': 'High-grade cement and concrete products'
                    },
                    {
                        'name': 'Steel & Reinforcement',
                        'description': 'Construction steel, rebar, and reinforcement materials',
                        'short_description': 'Quality steel for structural integrity'
                    }
                ]
            },
            {
                'name': 'Interior Finishing Services',
                'slug': 'interior-finishing-services',
                'description': 'Professional finishing services including painting, tiling, roofing, and HVAC installation.',
                'short_description': 'Expert finishing touches for your project',
                'icon': 'paint-brush',
                'services': [
                    {
                        'name': 'Interior Painting',
                        'description': 'Professional interior painting and decorating',
                        'short_description': 'Transform interiors with expert painting'
                    },
                    {
                        'name': 'Roofing Services',
                        'description': 'Roof installation, repair, and maintenance',
                        'short_description': 'Complete roofing solutions'
                    }
                ]
            },
            {
                'name': 'Architectural & Design Services',
                'slug': 'architectural-design-services',
                'description': 'Custom architectural design, 3D rendering, and structural engineering consultation.',
                'short_description': 'Professional design and planning services',
                'icon': 'blueprint',
                'services': [
                    {
                        'name': 'Architectural Design',
                        'description': 'Custom architectural plans and designs',
                        'short_description': 'Professional architectural planning'
                    },
                    {
                        'name': '3D Visualization',
                        'description': '3D rendering and virtual walkthroughs',
                        'short_description': 'See your project before it\'s built'
                    }
                ]
            }
        ]
        
        for cat_data in categories_data:
            services_data = cat_data.pop('services')
            category, created = ServiceCategory.objects.get_or_create(
                slug=cat_data['slug'],
                defaults=cat_data
            )
            if created:
                self.stdout.write(f'✓ Created service category: {category.name}')
            
            for service_data in services_data:
                service, created = Service.objects.get_or_create(
                    category=category,
                    name=service_data['name'],
                    defaults=service_data
                )
                if created:
                    self.stdout.write(f'  ✓ Created service: {service.name}')

    def create_careers(self):
        """Create departments and job positions"""
        departments_data = [
            {
                'name': 'Construction',
                'description': 'Field construction and project management',
                'head_of_department': 'John Mensah'
            },
            {
                'name': 'Engineering',
                'description': 'Structural and civil engineering',
                'head_of_department': 'Dr. Sarah Asante'
            },
            {
                'name': 'Architecture',
                'description': 'Design and architectural planning',
                'head_of_department': 'Kwame Osei'
            },
            {
                'name': 'Administration',
                'description': 'Human resources and administration',
                'head_of_department': 'Grace Adjei'
            }
        ]
        
        for dept_data in departments_data:
            department, created = Department.objects.get_or_create(
                name=dept_data['name'],
                defaults=dept_data
            )
            if created:
                self.stdout.write(f'✓ Created department: {department.name}')
        
        # Create job positions
        jobs_data = [
            {
                'title': 'Senior Construction Manager',
                'department': 'Construction',
                'job_type': 'full_time',
                'experience_level': 'senior',
                'location': 'Accra, Ghana',
                'summary': 'Lead construction projects from planning to completion, ensuring quality, safety, and timely delivery.',
                'description': 'We are seeking an experienced Construction Manager to oversee our residential and commercial construction projects. The ideal candidate will have extensive experience in project management, team leadership, and construction operations.',
                'responsibilities': 'Manage construction projects from start to finish\nCoordinate with architects, engineers, and subcontractors\nEnsure compliance with safety regulations and building codes\nMonitor project budgets and timelines\nLead and supervise construction teams',
                'requirements': 'Bachelor\'s degree in Construction Management or related field\n5+ years of construction management experience\nStrong leadership and communication skills\nKnowledge of building codes and safety regulations\nProficiency in project management software',
                'qualifications': 'PMP certification preferred\nExperience with commercial construction projects\nKnowledge of sustainable building practices\nBilingual (English/Local languages) preferred',
                'benefits': 'Competitive salary and performance bonuses\nHealth insurance for employee and family\nProfessional development opportunities\nCompany vehicle allowance\nPaid vacation and sick leave',
                'salary_min': 8000,
                'salary_max': 12000,
                'status': 'active',
                'is_featured': True,
                'application_deadline': timezone.now() + timedelta(days=30)
            },
            {
                'title': 'Civil Engineer',
                'department': 'Engineering',
                'job_type': 'full_time',
                'experience_level': 'mid',
                'location': 'Accra, Ghana',
                'summary': 'Design and oversee construction of infrastructure projects including roads, bridges, and buildings.',
                'description': 'Join our engineering team to work on exciting infrastructure and building projects across Ghana. You will be responsible for designing, planning, and overseeing construction projects.',
                'responsibilities': 'Design civil engineering projects and infrastructure\nPrepare technical drawings and specifications\nConduct site inspections and quality control\nCollaborate with construction teams and contractors\nEnsure compliance with engineering standards',
                'requirements': 'Bachelor\'s degree in Civil Engineering\n3+ years of civil engineering experience\nProficiency in AutoCAD and engineering software\nStrong analytical and problem-solving skills\nRegistered with Ghana Institution of Engineers',
                'qualifications': 'Master\'s degree in Civil Engineering\nExperience with structural design software\nKnowledge of Ghanaian building codes\nProject management experience',
                'benefits': 'Competitive salary package\nHealth and dental insurance\nProfessional development support\nFlexible working arrangements\nAnnual performance bonuses',
                'salary_min': 5000,
                'salary_max': 8000,
                'status': 'active',
                'application_deadline': timezone.now() + timedelta(days=45)
            },
            {
                'title': 'Architectural Designer',
                'department': 'Architecture',
                'job_type': 'full_time',
                'experience_level': 'junior',
                'location': 'Accra, Ghana',
                'summary': 'Create innovative architectural designs for residential and commercial projects.',
                'description': 'We are looking for a creative Architectural Designer to join our design team. You will work on diverse projects ranging from residential homes to commercial buildings.',
                'responsibilities': 'Develop architectural designs and concepts\nPrepare detailed drawings and 3D models\nCollaborate with clients and project teams\nConduct site visits and feasibility studies\nStay updated with design trends and building technologies',
                'requirements': 'Bachelor\'s degree in Architecture\n1-3 years of architectural design experience\nProficiency in AutoCAD, SketchUp, and Adobe Creative Suite\nStrong creative and visualization skills\nKnowledge of building codes and regulations',
                'qualifications': 'Experience with BIM software (Revit, ArchiCAD)\nPortfolio of completed projects\nSustainable design knowledge\nExcellent presentation skills',
                'benefits': 'Competitive starting salary\nHealth insurance coverage\nCreative and collaborative work environment\nTraining and mentorship programs\nCareer advancement opportunities',
                'salary_min': 3500,
                'salary_max': 5500,
                'status': 'active',
                'is_urgent': True,
                'application_deadline': timezone.now() + timedelta(days=20)
            }
        ]
        
        for job_data in jobs_data:
            dept_name = job_data.pop('department')
            department = Department.objects.get(name=dept_name)
            job_data['department'] = department
            
            job, created = JobPosition.objects.get_or_create(
                title=job_data['title'],
                department=department,
                defaults=job_data
            )
            if created:
                self.stdout.write(f'✓ Created job position: {job.title}')

    def create_testimonials(self):
        """Create sample testimonials"""
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

        created_count = 0
        for data in samples:
            obj, created = Testimonial.objects.get_or_create(
                name=data['name'], company=data['company'], defaults=data
            )
            if created:
                created_count += 1
        if created_count:
            self.stdout.write(f'✓ Created {created_count} testimonials')
        else:
            self.stdout.write('✓ Testimonials already exist')
