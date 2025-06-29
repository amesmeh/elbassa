from django import forms
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory
from .citizen_models import CitizenRegistrationRequest, CitizenRequestChild, CitizenRequestWife
from .models import Guardian, District


class CitizenRegistrationForm(forms.ModelForm):
    """نموذج تسجيل المواطن الجديد"""
    
    class Meta:
        model = CitizenRegistrationRequest
        fields = [
            'name', 'national_id', 'phone_number', 'gender', 'current_job',
            'district', 'marital_status', 'residence_status', 'children_count',
            'wives_count', 'housing_type', 'original_governorate', 
            'original_city', 'displacement_address'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'أدخل الاسم الكامل'
            }),
            'national_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'أدخل رقم الهوية'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'أدخل رقم الجوال'
            }),
            'gender': forms.Select(attrs={
                'class': 'form-select'
            }),
            'current_job': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'أدخل المهنة الحالية'
            }),
            'district': forms.Select(attrs={
                'class': 'form-select'
            }),
            'marital_status': forms.Select(attrs={
                'class': 'form-select'
            }),
            'residence_status': forms.Select(attrs={
                'class': 'form-select'
            }),
            'children_count': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '20'
            }),
            'wives_count': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '4'
            }),
            'housing_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'original_governorate': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'أدخل المحافظة الأصلية'
            }),
            'original_city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'أدخل المدينة الأصلية'
            }),
            'displacement_address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': '3',
                'placeholder': 'أدخل عنوان النزوح'
            }),
        }
    
    def clean_national_id(self):
        """التحقق من عدم وجود رقم الهوية مسبقاً"""
        national_id = self.cleaned_data.get('national_id')
        
        if national_id:
            # التحقق من وجود الرقم في طلبات التسجيل
            if CitizenRegistrationRequest.objects.filter(national_id=national_id).exists():
                raise forms.ValidationError('رقم الهوية موجود مسبقاً في طلبات التسجيل')
            
            # التحقق من وجود الرقم في أولياء الأمور
            if Guardian.objects.filter(national_id=national_id).exists():
                raise forms.ValidationError('رقم الهوية موجود مسبقاً في قاعدة البيانات')
        
        return national_id
    
    def clean_phone_number(self):
        """التحقق من صحة رقم الجوال"""
        phone_number = self.cleaned_data.get('phone_number')
        
        if phone_number:
            # إزالة المسافات والرموز
            phone_number = ''.join(filter(str.isdigit, phone_number))
            
            # التحقق من طول الرقم
            if len(phone_number) < 9 or len(phone_number) > 11:
                raise forms.ValidationError('رقم الجوال غير صحيح')
        
        return phone_number


class CitizenRequestChildForm(forms.ModelForm):
    """نموذج بيانات الطفل"""
    
    class Meta:
        model = CitizenRequestChild
        fields = ['name', 'national_id', 'birth_date']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'اسم الطفل'
            }),
            'national_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'رقم هوية الطفل'
            }),
            'birth_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }
    
    def clean_national_id(self):
        """التحقق من عدم وجود رقم الهوية مسبقاً"""
        national_id = self.cleaned_data.get('national_id')
        
        if national_id:
            # التحقق من وجود الرقم في الأطفال
            from .models import Child
            if Child.objects.filter(national_id=national_id).exists():
                raise forms.ValidationError('رقم هوية الطفل موجود مسبقاً')
            
            # التحقق من وجود الرقم في طلبات الأطفال
            if CitizenRequestChild.objects.filter(national_id=national_id).exists():
                raise forms.ValidationError('رقم هوية الطفل موجود مسبقاً في طلبات أخرى')
        
        return national_id


class CitizenRequestWifeForm(forms.ModelForm):
    """نموذج بيانات الزوجة"""
    
    class Meta:
        model = CitizenRequestWife
        fields = ['name', 'national_id']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'اسم الزوجة'
            }),
            'national_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'رقم هوية الزوجة'
            }),
        }
    
    def clean_national_id(self):
        """التحقق من عدم وجود رقم الهوية مسبقاً"""
        national_id = self.cleaned_data.get('national_id')
        
        if national_id:
            # التحقق من وجود الرقم في الزوجات
            from .models import Wife
            if Wife.objects.filter(national_id=national_id).exists():
                raise forms.ValidationError('رقم هوية الزوجة موجود مسبقاً')
            
            # التحقق من وجود الرقم في طلبات الزوجات
            if CitizenRequestWife.objects.filter(national_id=national_id).exists():
                raise forms.ValidationError('رقم هوية الزوجة موجود مسبقاً في طلبات أخرى')
        
        return national_id


# إنشاء FormSets للأطفال والزوجات
CitizenRequestChildFormSet = inlineformset_factory(
    CitizenRegistrationRequest,
    CitizenRequestChild,
    form=CitizenRequestChildForm,
    extra=1,
    can_delete=True,
    min_num=0,
    max_num=20
)

CitizenRequestWifeFormSet = inlineformset_factory(
    CitizenRegistrationRequest,
    CitizenRequestWife,
    form=CitizenRequestWifeForm,
    extra=1,
    can_delete=True,
    min_num=0,
    max_num=4
) 