# Generated by Django 5.0.4 on 2024-05-12 21:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("menu", "0002_rename_tinhtrangdquan_quanan_tinhtrangquan"),
    ]

    operations = [
        migrations.AddField(
            model_name="quanan",
            name="lat",
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name="quanan",
            name="var",
            field=models.FloatField(default=0),
        ),
    ]
