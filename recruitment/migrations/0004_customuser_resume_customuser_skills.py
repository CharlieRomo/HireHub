# Generated by Django 5.1 on 2024-09-22 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recruitment', '0003_customuser_password_reset_code_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='resume',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='skills',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
