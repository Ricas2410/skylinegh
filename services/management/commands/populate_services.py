from django.core.management.base import BaseCommand
from services.models import ServiceCategory, Service


class Command(BaseCommand):
    help = 'Populate services with sample data'

    def handle(self, *args, **options):
        self.stdout.write('Creating service categories and services...')

        # Create Residential & Commercial Construction category
        residential_category, created = ServiceCategory.objects.get_or_create(
            slug='residential-commercial-construction',
            defaults={
                'name': 'Residential & Commercial Construction',
                'description': 'Complete construction solutions for residential homes, commercial buildings, and mixed-use developments. From foundation to finishing, we deliver quality construction that stands the test of time.',
                'short_description': 'Complete construction solutions for homes and commercial buildings',
                'icon': 'fas fa-building',
                'is_active': True
            }
        )

        if created:
            # Create services for Residential & Commercial Construction
            services_data = [
                {
                    'name': 'New Home Construction',
                    'description': 'Complete new home construction from foundation to move-in ready.',
                    'short_description': 'Custom new home construction services',
                    'detailed_description': 'Our new home construction service provides complete end-to-end solutions for building your dream home. From initial design consultation to final walkthrough, we manage every aspect of the construction process. Our experienced team works with you to create a home that reflects your lifestyle and preferences while staying within your budget and timeline.',
                    'features': 'Custom architectural design\nQuality materials and craftsmanship\nProject management and coordination\nTimely completion\nWarranty and after-sales support',
                    'benefits': 'Personalized home design\nQuality construction\nProfessional project management\nOn-time delivery\nComprehensive warranty',
                    'process_steps': 'Initial consultation and site assessment\nArchitectural design and planning\nPermit acquisition\nFoundation and structural work\nRoofing and exterior work\nInterior finishing\nFinal inspection and handover',
                    'starting_price': 150000,
                    'price_unit': 'per project',
                    'is_featured': True
                },
                {
                    'name': 'Commercial Building Construction',
                    'description': 'Professional commercial construction for offices, retail, and industrial facilities.',
                    'short_description': 'Commercial building construction services',
                    'detailed_description': 'We specialize in commercial construction projects including office buildings, retail spaces, warehouses, and industrial facilities. Our team has extensive experience in commercial construction requirements, building codes, and project management for large-scale developments.',
                    'features': 'Commercial-grade construction\nCode compliance expertise\nProject scheduling\nQuality control systems\nSafety protocols',
                    'benefits': 'Professional construction standards\nRegulatory compliance\nEfficient project delivery\nQuality assurance\nSafety first approach',
                    'process_steps': 'Project planning and design\nPermit and regulatory approval\nSite preparation\nStructural construction\nMEP installation\nInterior build-out\nFinal inspection and commissioning',
                    'starting_price': 500000,
                    'price_unit': 'per project',
                    'is_featured': True
                },
                {
                    'name': 'Home Renovations',
                    'description': 'Complete home renovation and remodeling services.',
                    'short_description': 'Professional home renovation services',
                    'detailed_description': 'Transform your existing home with our comprehensive renovation services. Whether you\'re updating a single room or undertaking a whole-house renovation, we provide expert craftsmanship and project management to bring your vision to life.',
                    'features': 'Complete renovation planning\nStructural modifications\nModern design integration\nQuality materials\nMinimal disruption',
                    'benefits': 'Increased home value\nImproved functionality\nModern aesthetics\nEnergy efficiency\nPersonalized design',
                    'process_steps': 'Assessment and planning\nDesign development\nPermit acquisition\nDemolition and preparation\nConstruction and installation\nFinishing and cleanup\nFinal walkthrough',
                    'starting_price': 50000,
                    'price_unit': 'per project'
                }
            ]

            for service_data in services_data:
                Service.objects.create(
                    category=residential_category,
                    slug=service_data['name'].lower().replace(' ', '-'),
                    **service_data
                )

        # Create Building Materials Supply category
        materials_category, created = ServiceCategory.objects.get_or_create(
            slug='building-materials-supply',
            defaults={
                'name': 'Building Materials Supply',
                'description': 'High-quality building materials sourced from trusted suppliers. We provide everything you need for your construction project, from basic materials to specialized components.',
                'short_description': 'Quality building materials for all construction needs',
                'icon': 'fas fa-boxes',
                'is_active': True
            }
        )

        if created:
            # Create services for Building Materials Supply
            services_data = [
                {
                    'name': 'Cement & Concrete Products',
                    'description': 'Premium cement, concrete blocks, and ready-mix concrete.',
                    'short_description': 'Quality cement and concrete products',
                    'detailed_description': 'We supply high-grade cement and concrete products for all types of construction projects. Our products meet international standards and are sourced from reputable manufacturers to ensure durability and strength.',
                    'features': 'High-grade cement\nVarious concrete block sizes\nReady-mix concrete\nTimely delivery\nQuality assurance',
                    'benefits': 'Superior strength\nConsistent quality\nReliable supply\nCompetitive pricing\nTechnical support',
                    'process_steps': 'Material specification\nOrder placement\nQuality verification\nScheduled delivery\nOn-site support',
                    'starting_price': 25,
                    'price_unit': 'per bag'
                },
                {
                    'name': 'Steel & Reinforcement',
                    'description': 'Quality steel bars, mesh, and structural steel products.',
                    'short_description': 'Steel and reinforcement materials',
                    'detailed_description': 'Our steel and reinforcement products include rebar, steel mesh, structural steel, and specialized steel components. All products are certified and meet construction industry standards for strength and durability.',
                    'features': 'Certified steel products\nVarious sizes and grades\nStructural steel beams\nReinforcement mesh\nCustom cutting service',
                    'benefits': 'Structural integrity\nCorrosion resistance\nPrecise specifications\nReliable supply chain\nTechnical expertise',
                    'process_steps': 'Requirements assessment\nProduct selection\nQuality certification\nCustom processing\nDelivery and installation support',
                    'starting_price': 3500,
                    'price_unit': 'per ton'
                },
                {
                    'name': 'Roofing Materials',
                    'description': 'Complete roofing solutions including sheets, tiles, and accessories.',
                    'short_description': 'Quality roofing materials and accessories',
                    'detailed_description': 'We provide comprehensive roofing materials including metal sheets, clay tiles, concrete tiles, and all necessary accessories. Our products are weather-resistant and designed for Ghana\'s climate conditions.',
                    'features': 'Weather-resistant materials\nVarious roofing options\nComplete accessory range\nInstallation guidance\nWarranty coverage',
                    'benefits': 'Long-lasting protection\nClimate-appropriate\nAesthetic appeal\nEnergy efficiency\nProfessional support',
                    'process_steps': 'Roof assessment\nMaterial selection\nQuantity calculation\nOrder processing\nDelivery and installation support',
                    'starting_price': 45,
                    'price_unit': 'per sheet'
                }
            ]

            for service_data in services_data:
                Service.objects.create(
                    category=materials_category,
                    slug=service_data['name'].lower().replace(' ', '-').replace('&', 'and'),
                    **service_data
                )

        # Create Finishing & Specialized Services category
        finishing_category, created = ServiceCategory.objects.get_or_create(
            slug='finishing-specialized-services',
            defaults={
                'name': 'Finishing & Specialized Services',
                'description': 'Professional finishing services including painting, tiling, electrical, plumbing, and specialized construction services to complete your project.',
                'short_description': 'Professional finishing and specialized construction services',
                'icon': 'fas fa-paint-brush',
                'is_active': True
            }
        )

        if created:
            # Create services for Finishing & Specialized Services
            services_data = [
                {
                    'name': 'Interior & Exterior Painting',
                    'description': 'Professional painting services for interior and exterior surfaces.',
                    'short_description': 'Quality painting services for all surfaces',
                    'detailed_description': 'Our professional painting services cover both interior and exterior applications. We use premium paints and employ skilled painters to deliver flawless finishes that enhance the beauty and protect your property.',
                    'features': 'Premium paint products\nSurface preparation\nColor consultation\nProfessional application\nCleanup service',
                    'benefits': 'Beautiful finish\nLong-lasting protection\nExpert color advice\nProfessional results\nComplete service',
                    'process_steps': 'Surface inspection\nPreparation and priming\nColor selection\nPaint application\nQuality inspection\nCleanup and handover',
                    'starting_price': 15,
                    'price_unit': 'per sq meter'
                },
                {
                    'name': 'Tiling & Flooring',
                    'description': 'Expert tiling and flooring installation services.',
                    'short_description': 'Professional tiling and flooring services',
                    'detailed_description': 'We provide comprehensive tiling and flooring services including ceramic tiles, porcelain tiles, natural stone, and various flooring options. Our skilled craftsmen ensure precise installation and beautiful results.',
                    'features': 'Various tile options\nPrecise installation\nPattern design\nWaterproofing\nFinishing work',
                    'benefits': 'Durable surfaces\nAesthetic appeal\nWater resistance\nEasy maintenance\nProfessional finish',
                    'process_steps': 'Surface preparation\nMaterial selection\nLayout planning\nInstallation\nGrouting and sealing\nFinal cleaning',
                    'starting_price': 35,
                    'price_unit': 'per sq meter'
                },
                {
                    'name': 'Electrical & Plumbing',
                    'description': 'Complete electrical and plumbing installation and maintenance.',
                    'short_description': 'Electrical and plumbing services',
                    'detailed_description': 'Our certified electricians and plumbers provide complete installation, repair, and maintenance services. We ensure all work meets safety standards and building codes.',
                    'features': 'Certified professionals\nCode compliance\nSafety standards\nQuality materials\nMaintenance support',
                    'benefits': 'Safe installations\nReliable systems\nCode compliance\nProfessional service\nOngoing support',
                    'process_steps': 'System design\nMaterial procurement\nInstallation\nTesting and commissioning\nCertification\nMaintenance planning',
                    'starting_price': 2500,
                    'price_unit': 'per room'
                }
            ]

            for service_data in services_data:
                Service.objects.create(
                    category=finishing_category,
                    slug=service_data['name'].lower().replace(' ', '-').replace('&', 'and'),
                    **service_data
                )

        # Create Architectural Design Services category
        design_category, created = ServiceCategory.objects.get_or_create(
            slug='architectural-design-services',
            defaults={
                'name': 'Architectural Design Services',
                'description': 'Professional architectural design and planning services for residential, commercial, and industrial projects. From concept to construction drawings.',
                'short_description': 'Professional architectural design and planning services',
                'icon': 'fas fa-drafting-compass',
                'is_active': True
            }
        )

        if created:
            # Create services for Architectural Design Services
            services_data = [
                {
                    'name': 'Residential Design',
                    'description': 'Custom residential architectural design services.',
                    'short_description': 'Custom home and residential design',
                    'detailed_description': 'Our residential design services create beautiful, functional homes tailored to your lifestyle and preferences. We work closely with clients to develop designs that maximize space, natural light, and comfort while reflecting personal style.',
                    'features': 'Custom design solutions\n3D visualization\nSpace optimization\nSustainable design\nLocal building compliance',
                    'benefits': 'Personalized design\nOptimal space usage\nEnergy efficiency\nIncreased property value\nProfessional expertise',
                    'process_steps': 'Client consultation\nSite analysis\nConcept development\nDesign refinement\nTechnical drawings\nPermit documentation',
                    'starting_price': 25000,
                    'price_unit': 'per project'
                },
                {
                    'name': 'Commercial Design',
                    'description': 'Professional commercial and office building design.',
                    'short_description': 'Commercial building design services',
                    'detailed_description': 'We specialize in commercial architectural design including office buildings, retail spaces, restaurants, and mixed-use developments. Our designs focus on functionality, efficiency, and creating environments that support business success.',
                    'features': 'Functional design\nBrand integration\nAccessibility compliance\nEfficient layouts\nFuture expansion planning',
                    'benefits': 'Business-focused design\nRegulatory compliance\nOperational efficiency\nBrand enhancement\nScalable solutions',
                    'process_steps': 'Business requirements analysis\nSpace programming\nConcept design\nDevelopment design\nConstruction documentation\nPermit assistance',
                    'starting_price': 75000,
                    'price_unit': 'per project'
                },
                {
                    'name': 'Interior Design',
                    'description': 'Complete interior design and space planning services.',
                    'short_description': 'Professional interior design services',
                    'detailed_description': 'Our interior design services transform spaces into beautiful, functional environments. We handle everything from space planning and color schemes to furniture selection and lighting design.',
                    'features': 'Space planning\nColor consultation\nFurniture selection\nLighting design\nMaterial specification',
                    'benefits': 'Beautiful interiors\nFunctional layouts\nPersonalized style\nProfessional coordination\nComplete service',
                    'process_steps': 'Space assessment\nDesign concept\nMaterial selection\nFurniture planning\nImplementation\nStyling and finishing',
                    'starting_price': 15000,
                    'price_unit': 'per room'
                }
            ]

            for service_data in services_data:
                Service.objects.create(
                    category=design_category,
                    slug=service_data['name'].lower().replace(' ', '-'),
                    **service_data
                )

        self.stdout.write(self.style.SUCCESS('Successfully populated services'))
