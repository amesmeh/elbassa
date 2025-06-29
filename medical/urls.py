from django.urls import path
from . import views

app_name = 'medical'

urlpatterns = [
    # قائمة البيانات المرضية
    path('', views.medical_list, name='medical_list'),
    
    # إضافة سجل مرضي جديد
    path('add/', views.medical_add, name='medical_add'),
    
    # عرض تفاصيل سجل مرضي
    path('<int:pk>/', views.medical_detail, name='medical_detail'),
    
    # تعديل سجل مرضي
    path('<int:pk>/edit/', views.medical_edit, name='medical_edit'),
    
    # حذف سجل مرضي
    path('<int:pk>/delete/', views.medical_delete, name='medical_delete'),
    
    # تصدير واستيراد Excel
    path('export-excel/', views.export_medical_excel, name='export_medical_excel'),
    path('import-excel/', views.import_medical_excel, name='import_medical_excel'),
    path('download-template/', views.download_medical_template, name='download_medical_template'),
    
    # البحث السريع عبر AJAX
    path('ajax-search/', views.medical_ajax_search, name='medical_ajax_search'),
    
    # البحث عن ولي أمر عبر AJAX
    path('guardian-lookup/', views.guardian_lookup_ajax, name='guardian_lookup_ajax'),
]