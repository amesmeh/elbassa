# تحسينات صفحة أولياء الأمور - Excel

## المشاكل التي تم حلها

### 1. مشكلة التصدير بصيغة CSV بدلاً من Excel
**المشكلة:** زر التصدير كان يصدر ملفات بصيغة CSV بدلاً من Excel.

**الحل:** 
- تم تحديث وظيفة `export_guardians_excel` في `basic_data/views.py`
- الآن يتم التصدير بصيغة `.xlsx` باستخدام `pandas` و `openpyxl`
- تم إضافة تنسيق عربي محسن للملفات المصدرة

### 2. التصدير لا يطبق الفلاتر الحالية
**المشكلة:** عند التصدير، كان يتم تصدير جميع البيانات دون تطبيق الفلاتر المطبقة في الصفحة.

**الحل:**
- تم تحديث وظيفة التصدير لتطبق نفس الفلاتر المستخدمة في القائمة:
  - البحث بالاسم/رقم الهوية/رقم الجوال
  - فلتر الحي
  - فلتر الجنس
  - فلتر الحالة الاجتماعية
  - فلتر حالة الإقامة
  - فلتر عدد أفراد العائلة

### 3. عدم وجود زر استيراد
**المشكلة:** لم يكن هناك زر لاستيراد البيانات من ملفات Excel.

**الحل:**
- تم إضافة زر استيراد في القائمة المنسدلة
- تم إنشاء نافذة استيراد مع تعليمات واضحة
- تم ربط الزر بوظيفة `import_guardians_excel`

### 4. عدم وجود زر تحميل النموذج
**المشكلة:** لم يكن هناك زر لتحميل نموذج Excel لضمان التنسيق الصحيح.

**الحل:**
- تم إضافة زر تحميل النموذج في القائمة المنسدلة
- النموذج يحتوي على بيانات مثال وتعليمات مفصلة
- يتم إنشاء النموذج باستخدام وظيفة `create_guardians_template`

### 5. دمج الأزرار في زر واحد
**المشكلة:** كانت الأزرار منفصلة ومشتتة.

**الحل:**
- تم دمج جميع وظائف Excel في زر واحد مع قائمة منسدلة
- القائمة تحتوي على:
  - استيراد Excel
  - تحميل النموذج
  - تحميل ملف الأخطاء (إذا وجدت)
  - تصدير البيانات الحالية

## التحديثات المطبقة

### 1. تحديث صفحة القائمة (`templates/basic_data/guardian_list.html`)
```html
<!-- تم استبدال زر التصدير البسيط بقائمة منسدلة -->
<div class="dropdown">
    <button class="btn btn-success dropdown-toggle" type="button" id="excelDropdown" data-bs-toggle="dropdown">
        <i class="fas fa-file-excel me-1"></i>Excel
    </button>
    <ul class="dropdown-menu">
        <li><a class="dropdown-item" href="#" data-bs-toggle="modal" data-bs-target="#importModal">
            <i class="fas fa-upload me-2"></i>استيراد Excel
        </a></li>
        <li><a class="dropdown-item" href="{% url 'basic_data:download_guardians_template' %}">
            <i class="fas fa-download me-2"></i>تحميل النموذج
        </a></li>
        <li><a class="dropdown-item" href="{% url 'basic_data:export_guardians_excel' %}{% if request.GET %}?{{ request.GET.urlencode }}{% endif %}">
            <i class="fas fa-download me-2"></i>تصدير البيانات الحالية
        </a></li>
    </ul>
</div>
```

### 2. إضافة نافذة الاستيراد
```html
<!-- نافذة استيراد Excel -->
<div class="modal fade" id="importModal">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title">
                    <i class="fas fa-file-upload me-2"></i>استيراد أولياء الأمور من Excel
                </h5>
            </div>
            <form method="post" action="{% url 'basic_data:import_guardians_excel' %}" enctype="multipart/form-data">
                <!-- محتوى النافذة -->
            </form>
        </div>
    </div>
</div>
```

