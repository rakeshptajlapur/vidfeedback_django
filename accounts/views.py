from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required  # Add this import
from django.contrib import messages
from .forms import UserRegistrationStep1Form, BusinessDetailsStep2Form
from .models import BusinessOwner  # Add this import too

def register(request):
    step = request.session.get('registration_step', 1)
    
    if request.method == 'POST':
        if step == 1:
            form = UserRegistrationStep1Form(request.POST)
            if form.is_valid():
                request.session['step1_data'] = form.cleaned_data
                request.session['registration_step'] = 2
                return redirect('accounts:register')
        else:
            form = BusinessDetailsStep2Form(request.POST)
            if form.is_valid():
                # Combine data from both steps
                step1_data = request.session.get('step1_data')
                user = BusinessOwner(
                    username=step1_data['username'],
                    email=step1_data['email'],
                    business_name=form.cleaned_data['business_name'],
                    phone=form.cleaned_data['phone'],
                    plan_type=form.cleaned_data['plan_type']
                )
                user.set_password(step1_data['password1'])
                user.save()
                
                # Clear session
                del request.session['step1_data']
                del request.session['registration_step']
                
                login(request, user)
                messages.success(request, f'Welcome to VidFeedback, {user.business_name}!')
                return redirect('accounts:dashboard')
    else:
        initial_plan = request.GET.get('plan', 'FREE')
        if step == 1:
            form = UserRegistrationStep1Form()
        else:
            form = BusinessDetailsStep2Form(initial={'plan_type': initial_plan})
    
    return render(request, 'registration/register.html', {
        'form': form,
        'step': step,
        'progress': 50 if step == 1 else 100
    })

@login_required
def dashboard(request):
    plan_details = {
        'FREE': '1 Form, 10 Submissions',
        'BASIC': '5 Forms, 100 Submissions',
        'PRO': 'Unlimited Forms & Submissions'
    }
    context = {
        'plan_details': plan_details[request.user.plan_type]
    }
    return render(request, 'accounts/dashboard.html', context)
