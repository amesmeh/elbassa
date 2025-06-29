from django.core.management.base import BaseCommand
from assistance.models import Assistance
import random

class Command(BaseCommand):
    help = 'تحديث أنواع المساعدات بأسماء واقعية كما في الكشف الفعلي'

    def handle(self, *args, **options):
        # قائمة أسماء المساعدات الواقعية كما تأتي في الكشوف
        realistic_assistance_types = [
            # طرود غذائية
            'طرد غذائي كريستال',
            'طرد غذائي الوكالة',
            'طرد غذائي أونروا',
            'طرد غذائي رمضان',
            'سلة غذائية شاملة',
            'مؤن غذائية أساسية',
            
            # مساعدات نقدية
            'مساعدة نقدية 500 شيكل',
            'مساعدة نقدية 300 شيكل',
            'مساعدة نقدية طوارئ',
            'كوبون تسوق 200 شيكل',
            
            # ملابس
            'حرامات شتوية',
            'ملابس أطفال',
            'أحذية شتوية',
            'بطانيات صوف',
            'ملابس داخلية',
            'جوارب وقبعات',
            
            # أدوية ومستلزمات طبية
            'أدوية مزمنة',
            'أدوية أطفال',
            'مستلزمات طبية',
            'حفاضات أطفال',
            'أدوية ضغط وسكري',
            
            # مواد تنظيف ومستلزمات منزلية
            'مواد تنظيف أساسية',
            'صابون ومنظفات',
            'مستلزمات نظافة شخصية',
            'مناديل ومستلزمات',
            
            # وقود وطاقة
            'بطارية غاز للطبخ',
            'شحن غاز منزلي',
            'كوبون محروقات',
            
            # مساعدات متنوعة
            'مستلزمات مدرسية',
            'حقائب مدرسية',
            'قرطاسية وأدوات',
            'مستلزمات نسائية',
            'مواد إسعافات أولية',
            'معقمات وكمامات',
            'مياه شرب',
            'فرش ومستلزمات نوم',
            'أواني منزلية',
            'مولد كهرباء صغير',
        ]
        
        # الحصول على جميع السجلات
        all_records = list(Assistance.objects.all())
        total_count = len(all_records)
        
        if total_count == 0:
            self.stdout.write(self.style.WARNING('لا توجد سجلات في قاعدة البيانات.'))
            return
        
        self.stdout.write(f'تم العثور على {total_count} سجل لتحديثه بأسماء واقعية')
        
        # خلط قائمة السجلات لتوزيع عشوائي
        random.shuffle(all_records)
        
        updated_count = 0
        type_counts = {}
        
        # توزيع أنواع المساعدات بشكل عشوائي على السجلات
        for i, record in enumerate(all_records):
            # اختيار نوع مساعدة عشوائي
            assistance_type = random.choice(realistic_assistance_types)
            
            # تحديث السجل
            record.assistance_type = assistance_type
            record.save()
            
            # تتبع الإحصائيات
            if assistance_type in type_counts:
                type_counts[assistance_type] += 1
            else:
                type_counts[assistance_type] = 1
            
            updated_count += 1
            
            # عرض التقدم كل 1000 سجل
            if (i + 1) % 1000 == 0:
                self.stdout.write(f'تم تحديث {i + 1} من {total_count} سجل...')
        
        self.stdout.write(
            self.style.SUCCESS(f'تم تحديث {updated_count} سجل بأسماء مساعدات واقعية!')
        )
        
        # عرض الإحصائيات النهائية
        self.stdout.write('\n--- إحصائيات أنواع المساعدات الجديدة ---')
        
        # ترتيب الأنواع حسب العدد
        sorted_types = sorted(type_counts.items(), key=lambda x: x[1], reverse=True)
        
        for assistance_type, count in sorted_types:
            self.stdout.write(f'{assistance_type}: {count} سجل')
        
        self.stdout.write(f'\nإجمالي أنواع المساعدات: {len(type_counts)}')
        self.stdout.write(f'إجمالي السجلات: {updated_count}')
        
        # التحقق من التحديث
        verification_count = Assistance.objects.exclude(
            assistance_type__in=['أخرى', 'مواد غذائية', 'مساعدة نقدية', 'أدوية', 'ملابس', 'مواد تنظيف']
        ).count()
        
        self.stdout.write(f'عدد السجلات بأسماء جديدة: {verification_count}') 