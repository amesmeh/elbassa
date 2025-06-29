// إعداد الخطوط العربية لـ pdfMake
(function() {
    // إعداد الخط العربي
    if (typeof pdfMake !== 'undefined') {
        // تحديد الخطوط المدعومة
        pdfMake.fonts = {
            // الخط الافتراضي (يدعم العربية)
            Roboto: {
                normal: 'Roboto-Regular.ttf',
                bold: 'Roboto-Medium.ttf',
                italics: 'Roboto-Italic.ttf',
                bolditalics: 'Roboto-MediumItalic.ttf'
            },
            // خط عربي (سنستخدم خط النظام)
            Arial: {
                normal: 'Arial',
                bold: 'Arial-Bold',
                italics: 'Arial-Italic',
                bolditalics: 'Arial-BoldItalic'
            }
        };

        // إعداد الخط الافتراضي
        pdfMake.defaultFont = 'Arial';

        // دالة لإعداد PDF مع دعم العربية
        window.setupArabicPDF = function() {
            return {
                pageSize: 'A4',
                pageOrientation: 'portrait',
                pageMargins: [40, 60, 40, 60],
                defaultStyle: {
                    font: 'Arial',
                    fontSize: 10,
                    direction: 'rtl',
                    alignment: 'right'
                },
                styles: {
                    header: {
                        fontSize: 18,
                        bold: true,
                        alignment: 'center',
                        margin: [0, 0, 0, 20]
                    },
                    subheader: {
                        fontSize: 14,
                        bold: true,
                        margin: [0, 10, 0, 5]
                    },
                    tableHeader: {
                        bold: true,
                        fontSize: 11,
                        color: 'black',
                        fillColor: '#f0f0f0'
                    },
                    tableCell: {
                        fontSize: 10,
                        margin: [2, 2, 2, 2]
                    }
                }
            };
        };

        // دالة لتحويل جدول HTML إلى PDF مع دعم العربية
        window.exportTableToPDF = function(tableId, title, filename) {
            try {
                const table = document.getElementById(tableId);
                if (!table) {
                    alert('لم يتم العثور على الجدول');
                    return;
                }

                // استخراج البيانات من الجدول
                const headers = [];
                const headerCells = table.querySelectorAll('thead th');
                headerCells.forEach(cell => {
                    headers.push({
                        text: cell.textContent.trim(),
                        style: 'tableHeader',
                        alignment: 'center'
                    });
                });

                const rows = [];
                const bodyRows = table.querySelectorAll('tbody tr');
                bodyRows.forEach(row => {
                    const rowData = [];
                    const cells = row.querySelectorAll('td');
                    cells.forEach((cell, index) => {
                        // تجاهل عمود الإجراءات (عادة الأخير)
                        if (index < cells.length - 1) {
                            rowData.push({
                                text: cell.textContent.trim(),
                                style: 'tableCell',
                                alignment: 'center'
                            });
                        }
                    });
                    if (rowData.length > 0) {
                        rows.push(rowData);
                    }
                });

                // إنشاء محتوى PDF
                const docDefinition = {
                    ...window.setupArabicPDF(),
                    content: [
                        {
                            text: title || 'تقرير',
                            style: 'header'
                        },
                        {
                            text: `تاريخ التصدير: ${new Date().toLocaleDateString('ar-EG')}`,
                            style: 'subheader',
                            alignment: 'center',
                            margin: [0, 0, 0, 20]
                        },
                        {
                            table: {
                                headerRows: 1,
                                widths: Array(headers.length - 1).fill('*'), // تجاهل عمود الإجراءات
                                body: [
                                    headers.slice(0, -1), // إزالة عمود الإجراءات من الرؤوس
                                    ...rows
                                ]
                            },
                            layout: {
                                fillColor: function (rowIndex, node, columnIndex) {
                                    return (rowIndex % 2 === 0) ? '#f9f9f9' : null;
                                },
                                hLineWidth: function (i, node) {
                                    return 0.5;
                                },
                                vLineWidth: function (i, node) {
                                    return 0.5;
                                },
                                hLineColor: function (i, node) {
                                    return '#ddd';
                                },
                                vLineColor: function (i, node) {
                                    return '#ddd';
                                }
                            }
                        }
                    ]
                };

                // تصدير PDF
                pdfMake.createPdf(docDefinition).download(filename || 'report.pdf');
                
            } catch (error) {
                console.error('خطأ في تصدير PDF:', error);
                alert('حدث خطأ أثناء تصدير PDF. سيتم استخدام طريقة بديلة.');
                
                // طريقة بديلة: طباعة الصفحة
                window.print();
            }
        };

        // دالة لتصدير إحصائيات مخصصة
        window.exportStatisticsToPDF = function(title, data, filename) {
            try {
                const docDefinition = {
                    ...window.setupArabicPDF(),
                    content: [
                        {
                            text: title || 'تقرير إحصائي',
                            style: 'header'
                        },
                        {
                            text: `تاريخ التقرير: ${new Date().toLocaleDateString('ar-EG')}`,
                            style: 'subheader',
                            alignment: 'center',
                            margin: [0, 0, 0, 20]
                        }
                    ]
                };

                // إضافة البيانات
                if (Array.isArray(data)) {
                    data.forEach(section => {
                        if (section.title) {
                            docDefinition.content.push({
                                text: section.title,
                                style: 'subheader'
                            });
                        }
                        
                        if (section.table) {
                            docDefinition.content.push({
                                table: {
                                    headerRows: 1,
                                    widths: section.table.widths || ['*', '*'],
                                    body: section.table.body
                                },
                                layout: 'lightHorizontalLines',
                                margin: [0, 5, 0, 15]
                            });
                        }
                        
                        if (section.text) {
                            docDefinition.content.push({
                                text: section.text,
                                margin: [0, 5, 0, 10]
                            });
                        }
                    });
                }

                pdfMake.createPdf(docDefinition).download(filename || 'statistics.pdf');
                
            } catch (error) {
                console.error('خطأ في تصدير الإحصائيات:', error);
                alert('حدث خطأ أثناء تصدير PDF');
            }
        };
    }

    // إعداد DataTables مع دعم العربية محسن
    window.setupDataTablesWithArabicPDF = function(tableSelector, options = {}) {
        const defaultOptions = {
            language: {
                url: '//cdn.datatables.net/plug-ins/1.13.6/i18n/ar.json'
            },
            dom: 'Bfrtip',
            buttons: [
                {
                    extend: 'excel',
                    text: '<i class="bi bi-file-earmark-excel me-1"></i>تصدير Excel',
                    className: 'btn btn-success btn-sm',
                    charset: 'utf-8',
                    bom: true
                },
                {
                    text: '<i class="bi bi-file-earmark-pdf me-1"></i>تصدير PDF',
                    className: 'btn btn-danger btn-sm',
                    action: function (e, dt, button, config) {
                        const tableId = dt.table().node().id;
                        const title = options.pdfTitle || 'تقرير';
                        const filename = options.pdfFilename || 'report.pdf';
                        window.exportTableToPDF(tableId, title, filename);
                    }
                },
                {
                    extend: 'print',
                    text: '<i class="bi bi-printer me-1"></i>طباعة',
                    className: 'btn btn-info btn-sm'
                }
            ],
            responsive: true,
            pageLength: 25,
            order: [[0, 'asc']]
        };

        // دمج الخيارات
        const finalOptions = { ...defaultOptions, ...options };
        
        return $(tableSelector).DataTable(finalOptions);
    };

})(); 