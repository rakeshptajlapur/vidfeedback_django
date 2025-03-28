from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import BusinessOwner

@admin.register(BusinessOwner)
class BusinessOwnerAdmin(UserAdmin):
    list_display = ('username', 'email', 'business_name', 'plan_type', 'created_at', 'is_active')
    list_filter = ('plan_type', 'is_active', 'created_at')
    search_fields = ('username', 'email', 'business_name')
    
    fieldsets = UserAdmin.fieldsets + (
        ('Business Information', {
            'fields': ('business_name', 'phone', 'plan_type'),
        }),
    )
