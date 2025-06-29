# دليل نشر المشروع

## النشر على GitHub

### الخطوات الأساسية

1. **إنشاء مستودع جديد على GitHub**
   - اذهب إلى [GitHub](https://github.com)
   - انقر على "New repository"
   - اختر اسم المستودع: `ELBassa`
   - اختر "Public" أو "Private"
   - لا تضع علامة على "Initialize this repository with a README"

2. **إعداد Git محلياً** (إذا لم يكن Git مثبتاً)
   ```bash
   # تثبيت Git على Windows
   winget install Git.Git
   # أو
   choco install git -y
   ```

3. **تهيئة Git في المشروع**
   ```bash
   cd R:\Python\ELBassa
   git init
   git config user.name "Your Name"
   git config user.email "your.email@example.com"
   ```

4. **إضافة الملفات إلى Git**
   ```bash
   git add .
   git commit -m "Initial commit: نظام إدارة المساعدات ELBassa"
   ```

5. **ربط المستودع المحلي بـ GitHub**
   ```bash
   git remote add origin https://github.com/your-username/ELBassa.git
   git branch -M main
   git push -u origin main
   ```

### استبعاد الملفات الحساسة

تأكد من أن الملفات التالية مستبعدة من Git:
- `db.sqlite3` (قاعدة البيانات)
- `local_settings.py` (إعدادات محلية)
- ملفات `.env` (متغيرات البيئة)
- مجلد `media/` (الملفات المرفوعة)
- مجلد `staticfiles/` (الملفات الثابتة المجمعة)

## النشر على الخوادم

### النشر على Heroku

1. **إنشاء حساب على Heroku**
2. **تثبيت Heroku CLI**
3. **إنشاء ملف `Procfile`**
   ```
   web: gunicorn mosa3adat_project.wsgi --log-file -
   ```
4. **إضافة `gunicorn` إلى requirements.txt**
   ```
   gunicorn==21.2.0
   ```
5. **نشر التطبيق**
   ```bash
   heroku create elbassa-app
   git push heroku main
   ```

### النشر على VPS

1. **إعداد الخادم**
   ```bash
   # تثبيت Python و Nginx
   sudo apt update
   sudo apt install python3 python3-pip nginx
   ```

2. **نسخ المشروع**
   ```bash
   git clone https://github.com/your-username/ELBassa.git
   cd ELBassa
   ```

3. **إعداد البيئة الافتراضية**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. **إعداد قاعدة البيانات**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py collectstatic
   ```

5. **إعداد Gunicorn**
   ```bash
   pip install gunicorn
   gunicorn --bind 0.0.0.0:8000 mosa3adat_project.wsgi
   ```

6. **إعداد Nginx**
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location /static/ {
           alias /path/to/ELBassa/staticfiles/;
       }

       location /media/ {
           alias /path/to/ELBassa/media/;
       }

       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

## إعدادات الإنتاج

### ملف الإعدادات للإنتاج

أنشئ ملف `production_settings.py`:

```python
from .settings import *

DEBUG = False
ALLOWED_HOSTS = ['your-domain.com', 'www.your-domain.com']

# قاعدة بيانات PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'elbassa_db',
        'USER': 'elbassa_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# إعدادات الأمان
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# إعدادات الجلسات
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

### متغيرات البيئة

أنشئ ملف `.env`:

```env
SECRET_KEY=your-secret-key-here
DEBUG=False
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
```

## النسخ الاحتياطي

### نسخ احتياطي لقاعدة البيانات

```bash
# نسخ احتياطي يومي
python manage.py dumpdata > backup_$(date +%Y%m%d).json

# استعادة النسخة الاحتياطية
python manage.py loaddata backup_20250101.json
```

### نسخ احتياطي للملفات

```bash
# نسخ مجلد media
tar -czf media_backup_$(date +%Y%m%d).tar.gz media/

# نسخ مجلد staticfiles
tar -czf static_backup_$(date +%Y%m%d).tar.gz staticfiles/
```

## المراقبة والصيانة

### مراقبة الأداء

```bash
# مراقبة استخدام الذاكرة
htop

# مراقبة سجلات Nginx
tail -f /var/log/nginx/access.log

# مراقبة سجلات Django
tail -f /var/log/django/error.log
```

### تحديث التطبيق

```bash
# سحب التحديثات
git pull origin main

# تثبيت المتطلبات الجديدة
pip install -r requirements.txt

# تطبيق الترحيلات
python manage.py migrate

# جمع الملفات الثابتة
python manage.py collectstatic

# إعادة تشغيل الخادم
sudo systemctl restart gunicorn
sudo systemctl restart nginx
```

## الأمان

### إعدادات الأمان الأساسية

1. **تغيير SECRET_KEY**
2. **إعداد HTTPS**
3. **تحديث Django بانتظام**
4. **مراقبة سجلات الأمان**
5. **نسخ احتياطي منتظم**

### فحص الأمان

```bash
# فحص الثغرات الأمنية
pip install safety
safety check

# فحص التبعيات
pip install bandit
bandit -r .
``` 