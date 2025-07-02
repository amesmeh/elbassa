from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.db import transaction, models
from .citizen_models import CitizenRegistrationRequest, CitizenRequestChild, CitizenRequestWife
from .citizen_forms import CitizenRegistrationForm, CitizenRequestChildFormSet, CitizenRequestWifeFormSet
from .models import Guardian, District, Child, Wife
import json


def citizen_registration(request):
    """صفحة تسجيل مواطن جديد"""
    if request.method == 'POST':
        form = CitizenRegistrationForm(request.POST)
        if form.is_valid():
            registration_request = form.save(commit=False)
            registration_request.save()
            
            # معالجة بيانات الأطفال
            child_formset = CitizenRequestChildFormSet(request.POST, instance=registration_request)
            if child_formset.is_valid():
                child_formset.save()
            
            # معالجة بيانات الزوجات
            wife_formset = CitizenRequestWifeFormSet(request.POST, instance=registration_request)
            if wife_formset.is_valid():
                wife_formset.save()
            
            messages.success(request, 'تم تقديم طلب التسجيل بنجاح!')
            return redirect('citizen_registration:registration_success')
    else:
        form = CitizenRegistrationForm()
        child_formset = CitizenRequestChildFormSet(instance=CitizenRegistrationRequest())
        wife_formset = CitizenRequestWifeFormSet(instance=CitizenRegistrationRequest())
    
    return render(request, 'basic_data/citizen_registration.html', {
        'form': form,
        'child_formset': child_formset,
        'wife_formset': wife_formset
    })


def registration_success(request):
    """صفحة نجاح التسجيل"""
    # الحصول على آخر طلب تم إنشاؤه من الجلسة أو عرض رسالة عامة
    return render(request, 'basic_data/registration_success.html')


