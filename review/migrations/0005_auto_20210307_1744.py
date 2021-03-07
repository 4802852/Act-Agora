# Generated by Django 3.1.7 on 2021-03-07 17:44

from django.db import migrations
import imagekit.models.fields
import review.models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0004_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='image',
            field=imagekit.models.fields.ProcessedImageField(blank=True, null=True, upload_to=review.models.get_review_image_path),
        ),
    ]
