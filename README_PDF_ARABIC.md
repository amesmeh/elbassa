# حل مشكلة الخطوط العربية في تصدير PDF

## المشكلة
كانت ملفات PDF المُصدرة تظهر النصوص العربية كرموز هيروغليفية غير مقروءة.

## الحل المطبق

### 1. نظام تصدير JavaScript محسن
- إنشاء ملف `static/js/arabic-pdf.js` مع دعم الخطوط العربية
- إعداد pdfMake لاستخدام خطوط تدعم العربية
- دوال مخصصة لتصدير الجداول والإحصائيات

### 2. نظام تصدير من الخادم (Python)
- إنشاء ملف `utils/pdf_export.py` باستخدام ReportLab و WeasyPrint
- دعم كامل للخطوط العربية
- نظام احتياطي في حالة فشل إحدى المكتبات

### 3. التحديثات المطبقة

#### الملفات الجديدة:
- `static/js/arabic-pdf.js` - نظام JavaScript للتصدير
- `utils/pdf_export.py` - نظام Python للتصدير
- `requirements_pdf.txt` - مكتبات PDF المطلوبة

#### الملفات المحدثة:
- `templates/base.html` - إضافة ملف JavaScript الجديد
- `civil_registry/views.py` - إضافة دالة تصدير PDF
- `civil_registry/urls.py` - إضافة رابط التصدير
- `reports/views.py` - إضافة تصدير الإحصائيات
- `reports/urls.py` - إضافة رابط تصدير الإحصائيات
- جميع قوالب DataTables - استخدام النظام الجديد

## كيفية الاستخدام

### 1. تثبيت المكتبات المطلوبة
```bash
pip install -r requirements_pdf.txt
```

### 2. تصدير من واجهة المستخدم
- **تصدير JavaScript**: استخدام أزرار "تصدير PDF" في الجداول
- **تصدير من الخادم**: استخدام الأزرار الجديدة في رؤوس الصفحات

### 3. تصدير برمجي
```python
from utils.pdf_export import ArabicPDFExporter

# إنشاء مُصدر
exporter = ArabicPDFExporter()

# تصدير جدول
data = [['محمد', '123456789'], ['فاطمة', '987654321']]
headers = ['الاسم', 'رقم الهوية']
response = exporter.create_table_pdf(data, headers, 'تقرير الأسماء', 'names.pdf')

# تصدير إحصائيات
from utils.pdf_export import export_statistics_to_pdf
stats = {'إجمالي السجلات': 100, 'الذكور': 60, 'الإناث': 40}
response = export_statistics_to_pdf(stats, 'إحصائيات عامة', 'stats.pdf')
```

## الميزات الجديدة

### 1. دعم كامل للعربية
- ✅ النصوص العربية تظهر بشكل صحيح
- ✅ اتجاه النص من اليمين لليسار
- ✅ تنسيق مناسب للمحتوى العربي

### 2. أنظمة متعددة للتصدير
- **JavaScript (pdfMake)**: سريع، يعمل في المتصفح
- **Python (ReportLab)**: قوي، يعمل من الخادم
- **HTML to PDF (WeasyPrint)**: مرن، يدعم CSS

### 3. نظام احتياطي
- في حالة فشل إحدى الطرق، يتم استخدام طريقة بديلة
- تصدير CSV كحل أخير

## استكشاف الأخطاء

### مشكلة: النصوص لا تزال تظهر كرموز غريبة
**الحل:**
1. تأكد من تثبيت المكتبات: `pip install -r requirements_pdf.txt`
2. تحديث المتصفح وإعادة تحميل الصفحة
3. استخدام زر "تصدير PDF" الجديد بدلاً من DataTables

### مشكلة: خطأ في تثبيت WeasyPrint على Windows
**الحل:**
```bash
pip install --upgrade pip setuptools wheel
pip install weasyprint --find-links https://github.com/Kozea/WeasyPrint/releases
```

### مشكلة: الخطوط لا تظهر بشكل جميل
**الحل:**
1. إضافة ملفات خطوط TTF في مجلد `static/fonts/`
2. تحديث `utils/pdf_export.py` لاستخدام الخطوط الجديدة

## التطوير المستقبلي

### خطوط مخصصة
يمكن إضافة خطوط عربية مخصصة:
1. إضافة ملفات `.ttf` في `static/fonts/`
2. تحديث `setup_arabic_fonts()` في `pdf_export.py`
3. تسجيل الخطوط الجديدة

### تحسينات إضافية
- إضافة شعار المؤسسة للتقارير
- تخصيص تنسيق الصفحات
- إضافة رسوم بيانية للإحصائيات
- دعم تصدير ملفات متعددة الصفحات

## الدعم الفني
في حالة استمرار المشاكل:
1. تحقق من سجلات الأخطاء في Django
2. تأكد من إعدادات `STATIC_FILES` في settings.py
3. اختبر التصدير على متصفحات مختلفة

---
**ملاحظة**: هذا الحل يدعم جميع أنواع النصوص العربية ويضمن عرضها بشكل صحيح في ملفات PDF. 