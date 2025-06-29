/**
 * نظام التنسيق الديناميكي الشامل
 * يعمل تلقائياً مع جميع الجداول في البرنامج
 * مع تحكم عام وفردي متقدم
 */

document.addEventListener("DOMContentLoaded", function () {
    console.log('🚀 تهيئة نظام التنسيق الديناميكي الشامل...');
    
    // انتظار قليل للتأكد من تحميل كامل للصفحة
    setTimeout(() => {
        initializeGlobalFormattingSystem();
    }, 500);
});

function initializeGlobalFormattingSystem() {
    // البحث عن جميع الجداول في الصفحة
    const tables = document.querySelectorAll('table');
    
    if (tables.length === 0) {
        console.log('ℹ️ لا توجد جداول في هذه الصفحة');
        return;
    }

    console.log(`📊 تم العثور على ${tables.length} جدول - بدء التهيئة...`);

    // إنشاء زر التنسيق لكل جدول
    tables.forEach((table, tableIndex) => {
        // تجاهل الجداول المخفية أو الصغيرة جداً
        if (isTableValid(table)) {
            createFormatButton(table, tableIndex);
            console.log(`✅ تم تهيئة الجدول ${tableIndex + 1}`);
        } else {
            console.log(`⏭️ تم تجاهل الجدول ${tableIndex + 1} (غير صالح للتنسيق)`);
        }
    });

    console.log('🎉 تم إكمال تهيئة نظام التنسيق بنجاح!');
}

function isTableValid(table) {
    // فحص إذا كان الجدول صالح للتنسيق
    const rows = table.querySelectorAll('tr');
    const headers = table.querySelectorAll('thead th, thead td');
    
    // يجب أن يحتوي على أكثر من صف واحد وعمود واحد
    if (rows.length < 2 || headers.length < 2) {
        return false;
    }
    
    // تجاهل الجداول المخفية
    if (table.style.display === 'none' || table.offsetParent === null) {
        return false;
    }
    
    // تجاهل الجداول داخل النوافذ المنبثقة (modals)
    if (table.closest('.modal')) {
        return false;
    }
    
    return true;
}

function createFormatButton(table, tableIndex) {
    // تجنب إنشاء أزرار مكررة
    if (document.getElementById('formatButton-' + tableIndex)) {
        console.log(`⚠️ زر التنسيق موجود بالفعل للجدول ${tableIndex + 1}`);
        return;
    }

    // البحث عن أفضل مكان لإضافة الزر
    let buttonContainer = findBestButtonLocation(table);
    
    if (!buttonContainer) {
        console.log(`❌ لم يتم العثور على مكان مناسب لإضافة زر التنسيق للجدول ${tableIndex + 1}`);
        return;
    }

    // إنشاء زر التنسيق مع تصميم محسن
    const formatButton = createStyledFormatButton(tableIndex, table);
    
    // إضافة الزر في المكان المناسب
    insertButtonInContainer(buttonContainer, formatButton, table);
    
    console.log(`🎨 تم إنشاء زر التنسيق للجدول ${tableIndex + 1} بنجاح`);
}

function findBestButtonLocation(table) {
    // البحث في أماكن متعددة بترتيب الأولوية
    const searchLocations = [
        // 1. card-header (الأولوية الأولى)
        () => {
            const card = table.closest('.card');
            return card ? card.querySelector('.card-header') : null;
        },
        
        // 2. div يحتوي على أزرار أخرى
        () => {
            const parent = table.parentElement;
            const buttonsContainer = parent.querySelector('.btn-group, .d-flex, .text-end, .text-start');
            return buttonsContainer ? buttonsContainer.parentElement : null;
        },
        
        // 3. table-responsive parent
        () => {
            const tableResponsive = table.closest('.table-responsive');
            return tableResponsive ? tableResponsive.parentElement : null;
        },
        
        // 4. card-body
        () => {
            const cardBody = table.closest('.card-body');
            return cardBody;
        },
        
        // 5. أي container قريب
        () => {
            return table.closest('.container, .container-fluid, .col, [class*="col-"]');
        },
        
        // 6. parent مباشر كحل أخير
        () => {
            return table.parentElement;
        }
    ];
    
    for (let getLocation of searchLocations) {
        const location = getLocation();
        if (location) {
            return location;
        }
    }
    
    return null;
}

