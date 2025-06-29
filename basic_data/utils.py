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

def create_flexible_search_query(search_term, fields):
    """
    إنشاء استعلام بحث مرن يدعم:
    - البحث الجزئي
    - معالجة الهمزات
    - البحث بأجزاء من النص
    """
    if not search_term or not fields:
        return Q()
    
    # تطبيع النص المدخل
    normalized_search = normalize_arabic_text(search_term)
    
    # تقسيم النص إلى كلمات
    search_words = [word.strip() for word in normalized_search.split() if word.strip()]
    
    if not search_words:
        return Q()
    
    # إنشاء استعلامات للبحث
    queries = []
    
    for field in fields:
        # البحث بالنص الكامل
        queries.append(Q(**{f"{field}__icontains": search_term}))
        
        # البحث بالنص المطبع
        queries.append(Q(**{f"{field}__icontains": normalized_search}))
        
        # البحث بكل كلمة على حدة
        for word in search_words:
            if len(word) >= 2:  # تجاهل الكلمات القصيرة جداً
                queries.append(Q(**{f"{field}__icontains": word}))
    
    # دمج جميع الاستعلامات بـ OR
    if queries:
        return reduce(operator.or_, queries)
    
    return Q()

def create_advanced_name_search(search_term, name_field, search_type='exact'):
    """
    بحث متقدم للأسماء يدعم البحث بأجزاء من الاسم
    مثال: "عاطف مسمح" يجد "عاطف سعيد محمد مسمح"
    يعطي أولوية للبحث بجميع الكلمات معاً
    
    search_type:
    - 'exact': بحث دقيق (جميع الكلمات معاً)
    - 'broad': بحث شامل (أي كلمة منفصلة)
    """
    if not search_term:
        return Q()
    
    # تطبيع النص
    normalized_search = normalize_arabic_text(search_term)
    search_words = [word.strip() for word in normalized_search.split() if word.strip()]
    original_words = [word.strip() for word in search_term.split() if word.strip()]
    
    if not search_words:
        return Q()
    
    # إذا كانت كلمة واحدة فقط، ابحث بها مباشرة
    if len(original_words) == 1:
        return Q(**{f"{name_field}__icontains": search_term}) | Q(**{f"{name_field}__icontains": normalized_search})
    
    # البحث الدقيق (افتراضي)
    if search_type == 'exact':
        primary_queries = []
        
        # البحث بالنص الكامل الأصلي (أعلى أولوية)
        primary_queries.append(Q(**{f"{name_field}__icontains": search_term}))
        
        # البحث بالنص الكامل المطبع
        primary_queries.append(Q(**{f"{name_field}__icontains": normalized_search}))
        
        # البحث بجميع الكلمات الأصلية معاً (AND) - أولوية عالية
        if len(original_words) > 1:
            original_and_query = Q()
            for word in original_words:
                if len(word) >= 2:
                    original_and_query &= Q(**{f"{name_field}__icontains": word})
            if original_and_query:
                primary_queries.append(original_and_query)
        
        # البحث بجميع الكلمات المطبعة معاً (AND) - أولوية عالية
        if len(search_words) > 1:
            normalized_and_query = Q()
            for word in search_words:
                if len(word) >= 2:
                    normalized_and_query &= Q(**{f"{name_field}__icontains": word})
            if normalized_and_query:
                primary_queries.append(normalized_and_query)
        
        # دمج الاستعلامات الأساسية بـ OR
        if primary_queries:
            return reduce(operator.or_, primary_queries)
    
    # البحث الشامل
    elif search_type == 'broad':
        all_queries = []
        
        # البحث بالنص الكامل الأصلي
        all_queries.append(Q(**{f"{name_field}__icontains": search_term}))
        
        # البحث بالنص الكامل المطبع
        all_queries.append(Q(**{f"{name_field}__icontains": normalized_search}))
        
        # البحث بجميع الكلمات معاً (AND)
        if len(original_words) > 1:
            original_and_query = Q()
            for word in original_words:
                if len(word) >= 2:
                    original_and_query &= Q(**{f"{name_field}__icontains": word})
            if original_and_query:
                all_queries.append(original_and_query)
        
        if len(search_words) > 1:
            normalized_and_query = Q()
            for word in search_words:
                if len(word) >= 2:
                    normalized_and_query &= Q(**{f"{name_field}__icontains": word})
            if normalized_and_query:
                all_queries.append(normalized_and_query)
        
        # البحث بكل كلمة على حدة (OR)
        for word in original_words:
            if len(word) >= 2:
                all_queries.append(Q(**{f"{name_field}__icontains": word}))
        
        for word in search_words:
            if len(word) >= 2:
                all_queries.append(Q(**{f"{name_field}__icontains": word}))
        
        # دمج جميع الاستعلامات بـ OR
        if all_queries:
            return reduce(operator.or_, all_queries)
    
    return Q()

