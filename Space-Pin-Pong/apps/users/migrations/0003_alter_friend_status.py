# Generated by Django 5.0.7 on 2024-09-22 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friend',
            name='status',
            field=models.CharField(choices=[('pending', '보류 중'), ('accept', '수락'), ('reject', '거절')], default='pending', max_length=20),
        ),
    ]
