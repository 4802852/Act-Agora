from django.contrib import admin
from trainer.models import Genre, Hashtag, Trainer, Lecture, LectureInstance

admin.site.register(Genre)
admin.site.register(Hashtag)


class LectureInline(admin.TabularInline):
    model = Lecture


@admin.register(Trainer)
class TrainerAdmin(admin.ModelAdmin):
    list_display = ('writer', 'name', 'display_genre')
    fields = ['writer', 'name', 'genre', 'address', 'place', 'hashtag', 'summary']
    search_fields = ('writer__user_id', 'name')
    # inlines = [LectureInline]


class LectureInstanceInline(admin.TabularInline):
    model = LectureInstance


@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    list_display = ('name', 'trainer')
    fieldsets = (
        (None, {
            'fields': ('name', 'trainer', 'gym', 'genre', 'summary')
        }),
    )
    inlines = [LectureInstanceInline]


@admin.register(LectureInstance)
class LectureInstanceAdmin(admin.ModelAdmin):
    list_display = ('lecture', 'weekday', 'time')
    list_filter = ('weekday', 'time', 'status')
    fieldsets = (
        (None, {
            'fields': ('lecture', 'start_date', 'id')
        }),
        ('Day Time', {
            'fields': (('weekday', 'time'), 'status', 'trainee')
        })
    )
