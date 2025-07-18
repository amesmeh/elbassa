# دليل المساهمة في المشروع

شكراً لاهتمامك بالمساهمة في مشروع ELBassa! هذا الدليل سيساعدك على البدء.

## كيفية المساهمة

### 1. الإبلاغ عن الأخطاء

إذا وجدت خطأ في المشروع:

1. تحقق من أن الخطأ لم يتم الإبلاغ عنه مسبقاً
2. أنشئ Issue جديد مع:
   - وصف واضح للمشكلة
   - خطوات لتكرار الخطأ
   - معلومات النظام (نظام التشغيل، إصدار Python، إلخ)
   - لقطة شاشة إذا كان ذلك مناسباً

### 2. اقتراح ميزات جديدة

لاقتراح ميزة جديدة:

1. تحقق من أن الميزة لم يتم اقتراحها مسبقاً
2. أنشئ Issue جديد مع:
   - وصف مفصل للميزة
   - سبب الحاجة إليها
   - أمثلة على الاستخدام

### 3. المساهمة بالكود

#### إعداد البيئة التطويرية

1. **استنساخ المشروع**
   ```bash
   git clone https://github.com/your-username/ELBassa.git
   cd ELBassa
   ```

2. **إنشاء فرع جديد**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **إعداد البيئة الافتراضية**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # أو
   source venv/bin/activate  # Linux/Mac
   ```

4. **تثبيت المتطلبات**
   ```bash
   pip install -r requirements.txt
   ```

5. **إعداد قاعدة البيانات**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   ```

#### معايير الكود

- **التسمية**: استخدم أسماء واضحة ومفهومة باللغة الإنجليزية
- **التعليقات**: اكتب تعليقات باللغة العربية للوظائف المعقدة
- **التنسيق**: اتبع معايير PEP 8
- **الاختبارات**: اكتب اختبارات للميزات الجديدة

#### مثال على هيكل الكود

```python
def calculate_family_members(guardian):
    """
    حساب عدد أفراد العائلة بناءً على عدد الأبناء والزوجات
    
    Args:
        guardian: كائن ولي الأمر
        
    Returns:
        int: إجمالي عدد أفراد العائلة
    """
    children_count = guardian.children.count()
    wives_count = guardian.wives.count()
    
    # ولي الأمر + الزوجات + الأبناء
    total_members = 1 + wives_count + children_count
    
    return total_members
```

### 4. إرسال Pull Request

1. **تأكد من أن الكود يعمل**
   ```bash
   python manage.py test
   python manage.py runserver
   ```

2. **إضافة التغييرات**
   ```bash
   git add .
   git commit -m "إضافة ميزة: وصف الميزة المضافة"
   ```

3. **رفع التغييرات**
   ```bash
   git push origin feature/your-feature-name
   ```

4. **إنشاء Pull Request**
   - اذهب إلى GitHub
   - انقر على "New Pull Request"
   - اختر الفرع الخاص بك
   - اكتب وصفاً واضحاً للتغييرات

## معايير الالتزام (Commit Standards)

استخدم الرسائل التالية:

- `feat:` ميزة جديدة
- `fix:` إصلاح خطأ
- `docs:` تحديث الوثائق
- `style:` تحسينات في التنسيق
- `refactor:` إعادة هيكلة الكود
- `test:` إضافة أو تحديث الاختبارات
- `chore:` مهام الصيانة

أمثلة:
```
feat: إضافة نظام تصدير البيانات إلى PDF
fix: إصلاح مشكلة في حساب العمر
docs: تحديث دليل المستخدم
```

## إرشادات إضافية

### للواجهة الأمامية (Frontend)

- استخدم Bootstrap 5 للتصميم
- تأكد من أن الواجهة متجاوبة
- استخدم الأيقونات من Bootstrap Icons
- اكتب CSS باللغة العربية في التعليقات

### لقاعدة البيانات

- اكتب نماذج واضحة ومفهومة
- استخدم verbose_name باللغة العربية
- أضف help_text مفيد
- اكتب migrations واضحة

### للأمان

- لا تضع بيانات حساسة في الكود
- استخدم متغيرات البيئة
- تحقق من صحة المدخلات
- استخدم CSRF protection

## الحصول على المساعدة

إذا كنت بحاجة إلى مساعدة:

1. تحقق من الوثائق الموجودة
2. ابحث في Issues السابقة
3. أنشئ Issue جديد للمساعدة
4. تواصل مع فريق التطوير

## شكراً لك!

شكراً لمساهمتك في جعل ELBassa أفضل! كل مساهمة، مهما كانت صغيرة، مهمة جداً. 