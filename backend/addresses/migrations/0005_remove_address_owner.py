# Generated by Django 4.2.10 on 2024-02-19 08:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0004_alter_region_options_address_liter'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='owner',
        ),
    ]
