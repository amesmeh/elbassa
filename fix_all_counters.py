#!/usr/bin/env python
import os
import sys
import django

# إعداد Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mosa3adat_project.settings')
django.setup()

from basic_data.models import Guardian

print("=" * 60)
print("إصلاح جميع عدادات أولياء الأمور")
print("=" * 60)

total_guardians = Guardian.objects.count()
print(f"عدد أولياء الأمور: {total_guardians}")

if total_guardians == 0:
    print("لا يوجد أولياء أمور في النظام")
    sys.exit()

print("جاري إصلاح العدادات...")

fixed_count = 0
for guardian in Guardian.objects.all():
    # إعادة حساب العدادات الفعلية
    actual_children = guardian.children.count()
    actual_wives = guardian.wives.count()
    actual_family = 1 + actual_children + actual_wives
    
    # تحديث العدادات
    guardian.children_count = actual_children
    guardian.wives_count = actual_wives
    guardian.family_members_count = actual_family
    guardian.save()
    
    fixed_count += 1
    
    if fixed_count % 100 == 0:
        print(f"تم إصلاح {fixed_count} سجل...")

print(f"✅ تم إصلاح {fixed_count} سجل بنجاح")

# التحقق من النتيجة
from django.db.models import Sum
total_after_fix = Guardian.objects.aggregate(total=Sum('family_members_count'))['total'] or 0
print(f"إجمالي أفراد العائلات بعد الإصلاح: {total_after_fix}")

print("=" * 60)
print("الإصلاح مكتمل!") 