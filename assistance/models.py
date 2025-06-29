from django.db import models
from django.utils import timezone
from basic_data.models import Guardian

class Assistance(models.Model):
    """نموذج المساعدات"""
    
    # أنواع المساعدات
    ASSISTANCE_TYPES = [
        ('food', 'مساعدات غذائية'),
        ('money', 'مساعدات مالية'),
        ('medical', 'مساعدات طبية'),
        ('clothes', 'مساعدات كسوة'),
        ('shelter', 'مساعدات سكن'),
        ('education', 'مساعدات تعليمية'),
        ('fuel', 'مساعدات وقود'),
        ('blankets', 'أغطية ومفارش'),
        ('hygiene', 'مواد نظافة'),
        ('baby_supplies', 'مستلزمات أطفال'),
        ('emergency', 'مساعدات طوارئ'),
        ('other', 'أخرى'),
    ]
    
    # البيانات الأساسية
    national_id = models.CharField(
        max_length=9,
        verbose_name='رقم الهوية',
        help_text='رقم هوية المستفيد (يقبل التكرار)'
    )
    
    beneficiary_name = models.CharField(
        max_length=200,
        verbose_name='اسم المستفيد',
        help_text='يتم ملؤه تلقائياً من قاعدة البيانات أو يُدخل يدوياً'
    )
    
    # ربط مع ولي الأمر (اختياري - قد يكون المستفيد غير مسجل)
    guardian = models.ForeignKey(
        Guardian,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assistance_records',
        verbose_name='ولي الأمر'
    )
    
    # بيانات المساعدة
    assistance_type = models.CharField(
        max_length=100,
        verbose_name='نوع المساعدة',
        help_text='نوع المساعدة (يمكن الكتابة بحرية)'
    )
    
    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='الكمية',
        help_text='الكمية أو المبلغ'
    )
    
    assistance_date = models.DateField(
        default=timezone.now,
        verbose_name='تاريخ المساعدة'
    )
    
    # بيانات إضافية
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name='ملاحظات'
    )
    
    # بيانات تتبع النظام
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاريخ الإنشاء'
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='تاريخ التحديث'
    )
    
    # البيانات من ولي الأمر (للبحث والفلترة)
    district_name = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name='الحي',
        help_text='يتم نسخه من بيانات ولي الأمر'
    )
    
    family_members_count = models.PositiveIntegerField(
        default=0,
        verbose_name='عدد أفراد العائلة',
        help_text='يتم نسخه من بيانات ولي الأمر'
    )
    
    def __str__(self):
        return f'{self.beneficiary_name} - {self.get_assistance_type_display()} ({self.assistance_date})'
    
    def save(self, *args, **kwargs):
        """حفظ البيانات مع تحديث البيانات من ولي الأمر"""
        # البحث عن ولي الأمر برقم الهوية إذا لم يتم ربطه مسبقاً
        if not self.guardian and self.national_id:
            try:
                guardian = Guardian.objects.get(national_id=self.national_id)
                self.guardian = guardian
                self.beneficiary_name = guardian.name
            except Guardian.DoesNotExist:
                # إذا لم يوجد ولي الأمر، نحتفظ بالاسم المُدخل يدوياً
                pass
        
        # نسخ البيانات من ولي الأمر
        if self.guardian:
            self.beneficiary_name = self.guardian.name
            self.district_name = self.guardian.district.name if self.guardian.district else ''
            self.family_members_count = self.guardian.family_members_count
        
        super().save(*args, **kwargs)
    
    @property
    def beneficiary_total_assistance_count(self):
        """إجمالي عدد مرات الاستفادة لهذا المستفيد"""
        return Assistance.objects.filter(national_id=self.national_id).count()
    
    @property
    def beneficiary_last_assistance_date(self):
        """آخر تاريخ استفادة لهذا المستفيد"""
        latest = Assistance.objects.filter(
            national_id=self.national_id
        ).order_by('-assistance_date').first()
        return latest.assistance_date if latest else None
    
    @classmethod
    def get_beneficiary_history(cls, national_id):
        """الحصول على تاريخ الاستفادة للمستفيد"""
        return cls.objects.filter(
            national_id=national_id
        ).order_by('assistance_date')

    class Meta:
        verbose_name = 'مساعدة'
        verbose_name_plural = 'المساعدات'
        ordering = ['-assistance_date', '-created_at']
        db_table = 'assistance'
