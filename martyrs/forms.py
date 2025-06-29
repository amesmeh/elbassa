from django import forms
from django.core.exceptions import ValidationError
from .models import Martyr
from basic_data.models import District

class MartyrForm(forms.ModelForm):
    """نموذج إدخال وتعديل بيانات الشهداء"""
    
    class Meta:
        model = Martyr
        fields = [
            'name', 'national_id', 'martyrdom_date', 'agent_name',
            'agent_national_id', 'agent_phone', 'relationship_to_martyr',
            'notes'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'أدخل الاسم الرباعي للشهيد',
                'dir': 'rtl'
            }),
            'national_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '123456789',
                'maxlength': '9',
                'pattern': '[0-9]{9}'
            }),
            'martyrdom_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'agent_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'أدخل اسم وكيل الشهيد',
                'dir': 'rtl'
            }),
            'agent_national_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '123456789',
                'maxlength': '9',
                'pattern': '[0-9]{9}'
            }),
            'agent_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '0599123456',
                'dir': 'ltr'
            }),
            'relationship_to_martyr': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'صلة القرابة (مثل: والد، أخ، ابن...)',
                'dir': 'rtl'
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
        
        # جعل الحقول الاختيارية
        optional_fields = [
            'martyrdom_date', 'agent_name', 'agent_national_id', 
            'agent_phone', 'relationship_to_martyr', 'notes'
        ]
        for field_name in optional_fields:
            if field_name in self.fields:
                self.fields[field_name].required = False
        
        # إضافة العلامات المطلوبة للحقول الإجبارية فقط
        for field_name, field in self.fields.items():
            if field.required:
                field.widget.attrs.update({'required': True})

    def clean_national_id(self):
        national_id = self.cleaned_data.get('national_id')
        if national_id:
            # التحقق من عدم وجود رقم الهوية مسبقاً (إلا في حالة التعديل)
            qs = Martyr.objects.filter(national_id=national_id)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise ValidationError('رقم الهوية موجود مسبقاً في قاعدة البيانات')
        return national_id

class MartyrSearchForm(forms.Form):
    """نموذج البحث المرن في الشهداء"""
    
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
    

    
    year = forms.ChoiceField(
        choices=[],
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select'
        }),
        label="سنة الاستشهاد"
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # إضافة سنوات الاستشهاد المتاحة
        years = Martyr.objects.dates('martyrdom_date', 'year', order='DESC')
        year_choices = [('', 'جميع السنوات')]
        year_choices.extend([(year.year, str(year.year)) for year in years])
        self.fields['year'].choices = year_choices

class MartyrImportForm(forms.Form):
    """نموذج استيراد الشهداء من ملف Excel"""
    
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