# Generated by Django 5.1.4 on 2025-01-07 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_remove_category_category_accessory_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='sub_category_accessory',
            field=models.BooleanField(default=False),
        ),
    ]
