from django.db import models
from django.core.validators import RegexValidator
from basic_data.models import District
from datetime import date

class Orphan(models.Model):
    """نموذج الأيتام"""
    
    GENDER_CHOICES = [
        ('ذكر', 'ذكر'),
        ('أنثى', 'أنثى'),
    ]
    
    HEALTH_STATUS_CHOICES = [
        ('ممتازة', 'ممتازة'),
        ('جيدة', 'جيدة'),
        ('متوسطة', 'متوسطة'),
        ('سيئة', 'سيئة'),
        ('مرض مزمن', 'مرض مزمن'),
        ('إعاقة', 'إعاقة'),
        ('مصاب', 'مصاب'),
        # الخيارات الإنجليزية للتوافق مع البيانات القديمة
        ('excellent', 'ممتازة'),
        ('good', 'جيدة'),
        ('fair', 'متوسطة'),
        ('poor', 'سيئة'),
        ('chronic', 'مرض مزمن'),
        ('disabled', 'إعاقة'),
    ]
    
    EDUCATION_LEVEL_CHOICES = [
        ('روضة', 'روضة'),
        ('الصف الأول الابتدائي', 'الصف الأول الابتدائي'),
        ('الصف الثاني الابتدائي', 'الصف الثاني الابتدائي'),
        ('الصف الثالث الابتدائي', 'الصف الثالث الابتدائي'),
        ('الصف الرابع الابتدائي', 'الصف الرابع الابتدائي'),
        ('الصف الخامس الابتدائي', 'الصف الخامس الابتدائي'),
        ('الصف السادس الابتدائي', 'الصف السادس الابتدائي'),
        ('الصف السابع الأساسي', 'الصف السابع الأساسي'),
        ('الصف الثامن الأساسي', 'الصف الثامن الأساسي'),
        ('الصف التاسع الأساسي', 'الصف التاسع الأساسي'),
        ('الصف العاشر الثانوي', 'الصف العاشر الثانوي'),
        ('الصف الحادي عشر الثانوي', 'الصف الحادي عشر الثانوي'),
        ('الصف الثاني عشر الثانوي', 'الصف الثاني عشر الثانوي'),
        ('السنة الأولى جامعة', 'السنة الأولى جامعة'),
        ('السنة الثانية جامعة', 'السنة الثانية جامعة'),
        ('السنة الثالثة جامعة', 'السنة الثالثة جامعة'),
        ('السنة الرابعة جامعة', 'السنة الرابعة جامعة'),
        ('خريج جامعة', 'خريج جامعة'),
        ('دراسات عليا', 'دراسات عليا'),
        ('غير ملتحق بالتعليم', 'غير ملتحق بالتعليم'),
    ]
    
    GUARDIAN_RELATIONSHIP_CHOICES = [
        ('أم', 'أم'),
        ('عم', 'عم'),
        ('عمة', 'عمة'),
        ('خال', 'خال'),
        ('خالة', 'خالة'),
        ('جد', 'جد (من الأب)'),
        ('جدة', 'جدة (من الأب)'),
        ('جد لأم', 'جد (من الأم)'),
        ('جدة لأم', 'جدة (من الأم)'),
        ('أخ', 'أخ'),
        ('أخت', 'أخت'),
        ('ابن عم', 'ابن عم'),
        ('ابن خال', 'ابن خال'),
        ('أقارب آخرون', 'أقارب آخرون'),
        ('غير قريب', 'غير قريب'),
    ]
    

    
    # بيانات اليتيم
    name = models.CharField(
        max_length=100,
        verbose_name="اسم اليتيم",
        help_text="أدخل الاسم الرباعي لليتيم"
    )
    national_id = models.CharField(
        max_length=9,
        unique=True,
        verbose_name="رقم هوية اليتيم",
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
    health_status = models.CharField(
        max_length=20,
        choices=HEALTH_STATUS_CHOICES,
        verbose_name="الحالة الصحية"
    )
    education_level = models.CharField(
        max_length=100,
        choices=EDUCATION_LEVEL_CHOICES,
        verbose_name="المرحلة الدراسية",
        help_text="اختر المرحلة الدراسية"
    )
    
    # بيانات الشهيد/المتوفي
    deceased_national_id = models.CharField(
        max_length=9,
        verbose_name="رقم هوية الشهيد/المتوفي",
        validators=[RegexValidator(
            regex=r'^\d{9}$',
            message='رقم الهوية يجب أن يكون 9 أرقام'
        )],
        help_text="أدخل رقم هوية الشهيد/المتوفي (9 أرقام)"
    )
    deceased_name = models.CharField(
        max_length=100,
        verbose_name="اسم الشهيد/المتوفي"
    )
    
    # بيانات العائلة
    male_siblings_count = models.PositiveIntegerField(
        default=0,
        verbose_name="عدد الأخوة الذكور"
    )
    female_siblings_count = models.PositiveIntegerField(
        default=0,
        verbose_name="عدد الأخوة الإناث"
    )
    
    # بيانات الوصي
    guardian_name = models.CharField(
        max_length=100,
        verbose_name="اسم الوصي على الأيتام"
    )
    guardian_relationship = models.CharField(
        max_length=100,
        choices=GUARDIAN_RELATIONSHIP_CHOICES,
        verbose_name="صلة قرابة الوصي بالأيتام",
        help_text="اختر صلة القرابة"
    )
    phone_number = models.CharField(
        max_length=15,
        verbose_name="رقم الجوال",
        validators=[RegexValidator(
            regex=r'^(\+970|0)?5[0-9]{8}$',
            message='رقم الجوال غير صحيح'
        )],
        help_text="رقم جوال الوصي"
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
        verbose_name = "يتيم"
        verbose_name_plural = "الأيتام"
        ordering = ['name']
    
    @property
    def age(self):
        """حساب العمر تلقائياً حسب تاريخ الميلاد"""
        if self.birth_date:
            today = date.today()
            return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        return None
    
    @property
    def total_siblings(self):
        """إجمالي عدد الأخوة"""
        return self.male_siblings_count + self.female_siblings_count
    
    @property
    def age_category(self):
        """تصنيف العمر"""
        age = self.age
        if age is None:
            return 'غير محدد'
        elif age < 6:
            return 'طفولة مبكرة'
        elif age < 12:
            return 'طفولة'
        elif age < 18:
            return 'مراهقة'
        else:
            return 'بالغ'
    
    def __str__(self):
        return f"{self.name} - {self.national_id} - عمر {self.age} سنة"
