from django.urls import path
from . import citizen_views

app_name = 'citizen_registration'

urlpatterns = [
    # قائمة طلبات التسجيل
    path('requests/', citizen_views.registration_requests_list, name='registration_requests_list'),
    
    # تسجيل مواطن جديد (للموظفين)
    path('register/', citizen_views.citizen_registration, name='citizen_registration'),
    
    # تسجيل مواطن جديد (للمواطنين - عام)
    path('public-register/', citizen_views.public_citizen_registration, name='public_citizen_registration'),
    
    # صفحة النجاح
    path('success/', citizen_views.registration_success, name='registration_success'),
    
    # تفاصيل طلب التسجيل
    path('request/<int:request_id>/', citizen_views.registration_request_detail, name='registration_request_detail'),
    
    # التحقق من رقم الهوية (AJAX)
    path('check-national-id/', citizen_views.check_national_id, name='check_national_id'),
    
    # قبول طلب التسجيل (AJAX)
    path('request/<int:request_id>/approve/', citizen_views.approve_registration_request, name='approve_registration_request'),
    
    # رفض طلب التسجيل (AJAX)
    path('request/<int:request_id>/reject/', citizen_views.reject_registration_request, name='reject_registration_request'),
    
    # حذف طلب التسجيل (AJAX)
    path('request/<int:request_id>/delete/', citizen_views.delete_registration_request, name='delete_registration_request'),
] 