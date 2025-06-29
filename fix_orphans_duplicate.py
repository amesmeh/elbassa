#!/usr/bin/env python
# -*- coding: utf-8 -*-

# إصلاح الكود المكرر في ملف orphans/views.py

with open('orphans/views.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# إزالة الأسطر المكررة
cleaned_lines = []
skip_next = 0

for i, line in enumerate(lines):
    if skip_next > 0:
        skip_next -= 1
        continue
        
    # البحث عن النمط المكرر
    if "# البحث عن الحي إذا كان موجود" in line:
        # التحقق من وجود كود مكرر
        if i + 10 < len(lines) and "# البحث عن الحي إذا كان موجود" in lines[i + 10]:
            # إزالة الكود المكرر الأول
            skip_next = 9
            continue
    
    cleaned_lines.append(line)

with open('orphans/views.py', 'w', encoding='utf-8') as f:
    f.writelines(cleaned_lines)

print("تم إصلاح الكود المكرر!") 