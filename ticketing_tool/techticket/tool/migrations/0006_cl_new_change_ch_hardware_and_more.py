# Generated by Django 4.1.6 on 2023-03-24 12:09

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tool', '0005_alter_user_activity_log_duration'),
    ]

    operations = [
        migrations.AddField(
            model_name='cl_new_change',
            name='ch_hardware',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tool.cl_hardware'),
        ),
        migrations.AlterField(
            model_name='user_activity_log',
            name='duration',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 24, 12, 9, 50, 851949)),
        ),
    ]