function createStyledFormatButton(tableIndex, table) {
    const formatButton = document.createElement('button');
    formatButton.id = 'formatButton-' + tableIndex;
    formatButton.className = 'btn btn-outline-primary btn-sm ms-2 mb-2 format-table-btn';
    formatButton.innerHTML = '<i class="bi bi-palette me-1"></i>تنسيق الجدول';
    formatButton.title = 'تخصيص وتنسيق الجدول';
    
    // إضافة تأثيرات بصرية
    formatButton.style.transition = 'all 0.3s ease';
    formatButton.style.borderRadius = '8px';
    
    // ربط الحدث
    formatButton.onclick = function() { 
        openFormatModal(table, tableIndex); 
    };
    
    // تأثيرات hover
    formatButton.addEventListener('mouseenter', function() {
        this.style.transform = 'translateY(-1px)';
        this.style.boxShadow = '0 4px 12px rgba(74, 144, 226, 0.3)';
    });
    
    formatButton.addEventListener('mouseleave', function() {
        this.style.transform = 'translateY(0)';
        this.style.boxShadow = 'none';
    });
    
    return formatButton;
}

function insertButtonInContainer(container, button, table) {
    // فحص نوع الحاوية وإضافة الزر بالطريقة المناسبة
    const cardHeader = container.closest('.card-header');
    
    if (cardHeader) {
        // إضافة في card-header
        const existingButtons = cardHeader.querySelector('.btn-group, .d-flex');
        if (existingButtons) {
            existingButtons.appendChild(button);
        } else {
            // إنشاء مجموعة أزرار جديدة
            const buttonGroup = document.createElement('div');
            buttonGroup.className = 'd-flex gap-2 ms-auto';
            buttonGroup.appendChild(button);
            cardHeader.appendChild(buttonGroup);
        }
    } else {
        // إنشاء div للزر وإضافته قبل الجدول
        const buttonDiv = document.createElement('div');
        buttonDiv.className = 'mb-2 text-end table-format-controls';
        buttonDiv.appendChild(button);
        
        const tableContainer = table.closest('.table-responsive') || table;
        container.insertBefore(buttonDiv, tableContainer);
    }
}

function openFormatModal(table, tableIndex) {
    console.log('فتح نافذة التنسيق للجدول ' + (tableIndex + 1));
    
    // إنشاء النافذة إذا لم تكن موجودة
    let modal = document.getElementById('formatModal-' + tableIndex);
    if (!modal) {
        modal = createFormatModal(table, tableIndex);
    }

    // فتح النافذة
    const bootstrapModal = new bootstrap.Modal(modal);
    bootstrapModal.show();
}

