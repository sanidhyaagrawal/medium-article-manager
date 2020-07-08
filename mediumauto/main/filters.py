import django_filters
from django_filters import *
from distutils.util import strtobool
from .models import *


def getitem(obj, books):
    lis = []
    tt = []
    cities = books.objects.values(obj)
    for i in cities:
        tt.append(list(i.values())[0])
    try:
        tt.remove('')
    except:
        pass

    print('########################')
    for i in list(set(tt)):
        tup = (i, i)
        lis.append(tup)
    lis = tuple(lis)
    print(lis)
    return ChoiceFilter(field_name=obj, choices=(lis))


class bookFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    category = getitem('category', books)

    class Meta:
        model = books
        fields = []


class series(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    subtitle = django_filters.CharFilter(lookup_expr='icontains')
    richtext = django_filters.CharFilter(lookup_expr='icontains')
    endtime = DateRangeFilter(field_name='endtime')
    series = getitem('series', articles)
    episode = getitem('episode', articles)

    class Meta:
        model = articles
        fields = []


'''
 start_time = models.DateTimeField()
    endtime = models.DateTimeField(blank=True, null=True)
    link = models.URLField(max_length=300, blank=True)
    completed = models.BooleanField(default=False, blank=True)
    #series = models.CharField(max_length=100, blank=True)
    #episode = models.IntegerField(blank=True, null=True)
    #richtext = models.TextField(blank=True)
    #title = models.CharField(max_length=200, blank=True)
    #subtitle = models.CharField(max_length=200, blank=True)
    stops = models.ManyToManyField(stoptime, blank=True, null=True)
    #content = HTMLField(blank=True, null=True)
'''
