from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User

class District(models.Model):
    """نموذج المناطق والأحياء"""
    name = models.CharField(
        max_length=100, 
        verbose_name="اسم الحي",
        help_text="أدخل اسم الحي"
    )
    representative_name = models.CharField(
        max_length=100, 
        verbose_name="اسم مندوب الحي",
        help_text="أدخل اسم مندوب الحي"
    )
    representative_phone = models.CharField(
        max_length=15,
        verbose_name="رقم جوال مندوب الحي",
        validators=[RegexValidator(
            regex=r'^(\+970|0)?5[0-9]{8}$',
            message='رقم الجوال غير صحيح'
        )],
        help_text="أدخل رقم جوال مندوب الحي (مثال: 0599123456)",
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاريخ التحديث")

    class Meta:
        verbose_name = "حي"
        verbose_name_plural = "المناطق والأحياء"
        ordering = ['name']

    def __str__(self):
        return self.name


class Representative(models.Model):
    """نموذج مندوبي الأحياء"""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name="المستخدم"
    )
    district = models.ForeignKey(
        District,
        on_delete=models.CASCADE,
        verbose_name="الحي"
    )
    phone_number = models.CharField(
        max_length=15,
        verbose_name="رقم الجوال",
        validators=[RegexValidator(
            regex=r'^(\+970|0)?5[0-9]{8}$',
            message='رقم الجوال غير صحيح'
        )],
        help_text="مثال: 0599123456"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="نشط"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاريخ التحديث")

    class Meta:
        verbose_name = "مندوب"
        verbose_name_plural = "المندوبين"
        ordering = ['user__username']

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.district.name}"


class Guardian(models.Model):
    """نموذج أولياء الأمور"""
    GENDER_CHOICES = [
        ('ذكر', 'ذكر'),
        ('أنثى', 'أنثى'),
    ]
    
    MARITAL_STATUS_CHOICES = [
        ('متزوج', 'متزوج'),
        ('أرمل', 'أرمل'),
        ('مطلق', 'مطلق'),
        ('أعزب', 'أعزب'),
    ]
    
    RESIDENCE_STATUS_CHOICES = [
        ('نازح', 'نازح'),
        ('مقيم', 'مقيم'),
    ]
    
    HOUSING_TYPE_CHOICES = [
        ('ملك', 'ملك'),
        ('إيجار', 'إيجار'),
        ('مع الأهل', 'مع الأهل'),
        ('أخرى', 'أخرى'),
    ]

    # البيانات الأساسية
    name = models.CharField(
        max_length=100, 
        verbose_name="اسم ولي الأمر",
        help_text="أدخل الاسم الرباعي"
    )
    national_id = models.CharField(
        max_length=9,
        unique=True,
        verbose_name="رقم هوية ولي الأمر",
        validators=[RegexValidator(
            regex=r'^\d{9}$',
            message='رقم الهوية يجب أن يكون 9 أرقام'
        )],
        help_text="أدخل رقم الهوية (9 أرقام)"
    )
    current_job = models.CharField(
        max_length=100, 
        verbose_name="الوظيفة الحالية",
        blank=True,
        null=True
    )
    phone_number = models.CharField(
        max_length=15,
        verbose_name="رقم الجوال",
        validators=[RegexValidator(
            regex=r'^(\+970|0)?5[0-9]{8}$',
            message='رقم الجوال غير صحيح'
        )],
        help_text="مثال: 0599123456"
    )
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        verbose_name="الجنس"
    )
    
    # البيانات العائلية
    children_count = models.PositiveIntegerField(
        default=0,
        verbose_name="عدد الأبناء"
    )
    marital_status = models.CharField(
        max_length=20,
        choices=MARITAL_STATUS_CHOICES,
        verbose_name="الحالة الاجتماعية"
    )
    wives_count = models.PositiveIntegerField(
        default=0,
        verbose_name="عدد الزوجات"
    )
    family_members_count = models.PositiveIntegerField(
        default=1,
        verbose_name="عدد أفراد العائلة",
        help_text="يحسب تلقائياً"
    )
    
    # حالة الإقامة
    residence_status = models.CharField(
        max_length=20,
        choices=RESIDENCE_STATUS_CHOICES,
        verbose_name="حالة الإقامة"
    )
    original_governorate = models.CharField(
        max_length=50,
        verbose_name="المحافظة الأصلية",
        blank=True,
        null=True
    )
    original_city = models.CharField(
        max_length=50,
        verbose_name="المدينة",
        blank=True,
        null=True
    )
    displacement_address = models.TextField(
        verbose_name="عنوان النزوح",
        blank=True,
        null=True
    )
    
    # العنوان والسكن
    district = models.ForeignKey(
        District,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="الحي"
    )
    housing_type = models.CharField(
        max_length=20,
        choices=HOUSING_TYPE_CHOICES,
        verbose_name="نوع السكن",
        blank=True,
        null=True
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاريخ التحديث")

    class Meta:
        verbose_name = "ولي أمر"
        verbose_name_plural = "أولياء الأمور"
        ordering = ['name']

    def save(self, *args, **kwargs):
        # حساب عدد أفراد العائلة تلقائياً
        self.family_members_count = 1 + self.children_count + self.wives_count
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.national_id}"
    
    @property
    def assistance_count(self):
        """عدد المساعدات المستلمة"""
        return self.assistance_set.count()
    
    @property
    def last_assistance_date(self):
        """تاريخ آخر مساعدة"""
        last_assistance = self.assistance_set.order_by('-date').first()
        return last_assistance.date if last_assistance else None
    
    @property
    def assistance_records(self):
        """سجل المساعدات"""
        return self.assistance_set.all()
    
    @property
    def assistance_types_received(self):
        """أنواع المساعدات المستلمة"""
        return self.assistance_set.values_list('assistance_type', flat=True).distinct()


class Wife(models.Model):
    """نموذج الزوجات"""
    guardian = models.ForeignKey(
        Guardian,
        on_delete=models.CASCADE,
        related_name='wives',
        verbose_name="ولي الأمر"
    )
    name = models.CharField(
        max_length=100,
        verbose_name="اسم الزوجة"
    )
    national_id = models.CharField(
        max_length=9,
        verbose_name="رقم هوية الزوجة",
        validators=[RegexValidator(
            regex=r'^\d{9}$',
            message='رقم الهوية يجب أن يكون 9 أرقام'
        )],
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")

    class Meta:
        verbose_name = "زوجة"
        verbose_name_plural = "الزوجات"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} - {self.guardian.name}"


class Child(models.Model):
    """نموذج الأبناء"""
    guardian = models.ForeignKey(
        Guardian,
        on_delete=models.CASCADE,
        related_name='children',
        verbose_name="ولي الأمر"
    )
    name = models.CharField(
        max_length=100,
        verbose_name="اسم الابن/الابنة"
    )
    national_id = models.CharField(
        max_length=9,
        verbose_name="رقم الهوية",
        validators=[RegexValidator(
            regex=r'^\d{9}$',
            message='رقم الهوية يجب أن يكون 9 أرقام'
        )],
        blank=True,
        null=True,
        unique=True
    )
    birth_date = models.DateField(
        verbose_name="تاريخ الميلاد"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")

    class Meta:
        verbose_name = "ابن/ابنة"
        verbose_name_plural = "الأبناء"
        ordering = ['name']

    @property
    def age(self):
        """حساب العمر"""
        from datetime import date
        today = date.today()
        return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))

    def __str__(self):
        return f"{self.name} - {self.guardian.name}"
