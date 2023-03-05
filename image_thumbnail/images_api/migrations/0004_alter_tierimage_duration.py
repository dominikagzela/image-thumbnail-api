# Generated by Django 4.1.7 on 2023-03-05 12:41

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images_api', '0003_alter_user_tier'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tierimage',
            name='duration',
            field=models.IntegerField(blank=True, default=None, null=True, validators=[django.core.validators.MaxValueValidator(300), django.core.validators.MinValueValidator(300000)]),
        ),
    ]
