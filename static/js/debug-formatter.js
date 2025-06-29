/**
 * ملف تشخيص نظام التنسيق الديناميكي المبسط
 */

// فحص شامل للنظام
function debugFormatter() {
    console.log('=== تشخيص نظام التنسيق الديناميكي المبسط ===');
    
    // فحص Bootstrap
    if (typeof bootstrap !== 'undefined') {
        console.log('✅ Bootstrap متوفر');
    } else {
        console.log('❌ Bootstrap غير متوفر');
    }
    
    // فحص الجداول
    const tables = document.querySelectorAll('table');
    console.log('📊 عدد الجداول: ' + tables.length);
    
    if (tables.length > 0) {
        tables.forEach((table, index) => {
            const headers = table.querySelectorAll('thead th');
            console.log('   الجدول ' + (index + 1) + ': ' + headers.length + ' أعمدة');
            
            // فحص زر التنسيق لهذا الجدول
            const formatButton = document.getElementById('formatButton-' + index);
            console.log('   زر التنسيق: ' + (formatButton ? '✅' : '❌'));
        });
    }
    
    console.log('=== انتهاء التشخيص ===');
    
    return {
        bootstrap: typeof bootstrap !== 'undefined',
        tables: tables.length,
        formatButtons: document.querySelectorAll('[id^="formatButton-"]').length
    };
}

// اختبار فتح النافذة
function testModal() {
    console.log('🧪 اختبار فتح النافذة...');
    
    const formatButton = document.querySelector('[id^="formatButton-"]');
    if (formatButton) {
        console.log('✅ تم العثور على زر التنسيق');
        formatButton.click();
        
        setTimeout(() => {
            const modal = document.querySelector('.modal.show');
            if (modal) {
                console.log('✅ النافذة مفتوحة');
                testControls();
            } else {
                console.log('❌ فشل في فتح النافذة');
            }
        }, 1000);
    } else {
        console.log('❌ لم يتم العثور على زر التنسيق');
    }
}

// اختبار عناصر التحكم
function testControls() {
    console.log('🧪 اختبار عناصر التحكم...');
    
    // فحص أزرار المعاينة
    const showPreview = document.querySelector('[id^="showPreview-"]');
    const hidePreview = document.querySelector('[id^="hidePreview-"]');
    console.log('👁️ إظهار المعاينة: ' + (showPreview ? '✅' : '❌'));
    console.log('🙈 إخفاء المعاينة: ' + (hidePreview ? '✅' : '❌'));
    
    // فحص checkboxes الأعمدة
    const columnCheckboxes = document.querySelectorAll('[id^="col-"]');
    console.log('📋 عناصر تحكم الأعمدة: ' + columnCheckboxes.length);
    
    // فحص جدول المعاينة
    const previewTable = document.querySelector('[id^="previewTable-"]');
    const previewSection = document.querySelector('[id^="previewSection-"]');
    console.log('📊 جدول المعاينة: ' + (previewTable ? '✅' : '❌'));
    console.log('📦 قسم المعاينة: ' + (previewSection ? '✅' : '❌'));
    
    if (previewSection) {
        console.log('👁️ المعاينة مرئية: ' + (previewSection.style.display !== 'none' ? '✅' : '❌'));
    }
}

// اختبار تبديل المعاينة
function testPreviewToggle() {
    console.log('🧪 اختبار تبديل المعاينة...');
    
    const showPreview = document.querySelector('[id^="showPreview-"]');
    const hidePreview = document.querySelector('[id^="hidePreview-"]');
    const previewSection = document.querySelector('[id^="previewSection-"]');
    
    if (showPreview && hidePreview && previewSection) {
        // إخفاء المعاينة
        hidePreview.click();
        setTimeout(() => {
            console.log('المعاينة مخفية: ' + (previewSection.style.display === 'none' ? '✅' : '❌'));
            
            // إظهار المعاينة
            showPreview.click();
            setTimeout(() => {
                console.log('المعاينة مرئية: ' + (previewSection.style.display !== 'none' ? '✅' : '❌'));
            }, 500);
        }, 500);
    } else {
        console.log('❌ عناصر تحكم المعاينة غير موجودة');
    }
}

// اختبار إخفاء/إظهار الأعمدة
function testColumnToggle() {
    console.log('🧪 اختبار إخفاء/إظهار الأعمدة...');
    
    const columnCheckboxes = document.querySelectorAll('[id^="col-"]');
    
    if (columnCheckboxes.length > 0) {
        // اختبار أول checkbox
        const firstCheckbox = columnCheckboxes[0];
        console.log('اختبار العمود الأول...');
        
        // إلغاء التحديد
        firstCheckbox.checked = false;
        firstCheckbox.dispatchEvent(new Event('change'));
        
        setTimeout(() => {
            console.log('تم إخفاء العمود الأول');
            
            // إعادة التحديد
            firstCheckbox.checked = true;
            firstCheckbox.dispatchEvent(new Event('change'));
            
            setTimeout(() => {
                console.log('تم إظهار العمود الأول');
            }, 500);
        }, 500);
    } else {
        console.log('❌ لا توجد عناصر تحكم في الأعمدة');
    }
}

// اختبار شامل
function fullTest() {
    console.log('🚀 بدء الاختبار الشامل...');
    
    const report = debugFormatter();
    
    if (report.tables === 0) {
        console.log('❌ لا توجد جداول للاختبار');
        return;
    }
    
    if (report.formatButtons === 0) {
        console.log('❌ لا توجد أزرار تنسيق');
        return;
    }
    
    // اختبار فتح النافذة
    testModal();
    
    // اختبار الوظائف بعد فتح النافذة
    setTimeout(() => {
        testPreviewToggle();
        testColumnToggle();
    }, 2000);
}

// اختبار سريع (30 ثانية)
function quickTest() {
    console.log('⚡ اختبار سريع...');
    
    const report = debugFormatter();
    
    if (report.tables > 0 && report.formatButtons > 0) {
        console.log('✅ النظام يبدو جيداً - اختبار فتح النافذة...');
        testModal();
    } else {
        console.log('❌ مشكلة في النظام');
        console.log('الجداول: ' + report.tables);
        console.log('أزرار التنسيق: ' + report.formatButtons);
    }
}

// تشغيل تلقائي عند تحميل الصفحة
document.addEventListener('DOMContentLoaded', function() {
    setTimeout(() => {
        console.log('🔍 تشغيل التشخيص التلقائي...');
        debugFormatter();
    }, 2000); // انتظار أطول للتأكد من تحميل النظام
});

// إضافة الدوال للنافذة العامة
window.debugFormatter = debugFormatter;
window.testModal = testModal;
window.testControls = testControls;
window.testPreviewToggle = testPreviewToggle;
window.testColumnToggle = testColumnToggle;
window.fullTest = fullTest;
window.quickTest = quickTest; 