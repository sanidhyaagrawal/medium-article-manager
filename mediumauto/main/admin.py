from django.contrib import admin
from .models import *
from django_summernote.admin import SummernoteModelAdmin
from tinymce.widgets import TinyMCE
from django.db import models
from django.forms import TextInput, Textarea

# Apply summernote to all TextField in model.

'''
class articlesAdmin(SummernoteModelAdmin):  # instead of ModelAdmin
    summernote_fields = ('richtext',)
        start_time = models.DateTimeField()
    endtime = models.DateTimeField(blank=True, null=True)
    link = models.URLField(max_length=300, blank=True)
    completed = models.BooleanField(default=False, blank=True)
    series = models.CharField(max_length=100, blank=True)
    episode = models.IntegerField(blank=True)
    richtext = models.TextField(blank=True)
    title = models.CharField(max_length=200, blank=True)
    subtitle = models.CharField(max_length=200, blank=True)


'''


class articlesAdmin(admin.ModelAdmin):

    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
    }


admin.site.register(articles, articlesAdmin)
# Register your models here.
admin.site.register(books)
admin.site.register(stoptime)
admin.site.register(pages)
