from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count, Max
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import AidType, AidBeneficiary, AidDistribution
from basic_data.models import Guardian, District
from .utils import search_beneficiaries, search_distributions
from datetime import datetime

def aids_home(request):
    """الصفحة الرئيسية للمساعدات"""
    # إحصائيات عامة
    total_beneficiaries = AidBeneficiary.objects.values('guardian').distinct().count()
    total_distributions = AidDistribution.objects.count()
    total_aid_types = AidType.objects.filter(is_active=True).count()
    
    # إحصائيات حسب نوع المساعدة
    aid_stats = AidType.objects.annotate(
        beneficiaries_count=Count('aidbeneficiary'),
        distributions_count=Count('aiddistribution')
    ).filter(is_active=True)
    
    context = {
        'total_beneficiaries': total_beneficiaries,
        'total_distributions': total_distributions,
        'total_aid_types': total_aid_types,
        'aid_stats': aid_stats,
    }
    return render(request, 'aids/aids_home.html', context)


def beneficiaries_list(request):
    """قائمة المستفيدين مع البحث والفلترة المتقدمة"""
    # البحث المرن بالاسم أو رقم الهوية
    search_query = request.GET.get('search', '')
    if search_query:
        # استخدام البحث المرن
        guardians = search_beneficiaries(search_query)
        beneficiaries = AidBeneficiary.objects.filter(guardian__in=guardians).select_related('guardian', 'aid_type', 'guardian__district')
    else:
        beneficiaries = AidBeneficiary.objects.select_related('guardian', 'aid_type', 'guardian__district').all()
    
    # فلترة حسب نوع المساعدة
    selected_aid_type = request.GET.get('aid_type', '')
    if selected_aid_type:
        beneficiaries = beneficiaries.filter(aid_type_id=selected_aid_type)
    
    # فلترة حسب الحي
    selected_district = request.GET.get('district', '')
    if selected_district:
        beneficiaries = beneficiaries.filter(guardian__district_id=selected_district)
    
    # فلترة بين تاريخين
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    if date_from:
        beneficiaries = beneficiaries.filter(aid_date__gte=date_from)
    if date_to:
        beneficiaries = beneficiaries.filter(aid_date__lte=date_to)
    
    # إضافة إحصائيات لكل مستفيد
    beneficiaries_with_stats = []
    processed_guardians = set()
    
    for beneficiary in beneficiaries:
        if beneficiary.guardian.id not in processed_guardians:
            # حساب عدد مرات الاستفادة وآخر موعد
            guardian_benefits = AidBeneficiary.objects.filter(guardian=beneficiary.guardian)
            benefit_count = guardian_benefits.count()
            last_benefit_date = guardian_benefits.aggregate(Max('aid_date'))['aid_date__max']
            
            beneficiaries_with_stats.append({
                'beneficiary': beneficiary,
                'benefit_count': benefit_count,
                'last_benefit_date': last_benefit_date,
            })
            processed_guardians.add(beneficiary.guardian.id)
    
    # ترقيم الصفحات
    paginator = Paginator(beneficiaries_with_stats, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # البيانات للفلاتر
    aid_types = AidType.objects.filter(is_active=True)
    districts = District.objects.all()
    
    # إحصائيات
    total_count = len(beneficiaries_with_stats)
    unique_beneficiaries = len(processed_guardians)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'selected_aid_type': selected_aid_type,
        'selected_district': selected_district,
        'date_from': date_from,
        'date_to': date_to,
        'aid_types': aid_types,
        'districts': districts,
        'total_count': total_count,
        'unique_beneficiaries': unique_beneficiaries,
    }
    return render(request, 'aids/beneficiaries_list.html', context)


def beneficiary_detail(request, guardian_id):
    """تفاصيل المستفيد"""
    guardian = get_object_or_404(Guardian, pk=guardian_id)
    
    # جميع المساعدات التي حصل عليها
    benefits = AidBeneficiary.objects.filter(guardian=guardian).select_related('aid_type')
    
    # إحصائيات
    stats = AidBeneficiary.get_beneficiary_stats(guardian)
    
    # إحصائيات حسب نوع المساعدة
    aid_type_stats = benefits.values('aid_type__name').annotate(
        count=Count('id'),
        last_date=Max('aid_date')
    ).order_by('-count')
    
    context = {
        'guardian': guardian,
        'benefits': benefits,
        'stats': stats,
        'aid_type_stats': aid_type_stats,
    }
    return render(request, 'aids/beneficiary_detail.html', context)