function createFormatModal(table, tableIndex) {
    const modalId = 'formatModal-' + tableIndex;
    const previewTableId = 'previewTable-' + tableIndex;
    const columnsVisibilityId = 'columnsVisibility-' + tableIndex;
    const previewSectionId = 'previewSection-' + tableIndex;

    // إنشاء HTML للنافذة
    const modalHTML = '<div class="modal fade" id="' + modalId + '" tabindex="-1">' +
        '<div class="modal-dialog modal-xl">' +
            '<div class="modal-content">' +
                '<div class="modal-header">' +
                    '<h5 class="modal-title">' +
                        '<i class="bi bi-palette me-2"></i>تنسيق الجدول' +
                    '</h5>' +
                    '<button type="button" class="btn-close" data-bs-dismiss="modal"></button>' +
                '</div>' +
                '<div class="modal-body">' +
                    '<!-- التحكم العام -->' +
                    '<div class="card mb-3">' +
                        '<div class="card-header">' +
                            '<h6 class="mb-0">' +
                                '<i class="bi bi-gear me-2"></i>التحكم العام' +
                            '</h6>' +
                        '</div>' +
                        '<div class="card-body">' +
                            '<div class="row">' +
                                '<div class="col-md-6">' +
                                    '<label class="form-label">حجم الخط العام</label>' +
                                    '<div class="d-flex align-items-center">' +
                                        '<input type="range" class="form-range me-2" id="globalFontSize-' + tableIndex + '" min="10" max="24" value="14">' +
                                        '<span id="globalFontSizeValue-' + tableIndex + '" class="badge bg-primary">14px</span>' +
                                    '</div>' +
                                '</div>' +
                                '<div class="col-md-6">' +
                                    '<label class="form-label">عرض الأعمدة العام</label>' +
                                    '<div class="d-flex align-items-center">' +
                                        '<input type="range" class="form-range me-2" id="globalColumnWidth-' + tableIndex + '" min="80" max="300" value="150">' +
                                        '<span id="globalColumnWidthValue-' + tableIndex + '" class="badge bg-success">150px</span>' +
                                    '</div>' +
                                '</div>' +
                            '</div>' +
                            '<div class="row mt-3">' +
                                '<div class="col-md-6">' +
                                    '<label class="form-label">وزن الخط</label>' +
                                    '<select class="form-select" id="globalFontWeight-' + tableIndex + '">' +
                                        '<option value="normal">عادي</option>' +
                                        '<option value="bold">عريض</option>' +
                                    '</select>' +
                                '</div>' +
                                '<div class="col-md-6">' +
                                    '<label class="form-label">محاذاة النص</label>' +
                                    '<select class="form-select" id="globalTextAlign-' + tableIndex + '">' +
                                        '<option value="right">يمين</option>' +
                                        '<option value="center">وسط</option>' +
                                        '<option value="left">يسار</option>' +
                                    '</select>' +
                                '</div>' +
                            '</div>' +
                        '</div>' +
                    '</div>' +

                    '<!-- خيارات المعاينة -->' +
                    '<div class="card mb-3">' +
                        '<div class="card-header">' +
                            '<h6 class="mb-0">' +
                                '<i class="bi bi-eye me-2"></i>المعاينة' +
                            '</h6>' +
                        '</div>' +
                        '<div class="card-body">' +
                            '<div class="row">' +
                                '<div class="col-md-6">' +
                                    '<div class="form-check">' +
                                        '<input class="form-check-input" type="radio" name="previewMode-' + tableIndex + '" id="showPreview-' + tableIndex + '" checked>' +
                                        '<label class="form-check-label" for="showPreview-' + tableIndex + '">' +
                                            '<i class="bi bi-eye me-1"></i>إظهار المعاينة' +
                                        '</label>' +
                                    '</div>' +
                                '</div>' +
                                '<div class="col-md-6">' +
                                    '<div class="form-check">' +
                                        '<input class="form-check-input" type="radio" name="previewMode-' + tableIndex + '" id="hidePreview-' + tableIndex + '">' +
                                        '<label class="form-check-label" for="hidePreview-' + tableIndex + '">' +
                                            '<i class="bi bi-eye-slash me-1"></i>إخفاء المعاينة' +
                                        '</label>' +
                                    '</div>' +
                                '</div>' +
                            '</div>' +
                        '</div>' +
                    '</div>' +

                    '<!-- تحكم في الأعمدة -->' +
                    '<div class="card mb-3">' +
                        '<div class="card-header">' +
                            '<h6 class="mb-0">' +
                                '<i class="bi bi-columns me-2"></i>إظهار/إخفاء الأعمدة' +
                            '</h6>' +
                        '</div>' +
                        '<div class="card-body">' +
                            '<div class="row" id="' + columnsVisibilityId + '">' +
                                '<!-- سيتم إضافة checkboxes هنا -->' +
                            '</div>' +
                        '</div>' +
                    '</div>' +

                    '<!-- التحكم الخاص بالأعمدة -->' +
                    '<div class="card mb-3">' +
                        '<div class="card-header">' +
                            '<h6 class="mb-0">' +
                                '<i class="bi bi-sliders me-2"></i>التحكم الخاص بالأعمدة' +
                            '</h6>' +
                        '</div>' +
                        '<div class="card-body">' +
                            '<div id="individualColumnsControl-' + tableIndex + '">' +
                                '<!-- سيتم إضافة تحكم فردي لكل عمود -->' +
                            '</div>' +
                        '</div>' +
                    '</div>' +

                    '<!-- المعاينة -->' +
                    '<div class="card" id="' + previewSectionId + '">' +
                        '<div class="card-header">' +
                            '<h6 class="mb-0">' +
                                '<i class="bi bi-table me-2"></i>معاينة الجدول' +
                            '</h6>' +
                        '</div>' +
                        '<div class="card-body">' +
                            '<div class="table-responsive">' +
                                '<table class="table table-bordered" id="' + previewTableId + '">' +
                                    table.innerHTML +
                                '</table>' +
                            '</div>' +
                        '</div>' +
                    '</div>' +
                '</div>' +
                '<div class="modal-footer">' +
                    '<button type="button" class="btn btn-secondary" data-bs-dismiss="modal">' +
                        '<i class="bi bi-x me-1"></i>إغلاق' +
                    '</button>' +
                    '<button type="button" class="btn btn-success" onclick="applyChanges(\'' + tableIndex + '\')">' +
                        '<i class="bi bi-check me-1"></i>تطبيق التغييرات' +
                    '</button>' +
                '</div>' +
            '</div>' +
        '</div>' +
    '</div>';

    // إضافة النافذة للصفحة
    document.body.insertAdjacentHTML('beforeend', modalHTML);
    const modal = document.getElementById(modalId);

    // تطبيق الكود الذي اقترحه المستخدم
    setTimeout(function() {
        initializeTableControls(previewTableId, columnsVisibilityId, previewSectionId, tableIndex);
    }, 100);

    return modal;
}

