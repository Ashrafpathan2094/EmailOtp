# Generated by Django 4.0 on 2022-02-08 08:08

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_profile_forget_password_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='datetime',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]