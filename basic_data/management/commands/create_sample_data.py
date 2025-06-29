from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date, timedelta
import random
import faker

from basic_data.models import District, Guardian, Wife, Child
from martyrs.models import Martyr
from injured.models import Injured
from medical.models import MedicalRecord
from damages.models import Damage
from orphans.models import Orphan
from assistance.models import Assistance

class Command(BaseCommand):
    help = 'إنشاء بيانات تجريبية للاختبار'

    def handle(self, *args, **options):
        self.stdout.write('بدء إنشاء البيانات التجريبية...')
        
        # إنشاء المناطق
        districts_data = [
            'الشجاعية', 'الزيتون', 'التفاح', 'الدرج', 'الصبرة',
            'جباليا', 'بيت حانون', 'بيت لاهيا', 'العطاطرة', 'أم النصر',
            'النصيرات', 'البريج', 'المغازي', 'دير البلح', 'الزوايدة',
            'خان يونس', 'بني سهيلا', 'عبسان', 'القرارة', 'المعن',
            'رفح', 'الشوكة', 'تل السلطان', 'البرازيل', 'الجنينة'
        ]
        
        districts = []
        for district_name in districts_data:
            district, created = District.objects.get_or_create(
                name=district_name,
                defaults={
                    'representative_name': f'مندوب {district_name}',
                    'representative_phone': f'059{random.randint(1000000, 9999999)}'
                }
            )
            districts.append(district)
            if created:
                self.stdout.write(f'تم إنشاء المنطقة: {district_name}')

        # إنشاء أولياء أمور
        guardians_data = [
            ('أحمد محمد علي', 'ذكر', 'متزوج', 'مقيم'),
            ('فاطمة سعد حسن', 'أنثى', 'أرمل', 'نازح'),
            ('محمود عبد الله', 'ذكر', 'متزوج', 'مقيم'),
            ('خديجة أحمد', 'أنثى', 'مطلق', 'نازح'),
            ('عمر يوسف', 'ذكر', 'أعزب', 'مقيم'),
            ('زينب محمد', 'أنثى', 'متزوج', 'نازح'),
            ('سامي عبد الرحمن', 'ذكر', 'متزوج', 'مقيم'),
            ('نور الدين', 'أنثى', 'أرمل', 'نازح'),
            ('خالد إبراهيم', 'ذكر', 'متزوج', 'مقيم'),
            ('مريم سليمان', 'أنثى', 'متزوج', 'نازح'),
        ]
        
        guardians = []
        for i, (name, gender, marital_status, residence_status) in enumerate(guardians_data):
            guardian, created = Guardian.objects.get_or_create(
                national_id=f'{400000000 + i}',
                defaults={
                    'name': name,
                    'gender': gender,
                    'marital_status': marital_status,
                    'residence_status': residence_status,
                    'phone_number': f'059{random.randint(1000000, 9999999)}',
                    'children_count': random.randint(0, 6),
                    'district': random.choice(districts),
                    'current_job': random.choice(['موظف', 'عامل', 'تاجر', 'عاطل', 'متقاعد']),
                    'original_governorate': random.choice(['غزة', 'شمال غزة', 'الوسطى', 'خان يونس', 'رفح']),
                    'original_city': random.choice(['غزة', 'جباليا', 'دير البلح', 'خان يونس', 'رفح'])
                }
            )
            guardians.append(guardian)
            if created:
                self.stdout.write(f'تم إنشاء ولي الأمر: {name}')

        # إنشاء شهداء
        martyrs_data = [
            ('محمد أحمد الشهيد', 'father'),
            ('علي سعد المجاهد', 'brother'),
            ('يوسف عبد الله', 'son'),
            ('إبراهيم محمود', 'uncle'),
            ('عمر خالد', 'cousin'),
        ]
        
        for i, (name, relationship) in enumerate(martyrs_data):
            martyr, created = Martyr.objects.get_or_create(
                national_id=f'{500000000 + i}',
                defaults={
                    'name': name,
                    'martyrdom_date': date.today() - timedelta(days=random.randint(1, 365)),
                    'agent_name': random.choice(guardians).name,
                    'agent_national_id': f'{600000000 + i}',
                    'agent_phone': f'059{random.randint(1000000, 9999999)}',
                    'relationship_to_martyr': relationship,
                    'district': random.choice(districts),
                    'notes': f'ملاحظات عن الشهيد {name}'
                }
            )
            if created:
                self.stdout.write(f'تم إنشاء سجل الشهيد: {name}')

        # إنشاء جرحى
        injured_data = [
            ('سامي محمد الجريح', 'gunshot'),
            ('نور أحمد', 'shrapnel'),
            ('خالد عبد الله', 'explosion'),
            ('فاطمة سعد', 'burn'),
            ('محمود علي', 'fracture'),
        ]
        
        for i, (name, injury_type) in enumerate(injured_data):
            guardian = random.choice(guardians)
            injured, created = Injured.objects.get_or_create(
                national_id=f'{700000000 + i}',
                defaults={
                    'name': name,
                    'guardian_national_id': guardian.national_id,
                    'injury_date': date.today() - timedelta(days=random.randint(1, 200)),
                    'injury_type': injury_type,
                    'injury_description': f'وصف الإصابة لـ {name}',
                    'notes': f'ملاحظات عن الجريح {name}'
                }
            )
            if created:
                self.stdout.write(f'تم إنشاء سجل الجريح: {name}')

        # إنشاء سجلات مرضية
        medical_data = [
            ('أحمد المريض', 'ذكر', 'diabetes'),
            ('فاطمة المريضة', 'أنثى', 'heart'),
            ('محمد المصاب', 'ذكر', 'kidney'),
            ('زينب المعاقة', 'أنثى', 'chronic'),
            ('عمر المريض', 'ذكر', 'cancer'),
        ]
        
        for i, (name, gender, disease_type) in enumerate(medical_data):
            guardian = random.choice(guardians)
            medical, created = MedicalRecord.objects.get_or_create(
                national_id=f'{800000000 + i}',
                defaults={
                    'name': name,
                    'gender': gender,
                    'guardian_national_id': guardian.national_id,
                    'disease_type': disease_type,
                    'disease_description': f'وصف المرض لـ {name}',
                    'disability_type': random.choice(['none', 'physical', 'visual', 'hearing']),
                    'disability_percentage': random.randint(0, 100) if random.choice([True, False]) else None,
                    'notes': f'ملاحظات طبية عن {name}'
                }
            )
            if created:
                self.stdout.write(f'تم إنشاء السجل المرضي: {name}')

        # إنشاء أضرار
        damage_data = [
            ('owned', 'house', 'total'),
            ('rented', 'apartment', 'partial'),
            ('owned', 'shop', 'total'),
            ('rented', 'house', 'partial'),
            ('owned', 'apartment', 'total'),
        ]
        
        for i, (ownership, housing_type, damage_type) in enumerate(damage_data):
            guardian = random.choice(guardians)
            damage, created = Damage.objects.get_or_create(
                guardian_national_id=guardian.national_id,
                housing_type=housing_type,
                defaults={
                    'ownership_type': ownership,
                    'housing_condition': random.choice(['good', 'fair', 'poor']),
                    'construction_type': random.choice(['concrete', 'asbestos', 'mixed']),
                    'floors_count': random.randint(1, 4),
                    'damage_type': damage_type,
                    'damage_percentage': random.randint(20, 100),
                    'damage_date': date.today() - timedelta(days=random.randint(1, 100)),
                    'notes': f'ملاحظات عن الضرر'
                }
            )
            if created:
                self.stdout.write(f'تم إنشاء سجل ضرر: {guardian.name}')

        # إنشاء أيتام
        orphans_data = [
            ('محمد اليتيم', 'ذكر', 'elementary'),
            ('فاطمة اليتيمة', 'أنثى', 'middle'),
            ('أحمد الصغير', 'ذكر', 'kindergarten'),
            ('زينب الطفلة', 'أنثى', 'elementary'),
            ('عمر اليافع', 'ذكر', 'high'),
        ]
        
        for i, (name, gender, education_level) in enumerate(orphans_data):
            orphan, created = Orphan.objects.get_or_create(
                national_id=f'{900000000 + i}',
                defaults={
                    'name': name,
                    'gender': gender,
                    'birth_date': date.today() - timedelta(days=random.randint(365*2, 365*17)),
                    'health_status': random.choice(['excellent', 'good', 'fair']),
                    'education_level': education_level,
                    'deceased_national_id': f'{950000000 + i}',
                    'deceased_name': f'والد {name}',
                    'male_siblings_count': random.randint(0, 3),
                    'female_siblings_count': random.randint(0, 3),
                    'guardian_name': f'وصي {name}',
                    'guardian_relationship': random.choice(['grandfather', 'uncle', 'aunt']),
                    'phone_number': f'059{random.randint(1000000, 9999999)}',
                    'district': random.choice(districts),
                    'notes': f'ملاحظات عن اليتيم {name}'
                }
            )
            if created:
                self.stdout.write(f'تم إنشاء سجل اليتيم: {name}')

        self.stdout.write(
            self.style.SUCCESS('تم إنشاء جميع البيانات التجريبية بنجاح!')
        ) 