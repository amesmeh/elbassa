from django import forms
from django.core.validators import RegexValidator
from .models import CivilRegistry
from basic_data.models import District

class CivilRecordForm(forms.ModelForm):
    """نموذج إدخال السجل المدني"""
    
    class Meta:
        model = CivilRegistry
        fields = [
            'name', 'national_id', 'gender', 'birth_date',
            'governorate', 'city', 'neighborhood', 'address',
            'notes'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'أدخل الاسم الرباعي'
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
            'governorate': forms.Select(attrs={
                'class': 'form-select'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'أدخل اسم المدينة'
            }),
            'neighborhood': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'أدخل اسم الحي'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'أدخل العنوان التفصيلي',
                'rows': '3'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'أدخل أي ملاحظات إضافية',
                'rows': '3'
            })
        }
        
    def clean_national_id(self):
        """التحقق من صحة رقم الهوية"""
        national_id = self.cleaned_data.get('national_id')
        if national_id and len(national_id) != 9:
            raise forms.ValidationError('رقم الهوية يجب أن يكون 9 أرقام')
        if national_id and not national_id.isdigit():
            raise forms.ValidationError('رقم الهوية يجب أن يحتوي على أرقام فقط')
        return national_id

class CivilRecordSearchForm(forms.Form):
    """نموذج البحث في السجل المدني"""
    
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
        choices=[('', 'الجميع')] + CivilRegistry.GENDER_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='الجنس'
    )
    
    governorate = forms.ChoiceField(
        choices=[('', 'جميع المحافظات')] + CivilRegistry.GOVERNORATE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='المحافظة'
    )
    
    age_from = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '0',
            'max': '100',
            'placeholder': 'من عمر'
        }),
        label='من عمر'
    )
    
    age_to = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '0',
            'max': '100',
            'placeholder': 'إلى عمر'
        }),
        label='إلى عمر'
    )

class CivilRecordImportForm(forms.Form):
    """نموذج استيراد السجل المدني من ملف Excel"""
    
    excel_file = forms.FileField(
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.xlsx,.xls'
        }),
        label='ملف Excel',
        help_text='الحقول المطلوبة: name, national_id, gender, birth_date, governorate, city, family_members_count'
    ) 