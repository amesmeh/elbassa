from django.core.management.base import BaseCommand
from basic_data.models import Guardian, District
import random

class Command(BaseCommand):
    help = 'إنشاء أولياء أمور تجريبيين'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=20,
            help='عدد أولياء الأمور المراد إنشاؤهم'
        )

    def handle(self, *args, **options):
        count = options['count']
        
        # أسماء تجريبية
        first_names = [
            'محمد', 'أحمد', 'عبد الله', 'عمر', 'علي', 'حسن', 'يوسف', 'إبراهيم',
            'خالد', 'سعد', 'فهد', 'عبد العزيز', 'عبد الرحمن', 'ماجد', 'طارق',
            'عاطف', 'سعيد', 'محمود', 'حسام', 'وليد', 'نبيل', 'رامي', 'عادل'
        ]
        
        middle_names = [
            'سعيد', 'محمد', 'أحمد', 'علي', 'حسن', 'عبد الله', 'إبراهيم',
            'يوسف', 'عمر', 'خالد', 'فهد', 'ماجد', 'طارق', 'عادل'
        ]
        
        last_names = [
            'مسمح', 'الأغا', 'أبو شعبان', 'النجار', 'الحلو', 'عاشور', 'البرعي',
            'سلامة', 'عوض', 'الفرا', 'أبو عودة', 'الشاعر', 'قديح', 'الدلو',
            'أبو ريدة', 'الكحلوت', 'أبو حسنين', 'الغندور', 'أبو عمرة', 'الطويل'
        ]
        
        # الحصول على الأحياء
        districts = list(District.objects.all())
        if not districts:
            self.stdout.write(
                self.style.ERROR('لا توجد أحياء في النظام. يرجى إضافة الأحياء أولاً.')
            )
            return
        
        created_count = 0
        
        for i in range(count):
            # إنشاء اسم عشوائي
            first_name = random.choice(first_names)
            middle_name = random.choice(middle_names)
            last_name = random.choice(last_names)
            full_name = f"{first_name} {middle_name} {last_name}"
            
            # رقم هوية عشوائي (9 أرقام)
            national_id = f"{random.randint(100000000, 999999999)}"
            
            # رقم جوال عشوائي
            phone_number = f"059{random.randint(1000000, 9999999)}"
            
            # حي عشوائي
            district = random.choice(districts)
            
            # جنس عشوائي
            gender = random.choice(['ذكر', 'أنثى'])
            
            # حالة إقامة عشوائية
            residence_status = random.choice(['مقيم', 'نازح'])
            
            # التأكد من عدم تكرار رقم الهوية
            if not Guardian.objects.filter(national_id=national_id).exists():
                Guardian.objects.create(
                    name=full_name,
                    national_id=national_id,
                    phone_number=phone_number,
                    district=district,
                    gender=gender,
                    residence_status=residence_status
                )
                created_count += 1
        
        self.stdout.write(
            self.style.SUCCESS(f'تم إنشاء {created_count} ولي أمر بنجاح!')
        )
        
        # إحصائيات
        total_guardians = Guardian.objects.count()
        male_count = Guardian.objects.filter(gender='ذكر').count()
        female_count = Guardian.objects.filter(gender='أنثى').count()
        resident_count = Guardian.objects.filter(residence_status='مقيم').count()
        displaced_count = Guardian.objects.filter(residence_status='نازح').count()
        
        self.stdout.write(f'إجمالي أولياء الأمور: {total_guardians}')
        self.stdout.write(f'ذكور: {male_count} | إناث: {female_count}')
        self.stdout.write(f'مقيمين: {resident_count} | نازحين: {displaced_count}') 