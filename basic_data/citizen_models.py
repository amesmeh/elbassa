from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import transaction
from .models import District, Guardian, Child, Wife


class CitizenRegistrationRequest(models.Model):
    """طلب تسجيل مواطن جديد"""
    
    STATUS_CHOICES = [
        ('pending', 'في الانتظار'),
        ('approved', 'مقبول'),
        ('rejected', 'مرفوض'),
    ]
    
    GENDER_CHOICES = [
        ('ذكر', 'ذكر'),
        ('أنثى', 'أنثى'),
    ]
    
    MARITAL_STATUS_CHOICES = [
        ('أعزب', 'أعزب'),
        ('متزوج', 'متزوج'),
        ('مطلق', 'مطلق'),
        ('أرمل', 'أرمل'),
    ]
    
    RESIDENCE_STATUS_CHOICES = [
        ('مقيم', 'مقيم'),
        ('نازح', 'نازح'),
        ('لاجئ', 'لاجئ'),
    ]
    
    HOUSING_TYPE_CHOICES = [
        ('ملك', 'ملك'),
        ('إيجار', 'إيجار'),
        ('مستأجر', 'مستأجر'),
        ('مع أقارب', 'مع أقارب'),
        ('مخيم', 'مخيم'),
        ('خيمة', 'خيمة'),
        ('مدرسة', 'مدرسة'),
        ('مستشفى', 'مستشفى'),
        ('مسجد', 'مسجد'),
        ('مخزن', 'مخزن'),
        ('سيارة', 'سيارة'),
        ('شارع', 'شارع'),
        ('آخر', 'آخر'),
    ]
    
    # البيانات الأساسية
    name = models.CharField(max_length=100, verbose_name="الاسم الكامل")
    national_id = models.CharField(max_length=9, unique=True, verbose_name="رقم الهوية")
    phone_number = models.CharField(max_length=15, verbose_name="رقم الجوال")
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, verbose_name="الجنس")
    current_job = models.CharField(max_length=100, blank=True, null=True, verbose_name="المهنة الحالية")
    
    # البيانات العائلية
    children_count = models.PositiveIntegerField(default=0, verbose_name="عدد الأطفال")
    marital_status = models.CharField(max_length=20, choices=MARITAL_STATUS_CHOICES, verbose_name="الحالة الاجتماعية")
    wives_count = models.PositiveIntegerField(default=0, verbose_name="عدد الزوجات")
    
    # بيانات الإقامة
    residence_status = models.CharField(max_length=20, choices=RESIDENCE_STATUS_CHOICES, verbose_name="حالة الإقامة")
    original_governorate = models.CharField(max_length=50, blank=True, null=True, verbose_name="المحافظة الأصلية")
    original_city = models.CharField(max_length=50, blank=True, null=True, verbose_name="المدينة الأصلية")
    displacement_address = models.TextField(blank=True, null=True, verbose_name="عنوان النزوح")
    
    # العنوان والسكن
    district = models.ForeignKey('District', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="الحي")
    housing_type = models.CharField(max_length=20, choices=HOUSING_TYPE_CHOICES, blank=True, null=True, verbose_name="نوع السكن")
    
    # حالة الطلب
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="حالة الطلب")
    admin_notes = models.TextField(blank=True, null=True, verbose_name="ملاحظات الإدارة")
    
    # معلومات النظام
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الطلب")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاريخ التحديث")
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="تم القبول بواسطة")
    approved_at = models.DateTimeField(null=True, blank=True, verbose_name="تاريخ القبول")
    rejected_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='rejected_requests', verbose_name="تم الرفض بواسطة")
    rejected_at = models.DateTimeField(null=True, blank=True, verbose_name="تاريخ الرفض")
    
    class Meta:
        verbose_name = "طلب تسجيل مواطن"
        verbose_name_plural = "طلبات تسجيل المواطنين"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.national_id}"
    
    @transaction.atomic
    def approve(self, user):
        """قبول الطلب وإنشاء ولي الأمر"""
        if self.status != 'pending':
            raise ValueError('لا يمكن قبول طلب غير في حالة الانتظار')
        
        # إنشاء ولي الأمر
        guardian = Guardian.objects.create(
            name=self.name,
            national_id=self.national_id,
            phone_number=self.phone_number,
            gender=self.gender,
            current_job=self.current_job,
            children_count=self.children_count,
            marital_status=self.marital_status,
            wives_count=self.wives_count,
            residence_status=self.residence_status,
            original_governorate=self.original_governorate,
            original_city=self.original_city,
            displacement_address=self.displacement_address,
            district=self.district,
            housing_type=self.housing_type,
        )
        
        # إنشاء الأطفال
        for child_request in self.children.all():
            Child.objects.create(
                guardian=guardian,
                name=child_request.name,
                national_id=child_request.national_id,
                birth_date=child_request.birth_date,
            )
        
        # إنشاء الزوجات
        for wife_request in self.wives.all():
            Wife.objects.create(
                guardian=guardian,
                name=wife_request.name,
                national_id=wife_request.national_id,
            )
        
        # تحديث حالة الطلب
        self.status = 'approved'
        self.approved_by = user
        self.approved_at = timezone.now()
        self.save()
        
        return guardian
    
    def reject(self, user, notes=''):
        """رفض الطلب"""
        if self.status != 'pending':
            raise ValueError('لا يمكن رفض طلب غير في حالة الانتظار')
        
        self.status = 'rejected'
        self.admin_notes = notes
        self.rejected_by = user
        self.rejected_at = timezone.now()
        self.save()


class CitizenRequestChild(models.Model):
    """طفل في طلب التسجيل"""
    
    request = models.ForeignKey(CitizenRegistrationRequest, on_delete=models.CASCADE, related_name='children', verbose_name="طلب التسجيل")
    name = models.CharField(max_length=100, verbose_name="اسم الطفل")
    national_id = models.CharField(max_length=9, blank=True, null=True, verbose_name="رقم الهوية")
    birth_date = models.DateField(verbose_name="تاريخ الميلاد")
    
    class Meta:
        verbose_name = "طفل في طلب التسجيل"
        verbose_name_plural = "أطفال في طلبات التسجيل"
    
    def __str__(self):
        return f"{self.name} - {self.request.name}"
    
    @property
    def age(self):
        """حساب العمر"""
        from datetime import date
        today = date.today()
        return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))


class CitizenRequestWife(models.Model):
    """زوجة في طلب التسجيل"""
    
    request = models.ForeignKey(CitizenRegistrationRequest, on_delete=models.CASCADE, related_name='wives', verbose_name="طلب التسجيل")
    name = models.CharField(max_length=100, verbose_name="اسم الزوجة")
    national_id = models.CharField(max_length=9, blank=True, null=True, verbose_name="رقم الهوية")
    
    class Meta:
        verbose_name = "زوجة في طلب التسجيل"
        verbose_name_plural = "زوجات في طلبات التسجيل"
    
    def __str__(self):
        return f"{self.name} - {self.request.name}" 