import uuid
from datetime import datetime
import re

from django.db import models
from django.urls import reverse

from PTin import settings
from imagekit.models import ProcessedImageField
from imagekit.processors import Resize, ResizeToFill
from trainer.models import Trainer, Genre, Hashtag


def get_review_image_path(instance, filename):
    ymd_path = datetime.now().strftime('%Y/%m/%d')
    uuid_name = uuid.uuid4().hex
    return '/'.join(['review/', ymd_path, uuid_name])


class Review(models.Model):
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='작성자')
    trainer = models.ForeignKey(Trainer, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='트레이너')
    date = models.DateTimeField(auto_now_add=True, blank=False, verbose_name='작성일')
    genretext = models.CharField(max_length=200, null=True, blank=True)
    genre = models.ManyToManyField(Genre, blank=True, verbose_name='장르')
    tagtext = models.CharField(max_length=200, null=True, blank=True)
    hashtag = models.ManyToManyField(Hashtag, blank=True)
    title = models.CharField(max_length=100, null=True)
    content = models.TextField(null=True, blank=True)

    def hashtag_save(self):
        self.hashtag.set([])
        hashtags = re.findall(r'#(\w+)\b', str(self.tagtext))

        if not hashtags:
            return

        for tag in hashtags:
            tag, tag_created = Hashtag.objects.get_or_create(name=tag)
            self.hashtag.add(tag)

    def genre_save(self):
        self.genre.set([])
        genres = re.findall(r'(\w+)\b', str(self.genretext))

        if not genres:
            return

        for tag in genres:
            tag, tag_created = Genre.objects.get_or_create(name=tag)
            self.genre.add(tag)

    def __str__(self):
        """String for representing the Model object."""
        return str(self.id)

    def get_absolute_url(self):
        return reverse('review:review-detail', args=[str(self.id)])

    class Meta:
        db_table = '리뷰'
        verbose_name = '리뷰'
        verbose_name_plural = '리뷰'


class Photo(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, null=True)
    image = ProcessedImageField(
        upload_to=get_review_image_path, processors=[ResizeToFill(width=500, height=500, upscale=False)],
        null=True, blank=True, format='JPEG', options={'quality': 90},
    )

    def __str__(self):
        return str(self.review)
