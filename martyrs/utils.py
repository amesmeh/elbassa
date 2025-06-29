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
    مثال: "محمد الشهيد" يجد "محمد أحمد الشهيد"
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

def search_martyrs(search_term):
    """
    بحث مرن في الشهداء مع أولوية للبحث بـ AND
    """
    from .models import Martyr
    
    if not search_term:
        return Martyr.objects.all()
    
    # تطبيع النص وتقسيمه إلى كلمات
    normalized_search = normalize_arabic_text(search_term)
    search_words = [word.strip() for word in normalized_search.split() if word.strip()]
    original_words = [word.strip() for word in search_term.split() if word.strip()]
    
    # إذا كان هناك كلمة واحدة فقط، استخدم البحث العادي
    if len(search_words) == 1:
        word = search_words[0]
        original_word = original_words[0] if original_words else word
        
        # البحث في جميع الحقول
        query = (
            Q(name__icontains=original_word) |
            Q(name__icontains=word) |
            Q(national_id__icontains=original_word) |
            Q(agent_name__icontains=original_word) |
            Q(agent_name__icontains=word) |
            Q(agent_national_id__icontains=original_word) |
            Q(agent_phone__icontains=original_word)
        )
        return Martyr.objects.filter(query).distinct()
    
    # للبحث متعدد الكلمات، أعط الأولوية للبحث بـ AND
    and_queries = []
    
    # البحث بـ AND في اسم الشهيد (الأولوية العليا)
    martyr_name_and = Q()
    for word in original_words:
        if len(word) >= 2:
            martyr_name_and &= Q(name__icontains=word)
    if martyr_name_and != Q():
        and_queries.append(martyr_name_and)
    
    # البحث بـ AND في اسم الشهيد (النسخة المطبعة)
    martyr_name_and_norm = Q()
    for word in search_words:
        if len(word) >= 2:
            martyr_name_and_norm &= Q(name__icontains=word)
    if martyr_name_and_norm != Q():
        and_queries.append(martyr_name_and_norm)
    
    # البحث بـ AND في اسم الوكيل
    agent_name_and = Q()
    for word in original_words:
        if len(word) >= 2:
            agent_name_and &= Q(agent_name__icontains=word)
    if agent_name_and != Q():
        and_queries.append(agent_name_and)
    
    # البحث بـ AND في اسم الوكيل (النسخة المطبعة)
    agent_name_and_norm = Q()
    for word in search_words:
        if len(word) >= 2:
            agent_name_and_norm &= Q(agent_name__icontains=word)
    if agent_name_and_norm != Q():
        and_queries.append(agent_name_and_norm)
    
    # إذا وجدت نتائج بالبحث AND، اعرضها
    if and_queries:
        and_query = reduce(operator.or_, and_queries)
        and_results = Martyr.objects.filter(and_query).distinct()
        if and_results.exists():
            return and_results
    
    # إذا لم توجد نتائج بـ AND، ارجع للبحث العادي (OR) كما كان
    martyr_name_query = create_advanced_name_search(search_term, 'name')
    martyr_id_query = Q(national_id__icontains=search_term)
    agent_name_query = create_advanced_name_search(search_term, 'agent_name')
    agent_id_query = Q(agent_national_id__icontains=search_term)
    agent_phone_query = Q(agent_phone__icontains=search_term)
    
    final_query = martyr_name_query | martyr_id_query | agent_name_query | agent_id_query | agent_phone_query
    return Martyr.objects.filter(final_query).distinct() 