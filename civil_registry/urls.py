from django.urls import path
from . import views

app_name = 'civil_registry'  # مهم جدًا إذا كنت تستخدم namespaces

urlpatterns = [
    # قائمة السجلات المدنية - الرئيسية
    path('', views.civil_records_list, name='civil_registry_list'),
    
    # قائمة السجلات المدنية - للتوافق مع المراجع القديمة
    path('registry/list/', views.civil_records_list, name='civil_registry_list'),
    
    # إضافة سجل مدني جديد
    path('add/', views.civil_record_add, name='civil_record_add'),
    
    # عرض تفاصيل سجل مدني
    path('<int:pk>/', views.civil_record_detail, name='civil_record_detail'),
    
    # تعديل سجل مدني
    path('<int:pk>/edit/', views.civil_record_edit, name='civil_record_edit'),
    
    # حذف سجل مدني
    path('<int:pk>/delete/', views.civil_record_delete, name='civil_record_delete'),
    
    # استيراد السجلات المدنية
    path('import/', views.import_civil_registry_excel, name='import_civil_registry_excel'),
    
    # تصدير واستيراد Excel
    path('export/', views.export_civil_registry_excel, name='export_civil_registry_excel'),
    path('template/', views.download_civil_registry_template, name='download_civil_registry_template'),
    
    # البحث السريع عبر AJAX
    path('search/', views.civil_record_search_ajax, name='civil_record_search_ajax'),
] 