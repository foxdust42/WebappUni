# Generated by Django 4.2.8 on 2024-01-15 18:23

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_profile_date_of_birth'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='description',
            field=models.TextField(blank=True, default=None, max_length=5000, null=True, validators=[django.core.validators.ProhibitNullCharactersValidator(), django.core.validators.MaxLengthValidator(5000)]),
        ),
    ]