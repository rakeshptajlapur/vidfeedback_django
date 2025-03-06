from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import BusinessOwner

class UserRegistrationStep1Form(forms.ModelForm):
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Create a strong password'})
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Repeat your password'})
    )

    class Meta:
        model = BusinessOwner
        fields = ('username', 'email')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Choose a username'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email'
            }),
        }

class BusinessDetailsStep2Form(forms.ModelForm):
    class Meta:
        model = BusinessOwner
        fields = ('business_name', 'phone', 'plan_type')
        widgets = {
            'business_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your business name'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your phone number'
            }),
            'plan_type': forms.Select(attrs={
                'class': 'form-control'
            })
        }