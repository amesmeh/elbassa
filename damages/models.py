from django.db import models
from django.core.validators import RegexValidator
from basic_data.models import Guardian, District

class Damage(models.Model):
    """نموذج الأضرار"""
    
    OWNERSHIP_CHOICES = [
        ('owned', 'ملك'),
        ('rented', 'إيجار'),
    ]
    
    HOUSING_TYPE_CHOICES = [
        ('apartment', 'شقة'),
        ('house', 'بيت'),
        ('villa', 'فيلا'),
        ('room', 'غرفة'),
        ('shop', 'محل تجاري'),
        ('warehouse', 'مستودع'),
        ('other', 'أخرى'),
    ]
    
    HOUSING_CONDITION_CHOICES = [
        ('excellent', 'ممتازة'),
        ('good', 'جيدة'),
        ('fair', 'متوسطة'),
        ('poor', 'سيئة'),
        ('destroyed', 'مدمرة'),
    ]
    
    CONSTRUCTION_TYPE_CHOICES = [
        ('concrete', 'باطون'),
        ('asbestos', 'اسبست'),
        ('mixed', 'مختلط'),
    ]
    
    DAMAGE_TYPE_CHOICES = [
        ('total', 'كلي'),
        ('partial', 'جزئي'),
    ]
    
    # بيانات المالك/المستأجر (علاقة مع البيانات الأساسية)
    guardian_national_id = models.CharField(
        max_length=9,
        verbose_name="رقم الهوية",
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
        help_text="يقرأ تلقائياً من جدول البيانات الأساسية"
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
    
    # بيانات العقار
    ownership_type = models.CharField(
        max_length=10,
        choices=OWNERSHIP_CHOICES,
        verbose_name="ملك/إيجار"
    )
    housing_type = models.CharField(
        max_length=20,
        choices=HOUSING_TYPE_CHOICES,
        verbose_name="نوع الوحدة السكنية"
    )
    housing_condition = models.CharField(
        max_length=20,
        choices=HOUSING_CONDITION_CHOICES,
        verbose_name="حالة الوحدة السكنية"
    )
    construction_type = models.CharField(
        max_length=20,
        choices=CONSTRUCTION_TYPE_CHOICES,
        verbose_name="نوع البناء"
    )
    floors_count = models.PositiveIntegerField(
        verbose_name="عدد الطوابق",
        help_text="أدخل عدد الطوابق"
    )
    
    # بيانات الضرر
    damage_type = models.CharField(
        max_length=10,
        choices=DAMAGE_TYPE_CHOICES,
        verbose_name="نوع الضرر"
    )
    damage_percentage = models.PositiveIntegerField(
        verbose_name="نسبة الضرر (%)",
        help_text="أدخل النسبة من 0 إلى 100"
    )
    damage_date = models.DateField(
        verbose_name="تاريخ الضرر",
        null=True,
        blank=True
    )
    
    # التكلفة المقدرة
    estimated_cost_ils = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="التكلفة المقدرة (شيكل)",
        null=True,
        blank=True,
        help_text="أدخل التكلفة المقدرة بالشيكل"
    )
    estimated_cost_usd = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="التكلفة المقدرة (دولار)",
        null=True,
        blank=True,
        help_text="أدخل التكلفة المقدرة بالدولار"
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
        verbose_name = "ضرر"
        verbose_name_plural = "الأضرار"
        ordering = ['-damage_percentage', 'guardian_name']
    
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
        if self.damage_percentage < 0 or self.damage_percentage > 100:
            raise ValidationError('نسبة الضرر يجب أن تكون بين 0 و 100')
    
    def __str__(self):
        return f"{self.guardian_name} - {self.housing_type} - {self.damage_percentage}%"
    
    @property
    def is_total_damage(self):
        """التحقق من كون الضرر كلي"""
        return self.damage_type == 'total'
    
    @property
    def damage_severity(self):
        """تحديد شدة الضرر"""
        if self.damage_percentage >= 80:
            return 'شديد'
        elif self.damage_percentage >= 50:
            return 'متوسط'
        elif self.damage_percentage >= 20:
            return 'خفيف'
        else:
            return 'طفيف'

    @property
    def total_estimated_cost_ils(self):
        """إجمالي التكلفة المقدرة بالشيكل (مع تحويل الدولار إذا لزم)"""
        total = self.estimated_cost_ils or 0
        if self.estimated_cost_usd:
            # سعر صرف تقريبي (يمكن تحديثه)
            usd_to_ils_rate = 3.7
            total += self.estimated_cost_usd * usd_to_ils_rate
        return total
