# Generated by Django 4.1.3 on 2023-01-12 09:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tool', '0005_auto_20230110_0613'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cl_user_request',
            old_name='ch_agent',
            new_name='ch_assign_agent',
        ),
    ]
