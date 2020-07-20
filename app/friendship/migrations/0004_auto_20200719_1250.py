# Generated by Django 3.0.8 on 2020-07-19 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
        ('friendship', '0003_auto_20200719_1054'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='friendshiprequest',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='friendshiprequest',
            name='from_user',
        ),
        migrations.RemoveField(
            model_name='friendshiprequest',
            name='to_user',
        ),
        migrations.RenameField(
            model_name='friendship',
            old_name='to_user',
            new_name='user_one_id',
        ),
        migrations.RenameField(
            model_name='friendship',
            old_name='from_user',
            new_name='user_two_id',
        ),
        migrations.AddField(
            model_name='friendship',
            name='status',
            field=models.IntegerField(choices=[(1, 'Pending'), (2, 'Accepted'), (3, 'Declined')], null=True),
        ),
        migrations.AlterUniqueTogether(
            name='friendship',
            unique_together={('user_one_id', 'user_two_id')},
        ),
        migrations.DeleteModel(
            name='Block',
        ),
        migrations.DeleteModel(
            name='FriendshipRequest',
        ),
    ]