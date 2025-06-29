from django.contrib import admin
from .models import CivilRegistry

@admin.register(CivilRegistry)
class CivilRegistryAdmin(admin.ModelAdmin):
    list_display = [
        'name', 
        'national_id', 
        'gender',
        'age',
        'age_category',
        'governorate',
        'city'
    ]
    list_filter = [
        'gender',
        'governorate',
        'city',
        'created_at'
    ]
    search_fields = [
        'name',
        'national_id',
        'city',
        'neighborhood'
    ]
    date_hierarchy = 'birth_date'
    ordering = ['name']
    
    fieldsets = (
        ('البيانات الأساسية', {
            'fields': ('name', 'national_id', 'gender', 'birth_date')
        }),
        ('بيانات الموقع', {
            'fields': ('governorate', 'city', 'neighborhood', 'address')
        }),
        ('ملاحظات', {
            'fields': ('notes',)
        }),
    )
    
    readonly_fields = ['age']
    
    actions = ['export_to_excel']
    
    def export_to_excel(self, request, queryset):
        # سيتم تطوير هذه الوظيفة لاحقاً
        pass
    export_to_excel.short_description = "تصدير إلى Excel"
