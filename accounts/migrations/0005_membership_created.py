# Generated by Django 3.0.4 on 2020-04-08 08:08

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_profile_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='membership',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
