# Generated by Django 3.2 on 2022-12-14 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0018_employee_pin'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='ext',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
