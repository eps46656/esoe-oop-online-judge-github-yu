# Generated by Django 3.1.7 on 2021-04-05 20:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('judge', '0004_auto_20210405_2022'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='instructor',
        ),
    ]
