# Generated by Django 4.2.16 on 2024-10-16 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Alert',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(max_length=255)),
                ('sender', models.CharField(max_length=255)),
                ('sent_time', models.DateTimeField()),
                ('status', models.CharField(max_length=100)),
                ('msg_type', models.CharField(max_length=100)),
                ('scope', models.CharField(max_length=100)),
                ('category', models.TextField(null=True)),
                ('event', models.CharField(max_length=255)),
                ('urgency', models.CharField(max_length=100)),
                ('certainty', models.CharField(max_length=100)),
                ('effective', models.DateTimeField()),
                ('onset', models.DateTimeField(null=True)),
                ('expires', models.DateTimeField()),
                ('headline', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('area', models.TextField()),
                ('area_desc', models.CharField(max_length=255)),
                ('polygon', models.TextField()),
                ('severity', models.TextField()),
            ],
            options={
                'db_table': 'cap_alerts1',
            },
        ),
    ]