# Generated by Django 5.0.2 on 2024-02-29 15:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_user_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['email'], 'verbose_name': 'Пользователь', 'verbose_name_plural': 'Пользователи'},
        ),
    ]
