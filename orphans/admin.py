from django.contrib import admin
from .models import Orphan

@admin.register(Orphan)
class OrphanAdmin(admin.ModelAdmin):
    list_display = [
        'name', 
        'national_id', 
        'gender',
        'age',
        'age_category',
        'education_level',
        'guardian_name',
        'district'
    ]
    list_filter = [
        'gender',
        'health_status',
        'education_level',
        'guardian_relationship',
        'district',
        'created_at'
    ]
    search_fields = [
        'name',
        'national_id',
        'deceased_name',
        'deceased_national_id',
        'guardian_name',
        'phone_number'
    ]
    date_hierarchy = 'birth_date'
    ordering = ['name']
    
    fieldsets = (
        ('بيانات اليتيم', {
            'fields': ('name', 'national_id', 'gender', 'birth_date', 'health_status', 'education_level')
        }),
        ('بيانات الشهيد/المتوفي', {
            'fields': ('deceased_national_id', 'deceased_name')
        }),
        ('بيانات العائلة', {
            'fields': ('male_siblings_count', 'female_siblings_count')
        }),
        ('بيانات الوصي', {
            'fields': ('guardian_name', 'guardian_relationship', 'phone_number')
        }),
        ('الموقع والملاحظات', {
            'fields': ('district', 'notes')
        }),
    )
    
    readonly_fields = ['age']
    
    actions = ['export_to_excel']
    
    def export_to_excel(self, request, queryset):
        # سيتم تطوير هذه الوظيفة لاحقاً
        pass
    export_to_excel.short_description = "تصدير إلى Excel"
