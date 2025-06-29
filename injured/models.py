from django.db import models
from django.core.validators import RegexValidator
from basic_data.models import Guardian, District

class Injured(models.Model):
    """نموذج الجرحى"""
    
    INJURY_TYPE_CHOICES = [
        ('gunshot', 'إصابة بالرصاص'),
        ('shrapnel', 'إصابة بالشظايا'),
        ('explosion', 'إصابة بالانفجار'),
        ('burn', 'حروق'),
        ('fracture', 'كسور'),
        ('amputation', 'بتر'),
        ('other', 'أخرى'),
    ]
    
    # بيانات الجريح
    name = models.CharField(
        max_length=100,
        verbose_name="اسم الجريح",
        help_text="أدخل الاسم الرباعي للجريح"
    )
    national_id = models.CharField(
        max_length=9,
        unique=True,
        verbose_name="رقم هوية الجريح",
        validators=[RegexValidator(
            regex=r'^\d{9}$',
            message='رقم الهوية يجب أن يكون 9 أرقام'
        )],
        help_text="أدخل رقم الهوية (9 أرقام)"
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
    
    # بيانات الإصابة
    injury_date = models.DateField(
        verbose_name="تاريخ الإصابة"
    )
    injury_type = models.CharField(
        max_length=20,
        choices=INJURY_TYPE_CHOICES,
        verbose_name="نوع الإصابة"
    )
    injury_description = models.TextField(
        blank=True,
        null=True,
        verbose_name="وصف الإصابة",
        help_text="تفاصيل إضافية عن الإصابة"
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
        verbose_name = "جريح"
        verbose_name_plural = "الجرحى"
        ordering = ['-injury_date', 'name']
    
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
    
    def __str__(self):
        return f"{self.name} - {self.national_id}"
    
    @property
    def injury_year(self):
        """إرجاع سنة الإصابة"""
        return self.injury_date.year if self.injury_date else None
