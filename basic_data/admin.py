from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import District, Guardian, Wife, Child, Representative
from .citizen_models import CitizenRegistrationRequest, CitizenRequestChild, CitizenRequestWife

class RepresentativeInline(admin.StackedInline):
    """إضافة نموذج المندوب في صفحة المستخدم"""
    model = Representative
    can_delete = True
    verbose_name_plural = 'معلومات المندوب'

class CustomUserAdmin(UserAdmin):
    """تخصيص نموذج المستخدم لإضافة معلومات المندوب"""
    inlines = (RepresentativeInline, )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_district')
    
    def get_district(self, obj):
        try:
            return obj.representative.district.name
        except:
            return '-'
    get_district.short_description = 'الحي'

# إعادة تسجيل نموذج المستخدم مع الإدارة المخصصة
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

@admin.register(Representative)
class RepresentativeAdmin(admin.ModelAdmin):
    """إدارة المندوبين"""
    list_display = ['user', 'district', 'phone_number', 'is_active', 'created_at']
    list_filter = ['is_active', 'district', 'created_at']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'district__name']
    ordering = ['user__username']
    raw_id_fields = ['user']
    autocomplete_fields = ['district']

@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    """إدارة المناطق والأحياء"""
    list_display = ['name', 'representative_name', 'representative_phone', 'created_at']
    search_fields = ['name', 'representative_name']
    list_filter = ['created_at']
    ordering = ['name']

class WifeInline(admin.TabularInline):
    model = Wife
    extra = 1
    fields = ['name', 'national_id']

class ChildInline(admin.TabularInline):
    model = Child
    extra = 1
    fields = ['name', 'national_id', 'birth_date']
    readonly_fields = ['age']

@admin.register(Guardian)
class GuardianAdmin(admin.ModelAdmin):
    list_display = ['name', 'national_id', 'phone_number', 'district', 'residence_status', 'family_members_count', 'created_at']
    list_filter = ['gender', 'marital_status', 'residence_status', 'district', 'housing_type', 'created_at']
    search_fields = ['name', 'national_id', 'phone_number']
    readonly_fields = ['family_members_count', 'created_at', 'updated_at']
    inlines = [WifeInline, ChildInline]
    fieldsets = (
        ('البيانات الأساسية', {
            'fields': ('name', 'national_id', 'current_job', 'phone_number', 'gender')
        }),
        ('البيانات العائلية', {
            'fields': ('children_count', 'marital_status', 'wives_count', 'family_members_count')
        }),
        ('حالة الإقامة', {
            'fields': ('residence_status', 'original_governorate', 'original_city', 'displacement_address')
        }),
        ('العنوان والسكن', {
            'fields': ('district', 'housing_type')
        }),
        ('معلومات النظام', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    ordering = ['name']

@admin.register(Wife)
class WifeAdmin(admin.ModelAdmin):
    list_display = ['name', 'national_id', 'guardian', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'national_id', 'guardian__name']
    ordering = ['guardian__name', 'name']

@admin.register(Child)
class ChildAdmin(admin.ModelAdmin):
    list_display = ['name', 'national_id', 'guardian', 'birth_date', 'age', 'created_at']
    list_filter = ['birth_date', 'created_at']
    search_fields = ['name', 'national_id', 'guardian__name']
    readonly_fields = ['age']
    ordering = ['guardian__name', 'name']
    
    fieldsets = (
        ('البيانات الأساسية', {
            'fields': ('name', 'national_id', 'birth_date', 'guardian')
        }),
    )
    
    def age(self, obj):
        return obj.age
    age.short_description = 'العمر'
    

# نماذج طلبات تسجيل المواطنين
class CitizenRequestChildInline(admin.TabularInline):
    model = CitizenRequestChild
    extra = 1
    fields = ['name', 'national_id', 'birth_date']

class CitizenRequestWifeInline(admin.TabularInline):
    model = CitizenRequestWife
    extra = 1
    fields = ['name', 'national_id']

@admin.register(CitizenRegistrationRequest)
class CitizenRegistrationRequestAdmin(admin.ModelAdmin):
    list_display = ['name', 'national_id', 'phone_number', 'district', 'status', 'created_at']
    list_filter = ['status', 'gender', 'marital_status', 'residence_status', 'district', 'created_at']
    search_fields = ['name', 'national_id', 'phone_number']
    readonly_fields = ['created_at', 'updated_at', 'approved_by', 'approved_at']
    inlines = [CitizenRequestChildInline, CitizenRequestWifeInline]
    actions = ['approve_requests', 'reject_requests']
    
    fieldsets = (
        ('البيانات الأساسية', {
            'fields': ('name', 'national_id', 'current_job', 'phone_number', 'gender')
        }),
        ('البيانات العائلية', {
            'fields': ('children_count', 'marital_status', 'wives_count')
        }),
        ('حالة الإقامة', {
            'fields': ('residence_status', 'original_governorate', 'original_city', 'displacement_address')
        }),
        ('العنوان والسكن', {
            'fields': ('district', 'housing_type')
        }),
        ('حالة الطلب', {
            'fields': ('status', 'admin_notes', 'approved_by', 'approved_at')
        }),
        ('معلومات النظام', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def approve_requests(self, request, queryset):
        """إجراء قبول الطلبات المحددة"""
        approved_count = 0
        for registration_request in queryset.filter(status='pending'):
            try:
                registration_request.approve(request.user)
                approved_count += 1
            except Exception as e:
                self.message_user(request, f'خطأ في قبول طلب {registration_request.name}: {str(e)}', level='ERROR')
        
        self.message_user(request, f'تم قبول {approved_count} طلب بنجاح')
    approve_requests.short_description = "قبول الطلبات المحددة"
    
    def reject_requests(self, request, queryset):
        """إجراء رفض الطلبات المحددة"""
        rejected_count = 0
        for registration_request in queryset.filter(status='pending'):
            try:
                registration_request.reject(request.user, "رفض جماعي من الإدارة")
                rejected_count += 1
            except Exception as e:
                self.message_user(request, f'خطأ في رفض طلب {registration_request.name}: {str(e)}', level='ERROR')
        
        self.message_user(request, f'تم رفض {rejected_count} طلب بنجاح')
    reject_requests.short_description = "رفض الطلبات المحددة"
    
    def get_queryset(self, request):
        """تخصيص عرض الطلبات حسب الصلاحيات"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        # يمكن إضافة منطق إضافي للمندوبين هنا
        return qs

@admin.register(CitizenRequestChild)
class CitizenRequestChildAdmin(admin.ModelAdmin):
    list_display = ['name', 'national_id', 'request', 'birth_date']
    list_filter = ['birth_date']
    search_fields = ['name', 'national_id', 'request__name']
    ordering = ['request__name', 'name']

@admin.register(CitizenRequestWife)
class CitizenRequestWifeAdmin(admin.ModelAdmin):
    list_display = ['name', 'national_id', 'request']
    list_filter = []
    search_fields = ['name', 'national_id', 'request__name']
    ordering = ['request__name', 'name']


