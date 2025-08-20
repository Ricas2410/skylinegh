from django import forms
from core.models import SiteSettings


class SiteSettingsForm(forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = [
            'site_name', 'site_tagline',
            'phone_primary', 'phone_secondary', 'email_primary', 'email_secondary',
            'address_line_1', 'address_line_2', 'city', 'region', 'postal_code',
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
