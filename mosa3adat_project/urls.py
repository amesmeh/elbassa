"""
URL configuration for mosa3adat_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from basic_data.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    
    # مسارات المصادقة
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    
    # مسارات التطبيقات
    path('basic-data/', include('basic_data.urls')),
    path('assistance/', include('assistance.urls')),
    path('aids/', include('aids.urls')),
    path('reports/', include('reports.urls')),
    path('martyrs/', include('martyrs.urls')),
    path('injured/', include('injured.urls')),
    path('medical/', include('medical.urls')),
    path('damages/', include('damages.urls')),
    path('orphans/', include('orphans.urls')),
    path('citizen/', include('basic_data.citizen_urls')),
]

# إعدادات الملفات الثابتة في وضع التطوير
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
