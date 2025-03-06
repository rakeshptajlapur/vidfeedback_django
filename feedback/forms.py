from django import forms
from .models import FeedbackForm

class FeedbackFormForm(forms.ModelForm):
    class Meta:
        model = FeedbackForm
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter form name',
                'autofocus': True
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter form description',
                'rows': 3
            })
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) < 3:
            raise forms.ValidationError("Form name must be at least 3 characters long.")
        return name