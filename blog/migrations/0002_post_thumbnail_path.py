# Generated by Django 2.1.7 on 2019-04-04 06:50

from django.db import migrations
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='thumbnail_path',
            field=imagekit.models.fields.ProcessedImageField(blank=True, null=True, upload_to='blog/thumbnail/%Y%m%d'),
        ),
    ]
