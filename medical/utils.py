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

def search_medical_records(search_term):
    """
    بحث مرن في السجلات المرضية
    """
    from .models import MedicalRecord
    
    if not search_term:
        return MedicalRecord.objects.all()
    
    # البحث المرن في اسم المريض
    patient_name_query = create_advanced_name_search(search_term, 'name')
    
    # البحث في رقم هوية المريض
    patient_id_query = Q(national_id__icontains=search_term)
    
    # البحث المرن في اسم ولي الأمر
    guardian_name_query = create_advanced_name_search(search_term, 'guardian_name')
    
    # البحث في رقم هوية ولي الأمر
    guardian_id_query = Q(guardian_national_id__icontains=search_term)
    
    # البحث في رقم الهاتف
    phone_query = Q(phone_number__icontains=search_term)
    
    # البحث في الجنس (بالعربية)
    gender_query = Q()
    normalized_search = normalize_arabic_text(search_term)
    if 'ذكر' in search_term or 'ذكر' in normalized_search:
        gender_query |= Q(gender='M')
    if 'انثى' in normalized_search or 'أنثى' in search_term:
        gender_query |= Q(gender='F')
    
    # البحث في نوع المرض (بالعربية)
    disease_type_query = Q()
    disease_type_mapping = {
        'مزمن': 'chronic',
        'حاد': 'acute',
        'وراثي': 'genetic',
        'معدي': 'infectious',
        'نفسي': 'mental',
        'عصبي': 'neurological',
        'قلبي': 'cardiac',
        'تنفسي': 'respiratory',
        'هضمي': 'digestive',
        'كلوي': 'kidney',
        'سكري': 'diabetes',
        'ضغط': 'hypertension',
        'سرطان': 'cancer',
        'أخرى': 'other'
    }
    
    for arabic_term, english_value in disease_type_mapping.items():
        if normalized_search in normalize_arabic_text(arabic_term):
            disease_type_query |= Q(disease_type=english_value)
    
    # البحث في نوع الإعاقة (بالعربية)
    disability_type_query = Q()
    disability_type_mapping = {
        'حركية': 'mobility',
        'بصرية': 'visual',
        'سمعية': 'hearing',
        'ذهنية': 'intellectual',
        'متعددة': 'multiple',
        'لا يوجد': 'none'
    }
    
    for arabic_term, english_value in disability_type_mapping.items():
        if normalized_search in normalize_arabic_text(arabic_term):
            disability_type_query |= Q(disability_type=english_value)
    
    # البحث في وصف المرض
    disease_description_query = Q(disease_description__icontains=search_term)
    
    # البحث في الملاحظات
    notes_query = Q(notes__icontains=search_term)
    
    # دمج جميع الاستعلامات
    final_query = (patient_name_query | patient_id_query | guardian_name_query | 
                  guardian_id_query | phone_query | gender_query | 
                  disease_type_query | disability_type_query | 
                  disease_description_query | notes_query)
    
    return MedicalRecord.objects.filter(final_query).distinct() 