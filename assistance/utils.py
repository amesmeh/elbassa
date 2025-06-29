from django.db.models import Q
from .models import Assistance

def search_assistance(query):
    """البحث في سجلات المساعدات"""
    if not query:
        return Assistance.objects.all()
    
    return Assistance.objects.filter(
        Q(national_id__icontains=query) |
        Q(name__icontains=query) |
        Q(district_name__icontains=query)
    ) 