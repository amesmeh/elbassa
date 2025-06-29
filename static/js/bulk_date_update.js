// ملف JavaScript منفصل لميزة التحديث الجماعي للتواريخ

// التأكد من تحميل الصفحة كاملة
document.addEventListener('DOMContentLoaded', function() {
    console.log('Bulk date update script loaded');
});

// وظيفة عرض مودال التحديث الجماعي
function showBulkUpdateDateModal() {
    console.log('showBulkUpdateDateModal called from external file');
    
    // التحقق من وجود Bootstrap
    if (typeof bootstrap === 'undefined') {
        alert('Bootstrap غير متوفر!');
        return;
    }
    
    try {
        // التحقق من وجود العناصر
        const form = document.getElementById('bulkUpdateDateForm');
        const previewResults = document.getElementById('previewResults');
        const confirmBtn = document.getElementById('confirmBulkBtn');
        const modalElement = document.getElementById('bulkUpdateDateModal');
        
        console.log('Elements found:', {
            form: !!form,
            previewResults: !!previewResults,
            confirmBtn: !!confirmBtn,
            modalElement: !!modalElement
        });
        
        if (!form || !previewResults || !confirmBtn || !modalElement) {
            throw new Error('بعض عناصر المودال غير موجودة');
        }
        
        // إعادة تعيين النموذج
        form.reset();
        previewResults.classList.add('d-none');
        confirmBtn.disabled = true;
        
        // عرض المودال
        var modal = new bootstrap.Modal(modalElement);
        modal.show();
        console.log('Modal should be shown');
    } catch (error) {
        console.error('Error in showBulkUpdateDateModal:', error);
        alert('خطأ في فتح النافذة: ' + error.message);
    }
}

// وظيفة معاينة النتائج
function previewBulkUpdate() {
    console.log('previewBulkUpdate called');
    const oldDate = document.getElementById('bulkOldDate').value;
    const newDate = document.getElementById('bulkNewDate').value;
    const includeFilters = document.getElementById('includeFilters').checked;
    console.log('oldDate:', oldDate, 'newDate:', newDate);
    
    if (!oldDate || !newDate) {
        alert('يرجى تحديد التاريخ القديم والجديد');
        return;
    }
    
    if (oldDate === newDate) {
        alert('التاريخ الجديد نفس التاريخ القديم');
        return;
    }
    
    // إرسال طلب المعاينة
    const currentUrl = new URL(window.location);
    const searchParams = includeFilters ? currentUrl.searchParams.toString() : '';
    
    fetch('/assistance/bulk-update-date-preview/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            'X-Requested-With': 'XMLHttpRequest'
        },
        body: JSON.stringify({
            old_date: oldDate,
            new_date: newDate,
            include_filters: includeFilters,
            search_params: searchParams
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Preview response:', data);
        if (data.success) {
            const previewDiv = document.getElementById('previewResults');
            const previewText = document.getElementById('previewText');
            
            if (data.count > 0) {
                previewText.innerHTML = `
                    سيتم تحديث <strong>${data.count}</strong> مساعدة من تاريخ <strong>${oldDate}</strong> إلى <strong>${newDate}</strong>
                    ${data.sample_names ? '<br><small>أمثلة: ' + data.sample_names + '</small>' : ''}
                `;
                previewDiv.classList.remove('d-none');
                document.getElementById('confirmBulkBtn').disabled = false;
            } else {
                previewText.innerHTML = `لا توجد مساعدات بتاريخ <strong>${oldDate}</strong>`;
                previewDiv.classList.remove('d-none');
                document.getElementById('confirmBulkBtn').disabled = true;
            }
        } else {
            alert('حدث خطأ في المعاينة: ' + (data.error || 'خطأ غير معروف'));
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('حدث خطأ في الاتصال');
    });
}

// وظيفة تأكيد التحديث الجماعي
function confirmBulkUpdateDate() {
    console.log('confirmBulkUpdateDate called');
    const oldDate = document.getElementById('bulkOldDate').value;
    const newDate = document.getElementById('bulkNewDate').value;
    const reason = document.getElementById('bulkUpdateReason').value;
    const includeFilters = document.getElementById('includeFilters').checked;
    console.log('Data:', {oldDate, newDate, reason, includeFilters});
    
    if (!oldDate || !newDate || !reason.trim()) {
        alert('يرجى ملء جميع الحقول المطلوبة');
        return;
    }
    
    // تأكيد العملية
    if (!confirm(`هل أنت متأكد من تحديث جميع المساعدات من تاريخ ${oldDate} إلى ${newDate}؟\n\nهذا الإجراء لا يمكن التراجع عنه!`)) {
        return;
    }
    
    // إرسال الطلب
    const currentUrl = new URL(window.location);
    const searchParams = includeFilters ? currentUrl.searchParams.toString() : '';
    
    fetch('/assistance/bulk-update-date/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            'X-Requested-With': 'XMLHttpRequest'
        },
        body: JSON.stringify({
            old_date: oldDate,
            new_date: newDate,
            reason: reason,
            include_filters: includeFilters,
            search_params: searchParams
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Update response:', data);
        if (data.success) {
            // إغلاق المودال
            var modal = bootstrap.Modal.getInstance(document.getElementById('bulkUpdateDateModal'));
            modal.hide();
            
            // عرض رسالة نجاح وإعادة تحميل الصفحة
            showSuccessMessage(`تم تحديث ${data.updated_count} مساعدة بنجاح`);
            
            // إعادة تحميل الصفحة بعد ثانيتين
            setTimeout(() => {
                window.location.reload();
            }, 2000);
        } else {
            alert('حدث خطأ: ' + (data.error || 'خطأ غير معروف'));
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('حدث خطأ في الاتصال');
    });
}

// وظيفة عرض رسالة النجاح
function showSuccessMessage(message) {
    // إنشاء عنصر التنبيه
    const alert = document.createElement('div');
    alert.className = 'alert alert-success alert-dismissible fade show position-fixed';
    alert.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    alert.innerHTML = `
        <i class="fas fa-check-circle me-2"></i>${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    // إضافة التنبيه إلى الصفحة
    document.body.appendChild(alert);
    
    // إزالة التنبيه تلقائياً بعد 5 ثوان
    setTimeout(() => {
        if (alert.parentNode) {
            alert.remove();
        }
    }, 5000);
} 