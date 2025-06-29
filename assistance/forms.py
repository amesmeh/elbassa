from django import forms
from django.core.exceptions import ValidationError
from .models import Assistance

class AssistanceForm(forms.ModelForm):
    """نموذج إضافة/تعديل المساعدة"""
    
    class Meta:
        model = Assistance
        fields = [
            'national_id', 'beneficiary_name', 'assistance_type', 
            'quantity', 'assistance_date', 'notes'
        ]
        widgets = {
            'national_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'أدخل رقم الهوية',
                'maxlength': '9',
                'style': 'font-size: 1.2em; font-weight: bold;'
            }),
            'beneficiary_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'اسم المستفيد'
            }),
            'assistance_type': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نوع المساعدة (مثل: مواد غذائية، مساعدة نقدية، أدوية...)',
                'list': 'assistance-types-suggestions'
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'step': '0.01',
                'placeholder': 'الكمية أو المبلغ'
            }),
            'assistance_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'ملاحظات إضافية (اختياري)'
            }),
        }

    def clean_national_id(self):
        national_id = self.cleaned_data.get('national_id')
        if national_id:
            if len(national_id) != 9:
                raise ValidationError('رقم الهوية يجب أن يكون 9 أرقام')
            if not national_id.isdigit():
                raise ValidationError('رقم الهوية يجب أن يحتوي على أرقام فقط')
        return national_id
    
    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity is not None and quantity <= 0:
            raise ValidationError('الكمية يجب أن تكون أكبر من صفر')
        return quantity

class AssistanceSearchForm(forms.Form):
    """نموذج البحث والفلترة"""
    
    search_query = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'ابحث بالاسم أو رقم الهوية...'
        }),
        label='البحث'
    )
    
    assistance_type = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'نوع المساعدة',
            'list': 'assistance-types-list'
        }),
        label='نوع المساعدة'
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
    
    district = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'اسم الحي',
            'list': 'districts-list'
        }),
        label='الحي'
    )

class AssistanceImportForm(forms.Form):
    """نموذج استيراد المساعدات من Excel"""
    
    excel_file = forms.FileField(
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.xlsx,.xls'
        }),
        label='ملف Excel',
        help_text='يجب أن يكون الملف بصيغة .xlsx أو .xls'
    )

    def clean_excel_file(self):
        excel_file = self.cleaned_data.get('excel_file')
        if excel_file:
            if not excel_file.name.endswith(('.xlsx', '.xls')):
                raise ValidationError('يجب أن يكون الملف بصيغة Excel (.xlsx أو .xls)')
        return excel_file
