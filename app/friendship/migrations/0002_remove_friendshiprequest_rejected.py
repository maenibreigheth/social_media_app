# Generated by Django 3.0.8 on 2020-07-19 06:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('friendship', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='friendshiprequest',
            name='rejected',
        ),
    ]
