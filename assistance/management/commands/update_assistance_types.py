from django.core.management.base import BaseCommand
from assistance.models import Assistance

class Command(BaseCommand):
    help = 'تحديث أنواع المساعدات من الإنجليزية إلى العربية'

    def handle(self, *args, **options):
        # قاموس التحويل من الإنجليزية إلى العربية
        conversion_map = {
            'other': 'أخرى',
            'food': 'مواد غذائية',
            'cash': 'مساعدة نقدية',
            'medicine': 'أدوية',
            'clothes': 'ملابس',
            'medical_equipment': 'أجهزة طبية',
            'fuel': 'وقود',
            'cleaning_supplies': 'مواد تنظيف',
            'vouchers': 'كوبونات',
            'blankets': 'بطانيات',
            'shelter': 'مأوى',
            'education': 'تعليم',
            'water': 'مياه',
        }
        
        updated_count = 0
        
        for english_value, arabic_value in conversion_map.items():
            # البحث عن جميع السجلات التي تحتوي على القيمة الإنجليزية
            assistances_to_update = Assistance.objects.filter(assistance_type=english_value)
            count = assistances_to_update.count()
            
            if count > 0:
                # تحديث القيم
                assistances_to_update.update(assistance_type=arabic_value)
                updated_count += count
                self.stdout.write(
                    self.style.SUCCESS(f'تم تحديث {count} سجل من "{english_value}" إلى "{arabic_value}"')
                )
        
        if updated_count > 0:
            self.stdout.write(
                self.style.SUCCESS(f'تم تحديث {updated_count} سجل بنجاح!')
            )
        else:
            self.stdout.write(
                self.style.WARNING('لم يتم العثور على أي سجلات تحتاج إلى تحديث.')
            )
        
        # عرض إحصائيات الأنواع الحالية
        self.stdout.write('\n--- إحصائيات أنواع المساعدات الحالية ---')
        current_types = Assistance.objects.values('assistance_type').distinct().order_by('assistance_type')
        
        for type_info in current_types:
            count = Assistance.objects.filter(assistance_type=type_info['assistance_type']).count()
            self.stdout.write(f'{type_info["assistance_type"]}: {count} سجل') 