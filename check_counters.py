#!/usr/bin/env python
import os
import sys
import django

# إعداد Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mosa3adat_project.settings')
django.setup()

from basic_data.models import Guardian

print('🔍 جاري فحص العدادات...')
print('=' * 60)

mismatch_count = 0
total_count = 0

for guardian in Guardian.objects.all()[:10]:  # فحص أول 10 أولياء أمور
    real_children = guardian.children.count()
    real_wives = guardian.wives.count()
    real_family = 1 + real_children + real_wives
    
    children_match = guardian.children_count == real_children
    wives_match = guardian.wives_count == real_wives
    family_match = guardian.family_members_count == real_family
    
    all_match = children_match and wives_match and family_match
    
    if not all_match:
        mismatch_count += 1
    
    status = "✅" if all_match else "❌"
    
    print(f'{status} ولي الأمر: {guardian.name} (ID: {guardian.national_id})')
    
    if not children_match:
        print(f'   ⚠️  أطفال: مسجل={guardian.children_count} | فعلي={real_children}')
    else:
        print(f'   ✅ أطفال: {real_children}')
        
    if not wives_match:
        print(f'   ⚠️  زوجات: مسجل={guardian.wives_count} | فعلي={real_wives}')
    else:
        print(f'   ✅ زوجات: {real_wives}')
        
    if not family_match:
        print(f'   ⚠️  أفراد العائلة: مسجل={guardian.family_members_count} | فعلي={real_family}')
    else:
        print(f'   ✅ أفراد العائلة: {real_family}')
    
    print('-' * 40)
    total_count += 1

print('\n📊 ملخص النتائج:')
print(f'إجمالي الفحص: {total_count}')
print(f'العدادات الصحيحة: {total_count - mismatch_count}')
print(f'العدادات الخاطئة: {mismatch_count}')

if mismatch_count > 0:
    print(f'\n⚠️  يُنصح بتشغيل "إصلاح العدادات" لتصحيح {mismatch_count} من أولياء الأمور')
else:
    print('\n🎉 جميع العدادات صحيحة!') 