#!/usr/bin/env python
import os
import sys
import django

# إعداد Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mosa3adat_project.settings')
django.setup()

from basic_data.models import Guardian
from django.db.models import Sum

print("=" * 80)
print("فحص حساب إجمالي أفراد العائلات")
print("=" * 80)

total_guardians = Guardian.objects.count()
print(f"عدد أولياء الأمور: {total_guardians}")

if total_guardians == 0:
    print("لا يوجد أولياء أمور في النظام")
    sys.exit()

print()
print("طرق الحساب المختلفة:")
print("-" * 80)

# الطريقة 1: مجموع العدادات المحفوظة
total_from_stored = Guardian.objects.aggregate(total=Sum('family_members_count'))['total'] or 0
print(f"1. مجموع العدادات المحفوظة (family_members_count): {total_from_stored}")

# الطريقة 2: مجموع العدادات اليدوي
manual_total = 0
for guardian in Guardian.objects.all():
    manual_total += guardian.family_members_count

print(f"2. مجموع العدادات (حساب يدوي): {manual_total}")

# الطريقة 3: مجموع العدادات الفعلية من العلاقات
actual_total = 0
for guardian in Guardian.objects.all():
    actual_family_size = 1 + guardian.children.count() + guardian.wives.count()
    actual_total += actual_family_size

print(f"3. مجموع العدادات الفعلية (من العلاقات): {actual_total}")

# الطريقة 4: مجموع العدادات المنفصلة
children_sum = Guardian.objects.aggregate(total=Sum('children_count'))['total'] or 0
wives_sum = Guardian.objects.aggregate(total=Sum('wives_count'))['total'] or 0
guardians_sum = total_guardians  # كل ولي أمر = 1
calculated_total = guardians_sum + children_sum + wives_sum

print(f"4. مجموع محسوب ({guardians_sum} أولياء + {children_sum} أطفال + {wives_sum} زوجات): {calculated_total}")

print()
print("تحليل النتائج:")
print("-" * 80)

if total_from_stored == manual_total == calculated_total:
    print("✅ جميع الطرق تعطي نفس النتيجة - الحساب صحيح")
    print(f"   الإجمالي الصحيح: {total_from_stored}")
else:
    print("❌ هناك تضارب في النتائج:")
    print(f"   الفرق بين المحفوظ والمحسوب: {total_from_stored - calculated_total}")
    print(f"   الفرق بين المحفوظ والفعلي: {total_from_stored - actual_total}")

print()
print("أمثلة من البيانات (أول 5 سجلات):")
print("-" * 80)

for i, guardian in enumerate(Guardian.objects.all()[:5], 1):
    stored_family = guardian.family_members_count
    stored_children = guardian.children_count
    stored_wives = guardian.wives_count
    
    actual_children = guardian.children.count()
    actual_wives = guardian.wives.count()
    actual_family = 1 + actual_children + actual_wives
    
    calculated_family = 1 + stored_children + stored_wives
    
    print(f"{i}. {guardian.name}")
    print(f"   محفوظ: عائلة={stored_family}, أطفال={stored_children}, زوجات={stored_wives}")
    print(f"   فعلي: عائلة={actual_family}, أطفال={actual_children}, زوجات={actual_wives}")
    print(f"   محسوب: عائلة={calculated_family}")
    
    if stored_family == calculated_family == actual_family:
        print("   ✅ متطابق")
    else:
        print("   ❌ غير متطابق")
    print()

print("=" * 80)
print("الخلاصة:")
print("=" * 80)

if total_from_stored != calculated_total:
    print("🔧 هناك مشكلة في العدادات المحفوظة")
    print("   الحل: إعادة حساب العدادات أو إعادة استيراد من Excel")
elif total_from_stored != actual_total:
    print("📊 العدادات المحفوظة صحيحة ولكن لا تطابق البيانات الفعلية")
    print("   هذا طبيعي إذا كانت العدادات من ملف Excel")
else:
    print("✅ كل شيء يبدو صحيحاً")

print(f"الرقم الذي يجب أن يظهر في الإحصائيات: {total_from_stored}") 