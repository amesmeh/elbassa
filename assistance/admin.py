from django.contrib import admin
from .models import Assistance

@admin.register(Assistance)
class AssistanceAdmin(admin.ModelAdmin):
    list_display = [
        'beneficiary_name', 'national_id', 'assistance_type', 
        'quantity', 'assistance_date', 'district_name', 'created_at'
    ]
    list_filter = [
        'assistance_type', 'assistance_date', 'created_at'
    ]
    search_fields = [
        'beneficiary_name', 'national_id', 'district_name'
    ]
    date_hierarchy = 'assistance_date'
    ordering = ['-assistance_date', '-created_at']
    
    fieldsets = (
        ('معلومات المستفيد', {
            'fields': ('national_id', 'beneficiary_name')
        }),
        ('تفاصيل المساعدة', {
            'fields': ('assistance_type', 'quantity', 'assistance_date')
        }),
        ('معلومات إضافية', {
            'fields': ('district_name', 'family_members_count', 'notes'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ['created_at', 'updated_at']
        return self.readonly_fields
