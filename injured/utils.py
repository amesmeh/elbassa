import re
from django.db.models import Q
from functools import reduce
import operator

def normalize_arabic_text(text):
    """
    تطبيع النص العربي لمعالجة الهمزات والحروف المتشابهة
    """
    if not text:
        return ""
    
    # تحويل إلى نص صغير
    text = text.strip().lower()
    
    # معالجة الهمزات
    text = re.sub(r'[أإآا]', 'ا', text)
    text = re.sub(r'[ؤو]', 'و', text)
    text = re.sub(r'[ئي]', 'ي', text)
    text = re.sub(r'[ة]', 'ه', text)
    
    # إزالة التشكيل
    text = re.sub(r'[\u064B-\u0652]', '', text)
    
    # إزالة المسافات الزائدة
    text = re.sub(r'\s+', ' ', text)
    
    return text

def create_advanced_name_search(search_term, name_field):
    """
    بحث متقدم للأسماء يدعم البحث بأجزاء من الاسم
    مثال: "محمد أحمد" يجد "محمد أحمد علي"
    """
    if not search_term:
        return Q()
    
    # تطبيع النص
    normalized_search = normalize_arabic_text(search_term)
    search_words = [word.strip() for word in normalized_search.split() if word.strip()]
    original_words = [word.strip() for word in search_term.split() if word.strip()]
    
    if not search_words:
        return Q()
    
    # إنشاء استعلامات للبحث
    all_queries = []
    
    # البحث بالنص الكامل الأصلي
    all_queries.append(Q(**{f"{name_field}__icontains": search_term}))
    
    # البحث بالنص الكامل المطبع
    all_queries.append(Q(**{f"{name_field}__icontains": normalized_search}))
    
    # البحث بكل كلمة أصلية على حدة
    for word in original_words:
        if len(word) >= 2:
            all_queries.append(Q(**{f"{name_field}__icontains": word}))
    
    # البحث بكل كلمة مطبعة على حدة
    for word in search_words:
        if len(word) >= 2:
            all_queries.append(Q(**{f"{name_field}__icontains": word}))
    
    # البحث بجميع الكلمات الأصلية معاً (AND)
    if len(original_words) > 1:
        original_and_query = Q()
        for word in original_words:
            if len(word) >= 2:
                original_and_query &= Q(**{f"{name_field}__icontains": word})
        if original_and_query:
            all_queries.append(original_and_query)
    
    # البحث بجميع الكلمات المطبعة معاً (AND)
    if len(search_words) > 1:
        normalized_and_query = Q()
        for word in search_words:
            if len(word) >= 2:
                normalized_and_query &= Q(**{f"{name_field}__icontains": word})
        if normalized_and_query:
            all_queries.append(normalized_and_query)
    
    # دمج جميع الاستعلامات بـ OR
    if all_queries:
        return reduce(operator.or_, all_queries)
    
    return Q()

def search_injured(search_term):
    """
    بحث مرن في الجرحى
    """
    from .models import Injured
    
    if not search_term:
        return Injured.objects.all()
    
    # البحث المرن في اسم الجريح
    injured_name_query = create_advanced_name_search(search_term, 'name')
    
    # البحث في رقم هوية الجريح
    injured_id_query = Q(national_id__icontains=search_term)
    
    # البحث المرن في اسم ولي الأمر
    guardian_name_query = create_advanced_name_search(search_term, 'guardian_name')
    
    # البحث في رقم هوية ولي الأمر
    guardian_id_query = Q(guardian_national_id__icontains=search_term)
    
    # البحث في رقم الهاتف
    phone_query = Q(phone_number__icontains=search_term)
    
    # البحث في نوع الإصابة (بالعربية)
    injury_type_query = Q()
    injury_type_mapping = {
        'رصاص': 'gunshot',
        'شظايا': 'shrapnel',
        'انفجار': 'explosion',
        'حروق': 'burn',
        'كسور': 'fracture',
        'بتر': 'amputation',
        'أخرى': 'other'
    }
    
    normalized_search = normalize_arabic_text(search_term)
    for arabic_term, english_value in injury_type_mapping.items():
        if normalized_search in normalize_arabic_text(arabic_term):
            injury_type_query |= Q(injury_type=english_value)
    
    # البحث في وصف الإصابة
    injury_description_query = Q(injury_description__icontains=search_term)
    
    # البحث في الملاحظات
    notes_query = Q(notes__icontains=search_term)
    
    # دمج جميع الاستعلامات
    final_query = (injured_name_query | injured_id_query | guardian_name_query | 
                  guardian_id_query | phone_query | injury_type_query | 
                  injury_description_query | notes_query)
    
    return Injured.objects.filter(final_query).distinct() 