def distributions_list(request):
    """قائمة التوزيع مع البحث والفلترة"""
    # البحث المرن
    search_query = request.GET.get('search', '')
    if search_query:
        # استخدام البحث المرن
        guardians = search_beneficiaries(search_query)
        distributions = AidDistribution.objects.filter(guardian__in=guardians).select_related('guardian', 'aid_type', 'guardian__district')
    else:
        distributions = AidDistribution.objects.select_related('guardian', 'aid_type', 'guardian__district').all()
    
    # فلترة حسب نوع المساعدة
    selected_aid_type = request.GET.get('aid_type', '')
    if selected_aid_type:
        distributions = distributions.filter(aid_type_id=selected_aid_type)
    
    # فلترة حسب الحي
    selected_district = request.GET.get('district', '')
    if selected_district:
        distributions = distributions.filter(guardian__district_id=selected_district)
    
    # فلترة بين تاريخين
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    if date_from:
        distributions = distributions.filter(distribution_date__gte=date_from)
    if date_to:
        distributions = distributions.filter(distribution_date__lte=date_to)
    
    # فلترة حسب حالة الترحيل
    transfer_status = request.GET.get('transfer_status', '')
    if transfer_status == 'transferred':
        distributions = distributions.filter(is_transferred=True)
    elif transfer_status == 'not_transferred':
        distributions = distributions.filter(is_transferred=False)
    
    # ترقيم الصفحات
    paginator = Paginator(distributions, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # البيانات للفلاتر
    aid_types = AidType.objects.filter(is_active=True)
    districts = District.objects.all()
    
    # إحصائيات
    total_count = distributions.count()
    transferred_count = distributions.filter(is_transferred=True).count()
    not_transferred_count = distributions.filter(is_transferred=False).count()
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'selected_aid_type': selected_aid_type,
        'selected_district': selected_district,
        'date_from': date_from,
        'date_to': date_to,
        'transfer_status': transfer_status,
        'aid_types': aid_types,
        'districts': districts,
        'total_count': total_count,
        'transferred_count': transferred_count,
        'not_transferred_count': not_transferred_count,
    }
    return render(request, 'aids/distributions_list.html', context)


def distribution_create(request):
    """إضافة توزيع جديد"""
    copy_id = request.GET.get('copy')
    original_distribution = None
    
    # إذا كان هناك طلب للتكرار
    if copy_id:
        try:
            original_distribution = AidDistribution.objects.get(pk=copy_id)
        except AidDistribution.DoesNotExist:
            messages.warning(request, 'التوزيع المراد تكراره غير موجود')
    
    if request.method == 'POST':
        guardian_id = request.POST.get('guardian')
        aid_type_id = request.POST.get('aid_type')
        distribution_date = request.POST.get('distribution_date')
        notes = request.POST.get('notes', '')
        
        try:
            guardian = Guardian.objects.get(pk=guardian_id)
            aid_type = AidType.objects.get(pk=aid_type_id)
            
            distribution = AidDistribution.objects.create(
                guardian=guardian,
                aid_type=aid_type,
                distribution_date=distribution_date,
                notes=notes
            )
            
            messages.success(request, f'تم إضافة التوزيع بنجاح لـ {guardian.name}')
            return redirect('aids:distributions_list')
            
        except (Guardian.DoesNotExist, AidType.DoesNotExist):
            messages.error(request, 'خطأ في البيانات المدخلة')
    
    # البيانات للنموذج
    guardians = Guardian.objects.all().order_by('name')
    aid_types = AidType.objects.filter(is_active=True)
    
    context = {
        'guardians': guardians,
        'aid_types': aid_types,
        'original_distribution': original_distribution,
        'is_copy': bool(copy_id),
    }
    return render(request, 'aids/distribution_form.html', context)


