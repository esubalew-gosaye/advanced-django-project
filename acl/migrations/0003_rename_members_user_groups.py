# Generated by Django 5.0.3 on 2024-04-04 06:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('acl', '0002_testmodel_remove_group_members_user_members'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='members',
            new_name='groups',
        ),
    ]
