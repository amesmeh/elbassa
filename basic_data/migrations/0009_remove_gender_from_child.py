# Generated by Django 5.2.1 on 2025-06-06 05:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basic_data', '0008_remove_sibling_count_fields'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='child',
            name='gender',
        ),
    ]
