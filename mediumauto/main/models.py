from django.db import models
from tinymce.models import HTMLField

# Create your models here.


class pages(models.Model):
    page = models.IntegerField(blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)


class books(models.Model):
    pdf = models.FileField()
    name = models.CharField(max_length=300)
    thumbnail = models.ImageField()
    category = models.CharField(max_length=100, blank=True)
    dateadded = models.DateTimeField(blank=True, null=True)
    pages = models.ManyToManyField(pages, blank=True, null=True)

    def __str__(self):
        return self.name + ' | ' + self.category


class stoptime(models.Model):
    t1 = models.DateTimeField(blank=True, null=True)
    t2 = models.DateTimeField(blank=True, null=True)


class articles(models.Model):
    start_time = models.DateTimeField()
    endtime = models.DateTimeField(blank=True, null=True)
    link = models.URLField(max_length=300, blank=True)
    completed = models.BooleanField(default=False, blank=True)
    series = models.CharField(max_length=100, blank=True)
    episode = models.IntegerField(blank=True, null=True)
    richtext = models.TextField(blank=True)
    title = models.CharField(max_length=200, blank=True)
    subtitle = models.CharField(max_length=200, blank=True)
    stops = models.ManyToManyField(stoptime, blank=True, null=True)
    #content = HTMLField(blank=True, null=True)
