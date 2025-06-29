from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings
from .permissions import get_user_district

class LoginRequiredMiddleware:
    """وسيط للتأكد من تسجيل الدخول في جميع الصفحات"""
    
    def __init__(self, get_response):
        self.get_response = get_response
        # URLs التي لا تحتاج تسجيل دخول
        self.exempt_urls = [
            '/accounts/login/',
            '/admin/login/',
            '/static/',
            '/media/',
            '/admin/',
        ]
    
    def __call__(self, request):
        # التحقق من أن المستخدم مسجل دخول
        if not request.user.is_authenticated:
            # التحقق من أن الطلب ليس لصفحة معفاة
            path = request.path_info
            if not any(path.startswith(url) for url in self.exempt_urls):
                return redirect('login')
        
        response = self.get_response(request)
        return response

class DistrictFilterMiddleware:
    """وسيط لتصفية البيانات حسب الحي"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # تنفيذ الكود قبل معالجة الطلب
        if request.user.is_authenticated and not request.user.is_superuser:
            district = get_user_district(request.user)
            if district:
                # تخزين الحي في الطلب لاستخدامه لاحقاً
                request.user_district = district
            
        response = self.get_response(request)
        return response 