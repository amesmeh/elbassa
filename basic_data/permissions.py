from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from .models import District, Guardian, Wife, Child, Representative
from assistance.models import Assistance
from martyrs.models import Martyr
from injured.models import Injured
from medical.models import MedicalRecord
from orphans.models import Orphan
from damages.models import Damage

def get_user_district(user):
    """الحصول على الحي الخاص بالمستخدم إذا كان مندوباً"""
    if hasattr(user, 'representative'):
        return user.representative.district
    return None

def create_permission_groups():
    """إنشاء مجموعات المستخدمين مع الصلاحيات المناسبة"""
    
    # إنشاء المجموعات
    supervisor_group, _ = Group.objects.get_or_create(name='المشرفين')
    representative_group, _ = Group.objects.get_or_create(name='مندوبي الأحياء')
    data_entry_group, _ = Group.objects.get_or_create(name='موظفي الإدخال')
    reviewer_group, _ = Group.objects.get_or_create(name='المراجعين')
    general_observer_group, _ = Group.objects.get_or_create(name='المراقب العام')

    # الحصول على ContentTypes للنماذج
    district_ct = ContentType.objects.get_for_model(District)
    guardian_ct = ContentType.objects.get_for_model(Guardian)
    wife_ct = ContentType.objects.get_for_model(Wife)
    child_ct = ContentType.objects.get_for_model(Child)
    assistance_ct = ContentType.objects.get_for_model(Assistance)
    martyr_ct = ContentType.objects.get_for_model(Martyr)
    injured_ct = ContentType.objects.get_for_model(Injured)
    medical_ct = ContentType.objects.get_for_model(MedicalRecord)
    orphan_ct = ContentType.objects.get_for_model(Orphan)
    damage_ct = ContentType.objects.get_for_model(Damage)
    
    # إنشاء وتعيين الصلاحيات للمشرفين (كل الصلاحيات)
    supervisor_perms = Permission.objects.filter(
        content_type__in=[
            district_ct, guardian_ct, wife_ct, child_ct,
            assistance_ct, martyr_ct, injured_ct, medical_ct,
            orphan_ct, damage_ct
        ]
    )
    supervisor_group.permissions.set(supervisor_perms)
    
    # صلاحيات المراقب العام (عرض فقط)
    general_observer_perms = Permission.objects.filter(
        content_type__in=[
            district_ct, guardian_ct, wife_ct, child_ct,
            assistance_ct, martyr_ct, injured_ct, medical_ct,
            orphan_ct, damage_ct
        ],
        codename__startswith='view_'
    )
    general_observer_group.permissions.set(general_observer_perms)
    
    # صلاحيات مندوبي الأحياء (عرض فقط)
    representative_perms = Permission.objects.filter(
        content_type__in=[
            district_ct, guardian_ct, wife_ct, child_ct,
            assistance_ct, martyr_ct, injured_ct, medical_ct,
            orphan_ct, damage_ct
        ],
        codename__startswith='view_'
    )
    representative_group.permissions.set(representative_perms)
    
    # صلاحيات موظفي الإدخال
    data_entry_perms = Permission.objects.filter(
        content_type__in=[guardian_ct, wife_ct, child_ct],
        codename__in=[
            'add_guardian', 'change_guardian', 'view_guardian',
            'add_wife', 'change_wife', 'view_wife',
            'add_child', 'change_child', 'view_child'
        ]
    )
    data_entry_group.permissions.set(data_entry_perms)
    
    # صلاحيات المراجعين (عرض فقط)
    reviewer_perms = Permission.objects.filter(
        content_type__in=[
            district_ct, guardian_ct, wife_ct, child_ct,
            assistance_ct, martyr_ct, injured_ct, medical_ct,
            orphan_ct, damage_ct
        ],
        codename__startswith='view_'
    )
    reviewer_group.permissions.set(reviewer_perms)

def user_has_district_permission(user, district):
    """التحقق من صلاحية المستخدم للوصول إلى حي معين"""
    if user.is_superuser:
        return True
    if hasattr(user, 'representative'):
        return user.representative.district == district
    return False

def user_has_guardian_permission(user, guardian):
    """التحقق من صلاحية المستخدم للوصول إلى ولي أمر معين"""
    if user.is_superuser or user.groups.filter(name='المراقب العام').exists():
        return True
    if hasattr(user, 'representative'):
        return user.representative.district == guardian.district
    return False

def user_has_special_case_permission(user):
    """التحقق من صلاحية المستخدم للوصول إلى الحالات الخاصة (شهداء، جرحى، أيتام، حالات مرضية)"""
    return (user.is_superuser or 
            user.groups.filter(name__in=['المراقب العام', 'مندوبي الأحياء']).exists()) 