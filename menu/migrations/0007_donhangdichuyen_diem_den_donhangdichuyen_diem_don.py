# Generated by Django 5.0.4 on 2024-05-15 16:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("menu", "0006_donhangdichuyen"),
    ]

    operations = [
        migrations.AddField(
            model_name="donhangdichuyen",
            name="diem_den",
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AddField(
            model_name="donhangdichuyen",
            name="diem_don",
            field=models.CharField(max_length=150, null=True),
        ),
    ]
