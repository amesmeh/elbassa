from django import forms
from django.core.exceptions import ValidationError
from .models import Injured
from basic_data.models import District, Guardian

class InjuredForm(forms.ModelForm):
    """نموذج إدخال وتعديل بيانات الجرحى"""
    
    class Meta:
        model = Injured
        fields = [
            'name', 'national_id', 'guardian_national_id', 'guardian_name',
            'phone_number', 'injury_date', 'injury_type', 'injury_description',
            'district', 'notes'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'أدخل الاسم الرباعي للجريح',
                'dir': 'rtl'
            }),
            'national_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '123456789',
                'maxlength': '9',
                'pattern': '[0-9]{9}'
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
            'injury_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'injury_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'injury_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'وصف تفصيلي للإصابة',
                'dir': 'rtl'
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
        
        # إذا كان هناك جريح محدد، ملء البيانات
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
            qs = Injured.objects.filter(national_id=national_id)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise ValidationError('رقم الهوية موجود مسبقاً في قاعدة البيانات')
        return national_id

    def clean_guardian_national_id(self):
        guardian_national_id = self.cleaned_data.get('guardian_national_id')
        if guardian_national_id:
            try:
                guardian = Guardian.objects.get(national_id=guardian_national_id)
                return guardian_national_id
            except Guardian.DoesNotExist:
                # لا نرفع خطأ هنا، بل نترك النموذج يتم حفظه
                # وسيتم البحث مرة أخرى في save method
                pass
        return guardian_national_id

class InjuredSearchForm(forms.Form):
    """نموذج البحث المرن في الجرحى"""
    
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
    
    district = forms.ModelChoiceField(
        queryset=District.objects.all(),
        required=False,
        empty_label="جميع الأحياء",
        widget=forms.Select(attrs={
            'class': 'form-select'
        }),
        label="الحي"
    )
    
    injury_type = forms.ChoiceField(
        choices=[],
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select'
        }),
        label="نوع الإصابة"
    )
    
    year = forms.ChoiceField(
        choices=[],
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select'
        }),
        label="سنة الإصابة"
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # إضافة أنواع الإصابات المتاحة
        injury_choices = [('', 'جميع أنواع الإصابات')]
        injury_choices.extend(Injured.INJURY_TYPE_CHOICES)
        self.fields['injury_type'].choices = injury_choices
        
        # إضافة سنوات الإصابة المتاحة
        years = Injured.objects.dates('injury_date', 'year', order='DESC')
        year_choices = [('', 'جميع السنوات')]
        year_choices.extend([(year.year, str(year.year)) for year in years])
        self.fields['year'].choices = year_choices

class InjuredImportForm(forms.Form):
    """نموذج استيراد الجرحى من ملف Excel"""
    
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

class GuardianLookupForm(forms.Form):
    """نموذج البحث عن ولي الأمر"""
    
    guardian_national_id = forms.CharField(
        max_length=9,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '123456789',
            'maxlength': '9',
            'pattern': '[0-9]{9}'
        }),
        label="رقم هوية ولي الأمر"
    )
    
    def clean_guardian_national_id(self):
        national_id = self.cleaned_data.get('guardian_national_id')
        if national_id:
            if len(national_id) != 9 or not national_id.isdigit():
                raise ValidationError('رقم الهوية يجب أن يكون 9 أرقام')
        return national_id 