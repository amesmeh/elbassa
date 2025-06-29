#!/usr/bin/env python
import os
import sys
import django

# إعداد Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mosa3adat_project.settings')
django.setup()

from basic_data.models import Guardian
from django.db.models import Sum

print("=" * 60)
print("فحص إجمالي أفراد العائلات")
print("=" * 60)

total_guardians = Guardian.objects.count()
print(f"عدد أولياء الأمور: {total_guardians}")

if total_guardians == 0:
    print("لا يوجد أولياء أمور في النظام")
    sys.exit()

# الإجمالي من العدادات المحفوظة
total_from_stored = Guardian.objects.aggregate(total=Sum('family_members_count'))['total'] or 0
print(f"إجمالي أفراد العائلات (من العدادات المحفوظة): {total_from_stored}")

# الإجمالي الحقيقي
total_from_actual = 0
for guardian in Guardian.objects.all():
    actual_family_size = 1 + guardian.children.count() + guardian.wives.count()
    total_from_actual += actual_family_size

print(f"إجمالي أفراد العائلات (من البيانات الفعلية): {total_from_actual}")

print()
print("أمثلة من البيانات:")
print("-" * 60)

count = 0
for guardian in Guardian.objects.all()[:10]:
    stored_family = guardian.family_members_count
    actual_children = guardian.children.count()
    actual_wives = guardian.wives.count()
    actual_family = 1 + actual_children + actual_wives
    
    status = "✅" if stored_family == actual_family else "❌"
    
    print(f"{status} {guardian.name}")
    print(f"   محفوظ: أطفال={guardian.children_count}, زوجات={guardian.wives_count}, عائلة={stored_family}")
    print(f"   فعلي: أطفال={actual_children}, زوجات={actual_wives}, عائلة={actual_family}")
    print()
    count += 1

if Guardian.objects.count() > 10:
    print(f"... و {Guardian.objects.count() - 10} سجل آخر")

print()
print("=" * 60)
print("التحليل:")
print("=" * 60)

if total_from_stored == total_from_actual:
    print("✅ العدادات المحفوظة تطابق البيانات الفعلية")
else:
    difference = total_from_stored - total_from_actual
    print(f"❌ هناك فرق قدره {abs(difference)} في العدادات")
    if difference > 0:
        print("   العدادات المحفوظة أكبر من الفعلية")
    else:
        print("   العدادات المحفوظة أقل من الفعلية")
    
    print()
    print("🔧 حلول مقترحة:")
    print("1. استخدام 'إصلاح العدادات' لإعادة حساب جميع العدادات")
    print("2. إعادة استيراد ملف Excel مع التأكد من صحة العدادات")
    print("3. مراجعة البيانات يدوياً لتصحيح الأخطاء") 