def search_guardians(search_term, search_type='exact'):
    """
    بحث مرن في أولياء الأمور
    """
    from .models import Guardian
    
    if not search_term:
        return Guardian.objects.all()
    
    # البحث المرن في الاسم
    name_query = create_advanced_name_search(search_term, 'name', search_type)
    
    # البحث في رقم الهوية
    id_query = Q(national_id__icontains=search_term)
    
    # البحث في رقم الهاتف
    phone_query = Q(phone_number__icontains=search_term)
    
    # دمج جميع الاستعلامات
    final_query = name_query | id_query | phone_query
    
    return Guardian.objects.filter(final_query).distinct()

def search_children(search_term, guardian_filter=None, search_type='exact'):
    """
    بحث مرن في الأطفال
    """
    from .models import Child
    
    queryset = Child.objects.all()
    
    if guardian_filter:
        queryset = queryset.filter(guardian_id=guardian_filter)
    
    if not search_term:
        return queryset
    
    # البحث المرن في اسم الطفل
    child_name_query = create_advanced_name_search(search_term, 'name', search_type)
    
    # البحث في رقم هوية الطفل
    child_id_query = Q(national_id__icontains=search_term)
    
    # البحث في اسم ولي الأمر
    guardian_name_query = create_advanced_name_search(search_term, 'guardian__name', search_type)
    
    # البحث في رقم هوية ولي الأمر
    guardian_id_query = Q(guardian__national_id__icontains=search_term)
    
    # دمج جميع الاستعلامات
    final_query = child_name_query | child_id_query | guardian_name_query | guardian_id_query
    
    return queryset.filter(final_query).distinct()

def search_wives(search_term, search_type='exact'):
    """
    بحث مرن في الزوجات
    """
    from .models import Wife
    
    if not search_term:
        return Wife.objects.all()
    
    # البحث المرن في اسم الزوجة
    wife_name_query = create_advanced_name_search(search_term, 'name', search_type)
    
    # البحث في رقم هوية الزوجة
    wife_id_query = Q(national_id__icontains=search_term)
    
    # البحث في اسم ولي الأمر
    guardian_name_query = create_advanced_name_search(search_term, 'guardian__name', search_type)
    
    # البحث في رقم هوية ولي الأمر
    guardian_id_query = Q(guardian__national_id__icontains=search_term)
    
    # دمج جميع الاستعلامات
    final_query = wife_name_query | wife_id_query | guardian_name_query | guardian_id_query
    
    return Wife.objects.filter(final_query).distinct()

def search_districts(search_term, search_type='exact'):
    """
    بحث مرن في المناطق
    """
    from .models import District
    
    if not search_term:
        return District.objects.all()
    
    # البحث المرن في اسم المنطقة
    district_name_query = create_advanced_name_search(search_term, 'name', search_type)
    
    # البحث في اسم المندوب
    representative_name_query = create_advanced_name_search(search_term, 'representative_name', search_type)
    
    # البحث في رقم جوال المندوب
    representative_phone_query = Q(representative_phone__icontains=search_term)
    
    # دمج جميع الاستعلامات
    final_query = district_name_query | representative_name_query | representative_phone_query
    
    return District.objects.filter(final_query).distinct() 