from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import FeedbackForm, FormField, FormResponse
from django.core.files.storage import default_storage
import os

@login_required
def form_list(request):
    # Get all forms for the current user, ordered by creation date
    forms = FeedbackForm.objects.filter(owner=request.user).order_by('-created_at')
    context = {
        'forms': forms,
        'form_count': forms.count()
    }
    return render(request, 'feedback/form_list.html', context)

@login_required
def form_create(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('name', '').strip()
            description = request.POST.get('description', '').strip()

            if not name:
                messages.error(request, 'Form name is required.')
                return render(request, 'feedback/form_create.html')

            # Create the form
            form = FeedbackForm.objects.create(
                owner=request.user,
                name=name,
                description=description
            )
            
            messages.success(request, f'Form "{name}" created successfully!')
            return redirect('feedback:form_list')
            
        except Exception as e:
            messages.error(request, f'Error creating form: {str(e)}')
            return render(request, 'feedback/form_create.html')
    
    return render(request, 'feedback/form_create.html')

@login_required
def form_edit(request, slug):
    # Get the form using slug instead of pk
    form = get_object_or_404(FeedbackForm, slug=slug, owner=request.user)
    
    if request.method == 'POST':
        try:
            name = request.POST.get('name', '').strip()
            description = request.POST.get('description', '').strip()

            if not name:
                messages.error(request, 'Form name is required.')
                return render(request, 'feedback/form_edit.html', {'form': form})

            form.name = name
            form.description = description
            form.save()

            messages.success(request, 'Form updated successfully!')
            return redirect('feedback:form_list')

        except Exception as e:
            messages.error(request, f'Error updating form: {str(e)}')
            return render(request, 'feedback/form_edit.html', {'form': form})

    return render(request, 'feedback/form_edit.html', {'form': form})

def public_form_view(request, slug):
    """Public view for feedback form submission"""
    form = get_object_or_404(FeedbackForm, slug=slug, is_active=True)
    fields = form.fields.all().order_by('order')
    
    if request.method == 'POST':
        try:
            # Create form response
            response_data = {}
            video_file = None
            
            # Process each field
            for field in fields:
                if field.field_type == 'video':
                    if request.FILES.get(str(field.id)):
                        video_file = request.FILES[str(field.id)]
                        # Save video file
                        file_name = f"testimonials/{form.slug}/{video_file.name}"
                        file_path = default_storage.save(file_name, video_file)
                        response_data[field.label] = file_path
                else:
                    value = request.POST.get(str(field.id))
                    if field.required and not value:
                        raise ValueError(f"{field.label} is required")
                    response_data[field.label] = value

            # Save response
            FormResponse.objects.create(
                form=form,
                data=response_data
            )
            
            messages.success(request, "Thank you for your feedback!")
            return redirect('public_form', slug=slug)
            
        except Exception as e:
            messages.error(request, f"Error submitting form: {str(e)}")
    
    return render(request, 'feedback/public_form.html', {
        'form': form,
        'fields': fields
    })
