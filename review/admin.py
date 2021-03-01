from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('writer', 'trainer', 'title', 'date')
    fields = ['writer', 'trainer', 'trainer_idd', 'genre', 'hashtag', 'title', 'content']
    search_fields = ('writer__user_id', 'trainer', 'title')
