from django.db import models
from django.core.validators import RegexValidator
from basic_data.models import District

class Martyr(models.Model):
    """نموذج الشهداء"""
    
    RELATIONSHIP_CHOICES = [
        ('father', 'والد'),
        ('mother', 'والدة'),
        ('brother', 'أخ'),
        ('sister', 'أخت'),
        ('son', 'ابن'),
        ('daughter', 'ابنة'),
        ('uncle', 'عم'),
        ('aunt', 'عمة'),
        ('cousin', 'ابن عم'),
        ('other', 'أخرى'),
    ]
    
    # بيانات الشهيد
    name = models.CharField(
        max_length=100,
        verbose_name="اسم الشهيد",
        help_text="أدخل الاسم الرباعي للشهيد"
    )
    national_id = models.CharField(
        max_length=9,
        unique=True,
        verbose_name="رقم هوية الشهيد",
        validators=[RegexValidator(
            regex=r'^\d{9}$',
            message='رقم الهوية يجب أن يكون 9 أرقام'
        )],
        help_text="أدخل رقم الهوية (9 أرقام)"
    )
    martyrdom_date = models.DateField(
        blank=True,
        null=True,
        verbose_name="تاريخ الاستشهاد"
    )
    
    # بيانات الوكيل
    agent_name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="وكيل الشهيد",
        help_text="اسم الشخص المسؤول عن شؤون الشهيد"
    )
    agent_national_id = models.CharField(
        max_length=9,
        blank=True,
        null=True,
        verbose_name="رقم هوية الوكيل",
        validators=[RegexValidator(
            regex=r'^\d{9}$',
            message='رقم الهوية يجب أن يكون 9 أرقام'
        )],
        help_text="أدخل رقم هوية الوكيل (9 أرقام)"
    )
    agent_phone = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        verbose_name="رقم جوال الوكيل",
        validators=[RegexValidator(
            regex=r'^(\+970|0)?5[0-9]{8}$',
            message='رقم الجوال غير صحيح'
        )],
        help_text="مثال: 0599123456"
    )
    relationship_to_martyr = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="صلة القرابة بالشهيد",
        help_text="مثل: والد، أخ، ابن، عم..."
    )
    
    # الموقع
    district = models.ForeignKey(
        District,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="الحي"
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
        verbose_name = "شهيد"
        verbose_name_plural = "الشهداء"
        ordering = ['-martyrdom_date', 'name']
    
    def __str__(self):
        return f"{self.name} - {self.national_id}"
    
    @property
    def martyrdom_year(self):
        """إرجاع سنة الاستشهاد"""
        return self.martyrdom_date.year if self.martyrdom_date else None
