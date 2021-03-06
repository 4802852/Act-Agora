# Generated by Django 3.1.6 on 2021-02-20 21:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Enter a class genre (e.g. PT, yoga, pilates', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Gym',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Enter a place for a class(e.g. Gym name)', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Hashtag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Enter a feature of trainer.', max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Lecture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Enter a name of this class.', max_length=20)),
                ('summary', models.TextField(help_text='Enter a brief description of the class', max_length=1000)),
                ('genre', models.ManyToManyField(help_text='Select a genre for this class', to='trainer.Genre')),
                ('gym', models.ManyToManyField(help_text='Select a place for this class', to='trainer.Gym')),
            ],
        ),
        migrations.CreateModel(
            name='TrainerInformation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
                ('summary', models.TextField(help_text='Enter a brief description of the trainer.', max_length=1000)),
                ('registered_date', models.DateTimeField(auto_now_add=True, verbose_name='?????? ??????')),
                ('stat1', models.IntegerField(help_text='First Stat (0~99)')),
                ('stat2', models.IntegerField(help_text='Second Stat (0~99)')),
                ('stat3', models.IntegerField(help_text='Third Stat (0~99)')),
                ('stat4', models.IntegerField(help_text='Fourth Stat (0~99)')),
                ('stat5', models.IntegerField(help_text='Fifth Stat (0~99)')),
                ('stat6', models.IntegerField(help_text='Sixth Stat (0~99)')),
                ('genre', models.ManyToManyField(help_text='Select a genre for this trainer', to='trainer.Genre')),
                ('trainer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Trainer')),
            ],
        ),
        migrations.CreateModel(
            name='Trainer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('summary', models.TextField(help_text='Enter a brief description of the trainer.', max_length=1000)),
                ('tagtext', models.CharField(blank=True, max_length=200)),
                ('genre', models.ManyToManyField(blank=True, help_text='Select a genre for this trainer', to='trainer.Genre')),
                ('hashtag', models.ManyToManyField(blank=True, help_text='Select a feature for this trainer.', to='trainer.Hashtag')),
            ],
        ),
        migrations.CreateModel(
            name='LectureInstance',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, help_text='Unique ID for this class.', primary_key=True, serialize=False)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('weekday', models.CharField(choices=[('a', 'Monday'), ('b', 'Tuesday'), ('c', 'Wednesday'), ('d', 'Thursday'), ('e', 'Friday'), ('f', 'Saturday'), ('g', 'Sunday')], default='a', help_text='Class Day', max_length=1)),
                ('time', models.CharField(choices=[('a', 'AM 9:00~ AM 10:00'), ('b', 'AM 10:00~ AM 11:00'), ('c', 'AM 11:00~ PM 12:00'), ('d', 'PM 12:00~ PM 1:00'), ('e', 'PM 1:00~ PM 2:00'), ('f', 'PM 2:00~ PM 3:00'), ('g', 'PM 3:00~ PM 4:00'), ('h', 'PM 4:00~ PM 5:00'), ('i', 'PM 5:00~ PM 6:00'), ('j', 'PM 6:00~ PM 7:00'), ('k', 'PM 7:00~ PM 8:00'), ('l', 'PM 8:00~ PM 9:00'), ('m', 'PM 9:00~ PM 10:00')], default='a', help_text='Class Time', max_length=1)),
                ('status', models.CharField(choices=[('m', 'Maintenance'), ('o', 'Occupied'), ('a', 'Available')], default='a', help_text='Class Availability', max_length=1)),
                ('lecture', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='trainer.lecture')),
                ('trainee', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['weekday', 'time'],
            },
        ),
        migrations.AddField(
            model_name='lecture',
            name='trainer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='trainer.trainer'),
        ),
    ]
