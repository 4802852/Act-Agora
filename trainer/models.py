import re

from django.db import models
from django.urls import reverse
import uuid
from accounts.models import User

from PTin import settings


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


class Trainer(models.Model):
    """Model representing a trainer (not a specific class)"""
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE, verbose_name='작성자')
    name = models.CharField(max_length=10, verbose_name='이름')
    genretext = models.CharField(max_length=200, blank=True)
    genre = models.ManyToManyField(Genre, blank=True, verbose_name='장르')
    address = models.CharField(max_length=20, blank=True, verbose_name='지역')
    place = models.CharField(max_length=20, blank=True, verbose_name='장소')
    summary = models.TextField(max_length=1000, blank=True)
    tagtext = models.CharField(max_length=200, blank=True)
    hashtag = models.ManyToManyField(Hashtag, blank=True)

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


class Lecture(models.Model):
    """Model representing the lecture(but not a specific class)."""
    trainer = models.ForeignKey('Trainer', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=20, verbose_name='강의명')
    genre = models.ManyToManyField(Genre, verbose_name='장르', blank=True)
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
