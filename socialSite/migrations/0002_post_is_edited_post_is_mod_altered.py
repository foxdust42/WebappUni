# Generated by Django 4.2.8 on 2024-01-01 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialSite', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='is_edited',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='post',
            name='is_mod_altered',
            field=models.BooleanField(default=False),
        ),
    ]
