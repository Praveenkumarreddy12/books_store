# Generated by Django 4.2.7 on 2025-07-22 05:23

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_alter_customer_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='books_ordered',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
