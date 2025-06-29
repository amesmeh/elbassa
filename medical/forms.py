from django import forms
from django.core.exceptions import ValidationError
from .models import MedicalRecord
from basic_data.models import District, Guardian

class MedicalRecordForm(forms.ModelForm):
    """نموذج إدخال وتعديل البيانات المرضية"""
    
    class Meta:
        model = MedicalRecord
        fields = [
            'name', 'national_id', 'gender', 'guardian_national_id', 'guardian_name',
            'phone_number', 'disease_type', 'disease_description', 'disability_type',
            'disability_percentage', 'district', 'notes'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'أدخل الاسم الرباعي للمريض',
                'dir': 'rtl'
            }),
            'national_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '123456789',
                'maxlength': '9',
                'pattern': '[0-9]{9}'
            }),
            'gender': forms.Select(attrs={
                'class': 'form-select'
            }),
            'guardian_national_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '123456789',
                'maxlength': '9',
                'pattern': '[0-9]{9}',
                'onchange': 'loadGuardianData(this.value)'
            }),
            'guardian_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'سيتم ملؤه تلقائياً',
                'readonly': True,
                'dir': 'rtl'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '0599123456',
                'dir': 'ltr'
            }),
            'disease_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'disease_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'وصف تفصيلي للمرض',
                'dir': 'rtl'
            }),
            'disability_type': forms.Select(attrs={
                'class': 'form-select',
                'onchange': 'toggleDisabilityPercentage(this.value)'
            }),
            'disability_percentage': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '100',
                'placeholder': 'أدخل النسبة من 0 إلى 100'
            }),
            'district': forms.Select(attrs={
                'class': 'form-select',
                'readonly': True
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'أدخل أي ملاحظات إضافية',
                'dir': 'rtl'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # تحديث قائمة الأحياء
        self.fields['district'].queryset = District.objects.all().order_by('name')
        self.fields['district'].empty_label = "سيتم ملؤه تلقائياً"
        
        # إضافة العلامات المطلوبة
        for field_name, field in self.fields.items():
            if field.required:
                field.widget.attrs.update({'required': True})
        
        # إذا كان هناك سجل محدد، ملء البيانات
        if self.instance.pk and self.instance.guardian:
            self.fields['guardian_name'].initial = self.instance.guardian.name
            if not self.instance.phone_number and self.instance.guardian.phone_number:
                self.fields['phone_number'].initial = self.instance.guardian.phone_number
            if not self.instance.district and self.instance.guardian.district:
                self.fields['district'].initial = self.instance.guardian.district

    def clean_national_id(self):
        national_id = self.cleaned_data.get('national_id')
        if national_id:
            # التحقق من عدم وجود رقم الهوية مسبقاً (إلا في حالة التعديل)
            qs = MedicalRecord.objects.filter(national_id=national_id)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise ValidationError('رقم الهوية موجود مسبقاً في قاعدة البيانات')
        return national_id

    def clean_disability_percentage(self):
        disability_type = self.cleaned_data.get('disability_type')
        disability_percentage = self.cleaned_data.get('disability_percentage')
        
        if disability_type != 'none' and disability_percentage is None:
            raise ValidationError('يجب إدخال نسبة الإعاقة عند اختيار نوع إعاقة')
        
        if disability_type == 'none' and disability_percentage is not None:
            # إذا لم تكن هناك إعاقة، تجاهل النسبة
            return None
            
        if disability_percentage is not None:
            if disability_percentage < 0 or disability_percentage > 100:
                raise ValidationError('نسبة الإعاقة يجب أن تكون بين 0 و 100')
        
        return disability_percentage

    def clean_guardian_national_id(self):
        guardian_national_id = self.cleaned_data.get('guardian_national_id')
        if guardian_national_id:
            try:
                guardian = Guardian.objects.get(national_id=guardian_national_id)
                return guardian_national_id
            except Guardian.DoesNotExist:
                # لا نرفع خطأ هنا، بل نترك النموذج يتم حفظه
                pass
        return guardian_national_id

class MedicalRecordSearchForm(forms.Form):
    """نموذج البحث المرن في البيانات المرضية"""
    
    search = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'ابحث بالاسم أو رقم الهوية...',
            'dir': 'rtl'
        }),
        label="البحث"
    )
    
    gender = forms.ChoiceField(
        choices=[],
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select'
        }),
        label="الجنس"
    )
    
    district = forms.ModelChoiceField(
        queryset=District.objects.all(),
        required=False,
        empty_label="جميع الأحياء",
        widget=forms.Select(attrs={
            'class': 'form-select'
        }),
        label="الحي"
    )
    
    disease_type = forms.ChoiceField(
        choices=[],
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select'
        }),
        label="نوع المرض"
    )
    
    disability_type = forms.ChoiceField(
        choices=[],
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select'
        }),
        label="نوع الإعاقة"
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # إضافة خيارات الجنس
        gender_choices = [('', 'جميع الأجناس')]
        gender_choices.extend(MedicalRecord.GENDER_CHOICES)
        self.fields['gender'].choices = gender_choices
        
        # إضافة أنواع الأمراض المتاحة
        disease_choices = [('', 'جميع أنواع الأمراض')]
        disease_choices.extend(MedicalRecord.DISEASE_TYPE_CHOICES)
        self.fields['disease_type'].choices = disease_choices
        
        # إضافة أنواع الإعاقات المتاحة
        disability_choices = [('', 'جميع أنواع الإعاقات')]
        disability_choices.extend(MedicalRecord.DISABILITY_TYPE_CHOICES)
        self.fields['disability_type'].choices = disability_choices

class MedicalRecordImportForm(forms.Form):
    """نموذج استيراد البيانات المرضية من ملف Excel"""
    
    excel_file = forms.FileField(
        label="ملف Excel",
        help_text="يجب أن يكون الملف بصيغة .xlsx أو .xls",
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.xlsx,.xls'
        })
    )
    
    def clean_excel_file(self):
        file = self.cleaned_data.get('excel_file')
        if file:
            if not file.name.lower().endswith(('.xlsx', '.xls')):
                raise ValidationError('يجب أن يكون الملف بصيغة Excel (.xlsx أو .xls)')
            if file.size > 5 * 1024 * 1024:  # 5MB
                raise ValidationError('حجم الملف يجب أن يكون أقل من 5 ميجابايت')
        return file 