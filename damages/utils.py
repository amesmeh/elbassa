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

def search_damages(search_term):
    """
    بحث مرن في الأضرار
    """
    from .models import Damage
    
    if not search_term:
        return Damage.objects.all()
    
    # البحث المرن في اسم ولي الأمر
    guardian_name_query = create_advanced_name_search(search_term, 'guardian_name')
    
    # البحث في رقم هوية ولي الأمر
    guardian_id_query = Q(guardian_national_id__icontains=search_term)
    
    # البحث في رقم الهاتف
    phone_query = Q(phone_number__icontains=search_term)
    
    # البحث في نوع السكن (بالعربية)
    housing_type_query = Q()
    housing_type_mapping = {
        'شقة': 'apartment',
        'بيت': 'house', 
        'فيلا': 'villa',
        'غرفة': 'room',
        'محل': 'shop',
        'مستودع': 'warehouse',
        'أخرى': 'other'
    }
    
    normalized_search = normalize_arabic_text(search_term)
    for arabic_term, english_value in housing_type_mapping.items():
        if normalized_search in normalize_arabic_text(arabic_term):
            housing_type_query |= Q(housing_type=english_value)
    
    # البحث في نوع الضرر
    damage_type_query = Q()
    if 'كلي' in search_term or 'كلي' in normalized_search:
        damage_type_query |= Q(damage_type='total')
    if 'جزئي' in search_term or 'جزئي' in normalized_search:
        damage_type_query |= Q(damage_type='partial')
    
    # البحث في الملاحظات
    notes_query = Q(notes__icontains=search_term)
    
    # دمج جميع الاستعلامات
    final_query = (guardian_name_query | guardian_id_query | phone_query | 
                  housing_type_query | damage_type_query | notes_query)
    
    return Damage.objects.filter(final_query).distinct() 