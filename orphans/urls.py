from django.urls import path
from . import views

app_name = 'orphans'

urlpatterns = [
    path('', views.orphans_list, name='orphans_list'),
    path('add/', views.orphan_add, name='orphan_add'),
    path('import/', views.orphans_import, name='orphans_import'),
    path('ajax-search/', views.orphans_ajax_search, name='orphans_ajax_search'),
    path('<int:pk>/', views.orphan_detail, name='orphan_detail'),
    path('<int:pk>/edit/', views.orphan_edit, name='orphan_edit'),
    path('<int:pk>/delete/', views.orphan_delete, name='orphan_delete'),
    path('export-excel/', views.export_orphans_excel, name='export_orphans_excel'),
    path('import-excel/', views.import_orphans_excel, name='import_orphans_excel'),
    path('download-template/', views.download_orphans_template, name='download_orphans_template'),
] 