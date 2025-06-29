from django.contrib import admin
from .models import Damage

@admin.register(Damage)
class DamageAdmin(admin.ModelAdmin):
    list_display = [
        'guardian_name', 
        'guardian_national_id',
        'housing_type', 
        'ownership_type',
        'damage_type', 
        'damage_percentage',
        'damage_severity',
        'district'
    ]
    list_filter = [
        'ownership_type',
        'housing_type',
        'damage_type',
        'construction_type',
        'district',
        'created_at'
    ]
    search_fields = [
        'guardian_name',
        'guardian_national_id',
        'phone_number'
    ]
    ordering = ['-damage_percentage', 'guardian_name']
    
    fieldsets = (
        ('بيانات المالك/المستأجر', {
            'fields': ('guardian_national_id', 'guardian_name', 'phone_number')
        }),
        ('بيانات العقار', {
            'fields': ('ownership_type', 'housing_type', 'housing_condition', 'construction_type', 'floors_count')
        }),
        ('بيانات الضرر', {
            'fields': ('damage_type', 'damage_percentage', 'damage_date')
        }),
        ('الموقع والملاحظات', {
            'fields': ('district', 'notes')
        }),
    )
    
    readonly_fields = ['guardian', 'guardian_name']
    
    actions = ['export_to_excel']
    
    def export_to_excel(self, request, queryset):
        # سيتم تطوير هذه الوظيفة لاحقاً
        pass
    export_to_excel.short_description = "تصدير إلى Excel"
