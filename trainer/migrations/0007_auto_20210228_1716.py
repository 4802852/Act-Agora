# Generated by Django 3.1.7 on 2021-02-28 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trainer', '0006_auto_20210228_1715'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trainer',
            name='genre',
            field=models.ManyToManyField(blank=True, to='trainer.Genre', verbose_name='장르'),
        ),
        migrations.AlterField(
            model_name='trainer',
            name='hashtag',
            field=models.ManyToManyField(blank=True, to='trainer.Hashtag'),
        ),
    ]
