# Generated by Django 3.0.5 on 2020-05-05 16:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0022_auto_20200505_2143'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscriptions',
            name='date_joined',
        ),
    ]
