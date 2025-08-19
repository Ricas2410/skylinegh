from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone
from core.models import TimeStampedModel
import os

class Department(TimeStampedModel):
    """Company departments"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    head_of_department = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Department"
        verbose_name_plural = "Departments"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class JobPosition(TimeStampedModel):
    """Job positions/openings"""
    JOB_TYPES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
        ('temporary', 'Temporary'),
    ]

    EXPERIENCE_LEVELS = [
        ('entry', 'Entry Level'),
        ('junior', 'Junior Level'),
        ('mid', 'Mid Level'),
        ('senior', 'Senior Level'),
        ('lead', 'Lead/Manager'),
        ('executive', 'Executive'),
    ]

    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('closed', 'Closed'),
        ('filled', 'Filled'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='positions')

    # Job details
    job_type = models.CharField(max_length=20, choices=JOB_TYPES, default='full_time')
    experience_level = models.CharField(max_length=20, choices=EXPERIENCE_LEVELS, default='mid')
    location = models.CharField(max_length=200, default='Accra, Ghana')
    remote_allowed = models.BooleanField(default=False)

    # Job description
    summary = models.TextField(help_text="Brief job summary")
    description = models.TextField(help_text="Detailed job description")
    responsibilities = models.TextField(help_text="Key responsibilities, one per line")
    requirements = models.TextField(help_text="Job requirements, one per line")
    qualifications = models.TextField(help_text="Preferred qualifications, one per line")
    benefits = models.TextField(blank=True, help_text="Benefits offered, one per line")

    # Compensation
    salary_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salary_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salary_currency = models.CharField(max_length=3, default='GHS')
    salary_period = models.CharField(max_length=20, default='monthly',
                                   choices=[('hourly', 'Hourly'), ('monthly', 'Monthly'), ('yearly', 'Yearly')])

    # Application settings
    application_deadline = models.DateTimeField(null=True, blank=True)
    max_applications = models.PositiveIntegerField(null=True, blank=True, help_text="Maximum number of applications")

    # Status and visibility
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    is_featured = models.BooleanField(default=False, help_text="Show prominently on careers page")
    is_urgent = models.BooleanField(default=False)

    # Tracking
    views_count = models.PositiveIntegerField(default=0)
    applications_count = models.PositiveIntegerField(default=0)

    # Contact person
    contact_person = models.CharField(max_length=100, blank=True)
    contact_email = models.EmailField(blank=True)

    class Meta:
        ordering = ['-is_featured', '-is_urgent', '-created_at']
        verbose_name = "Job Position"
        verbose_name_plural = "Job Positions"

    def __str__(self):
        return f"{self.title} - {self.department.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.title}-{self.department.name}")
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('careers:job_detail', kwargs={'slug': self.slug})

    def increment_views(self):
        """Increment view count"""
        self.views_count += 1
        self.save(update_fields=['views_count'])

    def increment_applications(self):
        """Increment applications count"""
        self.applications_count += 1
        self.save(update_fields=['applications_count'])

    @property
    def is_active(self):
        """Check if job is currently accepting applications"""
        if self.status != 'active':
            return False
        if self.application_deadline and self.application_deadline < timezone.now():
            return False
        if self.max_applications and self.applications_count >= self.max_applications:
            return False
        return True

    @property
    def salary_range(self):
        """Get formatted salary range"""
        if self.salary_min and self.salary_max:
            return f"{self.salary_currency} {self.salary_min:,.0f} - {self.salary_max:,.0f} {self.salary_period}"
        elif self.salary_min:
            return f"From {self.salary_currency} {self.salary_min:,.0f} {self.salary_period}"
        return "Competitive"

    def get_responsibilities_list(self):
        """Return responsibilities as a list"""
        if self.responsibilities:
            return [resp.strip() for resp in self.responsibilities.split('\n') if resp.strip()]
        return []

    def get_requirements_list(self):
        """Return requirements as a list"""
        if self.requirements:
            return [req.strip() for req in self.requirements.split('\n') if req.strip()]
        return []

    def get_qualifications_list(self):
        """Return qualifications as a list"""
        if self.qualifications:
            return [qual.strip() for qual in self.qualifications.split('\n') if qual.strip()]
        return []

    def get_benefits_list(self):
        """Return benefits as a list"""
        if self.benefits:
            return [benefit.strip() for benefit in self.benefits.split('\n') if benefit.strip()]
        return []

def upload_cv_path(instance, filename):
    """Generate upload path for CV files"""
    return f'careers/cvs/{instance.position.slug}/{filename}'

def upload_cover_letter_path(instance, filename):
    """Generate upload path for cover letter files"""
    return f'careers/cover_letters/{instance.position.slug}/{filename}'

class JobApplication(TimeStampedModel):
    """Job applications submitted by candidates"""
    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('shortlisted', 'Shortlisted'),
        ('interview_scheduled', 'Interview Scheduled'),
        ('interviewed', 'Interviewed'),
        ('offer_made', 'Offer Made'),
        ('hired', 'Hired'),
        ('rejected', 'Rejected'),
        ('withdrawn', 'Withdrawn'),
    ]

    position = models.ForeignKey(JobPosition, on_delete=models.CASCADE, related_name='applications')

    # Personal Information
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    # Address
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, default='Ghana')

    # Professional Information
    current_position = models.CharField(max_length=200, blank=True)
    current_company = models.CharField(max_length=200, blank=True)
    years_of_experience = models.PositiveIntegerField(null=True, blank=True)
    expected_salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    availability_date = models.DateField(null=True, blank=True, help_text="When can you start?")

    # Application Materials
    cv_file = models.FileField(upload_to=upload_cv_path, help_text="Upload your CV/Resume (PDF preferred)")
    cover_letter_file = models.FileField(upload_to=upload_cover_letter_path, blank=True,
                                       help_text="Upload cover letter (PDF preferred)")
    cover_letter_text = models.TextField(blank=True, help_text="Or write your cover letter here")

    # Additional Information
    portfolio_url = models.URLField(blank=True, help_text="Link to your portfolio/LinkedIn")
    additional_info = models.TextField(blank=True, help_text="Any additional information")

    # Application Status
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='submitted')

    # Admin fields
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_applications')
    reviewed_at = models.DateTimeField(null=True, blank=True)
    admin_notes = models.TextField(blank=True, help_text="Internal notes about the candidate")

    # Interview details
    interview_date = models.DateTimeField(null=True, blank=True)
    interview_location = models.CharField(max_length=200, blank=True)
    interview_notes = models.TextField(blank=True)

    # Tracking
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['position', 'email']  # Prevent duplicate applications
        verbose_name = "Job Application"
        verbose_name_plural = "Job Applications"

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.position.title}"

    @property
    def full_name(self):
        """Get candidate's full name"""
        return f"{self.first_name} {self.last_name}"

    def update_status(self, new_status, user=None, notes=None):
        """Update application status with tracking"""
        self.status = new_status
        if user:
            self.reviewed_by = user
            self.reviewed_at = timezone.now()
        if notes:
            self.admin_notes = notes
        self.save()

        # Create status history entry
        ApplicationStatusHistory.objects.create(
            application=self,
            status=new_status,
            changed_by=user,
            notes=notes
        )

    def schedule_interview(self, date, location, user=None):
        """Schedule interview for candidate"""
        self.interview_date = date
        self.interview_location = location
        self.status = 'interview_scheduled'
        if user:
            self.reviewed_by = user
            self.reviewed_at = timezone.now()
        self.save()

    @property
    def cv_filename(self):
        """Get CV filename"""
        if self.cv_file:
            return os.path.basename(self.cv_file.name)
        return None

    @property
    def cover_letter_filename(self):
        """Get cover letter filename"""
        if self.cover_letter_file:
            return os.path.basename(self.cover_letter_file.name)
        return None

