#!/usr/bin/env python
"""
سكريبت للتحقق من العدادات في ملف Excel مقابل قاعدة البيانات
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

def check_excel_vs_database(excel_file_path):
    """مقارنة العدادات في ملف Excel مع قاعدة البيانات"""
    
    print("=" * 80)
    print("فحص العدادات: ملف Excel مقابل قاعدة البيانات")
    print("=" * 80)
    
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
        found_in_db = 0
        not_found_in_db = 0
        counters_match = 0
        counters_mismatch = 0
        
        mismatches = []
        
        print("التحقق من كل سجل...")
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
                found_in_db += 1
                
                # العدادات من قاعدة البيانات
                children_db_stored = guardian.children_count
                wives_db_stored = guardian.wives_count
                family_db_stored = guardian.family_members_count
                
                # العدادات الفعلية من العلاقات
                children_db_actual = guardian.children.count()
                wives_db_actual = guardian.wives.count()
                family_db_actual = 1 + children_db_actual + wives_db_actual
                
                # مقارنة العدادات
                excel_vs_stored_match = (
                    children_excel == children_db_stored and 
                    wives_excel == wives_db_stored and 
                    family_excel == family_db_stored
                )
                
                excel_vs_actual_match = (
                    children_excel == children_db_actual and 
                    wives_excel == wives_db_actual and 
                    family_excel == family_db_actual
                )
                
                stored_vs_actual_match = (
                    children_db_stored == children_db_actual and 
                    wives_db_stored == wives_db_actual and 
                    family_db_stored == family_db_actual
                )
                
                if excel_vs_stored_match and stored_vs_actual_match:
                    counters_match += 1
                else:
                    counters_mismatch += 1
                    mismatches.append({
                        'national_id': national_id,
                        'name': name,
                        'children_excel': children_excel,
                        'children_db_stored': children_db_stored,
                        'children_db_actual': children_db_actual,
                        'wives_excel': wives_excel,
                        'wives_db_stored': wives_db_stored,
                        'wives_db_actual': wives_db_actual,
                        'family_excel': family_excel,
                        'family_db_stored': family_db_stored,
                        'family_db_actual': family_db_actual,
                        'excel_vs_stored_match': excel_vs_stored_match,
                        'excel_vs_actual_match': excel_vs_actual_match,
                        'stored_vs_actual_match': stored_vs_actual_match
                    })
                
            except Guardian.DoesNotExist:
                not_found_in_db += 1
                print(f"❌ غير موجود في قاعدة البيانات: {national_id} - {name}")
        
        # طباعة النتائج
        print()
        print("=" * 80)
        print("ملخص النتائج:")
        print("=" * 80)
        print(f"إجمالي السجلات في Excel: {len(df)}")
        print(f"موجود في قاعدة البيانات: {found_in_db}")
        print(f"غير موجود في قاعدة البيانات: {not_found_in_db}")
        print(f"العدادات متطابقة: {counters_match}")
        print(f"العدادات غير متطابقة: {counters_mismatch}")
        print()
        
        # طباعة تفاصيل عدم التطابق
        if mismatches:
            print("تفاصيل عدم التطابق:")
            print("=" * 80)
            
            for i, mismatch in enumerate(mismatches[:10], 1):  # أول 10 فقط
                print(f"{i}. {mismatch['name']} ({mismatch['national_id']})")
                print(f"   الأطفال - Excel: {mismatch['children_excel']}, "
                      f"DB المحفوظ: {mismatch['children_db_stored']}, "
                      f"DB الفعلي: {mismatch['children_db_actual']}")
                print(f"   الزوجات - Excel: {mismatch['wives_excel']}, "
                      f"DB المحفوظ: {mismatch['wives_db_stored']}, "
                      f"DB الفعلي: {mismatch['wives_db_actual']}")
                print(f"   العائلة - Excel: {mismatch['family_excel']}, "
                      f"DB المحفوظ: {mismatch['family_db_stored']}, "
                      f"DB الفعلي: {mismatch['family_db_actual']}")
                print(f"   Excel vs المحفوظ: {'✅' if mismatch['excel_vs_stored_match'] else '❌'}")
                print(f"   Excel vs الفعلي: {'✅' if mismatch['excel_vs_actual_match'] else '❌'}")
                print(f"   المحفوظ vs الفعلي: {'✅' if mismatch['stored_vs_actual_match'] else '❌'}")
                print()
            
            if len(mismatches) > 10:
                print(f"... و {len(mismatches) - 10} حالات أخرى")
        
        # توصيات
        print("=" * 80)
        print("التوصيات:")
        print("=" * 80)
        
        if counters_mismatch > 0:
            print("🔧 يُنصح بتشغيل إحدى العمليات التالية:")
            print("   1. استخدام 'تحديث من Excel' لتطبيق العدادات من ملف Excel")
            print("   2. استخدام 'إصلاح العدادات' لحساب العدادات من البيانات الفعلية")
            print("   3. إعادة استيراد ملف Excel مع التأكد من صحة العدادات")
        else:
            print("✅ جميع العدادات متطابقة!")
        
    except Exception as e:
        print(f"❌ خطأ في قراءة الملف: {str(e)}")

def main():
    if len(sys.argv) != 2:
        print("الاستخدام: python check_excel_counters.py <مسار_ملف_Excel>")
        print("مثال: python check_excel_counters.py guardians.xlsx")
        return
    
    excel_file = sys.argv[1]
    
    if not os.path.exists(excel_file):
        print(f"❌ الملف غير موجود: {excel_file}")
        return
    
    if not excel_file.endswith('.xlsx'):
        print("❌ يجب أن يكون الملف بصيغة .xlsx")
        return
    
    check_excel_vs_database(excel_file)

if __name__ == "__main__":
    main() 