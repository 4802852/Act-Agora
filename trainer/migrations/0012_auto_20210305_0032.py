# Generated by Django 3.1.7 on 2021-03-05 00:32

from django.db import migrations, models
import imagekit.models.fields
import trainer.models


class Migration(migrations.Migration):

    dependencies = [
        ('trainer', '0011_remove_lecture_genre'),
    ]

    operations = [
        migrations.AddField(
            model_name='trainer',
            name='cert1',
            field=models.CharField(max_length=40, null=True),
        ),
        migrations.AddField(
            model_name='trainer',
            name='cert10',
            field=models.CharField(max_length=40, null=True),
        ),
        migrations.AddField(
            model_name='trainer',
            name='cert2',
            field=models.CharField(max_length=40, null=True),
        ),
        migrations.AddField(
            model_name='trainer',
            name='cert3',
            field=models.CharField(max_length=40, null=True),
        ),
        migrations.AddField(
            model_name='trainer',
            name='cert4',
            field=models.CharField(max_length=40, null=True),
        ),
        migrations.AddField(
            model_name='trainer',
            name='cert5',
            field=models.CharField(max_length=40, null=True),
        ),
        migrations.AddField(
            model_name='trainer',
            name='cert6',
            field=models.CharField(max_length=40, null=True),
        ),
        migrations.AddField(
            model_name='trainer',
            name='cert7',
            field=models.CharField(max_length=40, null=True),
        ),
        migrations.AddField(
            model_name='trainer',
            name='cert8',
            field=models.CharField(max_length=40, null=True),
        ),
        migrations.AddField(
            model_name='trainer',
            name='cert9',
            field=models.CharField(max_length=40, null=True),
        ),
        migrations.AddField(
            model_name='trainer',
            name='certimg1',
            field=imagekit.models.fields.ProcessedImageField(blank=True, null=True, upload_to=trainer.models.get_profile_image_path),
        ),
        migrations.AddField(
            model_name='trainer',
            name='certimg10',
            field=imagekit.models.fields.ProcessedImageField(blank=True, null=True, upload_to=trainer.models.get_profile_image_path),
        ),
        migrations.AddField(
            model_name='trainer',
            name='certimg2',
            field=imagekit.models.fields.ProcessedImageField(blank=True, null=True, upload_to=trainer.models.get_profile_image_path),
        ),
        migrations.AddField(
            model_name='trainer',
            name='certimg3',
            field=imagekit.models.fields.ProcessedImageField(blank=True, null=True, upload_to=trainer.models.get_profile_image_path),
        ),
        migrations.AddField(
            model_name='trainer',
            name='certimg4',
            field=imagekit.models.fields.ProcessedImageField(blank=True, null=True, upload_to=trainer.models.get_profile_image_path),
        ),
        migrations.AddField(
            model_name='trainer',
            name='certimg5',
            field=imagekit.models.fields.ProcessedImageField(blank=True, null=True, upload_to=trainer.models.get_profile_image_path),
        ),
        migrations.AddField(
            model_name='trainer',
            name='certimg6',
            field=imagekit.models.fields.ProcessedImageField(blank=True, null=True, upload_to=trainer.models.get_profile_image_path),
        ),
        migrations.AddField(
            model_name='trainer',
            name='certimg7',
            field=imagekit.models.fields.ProcessedImageField(blank=True, null=True, upload_to=trainer.models.get_profile_image_path),
        ),
        migrations.AddField(
            model_name='trainer',
            name='certimg8',
            field=imagekit.models.fields.ProcessedImageField(blank=True, null=True, upload_to=trainer.models.get_profile_image_path),
        ),
        migrations.AddField(
            model_name='trainer',
            name='certimg9',
            field=imagekit.models.fields.ProcessedImageField(blank=True, null=True, upload_to=trainer.models.get_profile_image_path),
        ),
    ]