class ApplicationStatusHistory(TimeStampedModel):
    """Track status changes for job applications"""
    application = models.ForeignKey(JobApplication, on_delete=models.CASCADE, related_name='status_history')
    status = models.CharField(max_length=30, choices=JobApplication.STATUS_CHOICES)
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Application Status History"
        verbose_name_plural = "Application Status Histories"

    def __str__(self):
        return f"{self.application.full_name} - {self.status}"

class CareerPageContent(TimeStampedModel):
    """Content for the careers page"""
    title = models.CharField(max_length=200, default="Join Our Team")
    subtitle = models.CharField(max_length=300, default="Build Your Career with Skyline Ghana Constructions")
    description = models.TextField(default="We're always looking for talented individuals to join our growing team.")

    # Company culture section
    culture_title = models.CharField(max_length=200, default="Our Culture")
    culture_description = models.TextField(blank=True)

    # Benefits section
    benefits_title = models.CharField(max_length=200, default="Why Work With Us")
    benefits_description = models.TextField(blank=True)

    # Images
    hero_image = models.ImageField(upload_to='careers/', blank=True)
    culture_image = models.ImageField(upload_to='careers/', blank=True)

    # Contact information
    hr_email = models.EmailField(blank=True, help_text="HR contact email")
    hr_phone = models.CharField(max_length=20, blank=True)

    class Meta:
        verbose_name = "Career Page Content"
        verbose_name_plural = "Career Page Content"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        if not self.pk and CareerPageContent.objects.exists():
            raise ValueError("Only one CareerPageContent instance is allowed")
        super().save(*args, **kwargs)
