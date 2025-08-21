from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from core.models import SiteSettings
from projects.models import Project


class SiteSettingsForm(forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = [
            'site_name', 'site_tagline',
            'phone_primary', 'phone_secondary', 'email_primary', 'email_secondary',
            'address_line_1', 'address_line_2', 'city', 'region', 'postal_code', 'latitude', 'longitude',
            'facebook_url', 'twitter_url', 'instagram_url', 'linkedin_url', 'youtube_url',
            'business_hours',
            'logo', 'favicon',
            'hero_background', 'hero_card_image', 'services_hero_image', 'about_hero_image',
            'contact_hero_image', 'projects_hero_image', 'careers_hero_image', 'blog_hero_image',
            'featured_service_1_image', 'featured_service_2_image', 'featured_service_3_image',
            'about_company_image', 'why_choose_us_image', 'join_team_left_image',
            'default_testimonial_image', 'default_team_member_image',
            'top_navbar_email', 'top_navbar_phone',
            'blog_url', 'show_blog_in_top_nav',
            'google_analytics_id',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            widget_class_name = field.widget.__class__.__name__
            field.widget.attrs['widget_type'] = widget_class_name

    def clean_google_analytics_id(self):
        ga = self.cleaned_data.get('google_analytics_id')
        if ga and not ga.startswith('G-') and not ga.startswith('UA-'):
            # Allow both GA4 and older UA formats
            raise forms.ValidationError('Google Analytics ID should start with "G-" or "UA-".')
        return ga

    def clean(self):
        cleaned = super().clean()
        email1 = cleaned.get('email_primary')
        email2 = cleaned.get('email_secondary')
        if email1 and email2 and email1 == email2:
            self.add_error('email_secondary', 'Secondary email must be different from primary email.')
        phone1 = cleaned.get('phone_primary')
        phone2 = cleaned.get('phone_secondary')
        if phone1 and phone2 and phone1 == phone2:
            self.add_error('phone_secondary', 'Secondary phone must be different from primary phone.')
        return cleaned


class ProjectForm(forms.ModelForm):
    """Custom form for Project with proper date widgets"""

    class Meta:
        model = Project
        fields = [
            'title', 'short_description', 'description', 'location', 'client_name',
            'project_type', 'service_category', 'start_date', 'completion_date', 'featured_image',
            'is_featured', 'is_published'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent',
                'placeholder': 'Enter project title'
            }),
            'short_description': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent',
                'placeholder': 'Brief description for listings',
                'maxlength': '300'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent min-h-32',
                'placeholder': 'Detailed project description',
                'rows': 6
            }),
            'location': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent',
                'placeholder': 'Project location'
            }),
            'client_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent',
                'placeholder': 'Client name (optional)'
            }),
            'start_date': forms.DateInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent',
                'type': 'date'
            }),
            'completion_date': forms.DateInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent',
                'type': 'date'
            }),
            'project_type': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent'
            }),
            'service_category': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent'
            }),
            'featured_image': forms.FileInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-medium file:bg-primary-50 file:text-primary-700 hover:file:bg-primary-100',
                'accept': 'image/*'
            }),
        }


class CustomUserCreationForm(UserCreationForm):
    """Custom user creation form with additional fields"""
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    is_staff = forms.BooleanField(required=False, help_text="Allow user to access admin dashboard")

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'is_staff')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name not in ['is_staff']:
                field.widget.attrs['class'] = 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent'

        self.fields['username'].widget.attrs['placeholder'] = 'Enter username'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter email address'
        self.fields['first_name'].widget.attrs['placeholder'] = 'First name (optional)'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Last name (optional)'
        self.fields['password1'].widget.attrs['placeholder'] = 'Enter password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm password'


class UserUpdateForm(forms.ModelForm):
    """Form for updating user information"""

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent',
                'placeholder': 'Enter username'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent',
                'placeholder': 'Enter email address'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent',
                'placeholder': 'First name (optional)'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent',
                'placeholder': 'Last name (optional)'
            }),
        }
