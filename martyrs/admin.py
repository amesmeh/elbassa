from django.contrib import admin
from .models import Martyr

@admin.register(Martyr)
class MartyrAdmin(admin.ModelAdmin):
    list_display = [
        'name', 
        'national_id', 
        'martyrdom_date', 
        'agent_name', 
        'district', 
        'martyrdom_year'
    ]
    list_filter = [
        'martyrdom_date',
        'district',
        'relationship_to_martyr',
        'created_at'
    ]
    search_fields = [
        'name',
        'national_id',
        'agent_name',
        'agent_national_id'
    ]
    date_hierarchy = 'martyrdom_date'
    ordering = ['-martyrdom_date', 'name']
    
    fieldsets = (
        ('بيانات الشهيد', {
            'fields': ('name', 'national_id', 'martyrdom_date')
        }),
        ('بيانات الوكيل', {
            'fields': ('agent_name', 'agent_national_id', 'agent_phone', 'relationship_to_martyr')
        }),
        ('الموقع والملاحظات', {
            'fields': ('district', 'notes')
        }),
    )
    
    # إمكانية الاستيراد من Excel (سيتم تطويرها لاحقاً)
    actions = ['export_to_excel']
    
    def export_to_excel(self, request, queryset):
        # سيتم تطوير هذه الوظيفة لاحقاً
        pass
    export_to_excel.short_description = "تصدير إلى Excel"
