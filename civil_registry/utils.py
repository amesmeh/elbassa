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

def search_civil_registry(search_term):
    """
    بحث مرن في السجل المدني
    """
    from .models import CivilRegistry
    
    if not search_term:
        return CivilRegistry.objects.all()
    
    # البحث المرن في الاسم
    name_query = create_advanced_name_search(search_term, 'name')
    
    # البحث في رقم الهوية
    national_id_query = Q(national_id__icontains=search_term)
    
    # البحث في الجنس (بالعربية)
    gender_query = Q()
    normalized_search = normalize_arabic_text(search_term)
    if 'ذكر' in search_term or 'ذكر' in normalized_search:
        gender_query |= Q(gender='M')
    if 'انثى' in normalized_search or 'أنثى' in search_term:
        gender_query |= Q(gender='F')
    
    # البحث في المحافظة (بالعربية)
    governorate_query = Q()
    governorate_mapping = {
        'غزة': 'gaza',
        'شمال غزة': 'north_gaza',
        'الوسطى': 'middle_area',
        'خان يونس': 'khan_younis',
        'رفح': 'rafah',
        'الضفة الغربية': 'west_bank',
        'القدس': 'jerusalem',
        'أخرى': 'other'
    }
    
    for arabic_term, english_value in governorate_mapping.items():
        if normalized_search in normalize_arabic_text(arabic_term):
            governorate_query |= Q(governorate=english_value)
    
    # البحث في المدينة
    city_query = create_advanced_name_search(search_term, 'city')
    
    # البحث في الحي
    neighborhood_query = create_advanced_name_search(search_term, 'neighborhood')
    
    # البحث في العنوان
    address_query = Q(address__icontains=search_term)
    
    # البحث في الملاحظات
    notes_query = Q(notes__icontains=search_term)
    
    # دمج جميع الاستعلامات
    final_query = (name_query | national_id_query | gender_query | 
                  governorate_query | city_query | neighborhood_query | 
                  address_query | notes_query)
    
    return CivilRegistry.objects.filter(final_query).distinct() 