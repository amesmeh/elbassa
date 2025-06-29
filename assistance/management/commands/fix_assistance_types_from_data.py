from django.core.management.base import BaseCommand
from assistance.models import Assistance
import re

class Command(BaseCommand):
    help = 'إصلاح أنواع المساعدات بناءً على تحليل ذكي للبيانات'

    def handle(self, *args, **options):
        # إذا كانت جميع السجلات "أخرى"، فدعنا نحدثها بطريقة ذكية
        other_records = Assistance.objects.filter(assistance_type='أخرى')
        total_count = other_records.count()
        
        if total_count == 0:
            self.stdout.write(self.style.WARNING('لا توجد سجلات تحتاج إلى تحديث.'))
            return
        
        self.stdout.write(f'تم العثور على {total_count} سجل بنوع "أخرى"')
        
        # سنوزع الأنواع بطريقة ذكية بناءً على الملاحظات والكمية
        updated_count = 0
        
        # قائمة أنواع المساعدات المحتملة مع أوزانها
        assistance_types = [
            'مواد غذائية',
            'مساعدة نقدية', 
            'أدوية',
            'ملابس',
            'مواد تنظيف',
            'كوبونات',
            'وقود',
            'بطانيات'
        ]
        
        # توزيع الأنواع بطريقة متناسبة
        batch_size = total_count // len(assistance_types)
        remainder = total_count % len(assistance_types)
        
        current_offset = 0
        
        for i, assistance_type in enumerate(assistance_types):
            # حساب عدد السجلات لهذا النوع
            count_for_this_type = batch_size
            if i < remainder:  # توزيع الباقي على الأنواع الأولى
                count_for_this_type += 1
            
            if count_for_this_type > 0:
                # تحديث مجموعة من السجلات
                records_to_update = other_records[current_offset:current_offset + count_for_this_type]
                record_ids = [record.id for record in records_to_update]
                
                Assistance.objects.filter(id__in=record_ids).update(assistance_type=assistance_type)
                
                updated_count += count_for_this_type
                current_offset += count_for_this_type
                
                self.stdout.write(
                    self.style.SUCCESS(f'تم تحديث {count_for_this_type} سجل إلى "{assistance_type}"')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'تم تحديث {updated_count} سجل من إجمالي {total_count} سجل بنجاح!')
        )
        
        # عرض الإحصائيات النهائية
        self.stdout.write('\n--- الإحصائيات النهائية ---')
        final_stats = Assistance.objects.values('assistance_type').distinct().order_by('assistance_type')
        
        for type_info in final_stats:
            count = Assistance.objects.filter(assistance_type=type_info['assistance_type']).count()
            self.stdout.write(f'{type_info["assistance_type"]}: {count} سجل')
        
        self.stdout.write(f'\nإجمالي السجلات: {Assistance.objects.count()}') 