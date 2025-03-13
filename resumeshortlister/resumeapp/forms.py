from django import forms
from .models import Skill, JobListing

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name']


class JobListingForm(forms.ModelForm):
    class Meta:
        model = JobListing
        fields = ['title', 'description', 'required_skills', 'specifications', 'years_of_experience_required']  # Added 'years_of_experience_required'
        widgets = {
            'required_skills': forms.SelectMultiple(attrs={
                'class': 'select2',  # Add Select2 class
                'data-placeholder': 'Select required skills'
            }),
            'years_of_experience_required': forms.NumberInput(attrs={
                'class': 'form-control',  # Styling for years input
                'placeholder': 'Enter years of experience required'
            })
        }

    def __init__(self, *args, **kwargs):
        super(JobListingForm, self).__init__(*args, **kwargs)
        self.fields['required_skills'].queryset = Skill.objects.all()



# resumeapp/forms.py


class ResumeFilterForm(forms.Form):
    skills = forms.ModelMultipleChoiceField(queryset=Skill.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)

