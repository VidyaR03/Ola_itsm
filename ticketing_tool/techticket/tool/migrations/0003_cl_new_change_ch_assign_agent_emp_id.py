# Generated by Django 3.2.12 on 2023-01-09 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tool', '0002_auto_20230107_1123'),
    ]

    operations = [
        migrations.AddField(
            model_name='cl_new_change',
            name='ch_assign_agent_emp_id',
            field=models.CharField(default='Deallocated', max_length=100, null=True),
        ),
    ]