# Generated by Django 5.0.4 on 2024-05-12 21:15

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("menu", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="quanan",
            old_name="tinhtrangdquan",
            new_name="tinhtrangquan",
        ),
    ]
