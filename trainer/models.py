import os
import re

from django.db import models
from django.urls import reverse
import uuid
from datetime import datetime
from accounts.models import User

from PTin import settings

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill, Resize, SmartResize


class Genre(models.Model):
    """Model representing a book genre."""
    name = models.CharField(max_length=200, help_text='Enter a class genre (e.g. PT, yoga, pilates')

    def __str__(self):
        """String for representing the Model object."""
        return self.name


class Hashtag(models.Model):
    """Model representing a hashtag"""
    name = models.CharField(max_length=20, unique=True, help_text='Enter a feature of trainer.')

    def __str__(self):
        """String for representing the Model object"""
        return self.name


def get_file_path(instance, filename):
    ymd_path = datetime.now().strftime('%Y/%m/%d')
    uuid_name = uuid.uuid4().hex
    return '/'.join(['upload_file/', ymd_path, uuid_name])


def get_profile_image_path(instance, filename):
    ymd_path = datetime.now().strftime('%Y/%m/%d')
    uuid_name = uuid.uuid4().hex
    return '/'.join(['profile/', ymd_path, uuid_name])


class Trainer(models.Model):
    """Model representing a trainer (not a specific class)"""
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE, verbose_name='작성자')
    name = models.CharField(max_length=10, verbose_name='이름')
    genretext = models.CharField(max_length=200, null=True)
    genre = models.ManyToManyField(Genre, blank=True, verbose_name='장르')
    address = models.CharField(max_length=40, null=True, verbose_name='지역')
    place = models.CharField(max_length=40, null=True, verbose_name='장소')
    summary = models.TextField(null=True, blank=True)
    tagtext = models.CharField(max_length=200, null=True, blank=True)
    hashtag = models.ManyToManyField(Hashtag, blank=True)
    # upload_files = models.FileField(upload_to=get_file_path, null=True, blank=True, verbose_name='파일')
    # filename = models.CharField(max_length=64, null=True, verbose_name='첨부파일명')
    image = ProcessedImageField(
        upload_to=get_profile_image_path, processors=[ResizeToFill(width=500, height=500, upscale=False)],
        null=True, blank=True,
        format='JPEG', options={'quality': 90}, verbose_name="프로필 이미지"
    )
    imagename = models.CharField(max_length=64, null=True, blank=True, verbose_name='이미지파일')

    # Certificate
    cert1, cert2, cert3, cert4, cert5, cert6, cert7, cert8, cert9, cert10 = [
        models.CharField(max_length=40, null=True, blank=True) for i in range(10)
    ]
    certimg1, certimg2, certimg3, certimg4, certimg5, certimg6, certimg7, certimg8, certimg9, certimg10 = [
        ProcessedImageField(
            upload_to=get_profile_image_path, processors=[Resize(width=500, height=None, upscale=False)],
            null=True, blank=True, format='JPEG', options={'quality': 90}
        ) for i in range(10)
    ]
    # cert = [cert1, cert2, cert3, cert4, cert5, cert6, cert7, cert8, cert9, cert10]
    # certimg = [certimg1, certimg2, certimg3, certimg4, certimg5, certimg6, certimg7, certimg8, certimg9, certimg10]

    sns1, sns2, sns3, sns4, sns5 = [
        models.CharField(max_length=256, null=True, blank=True) for i in range(5)
    ]

    def hashtag_save(self):
        self.hashtag.set([])
        hashtags = re.findall(r'#(\w+)\b', self.tagtext)

        if not hashtags:
            return

        for tag in hashtags:
            tag, tag_created = Hashtag.objects.get_or_create(name=tag)
            self.hashtag.add(tag)

    def genre_save(self):
        self.genre.set([])
        genres = re.findall(r'(\w+)\b', self.genretext)

        if not genres:
            return

        for tag in genres:
            tag, tag_created = Genre.objects.get_or_create(name=tag)
            self.genre.add(tag)

    def __str__(self):
        """String for representing the Model object."""
        return self.name

    def get_absolute_url(self):
        """Returns the url to access a detail information for this trainer."""
        return reverse('trainer-detail', args=[str(self.id)])

    def display_genre(self):
        """Create a string for the Genre. This is required to display genre in Admin."""
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = 'Genre'

    class Meta:
        db_table = '트레이너'
        verbose_name = '트레이너'
        verbose_name_plural = '트레이너'

    def delete(self, *args, **kwargs):
        if self.image:
            os.remove(os.path.join(settings.MEDIA_ROOT, self.image.path))
        super(Trainer, self).delete(*args, **kwargs)


class Lecture(models.Model):
    """Model representing the lecture(but not a specific class)."""
    trainer = models.ForeignKey('Trainer', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=20, verbose_name='강의명')
    summary = models.TextField(max_length=1000, verbose_name='강의 설명')

    def __str__(self):
        """String for representing the Model object."""
        return f'{ self.name }, { self.trainer }'

    def get_absolute_url(self):
        """Returns the url to access a detail information for this class."""
        return reverse('lecture-detail', args=[str(self.id)])

    def display_genre(self):
        """Create a string for the Genre. This is required to display genre in Admin."""
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = 'Genre'

    class Meta:
        db_table = '강의'
        verbose_name = '강의'
        verbose_name_plural = '강의'


class LectureInstance(models.Model):
    """Model representing the lecture(but not a specific class)."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this class.')
    lecture = models.ForeignKey('Lecture', on_delete=models.SET_NULL, null=True)
    start_date = models.DateField(null=True, blank=True)
    trainee = models.ManyToManyField(User)

    WEEKDAY_TABLE = (
        ('a', 'Monday'),
        ('b', 'Tuesday'),
        ('c', 'Wednesday'),
        ('d', 'Thursday'),
        ('e', 'Friday'),
        ('f', 'Saturday'),
        ('g', 'Sunday'),
    )

    weekday = models.CharField(
        max_length=1,
        choices=WEEKDAY_TABLE,
        blank=False,
        default='a',
        help_text='Class Day',
    )

    TIME_TABLE = (
        ('a', 'AM 9:00~ AM 10:00'),
        ('b', 'AM 10:00~ AM 11:00'),
        ('c', 'AM 11:00~ PM 12:00'),
        ('d', 'PM 12:00~ PM 1:00'),
        ('e', 'PM 1:00~ PM 2:00'),
        ('f', 'PM 2:00~ PM 3:00'),
        ('g', 'PM 3:00~ PM 4:00'),
        ('h', 'PM 4:00~ PM 5:00'),
        ('i', 'PM 5:00~ PM 6:00'),
        ('j', 'PM 6:00~ PM 7:00'),
        ('k', 'PM 7:00~ PM 8:00'),
        ('l', 'PM 8:00~ PM 9:00'),
        ('m', 'PM 9:00~ PM 10:00'),
    )

    time = models.CharField(
        max_length=1,
        choices=TIME_TABLE,
        blank=False,
        default='a',
        help_text='Class Time',
    )

    CLASS_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'Occupied'),
        ('a', 'Available'),
    )

    status = models.CharField(
        max_length=1,
        choices=CLASS_STATUS,
        blank=False,
        default='a',
        help_text='Class Availability',
    )

    class Meta:
        ordering = ['weekday', 'time']

    def __str__(self):
        """String for representing the Model object."""
        return f'{ self.lecture }, { self.weekday }, { self.time }'
