# Generated by Django 4.2.16 on 2024-10-16 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alerts', '0003_alter_alert_area_desc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alert',
            name='area_desc',
            field=models.TextField(null=True),
        ),
    ]
