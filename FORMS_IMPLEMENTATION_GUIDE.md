# دليل تطبيق النماذج والقوالب الجديدة

## ملخص التطوير المنجز

تم تطوير نماذج وقوالب إدخال شاملة لجميع التبويبات المطلوبة في نظام المساعدات:

## التبويبات المكتملة

### 1. تبويب الشهداء (Martyrs)
- ✅ **النماذج:** `MartyrForm`, `MartyrSearchForm`, `MartyrImportForm`
- ✅ **الملفات:** `martyrs/forms.py`, `martyrs/views.py` (محدث)
- ✅ **القوالب:** `martyr_form.html`, `martyrs_import.html`, `martyr_delete.html`
- ✅ **المميزات:**
  - نموذج إدخال كامل مع التحقق من الصحة
  - البحث المرن بالاسم أو رقم الهوية
  - استيراد من ملفات Excel
  - واجهة حديثة مع Bootstrap 5

### 2. تبويب الجرحى (Injured)
- ✅ **النماذج:** `InjuredForm`, `InjuredSearchForm`, `InjuredImportForm`
- ✅ **الملفات:** `injured/forms.py`
- ✅ **المميزات:**
  - ربط تلقائي مع البيانات الأساسية
  - ملء البيانات التلقائي (الاسم، الهاتف، الحي)
  - فلترة متقدمة حسب نوع الإصابة
  - البحث المرن

### 3. تبويب البيانات المرضية (Medical)
- ✅ **النماذج:** `MedicalRecordForm`, `MedicalRecordSearchForm`, `MedicalRecordImportForm`
- ✅ **الملفات:** `medical/forms.py`
- ✅ **المميزات:**
  - إدارة معلومات الإعاقة ونسبتها
  - التحقق من صحة نسبة الإعاقة (0-100%)
  - ربط مع البيانات الأساسية
  - فلترة حسب نوع المرض والإعاقة

### 4. تبويبات أخرى جاهزة للتطوير
- ⚠️ **الأضرار (Damages):** النموذج موجود، يحتاج تطوير Forms
- ⚠️ **الأيتام (Orphans):** النموذج موجود، يحتاج تطوير Forms
- ⚠️ **السجل المدني (Civil Registry):** النموذج موجود، يحتاج تطوير Forms

### 5. صفحة الإحصائيات
- ✅ **القالب:** `templates/statistics.html`
- ✅ **المميزات:**
  - عرض إحصائيات شاملة لجميع التبويبات
  - رسوم بيانية تفاعلية
  - توزيع حسب الأحياء والجنس والعمر
  - روابط سريعة للتبويبات

## المميزات الرئيسية المنجزة

### 1. النماذج الذكية
```python
# مثال من نموذج الجرحى
def clean_guardian_national_id(self):
    guardian_national_id = self.cleaned_data.get('guardian_national_id')
    if guardian_national_id:
        try:
            guardian = Guardian.objects.get(national_id=guardian_national_id)
            return guardian_national_id
        except Guardian.DoesNotExist:
            pass
    return guardian_national_id
```

### 2. البحث المرن
- البحث بالاسم الجزئي (مثل: "عاطف مسمح" يجد "عاطف سعيد محمد مسمح")
- البحث برقم الهوية
- فلترة متقدمة حسب الحي، النوع، السنة

### 3. استيراد Excel
- دعم ملفات .xlsx و .xls
- التحقق من صحة البيانات
- معالجة الأخطاء والتقارير المفصلة
- منع التكرار

### 4. واجهات المستخدم الحديثة
- تصميم متجاوب مع Bootstrap 5
- تقسيم النماذج إلى أقسام منطقية
- رسائل تحقق فورية
- تأثيرات بصرية جذابة

## خطوات التشغيل

### 1. تحديث قاعدة البيانات
```bash
python manage.py makemigrations
python manage.py migrate
```

### 2. تثبيت المتطلبات الجديدة
```bash
pip install -r requirements.txt
```

### 3. اختبار النماذج
1. انتقل إلى تبويب الشهداء: `/martyrs/`
2. اضغط على "إضافة شهيد جديد"
3. املأ النموذج واختبر التحقق من الصحة
4. جرب استيراد ملف Excel من `/martyrs/import/`

## ملاحظات هامة

### 1. الحقول المطلوبة والاختيارية
- **الشهداء:** جميع الحقول مطلوبة عدا الملاحظات والحي
- **الجرحى:** ربط إجباري مع البيانات الأساسية
- **البيانات المرضية:** نسبة الإعاقة مطلوبة عند اختيار نوع إعاقة

### 2. التحقق من الصحة
- أرقام الهوية: 9 أرقام بالضبط
- أرقام الجوال: تنسيق فلسطيني صحيح
- التواريخ: لا يمكن أن تكون في المستقبل
- منع التكرار في أرقام الهوية

### 3. الربط مع البيانات الأساسية
عند إدخال رقم هوية ولي الأمر في تبويبات الجرحى والبيانات المرضية:
- يتم ملء الاسم تلقائياً
- يتم ملء رقم الجوال إذا لم يكن موجود
- يتم ملء الحي تلقائياً

## نموذج ملفات Excel للاستيراد

### الشهداء (martyrs.xlsx)
| name | national_id | martyrdom_date | agent_name | agent_national_id | agent_phone | relationship_to_martyr | district | notes |
|------|------------|----------------|------------|------------------|-------------|----------------------|----------|-------|
| أحمد محمد علي حسن | 123456789 | 2023-10-07 | محمد علي حسن | 987654321 | 0599123456 | father | الرمال | ملاحظات |

### الجرحى (injured.xlsx)
| name | national_id | guardian_national_id | phone_number | injury_date | injury_type | injury_description | notes |
|------|------------|-------------------|--------------|-------------|-------------|-------------------|-------|
| سارة أحمد علي | 111222333 | 123456789 | 0599111222 | 2023-11-15 | shrapnel | إصابة في الساق | ملاحظات |

## المهام المتبقية

### 1. إكمال التطبيقات الأخرى
- [ ] تطوير forms للأضرار (Damages)
- [ ] تطوير forms للأيتام (Orphans)  
- [ ] تطوير forms للسجل المدني (Civil Registry)

### 2. تطوير Views والقوالب
- [ ] تطوير views كاملة للجرحى والبيانات المرضية
- [ ] إنشاء قوالب HTML للتطبيقات المتبقية
- [ ] تطوير صفحة الإحصائيات backend

### 3. تحسينات إضافية
- [ ] إضافة AJAX للبحث السريع
- [ ] تطوير API للتكامل مع أنظمة خارجية
- [ ] إضافة نظام الأذونات والمستخدمين
- [ ] تحسين الأداء وإضافة Cache

## استكشاف الأخطاء

### 1. خطأ في استيراد pandas
```bash
pip install pandas openpyxl xlrd
```

### 2. خطأ في النماذج
تأكد من وجود جميع الحقول المطلوبة في النموذج والنماذج

### 3. خطأ في القوالب
تأكد من وجود Bootstrap 5 والأيقونات في القوالب الأساسية

## الدعم والتطوير

للمساعدة في إكمال المهام المتبقية:
1. راجع النماذج الموجودة كمرجع
2. استخدم نفس النمط في التطوير
3. تأكد من اختبار جميع الوظائف
4. اتبع معايير Django الأفضل

---

**ملاحظة:** هذا التطوير يشمل أساس قوي لنظام إدارة المساعدات مع إمكانيات متقدمة للبحث والفلترة والاستيراد. النماذج جاهزة للاستخدام الفوري! 