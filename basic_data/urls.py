from django.urls import path, include
from . import views
from django.views.generic import TemplateView

app_name = 'basic_data'

urlpatterns = [
    # الصفحة الرئيسية للبيانات الأساسية
    path('', views.basic_data_home, name='basic_data_home'),
    
    # المناطق والأحياء
    path('districts/', views.districts_list, name='districts_list'),
    path('districts/create/', views.district_create, name='district_create'),
    path('districts/<int:pk>/', views.district_detail, name='district_detail'),
    path('districts/<int:pk>/edit/', views.district_edit, name='district_edit'),
    path('districts/<int:pk>/delete/', views.district_delete, name='district_delete'),
    
    # أولياء الأمور
    path('guardians/', views.guardian_list, name='guardians_list'),
    path('guardians/create/', views.guardian_create, name='guardian_create'),
    path('guardians/<int:pk>/', views.guardian_detail, name='guardian_detail'),
    path('guardians/<int:pk>/edit/', views.guardian_edit, name='guardian_edit'),
    path('guardians/<int:pk>/delete/', views.guardian_delete, name='guardian_delete'),
    path('guardians/<int:pk>/aids/', views.guardian_aids_summary, name='guardian_aids_summary'),
    path('guardians/delete-selected/', views.delete_selected_guardians, name='delete_selected_guardians'),
    path('guardians/delete-all/', views.delete_all_guardians, name='delete_all_guardians'),
    path('guardians/fix-counters/', views.fix_guardian_counters, name='fix_guardian_counters'),
    path('guardians/update-counters-from-excel/', views.update_counters_from_excel, name='update_counters_from_excel'),
    path('guardians/duplicate-report/', views.duplicate_guardians_report, name='duplicate_guardians_report'),
    path('guardians/export/', views.export_guardians_excel, name='export_guardians_excel'),
    path('guardians/export-pdf/', views.export_guardians_pdf, name='export_guardians_pdf'),
    path('guardians/import/', views.import_guardians_excel, name='import_guardians_excel'),
    
    # الزوجات
    path('wives/', views.wives_list, name='wives_list'),
    path('wives/create/', views.wife_create, name='wife_create'),
    path('wives/<int:wife_id>/', views.wife_detail, name='wife_detail'),
    path('wives/<int:wife_id>/edit/', views.wife_edit, name='wife_edit'),
    path('wives/<int:wife_id>/delete/', views.wife_delete, name='wife_delete'),
    path('wives/export/', views.export_wives_excel, name='export_wives_excel'),
    path('wives/import/', views.import_wives_excel, name='import_wives_excel'),
    
    # الأبناء
    path('children/', views.children_list, name='children_list'),
    path('children/create/', views.child_create, name='child_create'),
    path('children/delete-selected/', views.delete_selected_children, name='delete_selected_children'),
    path('children/delete-all/', views.delete_all_children, name='delete_all_children'),
    path('children/<int:child_id>/', views.child_detail, name='child_detail'),
    path('children/<int:child_id>/edit/', views.child_edit, name='child_edit'),
    path('children/<int:child_id>/delete/', views.child_delete, name='child_delete'),
    path('children/export/', views.export_children_excel, name='export_children_excel'),
    path('children/import/', views.import_children_excel, name='import_children_excel'),
    
    # مسارات الترحيل والإلغاء - إضافة المسارات المفقودة
    path('migrate/cancel/', views.cancel_migration, name='cancel_migration'),
    path('migrate/wife/<int:wife_id>/', views.migrate_wife_to_guardian, name='migrate_wife_to_guardian'),
    path('migrate/wives/<int:guardian_id>/', views.migrate_all_wives_to_guardian, name='migrate_all_wives_to_guardian'),
    path('migrate/child/<int:child_id>/', views.migrate_child_to_guardian, name='migrate_child_to_guardian'),
    path('migrate/children/<int:guardian_id>/', views.migrate_all_children_to_guardian, name='migrate_all_children_to_guardian'),
    
    # أدوات البحث والتحليل
    path('check-aids-integrity/', views.check_aids_data_integrity, name='check_aids_data_integrity'),
    path('search-guardian-aids/', views.search_guardian_aids, name='search_guardian_aids'),
    path('search-aids-direct/', views.search_aids_by_name, name='search_aids_by_name'),
    
    # صفحة مساعدة أخطاء الاستيراد
    path('import-errors/help/', TemplateView.as_view(template_name='basic_data/import_errors_help.html'), name='import_errors_help'),
    path('download-import-errors/', views.download_import_errors, name='download_import_errors'),
    
    # تحميل قوالب Excel
    path('guardians/template/', views.download_guardians_template, name='download_guardians_template'),
    path('children/template/', views.download_children_template, name='download_children_template'),
    path('wives/template/', views.download_wives_template, name='download_wives_template'),
    path('districts/template/', views.download_districts_template, name='download_districts_template'),
    
    # مسارات تسجيل المواطنين
    path('citizen-registration/', include('basic_data.citizen_urls')),
] 