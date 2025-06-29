from django.urls import path
from . import views

app_name = 'damages'

urlpatterns = [
    # قائمة الأضرار
    path('', views.damages_list, name='damages_list'),
    
    # إضافة ضرر جديد
    path('add/', views.damage_add, name='damage_add'),
    
    # عرض تفاصيل ضرر
    path('<int:pk>/', views.damage_detail, name='damage_detail'),
    
    # تعديل ضرر
    path('<int:pk>/edit/', views.damage_edit, name='damage_edit'),
    
    # حذف ضرر
    path('<int:pk>/delete/', views.damage_delete, name='damage_delete'),
    
    # استيراد الأضرار
    path('import/', views.damage_import, name='damage_import'),
    
    # تصدير واستيراد Excel
    path('export-excel/', views.export_damages_excel, name='export_damages_excel'),
    path('import-excel/', views.import_damages_excel, name='import_damages_excel'),
    path('download-template/', views.download_damages_template, name='download_damages_template'),
    
    # البحث السريع عبر AJAX
    path('search/', views.damage_search_ajax, name='damage_search_ajax'),
] 