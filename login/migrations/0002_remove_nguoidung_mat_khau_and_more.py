# Generated by Django 5.0.4 on 2024-05-07 20:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nguoidung',
            name='MAT_KHAU',
        ),
        migrations.RemoveField(
            model_name='nguoidung',
            name='NHAP_LAI_MAT_KHAU',
        ),
    ]
