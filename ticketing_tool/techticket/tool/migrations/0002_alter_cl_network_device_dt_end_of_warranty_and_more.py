# Generated by Django 4.1.3 on 2023-02-20 10:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tool', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cl_network_device',
            name='dt_end_of_warranty',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='user_activity_log',
            name='duration',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 20, 10, 47, 7, 186806)),
        ),
    ]