from django.urls import path
from . import views

app_name = 'martyrs'

urlpatterns = [
    path('', views.martyrs_list, name='martyrs_list'),
    path('add/', views.martyr_add, name='martyr_add'),
    path('import/', views.martyrs_import, name='martyrs_import'),
    path('export-excel/', views.export_martyrs_excel, name='export_martyrs_excel'),
    path('import-excel/', views.import_martyrs_excel, name='import_martyrs_excel'),
    path('download-template/', views.download_martyrs_template, name='download_martyrs_template'),
    path('ajax-search/', views.martyrs_ajax_search, name='martyrs_ajax_search'),
    path('<int:pk>/', views.martyr_detail, name='martyr_detail'),
    path('<int:pk>/edit/', views.martyr_edit, name='martyr_edit'),
    path('<int:pk>/delete/', views.martyr_delete, name='martyr_delete'),
] 