function initializeTableControls(previewTableId, columnsVisibilityId, previewSectionId, tableIndex) {
    const previewTable = document.getElementById(previewTableId);
    const columnsVisibilityContainer = document.getElementById(columnsVisibilityId);
    const previewSection = document.getElementById(previewSectionId);

    if (!previewTable || !columnsVisibilityContainer || !previewSection) {
        console.log('عناصر التحكم غير موجودة');
        return;
    }

    // التحكم العام في الخط وعرض الأعمدة
    setupGlobalControls(previewTable, tableIndex);

    // الحصول على جميع عناوين الأعمدة
    const headers = previewTable.querySelectorAll("thead th");

    // إنشاء التحكم الفردي بالأعمدة
    setupIndividualColumnControls(previewTable, tableIndex, headers);

    // إنشاء checkboxes لكل عمود
    headers.forEach(function(header, index) {
        const colName = header.textContent.trim();

        const div = document.createElement("div");
        div.className = "form-check col-md-4 mb-2";

        const checkbox = document.createElement("input");
        checkbox.type = "checkbox";
        checkbox.className = "form-check-input";
        checkbox.id = 'col-' + tableIndex + '-' + index;
        checkbox.checked = true;

        const label = document.createElement("label");
        label.className = "form-check-label";
        label.setAttribute("for", 'col-' + tableIndex + '-' + index);
        label.textContent = colName;

        div.appendChild(checkbox);
        div.appendChild(label);
        columnsVisibilityContainer.appendChild(div);

        // تعامل مع تغيير الحالة
        checkbox.addEventListener("change", function () {
            // إخفاء/إظهار العمود في المعاينة
            const headerCell = previewTable.querySelectorAll("thead th")[index];
            if (headerCell) {
                headerCell.style.display = this.checked ? "" : "none";
            }

            const rows = previewTable.querySelectorAll("tbody tr");
            rows.forEach(function(row) {
                const cells = row.getElementsByTagName("td");
                if (cells[index]) {
                    cells[index].style.display = checkbox.checked ? "" : "none";
                }
            });
        });
    });

    // التعامل مع زر المعاينة / إخفاء المعاينة
    const previewRadio = document.getElementById('showPreview-' + tableIndex);
    const hidePreviewRadio = document.getElementById('hidePreview-' + tableIndex);

    if (previewRadio) {
        previewRadio.addEventListener("change", function () {
            if (this.checked) {
                previewSection.style.display = "";
            }
        });
    }

    if (hidePreviewRadio) {
        hidePreviewRadio.addEventListener("change", function () {
            if (this.checked) {
                previewSection.style.display = "none";
            }
        });
    }

    console.log('✅ تم تهيئة التحكم في الجدول بنجاح');
}

