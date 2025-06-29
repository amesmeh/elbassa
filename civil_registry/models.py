from django.db import models
from django.core.validators import RegexValidator
from datetime import date

class CivilRegistry(models.Model):
    """نموذج السجل المدني"""
    
    GENDER_CHOICES = [
        ('ذكر', 'ذكر'),
        ('أنثى', 'أنثى'),
    ]
    
    GOVERNORATE_CHOICES = [
        ('gaza', 'غزة'),
        ('north_gaza', 'شمال غزة'),
        ('middle_area', 'الوسطى'),
        ('khan_younis', 'خان يونس'),
        ('rafah', 'رفح'),
        ('west_bank', 'الضفة الغربية'),
        ('jerusalem', 'القدس'),
        ('other', 'أخرى'),
    ]
    
    # البيانات الأساسية
    name = models.CharField(
        max_length=100,
        verbose_name="الاسم",
        help_text="أدخل الاسم الرباعي"
    )
    national_id = models.CharField(
        max_length=9,
        unique=True,
        verbose_name="رقم الهوية",
        validators=[RegexValidator(
            regex=r'^\d{9}$',
            message='رقم الهوية يجب أن يكون 9 أرقام'
        )],
        help_text="أدخل رقم الهوية (9 أرقام)"
    )
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        verbose_name="الجنس"
    )
    birth_date = models.DateField(
        verbose_name="تاريخ الميلاد"
    )
    
    # بيانات الموقع
    governorate = models.CharField(
        max_length=20,
        choices=GOVERNORATE_CHOICES,
        verbose_name="المحافظة"
    )
    city = models.CharField(
        max_length=50,
        verbose_name="المدينة"
    )
    neighborhood = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="الحي"
    )
    address = models.TextField(
        blank=True,
        null=True,
        verbose_name="العنوان التفصيلي"
    )
    
    # ملاحظات
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name="ملاحظات"
    )
    
    # تواريخ النظام
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاريخ التحديث")
    
    class Meta:
        verbose_name = "سجل مدني"
        verbose_name_plural = "السجل المدني"
        ordering = ['name']
        indexes = [
            models.Index(fields=['national_id']),
            models.Index(fields=['name']),
            models.Index(fields=['governorate']),
        ]
    
    @property
    def age(self):
        """حساب العمر تلقائياً حسب تاريخ الميلاد"""
        if self.birth_date:
            today = date.today()
            return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        return None
    
    @property
    def age_category(self):
        """تصنيف العمر"""
        age = self.age
        if age is None:
            return 'غير محدد'
        elif age < 18:
            return 'قاصر'
        elif age < 60:
            return 'بالغ'
        else:
            return 'كبير السن'
    
    @property
    def birth_year(self):
        """سنة الميلاد"""
        return self.birth_date.year if self.birth_date else None
    
    def __str__(self):
        return f"{self.name} - {self.national_id}"
    
    def clean(self):
        """التحقق من صحة البيانات"""
        from django.core.exceptions import ValidationError
        
        # التحقق من تاريخ الميلاد
        if self.birth_date and self.birth_date > date.today():
            raise ValidationError('تاريخ الميلاد لا يمكن أن يكون في المستقبل')
