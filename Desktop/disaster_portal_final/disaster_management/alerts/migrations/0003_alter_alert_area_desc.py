# Generated by Django 4.2.16 on 2024-10-16 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alerts', '0002_alter_alert_description_alter_alert_headline'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alert',
            name='area_desc',
            field=models.TextField(),
        ),
    ]