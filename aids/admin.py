from django.contrib import admin
from .models import AidType, AidBeneficiary, AidDistribution, AidBatch, AidRequest

@admin.register(AidType)
class AidTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'is_active', 'created_at']
    list_filter = ['category', 'is_active']
    search_fields = ['name', 'description']
    ordering = ['category', 'name']

@admin.register(AidBeneficiary)
class AidBeneficiaryAdmin(admin.ModelAdmin):
    list_display = ['guardian', 'aid_type', 'aid_date', 'guardian_district']
    list_filter = ['aid_type', 'aid_date', 'guardian__district']
    search_fields = ['guardian__name', 'guardian__national_id', 'aid_type__name']
    ordering = ['-aid_date']
    
    def guardian_district(self, obj):
        return obj.guardian_district
    guardian_district.short_description = 'الحي'

@admin.register(AidDistribution)
class AidDistributionAdmin(admin.ModelAdmin):
    list_display = ['guardian', 'aid_type', 'distribution_date', 'is_transferred', 'guardian_district']
    list_filter = ['aid_type', 'distribution_date', 'is_transferred', 'guardian__district']
    search_fields = ['guardian__name', 'guardian__national_id', 'aid_type__name']
    ordering = ['-distribution_date']
    actions = ['transfer_selected_to_beneficiaries']
    
    def guardian_district(self, obj):
        return obj.guardian_district
    guardian_district.short_description = 'الحي'
    
    def transfer_selected_to_beneficiaries(self, request, queryset):
        transferred_count = 0
        for distribution in queryset:
            if not distribution.is_transferred:
                distribution.transfer_to_beneficiaries()
                transferred_count += 1
        
        self.message_user(request, f'تم ترحيل {transferred_count} توزيع إلى قائمة المستفيدين')
    transfer_selected_to_beneficiaries.short_description = 'ترحيل المحدد إلى المستفيدين'

@admin.register(AidBatch)
class AidBatchAdmin(admin.ModelAdmin):
    list_display = ['name', 'start_date', 'end_date', 'status', 'total_beneficiaries']
    list_filter = ['status', 'start_date']
    search_fields = ['name', 'description']
    filter_horizontal = ['target_districts']
    ordering = ['-start_date']

@admin.register(AidRequest)
class AidRequestAdmin(admin.ModelAdmin):
    list_display = ['guardian', 'aid_type', 'priority', 'status', 'request_date']
    list_filter = ['status', 'priority', 'aid_type__category', 'request_date']
    search_fields = ['guardian__name', 'guardian__national_id', 'aid_type__name']
    ordering = ['-request_date']