function setupGlobalControls(previewTable, tableIndex) {
    // التحكم في حجم الخط العام
    const globalFontSize = document.getElementById('globalFontSize-' + tableIndex);
    const globalFontSizeValue = document.getElementById('globalFontSizeValue-' + tableIndex);
    
    if (globalFontSize && globalFontSizeValue) {
        globalFontSize.addEventListener('input', function() {
            const fontSize = this.value + 'px';
            globalFontSizeValue.textContent = fontSize;
            
            // تطبيق على جميع خلايا الجدول
            const allCells = previewTable.querySelectorAll('th, td');
            allCells.forEach(function(cell) {
                cell.style.fontSize = fontSize;
            });
        });
    }

    // التحكم في عرض الأعمدة العام
    const globalColumnWidth = document.getElementById('globalColumnWidth-' + tableIndex);
    const globalColumnWidthValue = document.getElementById('globalColumnWidthValue-' + tableIndex);
    
    if (globalColumnWidth && globalColumnWidthValue) {
        globalColumnWidth.addEventListener('input', function() {
            const width = this.value + 'px';
            globalColumnWidthValue.textContent = width;
            
            // تطبيق على جميع الأعمدة
            const headers = previewTable.querySelectorAll('thead th');
            headers.forEach(function(header) {
                header.style.minWidth = width;
                header.style.width = width;
            });
            
            const cells = previewTable.querySelectorAll('tbody td');
            cells.forEach(function(cell) {
                cell.style.minWidth = width;
                cell.style.width = width;
            });
        });
    }

    // التحكم في وزن الخط
    const globalFontWeight = document.getElementById('globalFontWeight-' + tableIndex);
    if (globalFontWeight) {
        globalFontWeight.addEventListener('change', function() {
            const fontWeight = this.value;
            
            const allCells = previewTable.querySelectorAll('th, td');
            allCells.forEach(function(cell) {
                cell.style.fontWeight = fontWeight;
            });
        });
    }

    // التحكم في محاذاة النص
    const globalTextAlign = document.getElementById('globalTextAlign-' + tableIndex);
    if (globalTextAlign) {
        globalTextAlign.addEventListener('change', function() {
            const textAlign = this.value;
            
            const allCells = previewTable.querySelectorAll('th, td');
            allCells.forEach(function(cell) {
                cell.style.textAlign = textAlign;
            });
        });
    }
}

function setupIndividualColumnControls(previewTable, tableIndex, headers) {
    const individualColumnsControl = document.getElementById('individualColumnsControl-' + tableIndex);
    if (!individualColumnsControl) {
        console.log('عنصر التحكم الفردي غير موجود');
        return;
    }

    headers.forEach(function(header, index) {
        const colName = header.textContent.trim();

        // إنشاء بطاقة لكل عمود
        const columnCard = document.createElement("div");
        columnCard.className = "card mb-3 column-control-card";
        
        const cardHeader = document.createElement("div");
        cardHeader.className = "card-header";
        cardHeader.innerHTML = '<h6 class="mb-0"><i class="bi bi-layout-text-window me-2"></i>' + colName + '</h6>';
        
        const cardBody = document.createElement("div");
        cardBody.className = "card-body";
        
        // إخفاء/إظهار العمود
        const visibilityDiv = document.createElement("div");
        visibilityDiv.className = "mb-3";
        visibilityDiv.innerHTML = 
            '<div class="form-check form-switch">' +
                '<input class="form-check-input" type="checkbox" id="colVisible-' + tableIndex + '-' + index + '" checked>' +
                '<label class="form-check-label" for="colVisible-' + tableIndex + '-' + index + '">' +
                    '<i class="bi bi-eye me-1"></i>إظهار العمود' +
                '</label>' +
            '</div>';
        
        // حجم الخط للعمود
        const fontSizeDiv = document.createElement("div");
        fontSizeDiv.className = "mb-3";
        fontSizeDiv.innerHTML = 
            '<label class="form-label">حجم الخط</label>' +
            '<div class="d-flex align-items-center">' +
                '<input type="range" class="form-range me-2" id="colFontSize-' + tableIndex + '-' + index + '" min="10" max="24" value="14">' +
                '<span id="colFontSizeValue-' + tableIndex + '-' + index + '" class="badge bg-info">14px</span>' +
            '</div>';
        
        // عرض العمود
        const widthDiv = document.createElement("div");
        widthDiv.className = "mb-3";
        widthDiv.innerHTML = 
            '<label class="form-label">عرض العمود</label>' +
            '<div class="d-flex align-items-center">' +
                '<input type="range" class="form-range me-2" id="colWidth-' + tableIndex + '-' + index + '" min="80" max="400" value="150">' +
                '<span id="colWidthValue-' + tableIndex + '-' + index + '" class="badge bg-warning">150px</span>' +
            '</div>';
        
        // وزن الخط ومحاذاة النص
        const styleDiv = document.createElement("div");
        styleDiv.className = "row";
        styleDiv.innerHTML = 
            '<div class="col-md-6">' +
                '<label class="form-label">وزن الخط</label>' +
                '<select class="form-select" id="colFontWeight-' + tableIndex + '-' + index + '">' +
                    '<option value="normal">عادي</option>' +
                    '<option value="bold">عريض</option>' +
                '</select>' +
            '</div>' +
            '<div class="col-md-6">' +
                '<label class="form-label">محاذاة النص</label>' +
                '<select class="form-select" id="colTextAlign-' + tableIndex + '-' + index + '">' +
                    '<option value="right">يمين</option>' +
                    '<option value="center">وسط</option>' +
                    '<option value="left">يسار</option>' +
                '</select>' +
            '</div>';
        
        // تجميع العناصر
        cardBody.appendChild(visibilityDiv);
        cardBody.appendChild(fontSizeDiv);
        cardBody.appendChild(widthDiv);
        cardBody.appendChild(styleDiv);
        
        columnCard.appendChild(cardHeader);
        columnCard.appendChild(cardBody);
        
        individualColumnsControl.appendChild(columnCard);
        
        // ربط الأحداث
        setupColumnEventListeners(previewTable, tableIndex, index);
    });
}

