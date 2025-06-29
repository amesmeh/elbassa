from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.statistics_dashboard, name='statistics_dashboard'),
    path('export-statistics-pdf/', views.export_statistics_pdf, name='export_statistics_pdf'),
    path('detailed/<str:report_type>/', views.detailed_report, name='detailed_report'),
] 