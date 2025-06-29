from django import forms
from .models import District, Guardian, Wife, Child

class DistrictForm(forms.ModelForm):
    """نموذج إضافة وتعديل الأحياء"""
    class Meta:
        model = District
        fields = ['name', 'representative_name', 'representative_phone']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'اسم الحي'
            }),
            'representative_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'اسم المندوب'
            }),
            'representative_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'رقم جوال المندوب'
            }),
        }
        labels = {
            'name': 'اسم الحي',
            'representative_name': 'اسم المندوب',
            'representative_phone': 'رقم جوال المندوب',
        }

class GuardianForm(forms.ModelForm):
    """نموذج إضافة وتعديل أولياء الأمور"""
    class Meta:
        model = Guardian
        fields = [
            'name', 'national_id', 'current_job', 'phone_number', 'gender',
            'marital_status', 'children_count', 'wives_count', 'residence_status', 
            'original_governorate', 'original_city', 'displacement_address', 'district', 'housing_type'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'الاسم الكامل'
            }),
            'national_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'رقم الهوية (9 أرقام)'
            }),
            'current_job': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'الوظيفة الحالية'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'رقم الجوال'
            }),
            'gender': forms.Select(attrs={
                'class': 'form-control'
            }),
            'marital_status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'children_count': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'عدد الأبناء',
                'min': '0'
            }),
            'wives_count': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'عدد الزوجات',
                'min': '0'
            }),
            'residence_status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'original_governorate': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'المحافظة الأصلية'
            }),
            'original_city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'المدينة الأصلية'
            }),
            'displacement_address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'عنوان النزوح'
            }),
            'district': forms.Select(attrs={
                'class': 'form-control'
            }),
            'housing_type': forms.Select(attrs={
                'class': 'form-control'
            }),
        }
        labels = {
            'name': 'اسم ولي الأمر',
            'national_id': 'رقم الهوية',
            'current_job': 'الوظيفة الحالية',
            'phone_number': 'رقم الجوال',
            'gender': 'الجنس',
            'marital_status': 'الحالة الاجتماعية',
            'children_count': 'عدد الأبناء',
            'wives_count': 'عدد الزوجات',
            'residence_status': 'حالة الإقامة',
            'original_governorate': 'المحافظة الأصلية',
            'original_city': 'المدينة الأصلية',
            'displacement_address': 'عنوان النزوح',
            'district': 'الحي الحالي',
            'housing_type': 'نوع السكن',
        }

class WifeForm(forms.ModelForm):
    """نموذج إضافة وتعديل الزوجات"""
    class Meta:
        model = Wife
        fields = ['name', 'national_id', 'guardian']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'اسم الزوجة'
            }),
            'national_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'رقم الهوية (اختياري)'
            }),
            'guardian': forms.Select(attrs={
                'class': 'form-control'
            }),
        }
        labels = {
            'name': 'اسم الزوجة',
            'national_id': 'رقم الهوية',
            'guardian': 'ولي الأمر',
        }

class ChildForm(forms.ModelForm):
    """نموذج إضافة وتعديل الأطفال"""
    class Meta:
        model = Child
        fields = ['name', 'national_id', 'birth_date', 'guardian']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'اسم الطفل'
            }),
            'national_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'رقم الهوية (اختياري)'
            }),
            'birth_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'guardian': forms.Select(attrs={
                'class': 'form-control'
            }),
        }
        labels = {
            'name': 'اسم الطفل',
            'national_id': 'رقم الهوية',
            'birth_date': 'تاريخ الميلاد',
            'guardian': 'ولي الأمر',
        }

class GuardianSearchForm(forms.Form):
    """نموذج البحث عن أولياء الأمور"""
    search_query = forms.CharField(required=False, label='بحث عام')
    district = forms.CharField(required=False, label='الحي')