function setupColumnEventListeners(previewTable, tableIndex, columnIndex) {
    // إخفاء/إظهار العمود
    const visibilityCheckbox = document.getElementById('colVisible-' + tableIndex + '-' + columnIndex);
    if (visibilityCheckbox) {
        visibilityCheckbox.addEventListener('change', function() {
            const headerCell = previewTable.querySelectorAll("thead th")[columnIndex];
            if (headerCell) {
                headerCell.style.display = this.checked ? "" : "none";
            }

            const rows = previewTable.querySelectorAll("tbody tr");
            rows.forEach(function(row) {
                const cells = row.getElementsByTagName("td");
                if (cells[columnIndex]) {
                    cells[columnIndex].style.display = visibilityCheckbox.checked ? "" : "none";
                }
            });
        });
    }
    
    // حجم الخط
    const fontSizeRange = document.getElementById('colFontSize-' + tableIndex + '-' + columnIndex);
    const fontSizeValue = document.getElementById('colFontSizeValue-' + tableIndex + '-' + columnIndex);
    if (fontSizeRange && fontSizeValue) {
        fontSizeRange.addEventListener('input', function() {
            const fontSize = this.value + 'px';
            fontSizeValue.textContent = fontSize;
            
            // تطبيق على العمود المحدد
            const headerCell = previewTable.querySelectorAll("thead th")[columnIndex];
            if (headerCell) {
                headerCell.style.fontSize = fontSize;
            }
            
            const rows = previewTable.querySelectorAll("tbody tr");
            rows.forEach(function(row) {
                const cells = row.getElementsByTagName("td");
                if (cells[columnIndex]) {
                    cells[columnIndex].style.fontSize = fontSize;
                }
            });
        });
    }
    
    // عرض العمود
    const widthRange = document.getElementById('colWidth-' + tableIndex + '-' + columnIndex);
    const widthValue = document.getElementById('colWidthValue-' + tableIndex + '-' + columnIndex);
    if (widthRange && widthValue) {
        widthRange.addEventListener('input', function() {
            const width = this.value + 'px';
            widthValue.textContent = width;
            
            // تطبيق على العمود المحدد
            const headerCell = previewTable.querySelectorAll("thead th")[columnIndex];
            if (headerCell) {
                headerCell.style.minWidth = width;
                headerCell.style.width = width;
            }
            
            const rows = previewTable.querySelectorAll("tbody tr");
            rows.forEach(function(row) {
                const cells = row.getElementsByTagName("td");
                if (cells[columnIndex]) {
                    cells[columnIndex].style.minWidth = width;
                    cells[columnIndex].style.width = width;
                }
            });
        });
    }
    
    // وزن الخط
    const fontWeightSelect = document.getElementById('colFontWeight-' + tableIndex + '-' + columnIndex);
    if (fontWeightSelect) {
        fontWeightSelect.addEventListener('change', function() {
            const fontWeight = this.value;
            
            const headerCell = previewTable.querySelectorAll("thead th")[columnIndex];
            if (headerCell) {
                headerCell.style.fontWeight = fontWeight;
            }
            
            const rows = previewTable.querySelectorAll("tbody tr");
            rows.forEach(function(row) {
                const cells = row.getElementsByTagName("td");
                if (cells[columnIndex]) {
                    cells[columnIndex].style.fontWeight = fontWeight;
                }
            });
        });
    }
    
    // محاذاة النص
    const textAlignSelect = document.getElementById('colTextAlign-' + tableIndex + '-' + columnIndex);
    if (textAlignSelect) {
        textAlignSelect.addEventListener('change', function() {
            const textAlign = this.value;
            
            const headerCell = previewTable.querySelectorAll("thead th")[columnIndex];
            if (headerCell) {
                headerCell.style.textAlign = textAlign;
            }
            
            const rows = previewTable.querySelectorAll("tbody tr");
            rows.forEach(function(row) {
                const cells = row.getElementsByTagName("td");
                if (cells[columnIndex]) {
                    cells[columnIndex].style.textAlign = textAlign;
                }
            });
        });
    }
}

