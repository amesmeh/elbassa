from django.shortcuts import render
from django.db.models import Count, Q, Sum, Avg, F
from django.db.models.functions import Extract
from datetime import date, datetime
from basic_data.models import Guardian, District, Child, Wife
from martyrs.models import Martyr
from injured.models import Injured
from medical.models import MedicalRecord
from damages.models import Damage
from orphans.models import Orphan

# استيراد نظام المساعدات
try:
    from assistance.models import Assistance
except ImportError:
    Assistance = None

# إضافة استيراد نظام التصدير
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
# from utils.pdf_export import ArabicPDFExporter

def statistics_dashboard(request):
    """لوحة الإحصائيات الرئيسية الشاملة"""
    
    try:
        # إحصائيات العائلات والمقيمين
        total_families = Guardian.objects.count()
        small_families = Guardian.objects.filter(family_members_count__lte=3).count()
        medium_families = Guardian.objects.filter(
            family_members_count__gte=4,
            family_members_count__lte=6
        ).count()
        large_families = Guardian.objects.filter(family_members_count__gte=7).count()
        
        # حساب النسب المئوية
        small_percentage = (small_families * 100 / total_families) if total_families > 0 else 0
        medium_percentage = (medium_families * 100 / total_families) if total_families > 0 else 0
        large_percentage = (large_families * 100 / total_families) if total_families > 0 else 0
        
        # حساب إجمالي المقيمين بطريقة دقيقة
        try:
            # عدد أولياء الأمور
            total_guardians = Guardian.objects.count()
            # عدد الزوجات من جدول الزوجات المنفصل
            total_wives = Wife.objects.count()
            # عدد الأطفال من جدول الأطفال المنفصل
            total_children = Child.objects.count()
            
            # إجمالي المقيمين = أولياء الأمور + الزوجات + الأطفال
            total_residents_calculated = total_guardians + total_wives + total_children
        except Exception as e:
            print(f"خطأ في حساب المقيمين بالطريقة الدقيقة: {e}")
            # في حالة الخطأ، استخدم الطريقة القديمة
            total_residents_calculated = Guardian.objects.aggregate(
                total=Sum('family_members_count')
            )['total'] or 0
        
        family_stats = {
            'total_families': total_families,
            'total_residents': total_residents_calculated,
            'total_displaced': Guardian.objects.filter(
                residence_status='نازح'
            ).count(),
            'families_by_size': {
                'small': small_families,
                'medium': medium_families,
                'large': large_families,
                'small_percentage': round(small_percentage, 1),
                'medium_percentage': round(medium_percentage, 1),
                'large_percentage': round(large_percentage, 1),
            }
        }
        
        # إحصائيات حسب الحي - محسّنة لتعطي أرقام دقيقة
        try:
            # حساب دقيق للأعضاء في كل حي
            district_stats_raw = Guardian.objects.values('district__name').annotate(
                families_count=Count('id'),
                guardians_count=Count('id'),  # عدد أولياء الأمور
            ).order_by('-families_count')[:10]
            
            district_stats = []
            for district_data in district_stats_raw:
                district_name = district_data['district__name']
                families_count = district_data['families_count']
                
                # حساب دقيق للأعضاء في هذا الحي
                try:
                    # أولياء الأمور في هذا الحي
                    guardians_in_district = Guardian.objects.filter(
                        district__name=district_name
                    ).count() if district_name else 0
                    
                    # الزوجات في هذا الحي
                    wives_in_district = Wife.objects.filter(
                        guardian__district__name=district_name
                    ).count() if district_name else 0
                    
                    # الأطفال في هذا الحي
                    children_in_district = Child.objects.filter(
                        guardian__district__name=district_name
                    ).count() if district_name else 0
                    
                    total_members = guardians_in_district + wives_in_district + children_in_district
                except:
                    # في حالة الخطأ، استخدم الطريقة القديمة
                    total_members = Guardian.objects.filter(
                        district__name=district_name
                    ).aggregate(total=Sum('family_members_count'))['total'] or 0
                
                district_stats.append({
                    'district__name': district_name,
                    'families_count': families_count,
                    'total_members': total_members
                })
        except Exception as e:
            print(f"خطأ في إحصائيات المناطق: {e}")
            # الطريقة القديمة في حالة الخطأ
            district_stats = Guardian.objects.values('district__name').annotate(
                families_count=Count('id'),
                total_members=Sum('family_members_count')
            ).order_by('-families_count')[:10]
        
        # إحصائيات حسب الحالة الاجتماعية
        marital_status_stats = Guardian.objects.values('marital_status').annotate(
            count=Count('id')
        )
        
        # إحصائيات الأبناء حسب الجنس من جدول الأطفال (مع معالجة أخطاء)
        try:
            children_by_gender = {
                'male_children': Child.objects.filter(gender='ذكر').count(),
                'female_children': Child.objects.filter(gender='أنثى').count(),
            }
        except:
            children_by_gender = {
                'male_children': 0,
                'female_children': 0,
            }
        
        # إحصائيات المراحل العمرية بناءً على العمر الفعلي (مع معالجة أخطاء)
        try:
            from datetime import date
            current_year = date.today().year
            
            age_groups = {
                'preschool': Child.objects.extra(
                    where=[f"{current_year} - CAST(strftime('%%Y', birth_date) AS INTEGER) < 6"]
                ).count(),
                'school': Child.objects.extra(
                    where=[f"{current_year} - CAST(strftime('%%Y', birth_date) AS INTEGER) BETWEEN 6 AND 17"]
                ).count(),
                'university': Child.objects.extra(
                    where=[f"{current_year} - CAST(strftime('%%Y', birth_date) AS INTEGER) BETWEEN 18 AND 25"]
                ).count(),
            }
        except:
            age_groups = {
                'preschool': 0,
                'school': 0,
                'university': 0,
            }
        
        # إحصائيات المساعدات (إذا كانت متاحة)
        assistance_stats = {}
        if Assistance:
            try:
                # عدد مرات التوزيع (التواريخ الفريدة)
                unique_distribution_dates = Assistance.objects.values(
                    'assistance_date'
                ).distinct().count()
                
                # عدد المستفيدين
                total_assistances = Assistance.objects.count()
                unique_beneficiaries = Assistance.objects.values(
                    'national_id'
                ).distinct().count()
                
                # المساعدات حسب الأحياء
                assistance_by_district = Assistance.objects.values(
                    'district_name'
                ).annotate(count=Count('id')).order_by('-count')[:10]
                
                assistance_stats = {
                    'distribution_dates': unique_distribution_dates,
                    'total_assistances': total_assistances,
                    'unique_beneficiaries': unique_beneficiaries,
                    'individual_beneficiaries': unique_beneficiaries,  # نفس القيمة
                    'by_district': assistance_by_district,
                    'by_type': Assistance.objects.values('assistance_type').annotate(
                        count=Count('id')
                    ),
                    'total_quantity': Assistance.objects.aggregate(
                        total=Sum('quantity')
                    )['total'] or 0,
                }
            except Exception as e:
                print(f"خطأ في إحصائيات المساعدات: {e}")
                assistance_stats = {}
        
        # إحصائيات الشهداء
        martyrs_stats = {
            'total_martyrs': Martyr.objects.count(),
            'martyrs_by_district': Martyr.objects.values('district__name').annotate(
                count=Count('id')
            ).order_by('-count'),
            'martyrs_by_relationship': Martyr.objects.values(
                'relationship_to_martyr'
            ).annotate(count=Count('id')),
            'martyrs_by_year': Martyr.objects.filter(
                martyrdom_date__isnull=False
            ).extra(
                select={'year': "strftime('%%Y', martyrdom_date)"}
            ).values('year').annotate(count=Count('id')).order_by('-year'),
        }
        
        # إحصائيات الجرحى (مع إصلاح الخطأ)
        injured_stats = {
            'total_injured': Injured.objects.count(),
            'injured_by_type': Injured.objects.values('injury_type').annotate(
                count=Count('id')
            ),
            'injured_by_district': Injured.objects.values('district__name').annotate(
                count=Count('id')
            ).order_by('-count'),
            # إزالة injury_severity لأنه غير موجود في النموذج
        }
        
        # إحصائيات البيانات المرضية
        medical_stats = {
            'total_patients': MedicalRecord.objects.count(),
            'patients_by_gender': MedicalRecord.objects.values('gender').annotate(
                count=Count('id')
            ),
            'patients_by_disease': MedicalRecord.objects.values('disease_type').annotate(
                count=Count('id')
            ),
            'patients_with_disability': MedicalRecord.objects.exclude(
                disability_type='none'
            ).count(),
            'disability_by_type': MedicalRecord.objects.exclude(
                disability_type='none'
            ).values('disability_type').annotate(count=Count('id')),
        }
        
        # إحصائيات الأضرار
        damages_stats = {
            'total_damages': Damage.objects.count(),
            'damages_by_type': Damage.objects.values('damage_type').annotate(
                count=Count('id')
            ),
            'damages_by_housing_type': Damage.objects.values('housing_type').annotate(
                count=Count('id')
            ),
            'total_cost_ils': Damage.objects.aggregate(
                total=Sum('estimated_cost_ils')
            )['total'] or 0,
            'total_cost_usd': Damage.objects.aggregate(
                total=Sum('estimated_cost_usd')
            )['total'] or 0,
            'avg_damage_percentage': Damage.objects.aggregate(
                avg=Avg('damage_percentage')
            )['avg'] or 0,
            'damages_by_district': Damage.objects.values('district__name').annotate(
                count=Count('id')
            ).order_by('-count'),
        }
        
        # إحصائيات الأيتام
        orphans_stats = {
            'total_orphans': Orphan.objects.count(),
            'orphans_by_gender': Orphan.objects.values('gender').annotate(
                count=Count('id')
            ),
            'orphans_by_education': Orphan.objects.values('education_level').annotate(
                count=Count('id')
            ),
            'orphans_by_health': Orphan.objects.values('health_status').annotate(
                count=Count('id')
            ),
            'orphans_by_district': Orphan.objects.values('district__name').annotate(
                count=Count('id')
            ).order_by('-count'),
        }
        
        # إحصائيات عامة
        try:
            child_count = Child.objects.count()
        except:
            child_count = 0
            
        general_stats = {
            'total_records': (
                Guardian.objects.count() + 
                Martyr.objects.count() + 
                Injured.objects.count() + 
                MedicalRecord.objects.count() + 
                Damage.objects.count() + 
                Orphan.objects.count() +
                child_count
            ),
            'districts_count': District.objects.count(),
            'last_update': datetime.now(),
        }
        
    except Exception as e:
        print(f"خطأ في الإحصائيات: {e}")
        # إرجاع قيم افتراضية في حالة الخطأ
        family_stats = {
            'total_families': 0, 
            'total_residents': 0, 
            'total_displaced': 0, 
            'families_by_size': {
                'small': 0, 
                'medium': 0, 
                'large': 0,
                'small_percentage': 0,
                'medium_percentage': 0,
                'large_percentage': 0,
            }
        }
        district_stats = []
        marital_status_stats = []

        age_groups = {'preschool': 0, 'school': 0, 'university': 0}
        assistance_stats = {}
        martyrs_stats = {'total_martyrs': 0, 'martyrs_by_district': [], 'martyrs_by_relationship': [], 'martyrs_by_year': []}
        injured_stats = {'total_injured': 0, 'injured_by_type': [], 'injured_by_district': []}
        medical_stats = {'total_patients': 0, 'patients_by_gender': [], 'patients_by_disease': [], 'patients_with_disability': 0, 'disability_by_type': []}
        damages_stats = {'total_damages': 0, 'damages_by_type': [], 'damages_by_housing_type': [], 'total_cost_ils': 0, 'total_cost_usd': 0, 'avg_damage_percentage': 0, 'damages_by_district': []}
        orphans_stats = {'total_orphans': 0, 'orphans_by_gender': [], 'orphans_by_education': [], 'orphans_by_health': [], 'orphans_by_district': []}
        general_stats = {'total_records': 0, 'districts_count': 0, 'last_update': datetime.now()}
    
    context = {
        'family_stats': family_stats,
        'district_stats': district_stats,
        'marital_status_stats': marital_status_stats,

        'age_groups': age_groups,
        'assistance_stats': assistance_stats,
        'martyrs_stats': martyrs_stats,
        'injured_stats': injured_stats,
        'medical_stats': medical_stats,
        'damages_stats': damages_stats,
        'orphans_stats': orphans_stats,
        'general_stats': general_stats,
    }
    
    return render(request, 'reports/statistics_dashboard.html', context)

