# Generated by Django 4.2.10 on 2024-02-20 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attributes', '0003_strtype_rename_bool_booltype_rename_float_floattype_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='StrTypeChoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AlterModelOptions(
            name='strtype',
            options={'base_manager_name': 'objects'},
        ),
        migrations.RemoveConstraint(
            model_name='strtype',
            name='unique_value',
        ),
        migrations.RemoveField(
            model_name='strtype',
            name='value',
        ),
        migrations.AddConstraint(
            model_name='attrcategory',
            constraint=models.UniqueConstraint(fields=('name',), name='unique_name'),
        ),
        migrations.AddField(
            model_name='strtype',
            name='value',
            field=models.ManyToManyField(blank=True, to='attributes.strtypechoice'),
        ),
    ]
