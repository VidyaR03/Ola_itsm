# Generated by Django 4.1.6 on 2023-03-16 15:12

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tool', '0002_alter_user_activity_log_duration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_activity_log',
            name='duration',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 16, 15, 12, 36, 577540)),
        ),
        migrations.CreateModel(
            name='cl_Ticket_Logs',
            fields=[
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('action', models.CharField(max_length=100)),
                ('logged_user', models.CharField(max_length=100)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('change_req_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tool.cl_new_change')),
                ('incident_req_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tool.cl_user_request')),
            ],
            options={
                'db_table': 'cl_ticket_logs',
            },
        ),
    ]
