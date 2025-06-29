from django.core.management.base import BaseCommand
from basic_data.models import Child

class Command(BaseCommand):
    help = 'تحديث جنس الأطفال من الإنجليزية إلى العربية'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='عرض التحديثات بدون تطبيقها فعلياً',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        # خريطة تحويل الجنس
        gender_mapping = {
            'male': 'ذكر',
            'female': 'أنثى',
            'M': 'ذكر',
            'F': 'أنثى',
        }
        
        self.stdout.write("=== فحص وتحديث جنس الأطفال ===\n")
        
        total_updated = 0
        
        # تحديث الجنس
        self.stdout.write("🔍 فحص جنس الأطفال...")
        for old_value, new_value in gender_mapping.items():
            count = Child.objects.filter(gender=old_value).count()
            if count > 0:
                self.stdout.write(f"  - وُجد {count} طفل بجنس '{old_value}' سيتم تحديثه إلى '{new_value}'")
                if not dry_run:
                    Child.objects.filter(gender=old_value).update(gender=new_value)
                total_updated += count
        
        # عرض النتائج
        self.stdout.write("\n" + "="*50)
        if dry_run:
            self.stdout.write(self.style.WARNING(f"📊 تجربة جافة - سيتم تحديث {total_updated} سجل"))
        else:
            self.stdout.write(self.style.SUCCESS(f"✅ تم تحديث {total_updated} سجل بنجاح"))
        
        if dry_run:
            self.stdout.write("\n" + self.style.WARNING("💡 لتطبيق التحديثات فعلياً، شغل الأمر بدون --dry-run"))
        else:
            self.stdout.write("\n" + self.style.SUCCESS("🎉 تم إكمال التحديث بنجاح!"))
        
        # عرض إحصائيات البيانات الحالية
        self.stdout.write("\n📈 إحصائيات الجنس الحالية:")
        for gender in Child.objects.values_list('gender', flat=True).distinct():
            count = Child.objects.filter(gender=gender).count()
            self.stdout.write(f"  - {gender}: {count}")
        
        self.stdout.write(f"\n📊 إجمالي الأطفال: {Child.objects.count()}") 