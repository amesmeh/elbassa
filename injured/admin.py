from django.contrib import admin
from .models import Injured

@admin.register(Injured)
class InjuredAdmin(admin.ModelAdmin):
    list_display = [
        'name', 
        'national_id', 
        'guardian_name', 
        'injury_date', 
        'injury_type', 
        'district'
    ]
    list_filter = [
        'injury_date',
        'injury_type',
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
    date_hierarchy = 'injury_date'
    ordering = ['-injury_date', 'name']
    
    fieldsets = (
        ('بيانات الجريح', {
            'fields': ('name', 'national_id')
        }),
        ('بيانات ولي الأمر', {
            'fields': ('guardian_national_id', 'guardian_name', 'phone_number')
        }),
        ('بيانات الإصابة', {
            'fields': ('injury_date', 'injury_type', 'injury_description')
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
