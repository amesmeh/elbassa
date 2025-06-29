from django.urls import path
from . import views

app_name = 'aids'

urlpatterns = [
    # الصفحة الرئيسية للمساعدات
    path('', views.aids_home, name='aids_home'),
    
    # المستفيدين
    path('beneficiaries/', views.beneficiaries_list, name='beneficiaries_list'),
    path('beneficiaries/<int:guardian_id>/', views.beneficiary_detail, name='beneficiary_detail'),
    
    # التوزيع
    path('distributions/', views.distributions_list, name='distributions_list'),
    path('distributions/create/', views.distribution_create, name='distribution_create'),
    path('distributions/<int:pk>/edit/', views.distribution_edit, name='distribution_edit'),
    path('distributions/<int:pk>/delete/', views.distribution_delete, name='distribution_delete'),
    path('distributions/<int:distribution_id>/transfer/', views.transfer_to_beneficiaries, name='transfer_to_beneficiaries'),
    path('distributions/bulk-transfer/', views.bulk_transfer_to_beneficiaries, name='bulk_transfer_to_beneficiaries'),
    
    # تصدير واستيراد التوزيعات - سيتم إضافتها لاحقاً
    # path('distributions/export-excel/', views.export_distributions_excel, name='export_distributions_excel'),
    # path('distributions/import-excel/', views.import_distributions_excel, name='import_distributions_excel'),
    # path('distributions/download-template/', views.download_distributions_template, name='download_distributions_template'),
    # path('distributions/download-import-errors/', views.download_import_errors, name='download_import_errors'),
    
    # حذف متعدد - المستفيدين
    path('beneficiaries/delete-selected/', views.delete_selected_beneficiaries, name='delete_selected_beneficiaries'),
    path('beneficiaries/delete-all/', views.delete_all_beneficiaries, name='delete_all_beneficiaries'),
    
    # حذف متعدد - التوزيعات
    path('distributions/delete-selected/', views.delete_selected_distributions, name='delete_selected_distributions'),
    path('distributions/delete-all/', views.delete_all_distributions, name='delete_all_distributions'),
    
    # حذف متعدد - أنواع المساعدات
    path('aid-types/delete-selected/', views.delete_selected_aid_types, name='delete_selected_aid_types'),
    path('aid-types/delete-all/', views.delete_all_aid_types, name='delete_all_aid_types'),
    
    # AJAX
    path('ajax/search-guardians/', views.search_guardians_ajax, name='search_guardians_ajax'),
] 