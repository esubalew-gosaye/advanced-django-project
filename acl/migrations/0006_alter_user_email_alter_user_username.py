# Generated by Django 5.0.3 on 2024-04-08 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acl', '0005_alter_user_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=150, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]