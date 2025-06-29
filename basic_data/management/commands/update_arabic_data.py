from django.core.management.base import BaseCommand
from basic_data.models import Guardian

class Command(BaseCommand):
    help = 'تحديث البيانات الإنجليزية إلى العربية في قاعدة البيانات'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='عرض التحديثات بدون تطبيقها فعلياً',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        # خريطة تحويل الحالة الاجتماعية
        marital_status_mapping = {
            'married': 'متزوج',
            'widowed': 'أرمل', 
            'divorced': 'مطلق',
            'single': 'أعزب',
        }
        
        # خريطة تحويل حالة الإقامة
        residence_status_mapping = {
            'displaced': 'نازح',
            'resident': 'مقيم',
        }
        
        # خريطة تحويل الجنس
        gender_mapping = {
            'male': 'ذكر',
            'female': 'أنثى',
            'M': 'ذكر',
            'F': 'أنثى',
        }
        
        total_updated = 0
        
        self.stdout.write("=== فحص وتحديث البيانات ===\n")
        
        # تحديث الحالة الاجتماعية
        self.stdout.write("🔍 فحص الحالة الاجتماعية...")
        marital_updated = 0
        for old_value, new_value in marital_status_mapping.items():
            count = Guardian.objects.filter(marital_status=old_value).count()
            if count > 0:
                self.stdout.write(f"  - وُجد {count} ولي أمر بحالة '{old_value}' سيتم تحديثها إلى '{new_value}'")
                if not dry_run:
                    Guardian.objects.filter(marital_status=old_value).update(marital_status=new_value)
                marital_updated += count
        
        # تحديث حالة الإقامة
        self.stdout.write("\n🔍 فحص حالة الإقامة...")
        residence_updated = 0
        for old_value, new_value in residence_status_mapping.items():
            count = Guardian.objects.filter(residence_status=old_value).count()
            if count > 0:
                self.stdout.write(f"  - وُجد {count} ولي أمر بحالة إقامة '{old_value}' سيتم تحديثها إلى '{new_value}'")
                if not dry_run:
                    Guardian.objects.filter(residence_status=old_value).update(residence_status=new_value)
                residence_updated += count
        
        # تحديث الجنس
        self.stdout.write("\n🔍 فحص الجنس...")
        gender_updated = 0
        for old_value, new_value in gender_mapping.items():
            count = Guardian.objects.filter(gender=old_value).count()
            if count > 0:
                self.stdout.write(f"  - وُجد {count} ولي أمر بجنس '{old_value}' سيتم تحديثه إلى '{new_value}'")
                if not dry_run:
                    Guardian.objects.filter(gender=old_value).update(gender=new_value)
                gender_updated += count
        
        total_updated = marital_updated + residence_updated + gender_updated
        
        # عرض النتائج
        self.stdout.write("\n" + "="*50)
        if dry_run:
            self.stdout.write(self.style.WARNING(f"📊 تجربة جافة - سيتم تحديث {total_updated} سجل:"))
        else:
            self.stdout.write(self.style.SUCCESS(f"✅ تم تحديث {total_updated} سجل بنجاح:"))
        
        self.stdout.write(f"  • الحالة الاجتماعية: {marital_updated} سجل")
        self.stdout.write(f"  • حالة الإقامة: {residence_updated} سجل") 
        self.stdout.write(f"  • الجنس: {gender_updated} سجل")
        
        if dry_run:
            self.stdout.write("\n" + self.style.WARNING("💡 لتطبيق التحديثات فعلياً، شغل الأمر بدون --dry-run"))
        else:
            self.stdout.write("\n" + self.style.SUCCESS("🎉 تم إكمال التحديث بنجاح!"))
        
        # عرض إحصائيات البيانات الحالية
        self.stdout.write("\n📈 إحصائيات البيانات الحالية:")
        
        # الحالة الاجتماعية
        self.stdout.write("  الحالة الاجتماعية:")
        for status in Guardian.objects.values_list('marital_status', flat=True).distinct():
            count = Guardian.objects.filter(marital_status=status).count()
            self.stdout.write(f"    - {status}: {count}")
        
        # حالة الإقامة
        self.stdout.write("  حالة الإقامة:")
        for status in Guardian.objects.values_list('residence_status', flat=True).distinct():
            count = Guardian.objects.filter(residence_status=status).count()
            self.stdout.write(f"    - {status}: {count}")
        
        # الجنس
        self.stdout.write("  الجنس:")
        for gender in Guardian.objects.values_list('gender', flat=True).distinct():
            count = Guardian.objects.filter(gender=gender).count()
            self.stdout.write(f"    - {gender}: {count}")
        
        self.stdout.write(f"\n📊 إجمالي أولياء الأمور: {Guardian.objects.count()}") 