@require_POST
def transfer_to_beneficiaries(request, distribution_id):
    """ترحيل التوزيع إلى قائمة المستفيدين"""
    distribution = get_object_or_404(AidDistribution, pk=distribution_id)
    
    if distribution.is_transferred:
        messages.warning(request, 'هذا التوزيع تم ترحيله مسبقاً')
    else:
        beneficiary = distribution.transfer_to_beneficiaries()
        if beneficiary:
            messages.success(request, f'تم ترحيل التوزيع بنجاح إلى قائمة المستفيدين')
        else:
            messages.error(request, 'حدث خطأ أثناء الترحيل')
    
    return redirect('distributions_list')


@require_POST
def bulk_transfer_to_beneficiaries(request):
    """ترحيل متعدد للتوزيعات"""
    distribution_ids = request.POST.getlist('distribution_ids')
    
    if not distribution_ids:
        messages.warning(request, 'لم يتم اختيار أي توزيعات للترحيل')
        return redirect('distributions_list')
    
    transferred_count = 0
    for distribution_id in distribution_ids:
        try:
            distribution = AidDistribution.objects.get(pk=distribution_id)
            if not distribution.is_transferred:
                distribution.transfer_to_beneficiaries()
                transferred_count += 1
        except AidDistribution.DoesNotExist:
            continue
    
    messages.success(request, f'تم ترحيل {transferred_count} توزيع بنجاح إلى قائمة المستفيدين')
    return redirect('distributions_list')


def search_guardians_ajax(request):
    """البحث عن أولياء الأمور عبر AJAX"""
    query = request.GET.get('q', '')
    guardians = []
    
    if len(query) >= 2:
        search_terms = query.split()
        q_objects = Q()
        for term in search_terms:
            q_objects |= Q(name__icontains=term) | Q(national_id__icontains=term)
        
        guardians_qs = Guardian.objects.filter(q_objects)[:10]
        guardians = [
            {
                'id': guardian.id,
                'name': guardian.name,
                'national_id': guardian.national_id,
                'phone': guardian.phone_number,
                'district': guardian.district.name if guardian.district else 'غير محدد'
            }
            for guardian in guardians_qs
        ]
    
    return JsonResponse({'guardians': guardians})


def distribution_edit(request, pk):
    """تعديل توزيع موجود"""
    distribution = get_object_or_404(AidDistribution, pk=pk)
    
    if request.method == 'POST':
        guardian_id = request.POST.get('guardian')
        aid_type_id = request.POST.get('aid_type')
        distribution_date = request.POST.get('distribution_date')
        notes = request.POST.get('notes', '')
        
        try:
            guardian = Guardian.objects.get(pk=guardian_id)
            aid_type = AidType.objects.get(pk=aid_type_id)
            
            distribution.guardian = guardian
            distribution.aid_type = aid_type
            distribution.distribution_date = distribution_date
            distribution.notes = notes
            distribution.save()
            
            messages.success(request, f'تم تعديل التوزيع بنجاح لـ {guardian.name}')
            return redirect('aids:distributions_list')
            
        except (Guardian.DoesNotExist, AidType.DoesNotExist):
            messages.error(request, 'خطأ في البيانات المدخلة')
    
    # البيانات للنموذج
    guardians = Guardian.objects.all().order_by('name')
    aid_types = AidType.objects.filter(is_active=True)
    
    context = {
        'distribution': distribution,
        'guardians': guardians,
        'aid_types': aid_types,
        'is_edit': True,
    }
    return render(request, 'aids/distribution_form.html', context)


def distribution_delete(request, pk):
    """حذف توزيع"""
    distribution = get_object_or_404(AidDistribution, pk=pk)
    
    if request.method == 'POST':
        guardian_name = distribution.guardian.name
        distribution.delete()
        messages.success(request, f'تم حذف التوزيع بنجاح لـ {guardian_name}')
        return redirect('aids:distributions_list')
    
    context = {
        'distribution': distribution,
    }
    return render(request, 'aids/distribution_confirm_delete.html', context)


@require_POST
def delete_selected_beneficiaries(request):
    """حذف المستفيدين المحددين"""
    try:
        beneficiary_ids = request.POST.getlist('beneficiary_ids')
        if not beneficiary_ids:
            return JsonResponse({
                'success': False,
                'message': 'لم يتم تحديد أي مستفيدين للحذف'
            })
        
        # الحصول على المستفيدين المحددين
        beneficiaries = AidBeneficiary.objects.filter(id__in=beneficiary_ids)
        deleted_count = beneficiaries.count()
        
        if deleted_count == 0:
            return JsonResponse({
                'success': False,
                'message': 'لم يتم العثور على المستفيدين المحددين'
            })
        
        # حذف المستفيدين
        beneficiaries.delete()
        
        return JsonResponse({
            'success': True,
            'deleted_count': deleted_count,
            'message': f'تم حذف {deleted_count} من المستفيدين بنجاح'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'حدث خطأ: {str(e)}'
        })

