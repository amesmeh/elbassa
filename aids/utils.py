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
    مثال: "عاطف مسمح" يجد "عاطف سعيد محمد مسمح"
    """
    if not search_term:
        return Q()
    
    # تطبيع النص
    normalized_search = normalize_arabic_text(search_term)
    search_words = [word.strip() for word in normalized_search.split() if word.strip()]
    
    if not search_words:
        return Q()
    
    # إنشاء استعلام يتطلب وجود جميع الكلمات في الاسم
    word_queries = []
    for word in search_words:
        if len(word) >= 2:
            word_queries.append(Q(**{f"{name_field}__icontains": word}))
    
    if word_queries:
        # جميع الكلمات يجب أن تكون موجودة (AND)
        return reduce(operator.and_, word_queries)
    
    return Q()

def search_beneficiaries(search_term):
    """
    بحث مرن في المستفيدين (أولياء الأمور)
    """
    from basic_data.models import Guardian
    
    if not search_term:
        return Guardian.objects.all()
    
    # البحث المرن في الاسم
    name_query = create_advanced_name_search(search_term, 'name')
    
    # البحث في رقم الهوية
    id_query = Q(national_id__icontains=search_term)
    
    # البحث في رقم الهاتف
    phone_query = Q(phone_number__icontains=search_term)
    
    # دمج جميع الاستعلامات
    final_query = name_query | id_query | phone_query
    
    return Guardian.objects.filter(final_query).distinct()

def search_distributions(search_term):
    """
    بحث مرن في التوزيعات
    """
    from .models import Distribution
    
    if not search_term:
        return Distribution.objects.all()
    
    # البحث في اسم التوزيع
    distribution_name_query = create_advanced_name_search(search_term, 'name')
    
    # البحث في الوصف
    description_query = Q(description__icontains=search_term)
    
    # البحث في نوع المساعدة
    aid_type_query = Q(aid_type__icontains=search_term)
    
    # دمج جميع الاستعلامات
    final_query = distribution_name_query | description_query | aid_type_query
    
    return Distribution.objects.filter(final_query).distinct() 