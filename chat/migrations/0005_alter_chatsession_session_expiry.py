# Generated by Django 5.1.3 on 2024-12-27 18:07

import chat.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_chatsession_session_expiry'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatsession',
            name='session_expiry',
            field=models.DateTimeField(default=chat.models.session_expiry_time, editable=False),
        ),
    ]
