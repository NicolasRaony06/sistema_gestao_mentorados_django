# Generated by Django 5.2 on 2025-04-04 00:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='navigators',
            name='user',
        ),
        migrations.DeleteModel(
            name='Mentorados',
        ),
        migrations.DeleteModel(
            name='Navigators',
        ),
    ]
