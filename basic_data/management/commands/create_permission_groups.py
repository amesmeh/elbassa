from django.core.management.base import BaseCommand
from basic_data.permissions import create_permission_groups

class Command(BaseCommand):
    help = 'إنشاء مجموعات المستخدمين مع الصلاحيات المناسبة'

    def handle(self, *args, **options):
        try:
            create_permission_groups()
            self.stdout.write(self.style.SUCCESS('تم إنشاء مجموعات المستخدمين بنجاح'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'حدث خطأ: {str(e)}')) 