from django.db import models
from django.conf import settings
from django.utils.text import slugify
import uuid

class FeedbackForm(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            # Create a unique slug using name and uuid
            self.slug = f"{slugify(self.name)}-{str(uuid.uuid4())[:8]}"
        
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        # Create default fields for new forms
        if is_new:
            default_fields = [
                ('Customer Name', 'text', True),
                ('Email Address', 'email', True),
                ('Rating', 'rating', True),
                ('Video Testimonial', 'video', True),
                ('Additional Feedback', 'textarea', False),
            ]
            
            for order, (label, field_type, required) in enumerate(default_fields):
                FormField.objects.create(
                    form=self,
                    label=label,
                    field_type=field_type,
                    required=required,
                    order=order
                )

    class Meta:
        ordering = ['-created_at']

class FormField(models.Model):
    FIELD_TYPES = [
        ('text', 'Text Input'),
        ('textarea', 'Text Area'),
        ('video', 'Video Upload'),
        ('rating', 'Star Rating'),
        ('checkbox', 'Checkbox'),
        ('email', 'Email Input'),
    ]

    form = models.ForeignKey('FeedbackForm', related_name='fields', on_delete=models.CASCADE)
    label = models.CharField(max_length=100)
    field_type = models.CharField(max_length=20, choices=FIELD_TYPES)
    required = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

class FormResponse(models.Model):
    form = models.ForeignKey(FeedbackForm, on_delete=models.CASCADE, related_name='responses')
    data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
