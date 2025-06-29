#!/usr/bin/env python
import os
import sys
import django

# إعداد Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mosa3adat_project.settings')
django.setup()

from basic_data.utils import normalize_arabic_text, search_guardians
from martyrs.utils import search_martyrs

def test_normalization():
    """اختبار تطبيع النص العربي"""
    print("=== اختبار تطبيع النص العربي ===")
    
    test_cases = [
        "إبراهيم الكحلوت",
        "ابراهيم الكحلوت", 
        "أبراهيم الكحلوت",
        "محمد الشهيد",
        "محمد أحمد الشهيد"
    ]
    
    for text in test_cases:
        normalized = normalize_arabic_text(text)
        print(f"الأصلي: {text}")
        print(f"المطبع: {normalized}")
        print("---")

def test_guardians_search():
    """اختبار البحث في أولياء الأمور"""
    print("\n=== اختبار البحث في أولياء الأمور ===")
    
    # البحث بـ "إبراهيم الكحلوت"
    print("البحث بـ 'إبراهيم الكحلوت':")
    results1 = search_guardians("إبراهيم الكحلوت")
    print(f"عدد النتائج: {results1.count()}")
    for guardian in results1[:3]:
        print(f"- {guardian.name}")
    
    print("\nالبحث بـ 'ابراهيم الكحلوت':")
    results2 = search_guardians("ابراهيم الكحلوت")
    print(f"عدد النتائج: {results2.count()}")
    for guardian in results2[:3]:
        print(f"- {guardian.name}")
    
    print("\nالبحث بـ 'ابراهيم':")
    results3 = search_guardians("ابراهيم")
    print(f"عدد النتائج: {results3.count()}")
    for guardian in results3[:3]:
        print(f"- {guardian.name}")

def test_martyrs_search():
    """اختبار البحث في الشهداء"""
    print("\n=== اختبار البحث في الشهداء ===")
    
    # البحث بـ "محمد الشهيد"
    print("البحث بـ 'محمد الشهيد':")
    results1 = search_martyrs("محمد الشهيد")
    print(f"عدد النتائج: {results1.count()}")
    for martyr in results1[:3]:
        print(f"- {martyr.name}")
    
    print("\nالبحث بـ 'محمد':")
    results2 = search_martyrs("محمد")
    print(f"عدد النتائج: {results2.count()}")
    for martyr in results2[:3]:
        print(f"- {martyr.name}")

if __name__ == "__main__":
    test_normalization()
    test_guardians_search()
    test_martyrs_search() 