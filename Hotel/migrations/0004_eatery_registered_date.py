# Generated by Django 4.0.5 on 2023-02-12 09:02

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Hotel', '0003_eatery_verification_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='eatery',
            name='registered_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
