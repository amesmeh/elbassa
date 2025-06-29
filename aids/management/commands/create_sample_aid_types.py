from django.core.management.base import BaseCommand
from aids.models import AidType

class Command(BaseCommand):
    help = 'إنشاء أنواع مساعدات تجريبية'

    def handle(self, *args, **options):
        aid_types_data = [
            # مواد غذائية
            {'name': 'أرز', 'category': 'food'},
            {'name': 'دقيق', 'category': 'food'},
            {'name': 'سكر', 'category': 'food'},
            {'name': 'زيت طبخ', 'category': 'food'},
            {'name': 'معلبات', 'category': 'food'},
            {'name': 'حليب أطفال', 'category': 'food'},
            {'name': 'خضروات', 'category': 'food'},
            
            # مساعدات طبية
            {'name': 'أدوية أطفال', 'category': 'medical'},
            {'name': 'أدوية مزمنة', 'category': 'medical'},
            {'name': 'مستلزمات طبية', 'category': 'medical'},
            {'name': 'فيتامينات', 'category': 'medical'},
            
            # ملابس
            {'name': 'ملابس أطفال', 'category': 'clothing'},
            {'name': 'ملابس رجالية', 'category': 'clothing'},
            {'name': 'ملابس نسائية', 'category': 'clothing'},
            {'name': 'أحذية', 'category': 'clothing'},
            {'name': 'بطانيات', 'category': 'clothing'},
            
            # مأوى
            {'name': 'خيام', 'category': 'shelter'},
            {'name': 'مراتب', 'category': 'shelter'},
            {'name': 'وسائد', 'category': 'shelter'},
            
            # مساعدات نقدية
            {'name': 'مساعدة نقدية شهرية', 'category': 'cash'},
            {'name': 'مساعدة طوارئ', 'category': 'cash'},
            
            # مساعدات تعليمية
            {'name': 'قرطاسية', 'category': 'education'},
            {'name': 'حقائب مدرسية', 'category': 'education'},
            {'name': 'كتب', 'category': 'education'},
            
            # أخرى
            {'name': 'مواد تنظيف', 'category': 'other'},
            {'name': 'مولدات كهرباء', 'category': 'other'},
            {'name': 'أدوات مطبخ', 'category': 'other'},
        ]

        created_count = 0
        for aid_data in aid_types_data:
            aid_type, created = AidType.objects.get_or_create(
                name=aid_data['name'],
                defaults={
                    'category': aid_data['category'],
                    'description': f"مساعدة من فئة {aid_data['name']}",
                    'is_active': True
                }
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'تم إنشاء نوع المساعدة: {aid_type.name}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'تم إنشاء {created_count} نوع مساعدة جديد بنجاح!')
        ) 