def check_national_id(request):
    """التحقق من رقم الهوية (AJAX)"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            national_id = data.get('national_id')
        except:
            national_id = request.POST.get('national_id')
    else:
        national_id = request.GET.get('national_id')
    
    if not national_id:
        return JsonResponse({'exists': False, 'error': 'رقم الهوية مطلوب'})
    
    # التحقق من وجود الرقم في طلبات التسجيل
    exists_in_requests = CitizenRegistrationRequest.objects.filter(national_id=national_id).exists()
    
    # التحقق من وجود الرقم في أولياء الأمور
    exists_in_guardians = Guardian.objects.filter(national_id=national_id).exists()
    
    exists = exists_in_requests or exists_in_guardians
    
    return JsonResponse({
        'exists': exists,
        'message': 'رقم الهوية موجود مسبقاً' if exists else 'رقم الهوية متاح'
    })


@login_required
@permission_required('basic_data.view_citizenregistrationrequest', raise_exception=True)
def registration_requests_list(request):
    """قائمة طلبات التسجيل"""
    requests = CitizenRegistrationRequest.objects.all().order_by('-created_at')
    districts = District.objects.all()
    
    # تطبيق الفلاتر
    status_filter = request.GET.get('status')
    district_filter = request.GET.get('district')
    search_query = request.GET.get('search')
    
    if status_filter:
        requests = requests.filter(status=status_filter)
    
    if district_filter:
        requests = requests.filter(district_id=district_filter)
    
    if search_query:
        requests = requests.filter(
            models.Q(name__icontains=search_query) |
            models.Q(national_id__icontains=search_query)
        )
    
    # إحصائيات
    total_requests = CitizenRegistrationRequest.objects.count()
    pending_requests = CitizenRegistrationRequest.objects.filter(status='pending').count()
    approved_requests = CitizenRegistrationRequest.objects.filter(status='approved').count()
    rejected_requests = CitizenRegistrationRequest.objects.filter(status='rejected').count()
    
    return render(request, 'basic_data/registration_requests_list.html', {
        'requests': requests,
        'districts': districts,
        'status_filter': status_filter,
        'district_filter': district_filter,
        'search_query': search_query,
        'total_requests': total_requests,
        'pending_requests': pending_requests,
        'approved_requests': approved_requests,
        'rejected_requests': rejected_requests,
    })


@login_required
@permission_required('basic_data.view_citizenregistrationrequest', raise_exception=True)
def registration_request_detail(request, request_id):
    """تفاصيل طلب التسجيل"""
    registration_request = get_object_or_404(CitizenRegistrationRequest, id=request_id)
    
    return render(request, 'basic_data/registration_request_detail.html', {
        'request': registration_request
    })


@login_required
@permission_required('basic_data.change_citizenregistrationrequest', raise_exception=True)
@require_http_methods(["POST"])
def approve_registration_request(request, request_id):
    """قبول طلب التسجيل"""
    try:
        registration_request = get_object_or_404(CitizenRegistrationRequest, id=request_id)
        
        if registration_request.status != 'pending':
            return JsonResponse({
                'success': False,
                'message': 'لا يمكن قبول طلب غير في حالة الانتظار'
            })
        
        # قبول الطلب وإنشاء ولي الأمر
        registration_request.approve(request.user)
        
        return JsonResponse({
            'success': True,
            'message': 'تم قبول الطلب وإنشاء ولي الأمر بنجاح'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'حدث خطأ أثناء قبول الطلب: {str(e)}'
        })


@login_required
@permission_required('basic_data.change_citizenregistrationrequest', raise_exception=True)
@require_http_methods(["POST"])
def reject_registration_request(request, request_id):
    """رفض طلب التسجيل"""
    try:
        registration_request = get_object_or_404(CitizenRegistrationRequest, id=request_id)
        
        if registration_request.status != 'pending':
            return JsonResponse({
                'success': False,
                'message': 'لا يمكن رفض طلب غير في حالة الانتظار'
            })
        
        # قراءة البيانات من الطلب
        data = json.loads(request.body)
        notes = data.get('notes', '')
        
        # رفض الطلب
        registration_request.reject(request.user, notes)
        
        return JsonResponse({
            'success': True,
            'message': 'تم رفض الطلب بنجاح'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'حدث خطأ أثناء رفض الطلب: {str(e)}'
        })


@login_required
@permission_required('basic_data.delete_citizenregistrationrequest', raise_exception=True)
@require_http_methods(["POST"])
def delete_registration_request(request, request_id):
    """حذف طلب التسجيل"""
    try:
        registration_request = get_object_or_404(CitizenRegistrationRequest, id=request_id)
        registration_request.delete()
        return JsonResponse({
            'success': True,
            'message': 'تم حذف الطلب بنجاح'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'حدث خطأ أثناء حذف الطلب: {str(e)}'
        })


def public_citizen_registration(request):
    """صفحة تسجيل مواطن جديد (للمواطنين)"""
    from .models import District
    
    if request.method == 'POST':
        try:
            # التحقق من وجود رقم الهوية
            national_id = request.POST.get('national_id')
            if CitizenRegistrationRequest.objects.filter(national_id=national_id).exists():
                messages.error(request, 'رقم الهوية موجود مسبقاً')
                return redirect('basic_data:public_citizen_registration')
            
            # إنشاء طلب التسجيل
            registration_request = CitizenRegistrationRequest.objects.create(
                name=request.POST.get('name'),
                national_id=national_id,
                phone_number=request.POST.get('phone_number'),
                gender=request.POST.get('gender'),
                current_job=request.POST.get('current_job', ''),
                children_count=request.POST.get('children_count', 0),
                marital_status=request.POST.get('marital_status'),
                wives_count=request.POST.get('wives_count', 0),
                residence_status=request.POST.get('residence_status'),
                original_governorate=request.POST.get('original_governorate', ''),
                original_city=request.POST.get('original_city', ''),
                displacement_address=request.POST.get('displacement_address', ''),
                district_id=request.POST.get('district'),
                housing_type=request.POST.get('housing_type', ''),
                status='pending'
            )

            # معالجة بيانات الأبناء
            children_names = request.POST.getlist('children_names[]')
            children_national_ids = request.POST.getlist('children_national_ids[]')
            children_birth_dates = request.POST.getlist('children_birth_dates[]')

            for i, name in enumerate(children_names):
                if name.strip():  # تأكد من أن الاسم ليس فارغاً
                    CitizenRequestChild.objects.create(
                        request=registration_request,
                        name=name.strip(),
                        national_id=children_national_ids[i].strip() if i < len(children_national_ids) and children_national_ids[i].strip() else None,
                        birth_date=children_birth_dates[i] if i < len(children_birth_dates) and children_birth_dates[i] else None
                    )

            # معالجة بيانات الزوجات
            wives_names = request.POST.getlist('wives_names[]')
            wives_national_ids = request.POST.getlist('wives_national_ids[]')

            for i, name in enumerate(wives_names):
                if name.strip():  # تأكد من أن الاسم ليس فارغاً
                    CitizenRequestWife.objects.create(
                        request=registration_request,
                        name=name.strip(),
                        national_id=wives_national_ids[i].strip() if i < len(wives_national_ids) and wives_national_ids[i].strip() else None
                    )
            
            messages.success(request, 'تم إرسال طلب التسجيل بنجاح')
            return redirect('citizen_registration:registration_success')
            
        except Exception as e:
            messages.error(request, f'حدث خطأ: {str(e)}')
            return redirect('citizen_registration:public_citizen_registration')
    
    # عرض النموذج
    districts = District.objects.all()
    return render(request, 'basic_data/citizen_public_registration.html', {
        'districts': districts
    }) 