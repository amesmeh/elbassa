from django.urls import path
from . import views

app_name = 'assistance'

urlpatterns = [
    # الصفحة الرئيسية للمساعدات
    path('', views.assistance_list, name='assistance_list'),
    
    # إضافة مساعدة
    path('create/', views.assistance_create, name='assistance_create'),
    
    # تفاصيل مساعدة
    path('<int:pk>/', views.assistance_detail, name='assistance_detail'),
    
    # تعديل مساعدة
    path('<int:pk>/edit/', views.assistance_edit, name='assistance_edit'),
    
    # حذف مساعدة
    path('<int:pk>/delete/', views.assistance_delete, name='assistance_delete'),
    
    # التعديل السريع
    path('<int:pk>/quick-edit/', views.assistance_quick_edit, name='assistance_quick_edit'),
    
    # تحديث التاريخ
    path('<int:pk>/update-date/', views.update_assistance_date, name='update_assistance_date'),
    
    # التحديث الجماعي للتواريخ
    path('bulk-update-date-preview/', views.bulk_update_date_preview, name='bulk_update_date_preview'),
    path('bulk-update-date/', views.bulk_update_date, name='bulk_update_date'),
    
    # الحصول على قيمة حقل
    path('<int:pk>/get-field-value/', views.assistance_get_field_value, name='assistance_get_field_value'),
    
    # البحث السريع عن المستفيدين
    path('beneficiary-search/', views.beneficiary_search_ajax, name='beneficiary_search'),
    
    # عمليات الاستيراد والتصدير
    path('export/excel/', views.export_assistance_excel, name='export_assistance_excel'),
    path('import/excel/', views.import_assistance_excel, name='import_assistance_excel'),
    path('template/download/', views.create_assistance_template, name='create_assistance_template'),
    
    # عمليات الحذف المتقدمة
    path('delete-selected/', views.delete_selected_assistance, name='delete_selected_assistance'),
    path('delete-all/', views.delete_all_assistance, name='delete_all_assistance'),
    

] 