# Generated by Django 5.1.4 on 2025-04-03 21:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0015_sliderhomegallery'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='cat_video',
            field=models.FileField(blank=True, null=True, upload_to='videos'),
        ),
    ]
