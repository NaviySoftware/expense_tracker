# Generated by Django 3.0.4 on 2020-04-07 02:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_profile_color'),
        ('budgeting', '0005_category_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='user',
        ),
        migrations.AddField(
            model_name='category',
            name='user',
            field=models.ManyToManyField(to='accounts.Profile'),
        ),
    ]
