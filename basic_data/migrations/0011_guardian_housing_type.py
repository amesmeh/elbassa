# Generated by Django 5.2.1 on 2025-06-06 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic_data', '0010_representative'),
    ]

    operations = [
        migrations.AddField(
            model_name='guardian',
            name='housing_type',
            field=models.CharField(blank=True, choices=[('ملك', 'ملك'), ('إيجار', 'إيجار'), ('مع الأهل', 'مع الأهل'), ('أخرى', 'أخرى')], max_length=20, null=True, verbose_name='نوع السكن'),
        ),
    ]
