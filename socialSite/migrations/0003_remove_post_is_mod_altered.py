# Generated by Django 4.2.8 on 2024-01-01 23:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('socialSite', '0002_post_is_edited_post_is_mod_altered'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='is_mod_altered',
        ),
    ]