@require_POST
def delete_all_beneficiaries(request):
    """حذف جميع المستفيدين"""
    try:
        # عد جميع المستفيدين
        total_count = AidBeneficiary.objects.count()
        
        if total_count == 0:
            return JsonResponse({
                'success': False,
                'message': 'لا يوجد مستفيدين للحذف'
            })
        
        # حذف جميع المستفيدين
        AidBeneficiary.objects.all().delete()
        
        return JsonResponse({
            'success': True,
            'deleted_count': total_count,
            'message': f'تم حذف جميع المستفيدين ({total_count}) بنجاح'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'حدث خطأ: {str(e)}'
        })

@require_POST
def delete_selected_distributions(request):
    """حذف التوزيعات المحددة"""
    try:
        distribution_ids = request.POST.getlist('distribution_ids')
        if not distribution_ids:
            return JsonResponse({
                'success': False,
                'message': 'لم يتم تحديد أي توزيعات للحذف'
            })
        
        # الحصول على التوزيعات المحددة
        distributions = AidDistribution.objects.filter(id__in=distribution_ids)
        deleted_count = distributions.count()
        
        if deleted_count == 0:
            return JsonResponse({
                'success': False,
                'message': 'لم يتم العثور على التوزيعات المحددة'
            })
        
        # حذف التوزيعات
        distributions.delete()
        
        return JsonResponse({
            'success': True,
            'deleted_count': deleted_count,
            'message': f'تم حذف {deleted_count} من التوزيعات بنجاح'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'حدث خطأ: {str(e)}'
        })

@require_POST
def delete_all_distributions(request):
    """حذف جميع التوزيعات"""
    try:
        # عد جميع التوزيعات
        total_count = AidDistribution.objects.count()
        
        if total_count == 0:
            return JsonResponse({
                'success': False,
                'message': 'لا يوجد توزيعات للحذف'
            })
        
        # حذف جميع التوزيعات
        AidDistribution.objects.all().delete()
        
        return JsonResponse({
            'success': True,
            'deleted_count': total_count,
            'message': f'تم حذف جميع التوزيعات ({total_count}) بنجاح'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'حدث خطأ: {str(e)}'
        })

@require_POST
def delete_selected_aid_types(request):
    """حذف أنواع المساعدات المحددة"""
    try:
        aid_type_ids = request.POST.getlist('aid_type_ids')
        if not aid_type_ids:
            return JsonResponse({
                'success': False,
                'message': 'لم يتم تحديد أي أنواع مساعدات للحذف'
            })
        
        # الحصول على أنواع المساعدات المحددة
        aid_types = AidType.objects.filter(id__in=aid_type_ids)
        deleted_count = aid_types.count()
        
        if deleted_count == 0:
            return JsonResponse({
                'success': False,
                'message': 'لم يتم العثور على أنواع المساعدات المحددة'
            })
        
        # حذف أنواع المساعدات
        aid_types.delete()
        
        return JsonResponse({
            'success': True,
            'deleted_count': deleted_count,
            'message': f'تم حذف {deleted_count} من أنواع المساعدات بنجاح'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'حدث خطأ: {str(e)}'
        })

@require_POST
def delete_all_aid_types(request):
    """حذف جميع أنواع المساعدات"""
    try:
        # عد جميع أنواع المساعدات
        total_count = AidType.objects.count()
        
        if total_count == 0:
            return JsonResponse({
                'success': False,
                'message': 'لا يوجد أنواع مساعدات للحذف'
            })
        
        # حذف جميع أنواع المساعدات
        AidType.objects.all().delete()
        
        return JsonResponse({
            'success': True,
            'deleted_count': total_count,
            'message': f'تم حذف جميع أنواع المساعدات ({total_count}) بنجاح'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'حدث خطأ: {str(e)}'
        })
