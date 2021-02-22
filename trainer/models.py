import re

from django.db import models
from django.urls import reverse
import uuid
from accounts.models import User


class Genre(models.Model):
    """Model representing a book genre."""
    name = models.CharField(max_length=200, help_text='Enter a class genre (e.g. PT, yoga, pilates')

    def __str__(self):
        """String for representing the Model object."""
        return self.name


class Gym(models.Model):
    """Model representing a Gym."""
    name = models.CharField(max_length=100, help_text='Enter a place for a class(e.g. Gym name)')

    def __str__(self):
        """String for representing the Model object"""
        return self.name


class Hashtag(models.Model):
    """Model representing a hashtag"""
    name = models.CharField(max_length=20, unique=True, help_text='Enter a feature of trainer.')

    def __str__(self):
        """String for representing the Model object"""
        return self.name


class Trainer(models.Model):
    """Model representing a trainer (not a specific class)"""
    name = models.CharField(max_length=10)
    date_of_birth = models.DateField(null=True, blank=True)
    genre = models.ManyToManyField(Genre, blank=True, help_text='Select a genre for this trainer')
    summary = models.TextField(max_length=1000, help_text='Enter a brief description of the trainer.')
    tagtext = models.CharField(max_length=200, blank=True)
    hashtag = models.ManyToManyField(Hashtag, blank=True, help_text='Select a feature for this trainer.')

    def hashtag_save(self):
        self.hashtag.set([])
        hashtags = re.findall(r'#(\w+)\b', self.tagtext)

        if not hashtags:
            return

        for tag in hashtags:
            tag, tag_created = Hashtag.objects.get_or_create(name=tag)
            self.hashtag.add(tag)

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


class Lecture(models.Model):
    """Model representing the lecture(but not a specific class)."""
    name = models.CharField(max_length=20, help_text='Enter a name of this class.')
    trainer = models.ForeignKey('Trainer', on_delete=models.SET_NULL, null=True)
    gym = models.ManyToManyField(Gym, help_text='Select a place for this class')
    genre = models.ManyToManyField(Genre, help_text='Select a genre for this class')
    summary = models.TextField(max_length=1000, help_text='Enter a brief description of the class')

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


class TrainerInformation(models.Model):
    """Model representing a trainer (not a specific class)"""
    name = models.CharField(max_length=10)
    genre = models.ManyToManyField(Genre, help_text='Select a genre for this trainer')
    summary = models.TextField(max_length=1000, help_text='Enter a brief description of the trainer.')
    registered_date = models.DateTimeField(auto_now_add=True, verbose_name="등록 시간")
    trainer = models.ForeignKey(User, verbose_name="Trainer", on_delete=models.CASCADE)

    stat1 = models.IntegerField(help_text='First Stat (0~99)')
    stat2 = models.IntegerField(help_text='Second Stat (0~99)')
    stat3 = models.IntegerField(help_text='Third Stat (0~99)')
    stat4 = models.IntegerField(help_text='Fourth Stat (0~99)')
    stat5 = models.IntegerField(help_text='Fifth Stat (0~99)')
    stat6 = models.IntegerField(help_text='Sixth Stat (0~99)')

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
