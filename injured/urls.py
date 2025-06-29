from django.urls import path
from . import views

app_name = 'injured'

urlpatterns = [
    path('', views.injured_list, name='injured_list'),
    path('add/', views.injured_add, name='injured_add'),
    path('import/', views.injured_import, name='injured_import'),
    path('export-excel/', views.export_injured_excel, name='export_injured_excel'),
    path('import-excel/', views.import_injured_excel, name='import_injured_excel'),
    path('download-template/', views.download_injured_template, name='download_injured_template'),
    path('ajax-search/', views.injured_ajax_search, name='injured_ajax_search'),
    path('guardian-lookup/', views.guardian_lookup_ajax, name='guardian_lookup_ajax'),
    path('<int:pk>/', views.injured_detail, name='injured_detail'),
    path('<int:pk>/edit/', views.injured_edit, name='injured_edit'),
    path('<int:pk>/delete/', views.injured_delete, name='injured_delete'),
] 