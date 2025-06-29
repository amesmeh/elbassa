from django.contrib import admin
from .models import District, Guardian, Wife, Child

@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ['name', 'representative_name', 'representative_phone', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'representative_name', 'representative_phone']
    ordering = ['name']

class WifeInline(admin.TabularInline):
    model = Wife
    extra = 0
    fields = ['name', 'national_id']

class ChildInline(admin.TabularInline):
    model = Child
    extra = 0
    fields = ['name', 'national_id', 'birth_date']
    readonly_fields = ['age']

@admin.register(Guardian)
class GuardianAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'national_id', 'phone_number', 'district', 
        'family_members_count', 'marital_status', 'residence_status'
    ]
    list_filter = [
        'gender', 'marital_status', 'residence_status', 
        'district', 'created_at'
    ]
    search_fields = ['name', 'national_id', 'phone_number']
    ordering = ['name']
    
    fieldsets = (
        ('البيانات الأساسية', {
            'fields': (
                'name', 'national_id', 'current_job', 
                'phone_number', 'gender'
            )
        }),
        ('البيانات العائلية', {
            'fields': (
                'children_count', 'marital_status', 'wives_count', 
                'family_members_count'
            )
        }),
        ('حالة الإقامة', {
            'fields': (
                'residence_status', 'original_governorate', 
                'original_city', 'displacement_address'
            ),
            'classes': ('collapse',)
        }),
        ('العنوان والسكن', {
            'fields': ('district',)
        }),
    )
    
    readonly_fields = ['family_members_count']
    inlines = [WifeInline, ChildInline]

@admin.register(Wife)
class WifeAdmin(admin.ModelAdmin):
    list_display = ['name', 'national_id', 'guardian', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'national_id', 'guardian__name']
    ordering = ['name']

@admin.register(Child)
class ChildAdmin(admin.ModelAdmin):
    list_display = ['name', 'national_id', 'birth_date', 'age', 'guardian']
    list_filter = ['birth_date', 'created_at']
    search_fields = ['name', 'national_id', 'guardian__name']
    ordering = ['birth_date']
    
    fieldsets = (
        ('البيانات الأساسية', {
            'fields': ('name', 'national_id', 'birth_date', 'guardian')
        }),
    )
    
    def age(self, obj):
        return obj.age
    age.short_description = 'العمر'
    

