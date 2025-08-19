from django.core.management.base import BaseCommand
from core.models import TeamMember


class Command(BaseCommand):
    help = 'Populate team members with sample data'

    def handle(self, *args, **options):
        self.stdout.write('Creating team members...')

        team_members_data = [
            {
                'name': 'Kwame Asante',
                'position': 'CEO & Founder',
                'bio': 'Visionary leader with over 25 years in construction management and business development.',
                'detailed_bio': 'Kwame Asante founded Skyline Ghana Constructions in 1998 with a vision to transform Ghana\'s construction landscape. With over 25 years of experience in construction management and business development, he has led the company from a small local contractor to one of Ghana\'s most trusted construction companies. His expertise spans project management, business strategy, and sustainable construction practices. Under his leadership, Skyline Ghana has completed over 500 successful projects across residential, commercial, and industrial sectors.',
                'years_experience': 25,
                'specializations': 'Strategic Planning\nBusiness Development\nProject Management\nSustainable Construction\nClient Relations',
                'education': 'MBA in Business Administration - University of Ghana Business School\nBSc Civil Engineering - Kwame Nkrumah University of Science and Technology',
                'certifications': 'Project Management Professional (PMP)\nGhana Institute of Construction Certification\nSustainable Building Council Certification',
                'email': 'kwame.asante@skylinegh.com',
                'phone': '+233 24 123 4567',
                'linkedin_url': 'https://linkedin.com/in/kwame-asante',
                'is_featured': True,
                'order': 1
            },
            {
                'name': 'Dr. Sarah Mensah',
                'position': 'Chief Engineer',
                'bio': 'PhD in Civil Engineering, specialist in sustainable construction and innovative building solutions.',
                'detailed_bio': 'Dr. Sarah Mensah brings over 15 years of engineering excellence to Skyline Ghana Constructions. With a PhD in Civil Engineering from KNUST and specialized training in sustainable construction, she leads our technical team in developing innovative solutions for complex construction challenges. Her research in green building technologies has been published in international journals, and she regularly speaks at construction industry conferences across West Africa.',
                'years_experience': 15,
                'specializations': 'Structural Engineering\nSustainable Construction\nGreen Building Technologies\nProject Design\nQuality Assurance',
                'education': 'PhD Civil Engineering - Kwame Nkrumah University of Science and Technology\nMSc Structural Engineering - University of Cape Coast\nBSc Civil Engineering - KNUST',
                'certifications': 'Professional Engineer (PE) License\nLEED Accredited Professional\nGhana Institution of Engineers Certification\nProject Management Certification',
                'email': 'sarah.mensah@skylinegh.com',
                'phone': '+233 24 234 5678',
                'linkedin_url': 'https://linkedin.com/in/sarah-mensah',
                'is_featured': True,
                'order': 2
            },
            {
                'name': 'John Osei',
                'position': 'Project Manager',
                'bio': 'Expert in large-scale commercial and residential projects with focus on timeline management and quality assurance.',
                'detailed_bio': 'John Osei is a certified Project Management Professional with over 12 years of experience managing complex construction projects. He has successfully delivered projects worth over GHS 50 million, consistently meeting deadlines and budget requirements. His expertise in project coordination, resource management, and stakeholder communication has made him an invaluable asset to our team.',
                'years_experience': 12,
                'specializations': 'Project Management\nResource Planning\nQuality Control\nStakeholder Management\nRisk Assessment',
                'education': 'MSc Project Management - University of Ghana\nBSc Construction Technology - KNUST',
                'certifications': 'Project Management Professional (PMP)\nPRINCE2 Certification\nConstruction Project Management Certificate',
                'email': 'john.osei@skylinegh.com',
                'phone': '+233 24 345 6789',
                'linkedin_url': 'https://linkedin.com/in/john-osei',
                'is_featured': True,
                'order': 3
            },
            {
                'name': 'Grace Adjei',
                'position': 'Head of Operations',
                'bio': 'Operations excellence specialist focused on quality control and process optimization.',
                'detailed_bio': 'Grace Adjei oversees all operational aspects of Skyline Ghana Constructions with a focus on quality control and process optimization. With an MBA in Operations Management and 10 years of experience in the construction industry, she ensures that every project meets our high standards of quality and efficiency. Her systematic approach to operations has improved project delivery times by 30% while maintaining exceptional quality standards.',
                'years_experience': 10,
                'specializations': 'Operations Management\nQuality Control\nProcess Optimization\nSupply Chain Management\nTeam Leadership',
                'education': 'MBA Operations Management - University of Ghana Business School\nBSc Business Administration - University of Cape Coast',
                'certifications': 'Six Sigma Green Belt\nQuality Management System Certification\nOperations Management Professional Certificate',
                'email': 'grace.adjei@skylinegh.com',
                'phone': '+233 24 456 7890',
                'linkedin_url': 'https://linkedin.com/in/grace-adjei',
                'is_featured': True,
                'order': 4
            },
            {
                'name': 'Michael Boateng',
                'position': 'Senior Architect',
                'bio': 'Creative architect specializing in modern residential and commercial design.',
                'detailed_bio': 'Michael Boateng is our lead architect with a passion for creating innovative and functional designs. With 8 years of experience in architectural design, he has contributed to some of Ghana\'s most iconic buildings. His designs seamlessly blend modern aesthetics with traditional Ghanaian elements, creating spaces that are both beautiful and culturally relevant.',
                'years_experience': 8,
                'specializations': 'Architectural Design\nSpace Planning\n3D Modeling\nSustainable Design\nBuilding Information Modeling (BIM)',
                'education': 'MArch Architecture - KNUST\nBSc Architecture - University of Ghana',
                'certifications': 'Ghana Institute of Architects Certification\nAutodesk Certified Professional\nGreen Building Design Certificate',
                'email': 'michael.boateng@skylinegh.com',
                'phone': '+233 24 567 8901',
                'linkedin_url': 'https://linkedin.com/in/michael-boateng',
                'is_featured': False,
                'order': 5
            },
            {
                'name': 'Akosua Frimpong',
                'position': 'Finance Director',
                'bio': 'Financial strategist ensuring project profitability and sustainable business growth.',
                'detailed_bio': 'Akosua Frimpong manages all financial aspects of Skyline Ghana Constructions with expertise in construction finance and cost management. Her strategic financial planning has enabled the company to maintain healthy profit margins while offering competitive pricing to clients. She holds professional certifications in accounting and has been instrumental in securing financing for major projects.',
                'years_experience': 12,
                'specializations': 'Financial Management\nCost Estimation\nBudget Planning\nRisk Management\nInvestment Analysis',
                'education': 'MBA Finance - University of Ghana Business School\nBSc Accounting - University of Professional Studies',
                'certifications': 'Chartered Accountant (CA)\nCertified Management Accountant (CMA)\nProject Finance Certification',
                'email': 'akosua.frimpong@skylinegh.com',
                'phone': '+233 24 678 9012',
                'linkedin_url': 'https://linkedin.com/in/akosua-frimpong',
                'is_featured': False,
                'order': 6
            }
        ]

        for member_data in team_members_data:
            member, created = TeamMember.objects.get_or_create(
                name=member_data['name'],
                defaults=member_data
            )
            if created:
                self.stdout.write(f'Created team member: {member.name}')
            else:
                self.stdout.write(f'Team member already exists: {member.name}')

        self.stdout.write(self.style.SUCCESS('Successfully populated team members'))
