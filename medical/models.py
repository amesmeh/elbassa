from django.db import models
from django.core.validators import RegexValidator
from basic_data.models import Guardian, District

class MedicalRecord(models.Model):
    """نموذج البيانات المرضية"""
    
    GENDER_CHOICES = [
        ('M', 'ذكر'),
        ('F', 'أنثى'),
    ]
    
    DISEASE_TYPE_CHOICES = [
        ('chronic', 'مرض مزمن'),
        ('mental', 'مرض نفسي'),
        ('physical', 'مرض جسدي'),
        ('genetic', 'مرض وراثي'),
        ('cancer', 'سرطان'),
        ('diabetes', 'سكري'),
        ('heart', 'أمراض القلب'),
        ('kidney', 'أمراض الكلى'),
        ('other', 'أخرى'),
    ]
    
    DISABILITY_TYPE_CHOICES = [
        ('physical', 'إعاقة جسدية'),
        ('mental', 'إعاقة ذهنية'),
        ('visual', 'إعاقة بصرية'),
        ('hearing', 'إعاقة سمعية'),
        ('speech', 'إعاقة في النطق'),
        ('multiple', 'إعاقة متعددة'),
        ('none', 'لا توجد إعاقة'),
    ]
    
    # بيانات المريض
    name = models.CharField(
        max_length=100,
        verbose_name="اسم المريض",
        help_text="أدخل الاسم الرباعي للمريض"
    )
    national_id = models.CharField(
        max_length=9,
        unique=True,
        verbose_name="رقم هوية المريض",
        validators=[RegexValidator(
            regex=r'^\d{9}$',
            message='رقم الهوية يجب أن يكون 9 أرقام'
        )],
        help_text="أدخل رقم الهوية (9 أرقام)"
    )
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        verbose_name="الجنس"
    )
    
    # بيانات ولي الأمر (علاقة مع البيانات الأساسية)
    guardian_national_id = models.CharField(
        max_length=9,
        verbose_name="رقم هوية ولي الأمر",
        validators=[RegexValidator(
            regex=r'^\d{9}$',
            message='رقم الهوية يجب أن يكون 9 أرقام'
        )],
        help_text="أدخل رقم هوية ولي الأمر (9 أرقام)"
    )
    guardian = models.ForeignKey(
        Guardian,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="ولي الأمر",
        help_text="سيتم ملؤه تلقائياً عند إدخال رقم الهوية"
    )
    guardian_name = models.CharField(
        max_length=100,
        verbose_name="اسم ولي الأمر",
        blank=True,
        help_text="يعبأ تلقائياً من البيانات الأساسية"
    )
    phone_number = models.CharField(
        max_length=15,
        verbose_name="رقم الجوال",
        validators=[RegexValidator(
            regex=r'^(\+970|0)?5[0-9]{8}$',
            message='رقم الجوال غير صحيح'
        )],
        help_text="يقرأ من البيانات الأساسية أو يكتب يدوياً"
    )
    
    # البيانات المرضية
    disease_type = models.CharField(
        max_length=20,
        choices=DISEASE_TYPE_CHOICES,
        verbose_name="نوع المرض"
    )
    disease_description = models.TextField(
        blank=True,
        null=True,
        verbose_name="وصف المرض",
        help_text="تفاصيل إضافية عن المرض"
    )
    
    # بيانات الإعاقة
    disability_type = models.CharField(
        max_length=20,
        choices=DISABILITY_TYPE_CHOICES,
        default='none',
        verbose_name="نوع الإعاقة"
    )
    disability_percentage = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="نسبة الإعاقة (%)",
        help_text="أدخل النسبة من 0 إلى 100"
    )
    
    # الموقع (يقرأ تلقائياً من البيانات الأساسية)
    district = models.ForeignKey(
        District,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="الحي",
        help_text="يقرأ تلقائياً من البيانات الأساسية"
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
        verbose_name = "سجل مرضي"
        verbose_name_plural = "البيانات المرضية"
        ordering = ['name']
    
    def save(self, *args, **kwargs):
        """ملء البيانات تلقائياً من جدول البيانات الأساسية"""
        if self.guardian_national_id:
            try:
                guardian = Guardian.objects.get(national_id=self.guardian_national_id)
                self.guardian = guardian
                self.guardian_name = guardian.name
                if not self.phone_number and guardian.phone_number:
                    self.phone_number = guardian.phone_number
                if not self.district and guardian.district:
                    self.district = guardian.district
            except Guardian.DoesNotExist:
                pass
        super().save(*args, **kwargs)
    
    def clean(self):
        """التحقق من صحة البيانات"""
        from django.core.exceptions import ValidationError
        if self.disability_percentage is not None:
            if self.disability_percentage < 0 or self.disability_percentage > 100:
                raise ValidationError('نسبة الإعاقة يجب أن تكون بين 0 و 100')
    
    def __str__(self):
        return f"{self.name} - {self.national_id}"
    
    @property
    def has_disability(self):
        """التحقق من وجود إعاقة"""
        return self.disability_type != 'none'
