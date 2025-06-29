#!/usr/bin/env python
# -*- coding: utf-8 -*-

# إصلاح مشكلة district في ملف orphans/views.py

with open('orphans/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

# البحث عن الموقع الصحيح لإضافة كود البحث عن الحي
insertion_point = "# إنشاء اليتيم"
district_code = """                    # البحث عن الحي إذا كان موجود
                    district = None
                    if not pd.isna(row.get('الحي')) or not pd.isna(row.get('المنطقة')):
                        district_name = str(row.get('الحي', row.get('المنطقة', ''))).strip()
                        if district_name:
                            try:
                                district = District.objects.get(name=district_name)
                            except District.DoesNotExist:
                                pass
                    
                    """

# إضافة كود البحث عن الحي قبل إنشاء اليتيم
content = content.replace(insertion_point, district_code + insertion_point)

# إزالة التعليق من district=district
content = content.replace('# district=district,  # تم إصلاح هذا السطر', 'district=district,')

with open('orphans/views.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("تم إصلاح مشكلة district بنجاح!") 