### 3. تحديث وظيفة التصدير (`basic_data/views.py`)
```python
@login_required
def export_guardians_excel(request):
    """تصدير أولياء الأمور إلى Excel مع تطبيق الفلاتر"""
    # تطبيق نفس الفلاتر المستخدمة في القائمة
    search_query = request.GET.get('q', '')
    search_type = request.GET.get('search_type', 'name')
    district_filter = request.GET.get('district', '')
    # ... باقي الفلاتر
    
    # تطبيق الفلاتر على البيانات
    if search_query:
        guardians = search_guardians(search_query, search_type)
    else:
        guardians = Guardian.objects.select_related('district').prefetch_related('wives').all()
    
    # ... تطبيق باقي الفلاتر
    
    # استخدام وظيفة التصدير المحسنة
    try:
        from utils.excel_utils import export_guardians_to_excel
        return export_guardians_to_excel(guardians)
    except ImportError:
        # نظام بديل في حالة عدم وجود utils
        # ... كود التصدير البديل
```

### 4. تحديث وظيفة الاستيراد
```python
@login_required 
def import_guardians_excel(request):
    """استيراد أولياء الأمور من Excel"""
    if request.method == 'POST':
        excel_file = request.FILES.get('excel_file')
        try:
            from utils.excel_utils import import_guardians_from_excel
            result = import_guardians_from_excel(excel_file)
            
            if result['success']:
                messages.success(request, f'تم استيراد {result["success_count"]} ولي أمر بنجاح')
                if result.get('error_messages'):
                    request.session['import_errors'] = result['error_messages']
                    request.session['detailed_errors'] = result.get('detailed_errors', [])
        except ImportError:
            # نظام بديل
            # ... كود الاستيراد البديل
```

## الميزات الجديدة

### 1. تصدير محسن
- تصدير بصيغة Excel (.xlsx) بدلاً من CSV
- تطبيق جميع الفلاتر الحالية
- تنسيق عربي محسن
- تضمين معلومات الزوجات

### 2. استيراد محسن
- دعم ملفات Excel (.xlsx)
- تحقق من صحة البيانات
- رسائل خطأ مفصلة
- إمكانية تحميل ملف الأخطاء

### 3. نموذج تحميل
- نموذج Excel جاهز للاستخدام
- بيانات مثال واقعية
- تعليمات مفصلة
- تنسيق عربي محسن

### 4. واجهة مستخدم محسنة
- زر واحد يجمع جميع وظائف Excel
- قائمة منسدلة منظمة
- نافذة استيراد سهلة الاستخدام
- رسائل تأكيد واضحة

## كيفية الاستخدام

### 1. تصدير البيانات
1. قم بتطبيق الفلاتر المطلوبة في الصفحة
2. انقر على زر "Excel"
3. اختر "تصدير البيانات الحالية"
4. سيتم تحميل ملف Excel يحتوي على البيانات المفلترة

### 2. استيراد البيانات
1. انقر على زر "Excel"
2. اختر "تحميل النموذج" أولاً
3. املأ النموذج بالبيانات المطلوبة
4. انقر على "استيراد Excel"
5. اختر الملف المملوء
6. انقر على "استيراد"

### 3. تحميل ملف الأخطاء
- إذا حدثت أخطاء أثناء الاستيراد، سيظهر خيار "تحميل ملف الأخطاء"
- يحتوي الملف على تفاصيل الأخطاء وطرق إصلاحها

## المتطلبات التقنية

- `pandas` للتعامل مع ملفات Excel
- `openpyxl` لإنشاء ملفات Excel
- `utils.excel_utils` للوظائف المحسنة
- Bootstrap للواجهة المنسدلة

## ملاحظات مهمة

1. **الصلاحيات:** الاستيراد متاح للمشرفين فقط
2. **التنسيق:** يجب أن تكون الملفات بصيغة .xlsx
3. **البيانات المطلوبة:** الاسم ورقم الهوية والجنس مطلوبان
4. **الأحياء:** يجب أن تكون الأحياء موجودة في النظام قبل الاستيراد
5. **التكرار:** البيانات المكررة ستُحدث بدلاً من إنشاء سجلات جديدة 