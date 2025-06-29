# سياسة الأمان

## الإبلاغ عن الثغرات الأمنية

نحن نأخذ الأمان على محمل الجد. إذا اكتشفت ثغرة أمنية، يرجى عدم فتح issue عام. بدلاً من ذلك، يرجى إرسال بريد إلكتروني إلى فريق الأمان.

### كيفية الإبلاغ عن ثغرة أمنية

1. **لا تفتح issue عام** - قد يؤدي ذلك إلى استغلال الثغرة من قبل أشخاص آخرين
2. **أرسل بريد إلكتروني** إلى فريق الأمان مع:
   - وصف مفصل للثغرة
   - خطوات لتكرار المشكلة
   - التأثير المحتمل
   - اقتراحات للإصلاح (إذا كان لديك)

### معلومات الاتصال

- **البريد الإلكتروني**: security@elbassa.org
- **الموضوع**: [SECURITY] وصف مختصر للثغرة

### ما نتوقعه منك

- **الإفصاح المسؤول**: امنحنا وقتاً كافياً لإصلاح الثغرة قبل الإفصاح العام
- **التعاون**: ساعدنا في فهم وتأكيد الثغرة
- **السرية**: لا تشارك معلومات الثغرة مع الآخرين

### ما يمكنك توقعه منا

- **الرد السريع**: سنرد عليك في غضون 48 ساعة
- **التحديثات المنتظمة**: سنوفر تحديثات حول التقدم في الإصلاح
- **الاعتراف**: سنعترف بمساهمتك في تقرير الأمان (إذا رغبت في ذلك)

## إرشادات الأمان للمطورين

### أفضل الممارسات

1. **تحديث التبعيات بانتظام**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

2. **فحص الثغرات الأمنية**
   ```bash
   pip install safety
   safety check
   ```

3. **فحص الكود**
   ```bash
   pip install bandit
   bandit -r .
   ```

4. **استخدام متغيرات البيئة**
   ```python
   # لا تفعل هذا
   SECRET_KEY = 'hardcoded-secret-key'
   
   # افعل هذا
   SECRET_KEY = os.environ.get('SECRET_KEY')
   ```

5. **التحقق من صحة المدخلات**
   ```python
   # استخدم Django Forms للتحقق من صحة البيانات
   from django import forms
   
   class GuardianForm(forms.ModelForm):
       def clean_national_id(self):
           national_id = self.cleaned_data['national_id']
           if not national_id.isdigit() or len(national_id) != 9:
               raise forms.ValidationError('رقم الهوية غير صحيح')
           return national_id
   ```

### إعدادات الأمان الموصى بها

```python
# settings.py
DEBUG = False
ALLOWED_HOSTS = ['your-domain.com']

# إعدادات الجلسات
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True

# إعدادات الأمان
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

### فحص الأمان الروتيني

```bash
# فحص التبعيات
safety check

# فحص الكود
bandit -r .

# فحص الثغرات المعروفة
pip install safety
safety check --json

# فحص إعدادات Django
python manage.py check --deploy
```

## سجل الثغرات الأمنية

### الإصدار 1.0.0
- لا توجد ثغرات أمنية معروفة

## تحديثات الأمان

### كيفية تطبيق تحديثات الأمان

1. **سحب التحديثات**
   ```bash
   git pull origin main
   ```

2. **تحديث التبعيات**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

3. **تطبيق الترحيلات**
   ```bash
   python manage.py migrate
   ```

4. **إعادة تشغيل الخادم**
   ```bash
   sudo systemctl restart gunicorn
   sudo systemctl restart nginx
   ```

## موارد إضافية

- [Django Security](https://docs.djangoproject.com/en/stable/topics/security/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Python Security](https://python-security.readthedocs.io/)

## شكراً لك

شكراً لمساهمتك في جعل ELBassa أكثر أماناً! مساعدتك في اكتشاف وإصلاح الثغرات الأمنية مهمة جداً لنا ولجميع مستخدمي النظام. 