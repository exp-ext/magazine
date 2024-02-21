# Generated by Django 4.2.10 on 2024-02-21 14:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ratings', '0002_alter_rating_options'),
        ('comments', '0002_remove_comment_inverted_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='rating',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='comment', to='ratings.rating'),
            preserve_default=False,
        ),
    ]