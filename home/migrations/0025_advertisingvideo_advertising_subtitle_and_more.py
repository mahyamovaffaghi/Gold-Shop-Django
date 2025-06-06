# Generated by Django 5.1.4 on 2025-04-18 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0024_advertisingvideo'),
    ]

    operations = [
        migrations.AddField(
            model_name='advertisingvideo',
            name='advertising_subtitle',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='advertisingvideo',
            name='advertising_text',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='advertisingvideo',
            name='advertising_title',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
