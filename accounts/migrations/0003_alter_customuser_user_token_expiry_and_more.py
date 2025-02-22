# Generated by Django 5.1.3 on 2025-01-14 14:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='user_token_expiry',
            field=models.TimeField(default=datetime.time(0, 0)),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='user_type',
            field=models.CharField(choices=[('restaurant_owner', 'Restaurant Owner'), ('customer', 'Customer')], default='customer', max_length=20),
        ),
    ]
