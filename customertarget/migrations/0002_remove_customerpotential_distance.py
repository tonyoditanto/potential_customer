# Generated by Django 3.1.3 on 2020-12-21 23:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customertarget', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customerpotential',
            name='distance',
        ),
    ]