def export_statistics_pdf(request):
    """تصدير الإحصائيات إلى PDF"""
    # جمع البيانات الإحصائية
    stats_data = {
        'إجمالي أولياء الأمور': Guardian.objects.count(),
        'إجمالي المناطق': District.objects.count(),
        'إجمالي الشهداء': Martyr.objects.count(),
        'إجمالي الجرحى': Injured.objects.count(),
        'إجمالي المرضى': MedicalRecord.objects.count(),
        'إجمالي الأضرار': Damage.objects.count(),
        'إجمالي الأيتام': Orphan.objects.count(),
    }
    
    # إضافة إحصائيات تفصيلية
    detailed_data = []
    
    # إحصائيات الشهداء حسب العلاقة
    martyrs_by_relationship = Martyr.objects.values('relationship_to_martyr').annotate(count=Count('id'))
    if martyrs_by_relationship:
        detailed_data.append(['', ''])  # فاصل
        detailed_data.append(['إحصائيات الشهداء حسب العلاقة', ''])
        for item in martyrs_by_relationship:
            detailed_data.append([item['relationship_to_martyr'], str(item['count'])])
    
    # إحصائيات الجرحى حسب نوع الإصابة
    injured_by_type = Injured.objects.values('injury_type').annotate(count=Count('id'))
    if injured_by_type:
        detailed_data.append(['', ''])  # فاصل
        detailed_data.append(['إحصائيات الجرحى حسب نوع الإصابة', ''])
        for item in injured_by_type:
            detailed_data.append([item['injury_type'], str(item['count'])])
    
    # إحصائيات المرضى حسب نوع المرض
    patients_by_disease = MedicalRecord.objects.values('disease_type').annotate(count=Count('id'))
    if patients_by_disease:
        detailed_data.append(['', ''])  # فاصل
        detailed_data.append(['إحصائيات المرضى حسب نوع المرض', ''])
        for item in patients_by_disease:
            detailed_data.append([item['disease_type'], str(item['count'])])
    
    # دمج البيانات الأساسية مع التفصيلية
    headers = ['البيان', 'القيمة']
    data = []
    
    # إضافة البيانات الأساسية
    for key, value in stats_data.items():
        data.append([key, str(value)])
    
    # إضافة البيانات التفصيلية
    data.extend(detailed_data)
    
    # تصدير PDF
    # exporter = ArabicPDFExporter()
    # return exporter.create_table_pdf(data, headers, 'تقرير الإحصائيات الشامل', 'statistics_report.pdf')
    
    # بديل مؤقت: إرجاع رسالة أن PDF غير متاح حالياً
    from django.http import HttpResponse
    return HttpResponse("تصدير PDF غير متاح حالياً. يرجى استخدام تصدير Excel بدلاً من ذلك.", content_type="text/plain; charset=utf-8")

def detailed_report(request, report_type):
    """تقارير مفصلة حسب النوع"""
    context = {'report_type': report_type}
    
    if report_type == 'martyrs':
        context['data'] = Martyr.objects.select_related('district').all()
        template = 'reports/martyrs_report.html'
    elif report_type == 'injured':
        context['data'] = Injured.objects.select_related('district', 'guardian').all()
        template = 'reports/injured_report.html'
    elif report_type == 'medical':
        context['data'] = MedicalRecord.objects.select_related('district', 'guardian').all()
        template = 'reports/medical_report.html'
    elif report_type == 'damages':
        context['data'] = Damage.objects.select_related('district', 'guardian').all()
        template = 'reports/damages_report.html'
    elif report_type == 'orphans':
        context['data'] = Orphan.objects.select_related('district').all()
        template = 'reports/orphans_report.html'
    else:
        template = 'reports/statistics_dashboard.html'
    
    return render(request, template, context)
