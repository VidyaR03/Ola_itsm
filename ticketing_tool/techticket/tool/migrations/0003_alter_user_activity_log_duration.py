# Generated by Django 4.1.6 on 2023-03-21 12:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tool', '0002_alter_user_activity_log_duration_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_activity_log',
            name='duration',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 21, 12, 17, 15, 57155)),
        ),
    ]
