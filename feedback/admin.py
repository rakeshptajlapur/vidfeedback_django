from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import FeedbackForm, FormField, FormResponse

class FormFieldInline(admin.TabularInline):
    model = FormField
    extra = 1
    ordering = ('order',)
    fields = ('label', 'field_type', 'required', 'order')
    classes = ['collapse']
    
    def get_extra(self, request, obj=None, **kwargs):
        if obj:  # If editing existing form
            return 0
        return 1  # For new forms

@admin.register(FeedbackForm)
class FeedbackFormAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'created_at', 'is_active', 'response_count', 'view_responses')
    list_filter = ('is_active', 'created_at', 'owner')
    search_fields = ('name', 'description', 'owner__username', 'owner__business_name')
    readonly_fields = ('created_at', 'updated_at', 'slug')
    inlines = [FormFieldInline]
    fieldsets = (
        ('Form Details', {
            'fields': ('name', 'description', 'owner', 'is_active')
        }),
        ('Form Configuration', {
            'classes': ('collapse',),
            'fields': ('slug', 'created_at', 'updated_at')
        })
    )
    
    def response_count(self, obj):
        count = obj.responses.count()
        return format_html(
            '<span class="badge badge-info">{}</span>',
            count
        )
    response_count.short_description = 'Responses'
    
    def view_responses(self, obj):
        if obj.responses.exists():
            url = reverse('admin:feedback_formresponse_changelist')
            return format_html(
                '<a class="button" href="{}?form__id__exact={}">View Responses</a>',
                url, obj.id
            )
        return "No responses"
    view_responses.short_description = 'View Responses'
    
    class Media:
        css = {
            'all': ('admin/css/forms.css',)
        }

@admin.register(FormResponse)
class FormResponseAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_details', 'rating_with_feedback', 'has_video', 'created_at', 'view_details')
    list_filter = ('created_at', 'form')
    search_fields = ('form__name', 'data')
    readonly_fields = ('created_at', 'form', 'display_data', 'video_player')

    def customer_details(self, obj):
        name = obj.data.get('customer_name', 'N/A')
        email = obj.data.get('email_address', 'N/A')
        return format_html(
            '<strong>{}</strong><br><small>{}</small>',
            name, email
        )
    customer_details.short_description = 'Customer'
    
    def rating_with_feedback(self, obj):
        rating = obj.data.get('rating', 0)
        feedback = obj.data.get('additional_feedback', '')
        stars = '⭐' * int(rating) if rating else 'No rating'
        if feedback:
            preview = (feedback[:50] + '...') if len(feedback) > 50 else feedback
            return format_html(
                '{}<br><small class="text-muted">{}</small>',
                stars, preview
            )
        return stars
    rating_with_feedback.short_description = 'Rating & Feedback'

    def has_video(self, obj):
        if obj.data.get('video_testimonial'):
            return format_html('<span style="color: green;">✔</span>')
        return format_html('<span style="color: red;">✘</span>')
    has_video.short_description = 'Video'

    def view_details(self, obj):
        return format_html(
            '<a class="button" href="{}">View Details</a>',
            reverse('admin:feedback_formresponse_change', args=[obj.pk])
        )
    view_details.short_description = 'Actions'

    def display_data(self, obj):
        """Display all response data in a formatted way"""
        html = ['<div class="module aligned">']
        for key, value in obj.data.items():
            if key != 'video_testimonial':
                html.append(f'<div class="form-row">')
                html.append(f'<label><strong>{key}:</strong></label>')
                if key == 'rating':
                    value = '⭐' * int(value) if value else 'No rating'
                html.append(f'<div class="data">{value}</div>')
                html.append('</div>')
        html.append('</div>')
        return mark_safe(''.join(html))
    display_data.short_description = 'Response Data'

    def video_player(self, obj):
        """Custom field for video display"""
        video_url = obj.data.get('video_testimonial')
        if video_url:
            return format_html(
                '<div class="video-wrapper">'
                '<video width="400" controls>'
                '<source src="{}" type="video/webm">'
                'Your browser does not support the video tag.'
                '</video></div>',
                video_url
            )
        return "No video uploaded"
    video_player.short_description = 'Video Testimonial'

    def get_fieldsets(self, request, obj=None):
        if obj:  # Change view
            return (
                (None, {
                    'fields': ('form', 'created_at')
                }),
                ('Response Data', {
                    'fields': ('display_data',)
                }),
                ('Video', {
                    'fields': ('video_player',)
                }),
            )
        return super().get_fieldsets(request, obj)

    class Media:
        css = {
            'all': ('admin/css/forms.css',)
        }
