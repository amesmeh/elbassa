#!/usr/bin/env python
"""
سكريبت لتطبيق العدادات من ملف Excel على قاعدة البيانات
"""

import os
import sys
import django
import pandas as pd

# إعداد Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mosa3adat_project.settings')
django.setup()

from basic_data.models import Guardian
from utils.excel_utils import clean_national_id

def apply_excel_counters(excel_file_path, dry_run=True):
    """تطبيق العدادات من ملف Excel على قاعدة البيانات"""
    
    print("=" * 80)
    print("تطبيق العدادات من ملف Excel")
    print("=" * 80)
    
    if dry_run:
        print("🔍 وضع المعاينة (لن يتم حفظ التغييرات)")
    else:
        print("💾 وضع التطبيق (سيتم حفظ التغييرات)")
    
    print()
    
    try:
        # قراءة ملف Excel
        df = pd.read_excel(excel_file_path, sheet_name=0)
        print(f"تم قراءة {len(df)} سجل من ملف Excel")
        
        # التحقق من وجود الأعمدة المطلوبة
        required_columns = ['رقم الهوية', 'اسم ولي الأمر', 'عدد الأبناء', 'عدد الزوجات']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            print(f"❌ أعمدة مفقودة في ملف Excel: {missing_columns}")
            return
        
        print("✅ جميع الأعمدة المطلوبة موجودة")
        print()
        
        # إحصائيات
        updated_count = 0
        not_found_count = 0
        no_change_count = 0
        
        updates = []
        
        print("معالجة السجلات...")
        print("-" * 80)
        
        for index, row in df.iterrows():
            if pd.isna(row['رقم الهوية']):
                continue
                
            national_id = clean_national_id(row['رقم الهوية'])
            name = row['اسم ولي الأمر']
            
            # العدادات من Excel
            children_excel = int(row['عدد الأبناء']) if not pd.isna(row['عدد الأبناء']) else 0
            wives_excel = int(row['عدد الزوجات']) if not pd.isna(row['عدد الزوجات']) else 0
            family_excel = 1 + children_excel + wives_excel
            
            try:
                guardian = Guardian.objects.get(national_id=national_id)
                
                # العدادات الحالية في قاعدة البيانات
                children_current = guardian.children_count
                wives_current = guardian.wives_count
                family_current = guardian.family_members_count
                
                # التحقق من الحاجة للتحديث
                needs_update = (
                    children_excel != children_current or 
                    wives_excel != wives_current or 
                    family_excel != family_current
                )
                
                if needs_update:
                    updates.append({
                        'guardian': guardian,
                        'national_id': national_id,
                        'name': name,
                        'children_old': children_current,
                        'children_new': children_excel,
                        'wives_old': wives_current,
                        'wives_new': wives_excel,
                        'family_old': family_current,
                        'family_new': family_excel
                    })
                    
                    if not dry_run:
                        guardian.children_count = children_excel
                        guardian.wives_count = wives_excel
                        guardian.family_members_count = family_excel
                        guardian.save()
                    
                    updated_count += 1
                    print(f"✏️  {name} ({national_id})")
                    print(f"    الأطفال: {children_current} → {children_excel}")
                    print(f"    الزوجات: {wives_current} → {wives_excel}")
                    print(f"    العائلة: {family_current} → {family_excel}")
                    print()
                else:
                    no_change_count += 1
                
            except Guardian.DoesNotExist:
                not_found_count += 1
                print(f"❌ غير موجود في قاعدة البيانات: {national_id} - {name}")
        
        # طباعة النتائج
        print()
        print("=" * 80)
        print("ملخص العملية:")
        print("=" * 80)
        print(f"إجمالي السجلات في Excel: {len(df)}")
        print(f"تم التحديث: {updated_count}")
        print(f"لا يحتاج تحديث: {no_change_count}")
        print(f"غير موجود في قاعدة البيانات: {not_found_count}")
        print()
        
        if dry_run and updated_count > 0:
            print("🔍 هذه معاينة فقط. لتطبيق التغييرات، استخدم:")
            print(f"python {sys.argv[0]} {excel_file_path} --apply")
        elif not dry_run and updated_count > 0:
            print("✅ تم تطبيق جميع التحديثات بنجاح!")
        elif updated_count == 0:
            print("ℹ️  لا توجد تحديثات مطلوبة. جميع العدادات متطابقة.")
        
    except Exception as e:
        print(f"❌ خطأ في معالجة الملف: {str(e)}")

def main():
    if len(sys.argv) < 2:
        print("الاستخدام:")
        print("  للمعاينة: python apply_excel_counters.py <مسار_ملف_Excel>")
        print("  للتطبيق: python apply_excel_counters.py <مسار_ملف_Excel> --apply")
        print()
        print("مثال:")
        print("  python apply_excel_counters.py guardians.xlsx")
        print("  python apply_excel_counters.py guardians.xlsx --apply")
        return
    
    excel_file = sys.argv[1]
    apply_changes = len(sys.argv) > 2 and sys.argv[2] == '--apply'
    
    if not os.path.exists(excel_file):
        print(f"❌ الملف غير موجود: {excel_file}")
        return
    
    if not excel_file.endswith('.xlsx'):
        print("❌ يجب أن يكون الملف بصيغة .xlsx")
        return
    
    if apply_changes:
        confirm = input("⚠️  هل أنت متأكد من تطبيق التغييرات؟ (نعم/لا): ")
        if confirm.lower() not in ['نعم', 'yes', 'y']:
            print("تم إلغاء العملية.")
            return
    
    apply_excel_counters(excel_file, dry_run=not apply_changes)

if __name__ == "__main__":
    main() 