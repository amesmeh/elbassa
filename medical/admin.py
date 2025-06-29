from django.contrib import admin
from .models import MedicalRecord

@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = [
        'name', 
        'national_id', 
        'gender',
        'guardian_name', 
        'disease_type', 
        'disability_type',
        'has_disability',
        'district'
    ]
    list_filter = [
        'gender',
        'disease_type',
        'disability_type',
        'district',
        'created_at'
    ]
    search_fields = [
        'name',
        'national_id',
        'guardian_name',
        'guardian_national_id',
        'phone_number'
    ]
    ordering = ['name']
    
    fieldsets = (
        ('بيانات المريض', {
            'fields': ('name', 'national_id', 'gender')
        }),
        ('بيانات ولي الأمر', {
            'fields': ('guardian_national_id', 'guardian_name', 'phone_number')
        }),
        ('البيانات المرضية', {
            'fields': ('disease_type', 'disease_description')
        }),
        ('بيانات الإعاقة', {
            'fields': ('disability_type', 'disability_percentage')
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
