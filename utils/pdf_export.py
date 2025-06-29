"""
نظام تصدير PDF مع دعم الخطوط العربية
"""
import os
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.conf import settings
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

try:
    from reportlab.lib.pagesizes import A4, letter
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.lib.enums import TA_RIGHT, TA_CENTER, TA_LEFT
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False
    logger.warning("ReportLab not installed. PDF export will use alternative method.")

try:
    import weasyprint
    WEASYPRINT_AVAILABLE = True
except ImportError:
    WEASYPRINT_AVAILABLE = False
    logger.warning("WeasyPrint not installed. HTML to PDF conversion not available.")


class ArabicPDFExporter:
    """فئة تصدير PDF مع دعم الخطوط العربية"""
    
    def __init__(self):
        self.setup_arabic_fonts()
    
    def setup_arabic_fonts(self):
        """إعداد الخطوط العربية"""
        if not REPORTLAB_AVAILABLE:
            return
            
        try:
            # محاولة تسجيل خط عربي
            # يمكن إضافة ملفات خطوط TTF في مجلد static/fonts/
            font_path = os.path.join(settings.STATIC_ROOT or settings.BASE_DIR, 'static', 'fonts')
            
            # خطوط افتراضية للنظام
            system_fonts = [
                'Arial Unicode MS',
                'Tahoma',
                'Arial',
                'DejaVu Sans'
            ]
            
            self.arabic_font = 'Helvetica'  # خط افتراضي
            
            # محاولة العثور على خط يدعم العربية
            for font_name in system_fonts:
                try:
                    # هذا مجرد اختبار - في الواقع نحتاج ملفات TTF
                    self.arabic_font = font_name
                    break
                except:
                    continue
                    
        except Exception as e:
            logger.warning(f"Could not setup Arabic fonts: {e}")
            self.arabic_font = 'Helvetica'
    
    def create_table_pdf(self, data, headers, title, filename=None, config=None):
        """إنشاء PDF من بيانات جدول"""
        if not REPORTLAB_AVAILABLE:
            return self._create_html_pdf(data, headers, title, filename)
        
        try:
            buffer = BytesIO()
            doc = SimpleDocTemplate(
                buffer,
                pagesize=A4,
                rightMargin=50,
                leftMargin=50,
                topMargin=50,
                bottomMargin=50
            )
            
            # إعداد الأنماط
            styles = getSampleStyleSheet()
            
            # استخدام الإعدادات المخصصة إذا توفرت
            font_name = config.get('font_name', 'Helvetica') if config else 'Helvetica'
            font_size = config.get('font_size', 12) if config else 12
            direction = config.get('direction', 'rtl') if config else 'rtl'
            align = config.get('align', 'right') if config else 'right'
            
            # تحديد محاذاة النص
            if align == 'right':
                alignment = TA_RIGHT
            elif align == 'center':
                alignment = TA_CENTER
            else:
                alignment = TA_LEFT
            
            # نمط العنوان
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontName=font_name,
                fontSize=font_size + 6,
                spaceAfter=30,
                alignment=TA_CENTER,
                textColor=colors.black
            )
            
            # نمط النص العادي
            normal_style = ParagraphStyle(
                'CustomNormal',
                parent=styles['Normal'],
                fontName=font_name,
                fontSize=font_size - 2,
                alignment=alignment
            )
            
            # بناء المحتوى
            story = []
            
            # العنوان
            story.append(Paragraph(title, title_style))
            story.append(Spacer(1, 12))
            
            # تاريخ التقرير
            date_text = f"تاريخ التقرير: {datetime.now().strftime('%Y/%m/%d %H:%M')}"
            story.append(Paragraph(date_text, normal_style))
            story.append(Spacer(1, 12))
            
            # إعداد بيانات الجدول
            table_data = [headers]
            table_data.extend(data)
            
            # حساب عرض الأعمدة بناءً على عدد الأعمدة
            num_cols = len(headers)
            if num_cols <= 5:
                col_widths = [A4[0] / num_cols * 0.8] * num_cols
            else:
                # للجداول الكبيرة، استخدم أعراض متغيرة
                col_widths = [A4[0] / num_cols * 0.7] * num_cols
            
            # إنشاء الجدول
            table = Table(table_data, colWidths=col_widths)
            table.setStyle(TableStyle([
                # نمط الرأس
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4472C4')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), font_name),
                ('FONTSIZE', (0, 0), (-1, 0), font_size),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('TOPPADDING', (0, 0), (-1, 0), 12),
                
                # نمط البيانات
                ('FONTNAME', (0, 1), (-1, -1), font_name),
                ('FONTSIZE', (0, 1), (-1, -1), font_size - 1),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('LEFTPADDING', (0, 0), (-1, -1), 6),
                ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 1), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
                
                # تلوين الصفوف بالتناوب
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F2F2F2')])
            ]))
            
            story.append(table)
            
            # بناء PDF
            doc.build(story)
            
            # إعداد الاستجابة
            buffer.seek(0)
            response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
            
            if filename:
                response['Content-Disposition'] = f'attachment; filename="{filename}"'
            else:
                response['Content-Disposition'] = 'attachment; filename="report.pdf"'
            
            return response
            
        except Exception as e:
            logger.error(f"Error creating PDF: {e}")
            return self._create_fallback_response(title, data, headers)
    
    def _create_html_pdf(self, data, headers, title, filename=None):
        """إنشاء PDF من HTML باستخدام WeasyPrint"""
        if not WEASYPRINT_AVAILABLE:
            return self._create_fallback_response(title, data, headers)
        
        try:
            # إنشاء HTML
            html_content = self._generate_html_table(data, headers, title)
            
            # تحويل إلى PDF
            pdf = weasyprint.HTML(string=html_content).write_pdf()
            
            response = HttpResponse(pdf, content_type='application/pdf')
            if filename:
                response['Content-Disposition'] = f'attachment; filename="{filename}"'
            else:
                response['Content-Disposition'] = 'attachment; filename="report.pdf"'
            
            return response
            
        except Exception as e:
            logger.error(f"Error creating HTML PDF: {e}")
            return self._create_fallback_response(title, data, headers)
    
    def _generate_html_table(self, data, headers, title):
        """إنشاء جدول HTML للتصدير"""
        html = f"""
        <!DOCTYPE html>
        <html dir="rtl" lang="ar">
        <head>
            <meta charset="UTF-8">
            <title>{title}</title>
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Arabic:wght@400;700&display=swap');
                
                body {{
                    font-family: 'Noto Sans Arabic', 'Simplified Arabic', 'Arial', 'Tahoma', sans-serif;
                    direction: rtl;
                    text-align: right;
                    margin: 20px;
                    font-size: 12px;
                    line-height: 1.4;
                }}
                h1 {{
                    text-align: center;
                    color: #333;
                    margin-bottom: 20px;
                    font-size: 18px;
                    font-weight: 700;
                }}
                .date {{
                    text-align: center;
                    color: #666;
                    margin-bottom: 20px;
                    font-size: 10px;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 20px;
                    font-size: 11px;
                }}
                th, td {{
                    border: 1px solid #333;
                    padding: 8px 6px;
                    text-align: center;
                    vertical-align: middle;
                }}
                th {{
                    background-color: #4472C4;
                    color: white;
                    font-weight: 700;
                    font-size: 12px;
                }}
                tr:nth-child(even) {{
                    background-color: #F2F2F2;
                }}
                tr:nth-child(odd) {{
                    background-color: white;
                }}
                td {{
                    word-wrap: break-word;
                    max-width: 150px;
                }}
                .gender-male {{
                    color: #0066CC;
                }}
                .gender-female {{
                    color: #CC0066;
                }}
            </style>
        </head>
        <body>
            <h1>{title}</h1>
            <div class="date">تاريخ التقرير: {datetime.now().strftime('%Y/%m/%d %H:%M')}</div>
            <table>
                <thead>
                    <tr>
        """
        
        # إضافة رؤوس الجدول
        for header in headers:
            html += f"<th>{header}</th>"
        
        html += """
                    </tr>
                </thead>
                <tbody>
        """
        
        # إضافة بيانات الجدول
        for row in data:
            html += "<tr>"
            for i, cell in enumerate(row):
                # تطبيق تنسيق خاص للجنس
                cell_class = ""
                if i == 2 and str(cell) == "ذكر":  # عمود الجنس
                    cell_class = ' class="gender-male"'
                elif i == 2 and str(cell) == "أنثى":
                    cell_class = ' class="gender-female"'
                
                html += f"<td{cell_class}>{cell}</td>"
            html += "</tr>"
        
        html += """
                </tbody>
            </table>
        </body>
        </html>
        """
        
        return html
    
    def _create_fallback_response(self, title, data, headers):
        """إنشاء استجابة بديلة في حالة فشل PDF"""
        # إنشاء ملف CSV كبديل
        import csv
        from django.http import HttpResponse
        
        response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
        response['Content-Disposition'] = 'attachment; filename="report.csv"'
        
        writer = csv.writer(response)
        writer.writerow(headers)
        for row in data:
            writer.writerow(row)
        
        return response


# دوال مساعدة للاستخدام السريع
def export_queryset_to_pdf(queryset, fields, title, filename=None):
    """تصدير QuerySet إلى PDF"""
    exporter = ArabicPDFExporter()
    
    # استخراج البيانات
    headers = [field.replace('_', ' ').title() for field in fields]
    data = []
    
    for obj in queryset:
        row = []
        for field in fields:
            value = getattr(obj, field, '')
            if hasattr(value, '__call__'):
                value = value()
            row.append(str(value))
        data.append(row)
    
    return exporter.create_table_pdf(data, headers, title, filename)


def export_statistics_to_pdf(stats_data, title, filename=None):
    """تصدير إحصائيات إلى PDF"""
    exporter = ArabicPDFExporter()
    
    # تحويل البيانات الإحصائية إلى جدول
    headers = ['البيان', 'القيمة']
    data = []
    
    for key, value in stats_data.items():
        data.append([str(key), str(value)])
    
    return exporter.create_table_pdf(data, headers, title, filename) 