function applyChanges(tableIndex) {
    const previewTable = document.getElementById('previewTable-' + tableIndex);
    const originalTable = document.querySelectorAll('table')[tableIndex];

    if (!previewTable || !originalTable) {
        console.log('❌ لم يتم العثور على الجداول');
        return;
    }

    // نسخ تغييرات الرؤية (إخفاء/إظهار الأعمدة)
    const previewHeaders = previewTable.querySelectorAll("thead th");
    const originalHeaders = originalTable.querySelectorAll("thead th");

    previewHeaders.forEach(function(previewHeader, index) {
        if (originalHeaders[index]) {
            originalHeaders[index].style.display = previewHeader.style.display;
        }
    });

    const previewRows = previewTable.querySelectorAll("tbody tr");
    const originalRows = originalTable.querySelectorAll("tbody tr");

    previewRows.forEach(function(previewRow, rowIndex) {
        if (originalRows[rowIndex]) {
            const previewCells = previewRow.querySelectorAll("td");
            const originalCells = originalRows[rowIndex].querySelectorAll("td");

            previewCells.forEach(function(previewCell, cellIndex) {
                if (originalCells[cellIndex]) {
                    originalCells[cellIndex].style.display = previewCell.style.display;
                }
            });
        }
    });

    // نسخ تغييرات التنسيق (الخط وعرض الأعمدة)
    copyFormattingStyles(previewTable, originalTable);

    // إغلاق النافذة
    const modal = bootstrap.Modal.getInstance(document.getElementById('formatModal-' + tableIndex));
    if (modal) {
        modal.hide();
    }

    console.log('✅ تم تطبيق التغييرات بنجاح');
}

function copyFormattingStyles(previewTable, originalTable) {
    // نسخ تنسيق العناوين
    const previewHeaders = previewTable.querySelectorAll('thead th');
    const originalHeaders = originalTable.querySelectorAll('thead th');
    
    previewHeaders.forEach(function(previewHeader, index) {
        if (originalHeaders[index]) {
            // نسخ جميع الأنماط
            originalHeaders[index].style.fontSize = previewHeader.style.fontSize;
            originalHeaders[index].style.fontWeight = previewHeader.style.fontWeight;
            originalHeaders[index].style.textAlign = previewHeader.style.textAlign;
            originalHeaders[index].style.minWidth = previewHeader.style.minWidth;
            originalHeaders[index].style.width = previewHeader.style.width;
        }
    });

    // نسخ تنسيق الخلايا
    const previewCells = previewTable.querySelectorAll('tbody td');
    const originalCells = originalTable.querySelectorAll('tbody td');
    
    previewCells.forEach(function(previewCell, index) {
        if (originalCells[index]) {
            // نسخ جميع الأنماط
            originalCells[index].style.fontSize = previewCell.style.fontSize;
            originalCells[index].style.fontWeight = previewCell.style.fontWeight;
            originalCells[index].style.textAlign = previewCell.style.textAlign;
            originalCells[index].style.minWidth = previewCell.style.minWidth;
            originalCells[index].style.width = previewCell.style.width;
        }
    });
}

// إضافة الدوال للنافذة العامة للاختبار
window.applyChanges = applyChanges;
window.createFormatButton = createFormatButton;
window.openFormatModal = openFormatModal;

// دالة لإعادة تهيئة النظام يدوياً
window.reinitializeFormatter = function() {
    console.log('🔄 إعادة تهيئة نظام التنسيق...');
    const tables = document.querySelectorAll('table');
    tables.forEach(function(table, tableIndex) {
        createFormatButton(table, tableIndex);
    });
}; 