from django.core.management.base import BaseCommand
from django.utils import timezone
from aids.models import AidDistribution, AidType
from basic_data.models import Guardian
import random
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'إنشاء بيانات توزيع تجريبية'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=50,
            help='عدد سجلات التوزيع المراد إنشاؤها'
        )

    def handle(self, *args, **options):
        count = options['count']
        
        # التأكد من وجود أولياء أمور وأنواع مساعدات
        guardians = list(Guardian.objects.all())
        aid_types = list(AidType.objects.filter(is_active=True))
        
        if not guardians:
            self.stdout.write(
                self.style.ERROR('لا توجد أولياء أمور في النظام. يرجى إضافة بيانات أولياء الأمور أولاً.')
            )
            return
        
        if not aid_types:
            self.stdout.write(
                self.style.ERROR('لا توجد أنواع مساعدات في النظام. يرجى إضافة أنواع المساعدات أولاً.')
            )
            return
        
        # ملاحظات تجريبية
        sample_notes = [
            'توزيع طارئ',
            'مساعدة شهرية',
            'دعم خاص للعائلات النازحة',
            'مساعدة موسمية',
            'دعم إضافي',
            'توزيع استثنائي',
            'مساعدة عاجلة',
            '',  # بدون ملاحظات
            '',
            '',
        ]
        
        created_count = 0
        
        for i in range(count):
            # اختيار ولي أمر ونوع مساعدة عشوائي
            guardian = random.choice(guardians)
            aid_type = random.choice(aid_types)
            
            # تاريخ عشوائي خلال الـ 6 أشهر الماضية
            days_ago = random.randint(1, 180)
            distribution_date = timezone.now().date() - timedelta(days=days_ago)
            
            # ملاحظات عشوائية
            notes = random.choice(sample_notes)
            
            # حالة الترحيل عشوائية (70% غير مرحل، 30% مرحل)
            is_transferred = random.choice([False, False, False, False, False, False, False, True, True, True])
            
            # التأكد من عدم وجود توزيع مكرر لنفس الشخص ونفس النوع في نفس اليوم
            existing = AidDistribution.objects.filter(
                guardian=guardian,
                aid_type=aid_type,
                distribution_date=distribution_date
            ).exists()
            
            if not existing:
                AidDistribution.objects.create(
                    guardian=guardian,
                    aid_type=aid_type,
                    distribution_date=distribution_date,
                    notes=notes,
                    is_transferred=is_transferred
                )
                created_count += 1
        
        self.stdout.write(
            self.style.SUCCESS(f'تم إنشاء {created_count} سجل توزيع بنجاح!')
        )
        
        # إحصائيات
        total_distributions = AidDistribution.objects.count()
        transferred = AidDistribution.objects.filter(is_transferred=True).count()
        not_transferred = AidDistribution.objects.filter(is_transferred=False).count()
        
        self.stdout.write(f'إجمالي سجلات التوزيع: {total_distributions}')
        self.stdout.write(f'المرحل: {transferred}')
        self.stdout.write(f'غير المرحل: {not_transferred}') 