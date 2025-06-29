from django.db import models
from django.core.validators import RegexValidator
from basic_data.models import Guardian, District
from django.utils import timezone
from decimal import Decimal
from django.db.models import Count, Max

class AidType(models.Model):
    """نموذج أنواع المساعدات"""
    CATEGORY_CHOICES = [
        ('food', 'مواد غذائية'),
        ('medical', 'مساعدات طبية'),
        ('clothing', 'ملابس'),
        ('shelter', 'مأوى'),
        ('cash', 'مساعدات نقدية'),
        ('education', 'مساعدات تعليمية'),
        ('other', 'أخرى'),
    ]
    
    UNIT_CHOICES = [
        ('kg', 'كيلوغرام'),
        ('piece', 'قطعة'),
        ('box', 'صندوق'),
        ('bag', 'كيس'),
        ('bottle', 'زجاجة'),
        ('package', 'عبوة'),
        ('liter', 'لتر'),
        ('meter', 'متر'),
        ('set', 'طقم'),
        ('unit', 'وحدة'),
    ]

    name = models.CharField(
        max_length=100,
        verbose_name="اسم نوع المساعدة",
        help_text="مثال: أرز، دقيق، دواء، ملابس"
    )
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        verbose_name="فئة المساعدة"
    )
    unit = models.CharField(
        max_length=20,
        choices=UNIT_CHOICES,
        verbose_name="وحدة القياس"
    )
    description = models.TextField(
        verbose_name="وصف المساعدة",
        blank=True,
        null=True
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="نشط"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاريخ التحديث")

    class Meta:
        verbose_name = "نوع مساعدة"
        verbose_name_plural = "أنواع المساعدات"
        ordering = ['category', 'name']

    def __str__(self):
        return f"{self.name} ({self.get_unit_display()})"


class AidBatch(models.Model):
    """نموذج دفعات المساعدات"""
    STATUS_CHOICES = [
        ('planned', 'مخطط'),
        ('in_progress', 'قيد التنفيذ'),
        ('completed', 'مكتمل'),
        ('cancelled', 'ملغي'),
    ]

    name = models.CharField(
        max_length=200,
        verbose_name="اسم الدفعة",
        help_text="مثال: دفعة رمضان 2024، مساعدات الشتاء"
    )
    description = models.TextField(
        verbose_name="وصف الدفعة",
        blank=True,
        null=True
    )
    start_date = models.DateField(
        verbose_name="تاريخ البداية"
    )
    end_date = models.DateField(
        verbose_name="تاريخ النهاية",
        blank=True,
        null=True
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='planned',
        verbose_name="حالة الدفعة"
    )
    target_districts = models.ManyToManyField(
        District,
        verbose_name="الأحياء المستهدفة",
        blank=True
    )
    total_beneficiaries = models.PositiveIntegerField(
        default=0,
        verbose_name="إجمالي المستفيدين"
    )
    notes = models.TextField(
        verbose_name="ملاحظات",
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاريخ التحديث")

    class Meta:
        verbose_name = "دفعة مساعدات"
        verbose_name_plural = "دفعات المساعدات"
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.name} - {self.start_date}"

    @property
    def is_active(self):
        """تحديد ما إذا كانت الدفعة نشطة"""
        today = timezone.now().date()
        return (self.status in ['planned', 'in_progress'] and 
                self.start_date <= today and 
                (self.end_date is None or self.end_date >= today))


class AidDistribution(models.Model):
    """نموذج التوزيع - البيانات الأولية للتوزيع"""
    guardian = models.ForeignKey(
        Guardian,
        on_delete=models.CASCADE,
        related_name='distributions',
        verbose_name="ولي الأمر"
    )
    aid_type = models.ForeignKey(
        AidType,
        on_delete=models.CASCADE,
        verbose_name="نوع المساعدة"
    )
    distribution_date = models.DateField(
        verbose_name="تاريخ المساعدة"
    )
    notes = models.TextField(
        verbose_name="ملاحظات",
        blank=True,
        null=True
    )
    is_transferred = models.BooleanField(
        default=False,
        verbose_name="تم الترحيل للمستفيدين"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاريخ التحديث")

    class Meta:
        verbose_name = "توزيع مساعدة"
        verbose_name_plural = "بيانات التوزيع"
        ordering = ['-distribution_date']

    def __str__(self):
        return f"{self.guardian.name} - {self.aid_type.name} - {self.distribution_date}"

    @property
    def guardian_name(self):
        """اسم ولي الأمر"""
        return self.guardian.name

    @property
    def guardian_phone(self):
        """رقم جوال ولي الأمر"""
        return self.guardian.phone_number

    @property
    def guardian_district(self):
        """حي ولي الأمر"""
        return self.guardian.district.name if self.guardian.district else "غير محدد"

    def transfer_to_beneficiaries(self):
        """ترحيل التوزيع إلى قائمة المستفيدين"""
        if not self.is_transferred:
            beneficiary, created = AidBeneficiary.objects.get_or_create(
                guardian=self.guardian,
                aid_type=self.aid_type,
                aid_date=self.distribution_date,
                defaults={
                    'notes': self.notes
                }
            )
            self.is_transferred = True
            self.save()
            return beneficiary
        return None


class AidBeneficiary(models.Model):
    """نموذج المستفيدين - الذين استلموا المساعدات فعلياً"""
    guardian = models.ForeignKey(
        Guardian,
        on_delete=models.CASCADE,
        related_name='aid_benefits',
        verbose_name="ولي الأمر المستفيد"
    )
    aid_type = models.ForeignKey(
        AidType,
        on_delete=models.CASCADE,
        verbose_name="نوع المساعدة"
    )
    aid_date = models.DateField(
        verbose_name="تاريخ المساعدة"
    )
    notes = models.TextField(
        verbose_name="ملاحظات",
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاريخ التحديث")

    class Meta:
        verbose_name = "مستفيد"
        verbose_name_plural = "بيانات المستفيدين"
        ordering = ['-aid_date']

    def __str__(self):
        return f"{self.guardian.name} - {self.aid_type.name} - {self.aid_date}"

    @property
    def guardian_name(self):
        """اسم ولي الأمر"""
        return self.guardian.name

    @property
    def guardian_national_id(self):
        """رقم هوية ولي الأمر"""
        return self.guardian.national_id

    @property
    def guardian_phone(self):
        """رقم جوال ولي الأمر"""
        return self.guardian.phone_number

    @property
    def guardian_district(self):
        """حي ولي الأمر"""
        return self.guardian.district.name if self.guardian.district else "غير محدد"

    @classmethod
    def get_beneficiary_stats(cls, guardian):
        """إحصائيات المستفيد"""
        benefits = cls.objects.filter(guardian=guardian)
        return {
            'total_benefits': benefits.count(),
            'last_benefit_date': benefits.aggregate(Max('aid_date'))['aid_date__max'],
            'aid_types': benefits.values('aid_type__name').distinct().count()
        }

    @classmethod
    def get_guardian_benefit_count(cls, guardian):
        """عدد مرات استفادة ولي الأمر"""
        return cls.objects.filter(guardian=guardian).count()

    @classmethod
    def get_guardian_last_benefit_date(cls, guardian):
        """آخر موعد استفادة لولي الأمر"""
        last_benefit = cls.objects.filter(guardian=guardian).order_by('-aid_date').first()
        return last_benefit.aid_date if last_benefit else None


class AidDistributionItem(models.Model):
    """نموذج أصناف التوزيع"""
    distribution = models.ForeignKey(
        AidDistribution,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name="التوزيع"
    )
    aid_type = models.ForeignKey(
        AidType,
        on_delete=models.CASCADE,
        verbose_name="نوع المساعدة"
    )
    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="الكمية"
    )
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name="سعر الوحدة",
        help_text="اختياري - للتقييم المالي"
    )
    expiry_date = models.DateField(
        verbose_name="تاريخ الانتهاء",
        blank=True,
        null=True
    )
    notes = models.TextField(
        verbose_name="ملاحظات",
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "صنف توزيع"
        verbose_name_plural = "أصناف التوزيع"
        unique_together = ['distribution', 'aid_type']

    def __str__(self):
        return f"{self.aid_type.name} - {self.quantity} {self.aid_type.get_unit_display()}"

    @property
    def total_value(self):
        """القيمة الإجمالية للصنف"""
        return self.quantity * self.unit_price

    @property
    def is_expired(self):
        """تحديد ما إذا كان الصنف منتهي الصلاحية"""
        if self.expiry_date:
            return self.expiry_date < timezone.now().date()
        return False


class AidRequest(models.Model):
    """نموذج طلبات المساعدة"""
    PRIORITY_CHOICES = [
        ('low', 'منخفضة'),
        ('medium', 'متوسطة'),
        ('high', 'عالية'),
        ('urgent', 'عاجلة'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'في الانتظار'),
        ('approved', 'موافق عليه'),
        ('rejected', 'مرفوض'),
        ('fulfilled', 'تم التنفيذ'),
    ]

    guardian = models.ForeignKey(
        Guardian,
        on_delete=models.CASCADE,
        related_name='aid_requests',
        verbose_name="ولي الأمر"
    )
    aid_type = models.ForeignKey(
        AidType,
        on_delete=models.CASCADE,
        verbose_name="نوع المساعدة المطلوبة"
    )
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='medium',
        verbose_name="الأولوية"
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="حالة الطلب"
    )
    reason = models.TextField(
        verbose_name="سبب الطلب",
        help_text="اشرح سبب الحاجة لهذه المساعدة"
    )
    request_date = models.DateTimeField(
        default=timezone.now,
        verbose_name="تاريخ الطلب"
    )
    response_date = models.DateTimeField(
        verbose_name="تاريخ الرد",
        blank=True,
        null=True
    )
    response_notes = models.TextField(
        verbose_name="ملاحظات الرد",
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاريخ التحديث")

    class Meta:
        verbose_name = "طلب مساعدة"
        verbose_name_plural = "طلبات المساعدة"
        ordering = ['-request_date']

    def __str__(self):
        return f"{self.guardian.name} - {self.aid_type.name} - {self.get_status_display()}"
