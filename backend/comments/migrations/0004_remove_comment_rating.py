# Generated by Django 4.2.10 on 2024-02-21 14:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0003_comment_rating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='rating',
        ),
    ]
