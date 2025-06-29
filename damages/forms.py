from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from .models import Damage
from basic_data.models import District, Guardian

class DamageForm(forms.ModelForm):
    """نموذج إدخال الأضرار"""
    
    class Meta:
        model = Damage
        fields = [
            'guardian_national_id', 'guardian_name', 'phone_number', 'district',
            'ownership_type', 'housing_type', 'housing_condition', 'construction_type',
            'floors_count', 'damage_type', 'damage_percentage', 'damage_date', 
            'estimated_cost_ils', 'estimated_cost_usd', 'notes'
        ]
        widgets = {
            'guardian_national_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'أدخل رقم الهوية (9 أرقام)',
                'maxlength': '9'
            }),
            'guardian_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'سيتم ملؤه تلقائياً'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'مثال: 0599123456'
            }),
            'district': forms.Select(attrs={
                'class': 'form-select'
            }),
            'ownership_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'housing_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'housing_condition': forms.Select(attrs={
                'class': 'form-select'
            }),
            'construction_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'floors_count': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '10'
            }),
            'damage_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'damage_percentage': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '100'
            }),
            'damage_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'estimated_cost_ils': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'step': '0.01',
                'placeholder': 'التكلفة بالشيكل'
            }),
            'estimated_cost_usd': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'step': '0.01',
                'placeholder': 'التكلفة بالدولار'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'أي ملاحظات إضافية'
            })
        }
        
    def clean_guardian_national_id(self):
        """التحقق من صحة رقم الهوية"""
        national_id = self.cleaned_data.get('guardian_national_id')
        if national_id and len(national_id) != 9:
            raise forms.ValidationError('رقم الهوية يجب أن يكون 9 أرقام')
        if national_id and not national_id.isdigit():
            raise forms.ValidationError('رقم الهوية يجب أن يحتوي على أرقام فقط')
        return national_id

class DamageSearchForm(forms.Form):
    """نموذج البحث في الأضرار"""
    
    search_query = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'ابحث بالاسم أو رقم الهوية...'
        }),
        label='بحث عام'
    )
    
    damage_type = forms.ChoiceField(
        choices=[('', 'جميع الأنواع')] + Damage.DAMAGE_TYPE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='نوع الضرر'
    )
    
    housing_type = forms.ChoiceField(
        choices=[('', 'جميع الأنواع')] + Damage.HOUSING_TYPE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='نوع السكن'
    )
    
    district = forms.ModelChoiceField(
        queryset=District.objects.all(),
        required=False,
        empty_label="جميع الأحياء",
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='الحي'
    )
    
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        label='من تاريخ'
    )
    
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        label='إلى تاريخ'
    )
    
    cost_ils_min = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'الحد الأدنى (شيكل)'
        }),
        label='التكلفة الدنيا (شيكل)'
    )
    
    cost_ils_max = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'الحد الأقصى (شيكل)'
        }),
        label='التكلفة العليا (شيكل)'
    )

class DamageImportForm(forms.Form):
    """نموذج استيراد الأضرار من ملف Excel"""
    
    excel_file = forms.FileField(
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.xlsx,.xls'
        }),
        label='ملف Excel',
        help_text='الحقول المطلوبة: guardian_national_id, guardian_name, damage_date, damage_type, housing_type'
    )
    
    def clean_excel_file(self):
        file = self.cleaned_data.get('excel_file')
        if file:
            if not file.name.lower().endswith(('.xlsx', '.xls')):
                raise ValidationError('يجب أن يكون الملف بصيغة Excel (.xlsx أو .xls)')
            if file.size > 5 * 1024 * 1024:  # 5MB
                raise ValidationError('حجم الملف يجب أن يكون أقل من 5 ميجابايت')
        return file 