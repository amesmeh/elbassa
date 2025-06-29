from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from .models import Orphan
from basic_data.models import District, Guardian

class OrphanForm(forms.ModelForm):
    """نموذج إدخال الأيتام"""
    
    class Meta:
        model = Orphan
        fields = [
            'name', 'national_id', 'gender', 'birth_date', 'health_status', 'education_level',
            'deceased_name', 'deceased_national_id', 'guardian_name', 'guardian_relationship',
            'phone_number', 'district', 'male_siblings_count', 'female_siblings_count', 'notes'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'أدخل الاسم الرباعي لليتيم'
            }),
            'national_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'أدخل رقم الهوية (9 أرقام)',
                'maxlength': '9'
            }),
            'gender': forms.Select(attrs={
                'class': 'form-select'
            }),
            'birth_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'health_status': forms.Select(attrs={
                'class': 'form-select'
            }),
            'education_level': forms.Select(attrs={
                'class': 'form-select'
            }),
            'deceased_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'أدخل اسم الشهيد/المتوفي'
            }),
            'deceased_national_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'أدخل رقم هوية الشهيد/المتوفي (9 أرقام)',
                'maxlength': '9'
            }),
            'guardian_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'أدخل اسم الوصي'
            }),
            'guardian_relationship': forms.Select(attrs={
                'class': 'form-select'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'مثال: 0599123456'
            }),
            'district': forms.Select(attrs={
                'class': 'form-select'
            }),
            'male_siblings_count': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '20'
            }),
            'female_siblings_count': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '20'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'أي ملاحظات إضافية'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # تحديث قائمة الأحياء
        self.fields['district'].queryset = District.objects.all().order_by('name')
        self.fields['district'].empty_label = "اختر الحي"
        
        # إضافة العلامات الفارغة للقوائم المنسدلة
        self.fields['education_level'].empty_label = "اختر المرحلة الدراسية"
        self.fields['guardian_relationship'].empty_label = "اختر صلة القرابة"
        
        # إضافة العلامات المطلوبة
        for field_name, field in self.fields.items():
            if field.required:
                field.widget.attrs.update({'required': True})

    def clean_national_id(self):
        """التحقق من صحة رقم الهوية"""
        national_id = self.cleaned_data.get('national_id')
        if national_id and len(national_id) != 9:
            raise forms.ValidationError('رقم الهوية يجب أن يكون 9 أرقام')
        if national_id and not national_id.isdigit():
            raise forms.ValidationError('رقم الهوية يجب أن يحتوي على أرقام فقط')
        return national_id
        
    def clean_deceased_national_id(self):
        """التحقق من صحة رقم هوية الشهيد/المتوفي"""
        national_id = self.cleaned_data.get('deceased_national_id')
        if national_id and len(national_id) != 9:
            raise forms.ValidationError('رقم الهوية يجب أن يكون 9 أرقام')
        if national_id and not national_id.isdigit():
            raise forms.ValidationError('رقم الهوية يجب أن يحتوي على أرقام فقط')
        return national_id

class OrphanSearchForm(forms.Form):
    """نموذج البحث في الأيتام"""
    
    search_query = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'ابحث بالاسم أو رقم الهوية...'
        }),
        label='بحث عام'
    )
    
    gender = forms.ChoiceField(
        choices=[('', 'الجميع')] + Orphan.GENDER_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='الجنس'
    )
    
    health_status = forms.ChoiceField(
        choices=[('', 'جميع الحالات')] + Orphan.HEALTH_STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='الحالة الصحية'
    )
    
    education_level = forms.ChoiceField(
        required=False,
        choices=[('', 'جميع المراحل')] + Orphan.EDUCATION_LEVEL_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='المرحلة الدراسية'
    )
    
    district = forms.ModelChoiceField(
        queryset=District.objects.all(),
        required=False,
        empty_label="جميع الأحياء",
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='الحي'
    )
    
    age_from = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '0',
            'max': '18',
            'placeholder': 'من عمر'
        }),
        label='من عمر'
    )
    
    age_to = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '0',
            'max': '18',
            'placeholder': 'إلى عمر'
        }),
        label='إلى عمر'
    )

class OrphanImportForm(forms.Form):
    """نموذج استيراد الأيتام من ملف Excel"""
    
    excel_file = forms.FileField(
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.xlsx,.xls'
        }),
        label='ملف Excel',
        help_text='الحقول المطلوبة: name, national_id, gender, birth_date, deceased_name, deceased_national_id'
    )
    
    def clean_excel_file(self):
        file = self.cleaned_data.get('excel_file')
        if file:
            if not file.name.lower().endswith(('.xlsx', '.xls')):
                raise ValidationError('يجب أن يكون الملف بصيغة Excel (.xlsx أو .xls)')
            if file.size > 5 * 1024 * 1024:  # 5MB
                raise ValidationError('حجم الملف يجب أن يكون أقل من 5 ميجابايت')
        return file 