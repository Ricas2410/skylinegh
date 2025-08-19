from django import forms
from .models import JobApplication

class JobApplicationForm(forms.ModelForm):
    """Job application form"""
    
    class Meta:
        model = JobApplication
        fields = [
            'first_name', 'last_name', 'email', 'phone',
            'address', 'city', 'country',
            'current_position', 'current_company', 'years_of_experience',
            'expected_salary', 'availability_date',
            'cv_file', 'cover_letter_file', 'cover_letter_text',
            'portfolio_url', 'additional_info'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'First name',
                'required': True
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Last name',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'your.email@example.com',
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': '+233 XX XXX XXXX',
                'required': True
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Your full address',
                'rows': 3
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'City'
            }),
            'country': forms.TextInput(attrs={
                'class': 'form-input',
                'value': 'Ghana'
            }),
            'current_position': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Current job title'
            }),
            'current_company': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Current company'
            }),
            'years_of_experience': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Years of experience',
                'min': 0
            }),
            'expected_salary': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Expected salary (GHS)',
                'min': 0,
                'step': '0.01'
            }),
            'availability_date': forms.DateInput(attrs={
                'class': 'form-input',
                'type': 'date'
            }),
            'cv_file': forms.FileInput(attrs={
                'class': 'form-input',
                'accept': '.pdf,.doc,.docx',
                'required': True
            }),
            'cover_letter_file': forms.FileInput(attrs={
                'class': 'form-input',
                'accept': '.pdf,.doc,.docx'
            }),
            'cover_letter_text': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Write your cover letter here...',
                'rows': 6
            }),
            'portfolio_url': forms.URLInput(attrs={
                'class': 'form-input',
                'placeholder': 'https://your-portfolio.com'
            }),
            'additional_info': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Any additional information you would like to share...',
                'rows': 4
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set required fields
        required_fields = ['first_name', 'last_name', 'email', 'phone', 'cv_file']
        for field_name in required_fields:
            self.fields[field_name].required = True
    
    def clean_cv_file(self):
        """Validate CV file"""
        cv_file = self.cleaned_data.get('cv_file')
        if cv_file:
            # Check file size (max 5MB)
            if cv_file.size > 5 * 1024 * 1024:
                raise forms.ValidationError('CV file size must be less than 5MB.')
            
            # Check file extension
            allowed_extensions = ['.pdf', '.doc', '.docx']
            file_extension = cv_file.name.lower().split('.')[-1]
            if f'.{file_extension}' not in allowed_extensions:
                raise forms.ValidationError('CV must be in PDF, DOC, or DOCX format.')
        
        return cv_file
    
    def clean_cover_letter_file(self):
        """Validate cover letter file"""
        cover_letter_file = self.cleaned_data.get('cover_letter_file')
        if cover_letter_file:
            # Check file size (max 5MB)
            if cover_letter_file.size > 5 * 1024 * 1024:
                raise forms.ValidationError('Cover letter file size must be less than 5MB.')
            
            # Check file extension
            allowed_extensions = ['.pdf', '.doc', '.docx']
            file_extension = cover_letter_file.name.lower().split('.')[-1]
            if f'.{file_extension}' not in allowed_extensions:
                raise forms.ValidationError('Cover letter must be in PDF, DOC, or DOCX format.')
        
        return cover_letter_file
    
    def clean(self):
        """Additional form validation"""
        cleaned_data = super().clean()
        cover_letter_file = cleaned_data.get('cover_letter_file')
        cover_letter_text = cleaned_data.get('cover_letter_text')
        
        # Require either cover letter file or text
        if not cover_letter_file and not cover_letter_text:
            raise forms.ValidationError('Please provide a cover letter either as a file upload or in the text field.')
        
        return cleaned_data
