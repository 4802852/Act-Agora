from django.contrib import admin
from .models import Review, Photo


class PhotoInline(admin.TabularInline):
    model = Photo


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'writer', 'trainer', 'title', 'date')
    fields = ['writer', 'trainer', 'genre', 'hashtag', 'title', 'content']
    search_fields = ('writer__user_id', 'trainer', 'title')
    inlines = [PhotoInline, ]


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    pass