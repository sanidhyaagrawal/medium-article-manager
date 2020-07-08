

from django.db.models import Count
from django.db.models.functions import *
from bs4 import BeautifulSoup
from selenium import webdriver
import pyautogui
from webdriver_manager.chrome import ChromeDriverManager
import time
import requests
from selenium.webdriver.common.keys import Keys
import dload
import urllib.request
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User, auth
from .models import *
from django.shortcuts import redirect
from django.core.signing import Signer
from .filters import *
from django_summernote.fields import SummernoteTextFormField, SummernoteTextField
from datetime import datetime
from .forms import *
from django.contrib import messages
from django.http import HttpResponseRedirect


signer = Signer()
# Create your views here.


def detlinkdata(link):

    driver = webdriver.Chrome('S:\\WORK\\Medium Automation\\chromedriver.exe')
    driver.get(link)

    with open('main\jquery-3.5.1.js', 'r') as jquery_js:
        jquery = jquery_js.read()  # read the jquery from a file
        driver.execute_script(jquery)  # active the jquery lib
        time.sleep(3)
        for bb in range(1, 5):
            driver.execute_script('''
    for (let i=0; i<document.body.scrollHeight; i++) {
    task(i);
    }

    function task(i) {
    setTimeout(function() {
        window.scrollTo(0, i)
    }, 10);
    }


    ''')
            time.sleep(1)

        print('Executing')
        driver.execute_script(jquery)
        driver.execute_script("window.stop();")

        print('stoped')
        driver.execute_script("""
            window.stop
            if (window.jQuery) {
                // jQuery is loaded
            $("nav").remove();

                for(var i = 0; i<187; i++){
                    $('.n').find("div").slice(-1).remove();
                }
                $('.n').find("div").slice(5,6).remove();
                $('.n').find("div").slice(5,6).remove();
                $('div').removeClass('rr');
            } else {
                // jQuery is not loaded class="ng nh r"
                alert("Doesn't Work");
            }
        """)
        element = driver.find_element_by_id("root")
        print(element.text)
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.hotkey('ctrl', 'c')
        driver.close()
        driver.quit()


def checkcomplete(i):
    if i.start_time != None and i.endtime != None and len(i.link) != 0 and len(i.series) != 0 and i.episode != None and len(i.richtext) != 0 and len(i.title) != 0 and len(i.subtitle) != 0:
        i.completed = True
    else:
        i.completed = False


def getimages(a):
    try:
        temp = 'dasdasdas'
        while True:
            n = a.find('https://miro.medium.com')
            n1 = a[n:].find('"')
            n2 = a[n:].find(',')
            n3 = a[n:].find(' ')
            name = ''
            if n1 < n2 and n1 < n3:
                link = a[n:n+n1]
            if n2 < n1 and n2 < n3:
                link = a[n:n+n2]
            if n3 < n1 and n3 < n2:
                link = a[n:n+n3]

            t1 = link.split('/')[-1]
            # print(t1)
            for i in t1:
                if(i == '?' or i == '.' or i == '=' or i == '*'):
                    pass
                else:
                    name = name+i

            dload.save(
                link, 'S:/WORK/Medium Automation/mediumauto/data/'+name+'.png')
            print(name)
            a = a.replace(link, '../../../../../media/'+name+'.png')

            if link != temp:
                temp = link
            else:
                break
        return(a)
    except:
        print("All data locally saved")
        return(a)


def gateway(request):
    if request.user.is_active:
        print(request.user)
        return redirect('/home')
    else:
        return redirect('/verification')


def verification(request):
    if request.user.is_active:
        return redirect('/home')
    else:
        return render(request, 'verification.html')


def home(request):
    if request.user.is_active:
        book = books.objects.all()

        Filter = bookFilter(request.GET, queryset=book)
        orders1 = Filter.qs
        for i in orders1:
            i.allpages = i.pages.all().order_by('date')
            dates = []
            for k in i.pages.all():
                dates.append(k.date.date())
                dates = list(set(dates))

            datepages = []
            for k in dates:
                pp = []
                totalpages = {}
                totalpages['Date'] = k
                a = i.pages.all().filter(date__date=k)
                for p in a:
                    pp.append(p.page)
                print('#########home##########')
                totalpages['Pages'] = max(pp)
                datepages.append(totalpages)
            i.datepages = datepages
        foo = articles.objects.all()
        drafts = articles.objects.all().filter(completed=False).order_by('episode')
        completed = articles.objects.all().filter(completed=True).order_by('-endtime')
        for i in foo:
            checkcomplete(i)
            a = getimages(i.richtext)
            i.richtext = a
            i.save()

        for i in drafts:
            time = datetime.now()
            naive = i.start_time.replace(tzinfo=None)
            print(naive)
            print(time)
            difference = time - naive
            seconds = difference.total_seconds()
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            seconds = seconds % 60
            time = {'hour': hours, 'min': minutes,
                    'sec': int(seconds)}
            i.time = time
            if len(i.stops.all()) == 0:
                # tim=stoptime.objects.create()
                # article.stops.add(tim.pk)
                i.btn = 'Take a Break'
                i.btnclr = 'success'
            else:
                for k in i.stops.all():
                    if k.t1 != None and k.t2 != None:
                        def ordinal(n): return "%d%s" % (
                            n, "tsnrhtdd"[(n/10 % 10 != 1)*(n % 10 < 4)*n % 10::4])

                        i.btn = 'Take ' + \
                            ordinal(len(i.stops.all())+1)+' break'
                        i.btnclr = 'success'
                    else:
                        i.btn = 'Resume'
                        i.btnclr = 'danger'

        context1 = {'books': orders1, 'Filter': Filter,
                    'drafts': drafts, 'completed': completed, 'datepages': datepages}
        return render(request, 'home.html', context1)
    else:
        return redirect('/verification')


def reducetime(j, seconds):
    if len(j.stops.all()) > 0:
        for k in j.stops.all():
            tempp = k.t2.replace(tzinfo=None) - k.t1.replace(tzinfo=None)
            print(tempp)
            print(seconds)
            seconds = seconds - abs(tempp.total_seconds())
            print(seconds)
            return seconds
    else:
        return seconds


def stats(request):
    if request.user.is_active:
        alls = articles.objects.all()
        drafts = articles.objects.all().filter(completed=False).order_by('episode')
        completed = articles.objects.all().filter(completed=True).order_by('-endtime')
        book = books.objects.all()
        Filter = series(request.GET, queryset=completed)
        fcompleted = Filter.qs
        for i in book:
            i.allpages = i.pages.all().order_by('-date')

        qs = articles.objects.annotate(day=ExtractDay('endtime'), month=ExtractMonth('endtime'), year=ExtractYear(
            'endtime'),).values('day', 'month', 'year').annotate(n=Count('pk')).order_by('day')

        seconds = 0
        dates = []
        for i in completed:
            dates.append(
                {'day': i.endtime.day, 'month': i.endtime.month, 'year': i.endtime.year})

        seen = set()

        new_l = []
        for d in dates:
            t = tuple(d.items())
            if t not in seen:
                seen.add(t)
                new_l.append(d)
        # print(new_l)

        for i in new_l:  # newl is unique dtaes when article was created
            # print(i['year'])
            objs = articles.objects.all().filter(
                endtime__year=i['year'], endtime__month=i['month'], endtime__day=i['day'])
            # print(len(objs))
            i['total'] = len(objs)
            for j in objs:
                time = j.endtime.replace(tzinfo=None)
                naive = j.start_time.replace(tzinfo=None)
                for k in j.stops.all():
                    tempp = k.t2.replace(tzinfo=None) - \
                        k.t1.replace(tzinfo=None)
                    # print(tempp)
                    seconds = seconds - abs(tempp.total_seconds())
                    # print(seconds)
                difference = time - naive
                seconds = seconds + difference.total_seconds()

            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            seconds = seconds % 60
            time = {'hour': int(hours), 'min': int(minutes),
                    'sec': int(seconds)}
            # print(time)
            i['time'] = time
        # print(new_l)
        for i in fcompleted:
            time = i.endtime.replace(tzinfo=None)
            naive = i.start_time.replace(tzinfo=None)
            difference = time - naive
            seconds = difference.total_seconds()

            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            sec = seconds % 60
            time = {'hour': int(hours), 'min': int(minutes),
                    'sec': int(sec)}
            i.ctime = time

            seconds = reducetime(i, seconds)
            #print('redddddd', seconds)
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            sec = seconds % 60
            time = {'hour': int(hours), 'min': int(minutes),
                    'sec': int(sec)}
            i.time = time
        # print(book)

        return render(request, 'stats.html', {'perdate': qs, 'completed': completed, 'new_l': new_l, 'book': book, 'Filter': Filter, 'fcompleted': fcompleted})
    else:
        return redirect('/verification')


def delete(request, key):
    print('#####delete#####')
    errors = []
    if request.method == 'GET':
        a = articles.objects.get(pk=key)
        for i in a.stops.all():
            i.delete()  # delete all stoptimes
        a.delete()
        messages.add_message(request, messages.INFO,
                             'Draft Has Been Deleted')
        return redirect('/')


def view(request, key):
    print('#####view#####')
    errors = []
    if request.method == 'GET':
        a = articles.objects.get(pk=key)
        return render(request, 'view.html', {'article': a})


def update(request, key):
    print('#####update#####')
    errors = []
    if request.method == 'GET':
        a = articles.objects.get(pk=key)
        detlinkdata(a.link)
        return redirect('/updatearticle/'+str(key))


def complete(request, key):
    print('#####complete#####')
    errors = []
    if request.method == 'GET':
        a = articles.objects.get(pk=key)
        key = str(key)
        print(len(a.link))
        if len(a.series) == 0:
            return HttpResponseRedirect('/admin/main/articles/'+key+'/change/')
        if (len(a.link) == 0 and len(a.richtext) != 0) or (len(a.link) != 0 and len(a.richtext) == 0):
            return HttpResponseRedirect('/admin/main/articles/'+key+'/change/')
        elif a.episode == None:
            return redirect('/newarticle-step2/'+key+'/')
        elif len(a.link) == 0:
            return redirect('/newarticle-step3/'+key+'/')
        elif len(a.richtext) == 0:
            return redirect('/newarticle-step4/'+key+'/')
        else:
            return HttpResponseRedirect('/admin/main/articles/'+key+'/change/')


def loginc(request):
    print('#####loginc#####')
    response_data = {}
    response_data['access_granted'] = False
    errors = []
    if request.method == 'POST':
        email = request.POST['email'].strip()
        if str(email) == '07091969':
            user = auth.authenticate(username="auth", password='sus@07091969')
            auth.login(request, user)
            response_data['access_granted'] = True
        else:
            errors = []
            errors.append('Invalid Password')

        print(errors, response_data['access_granted'])
        response_data['errors'] = errors
        return JsonResponse(response_data)
    else:
        return redirect('/verification')


def newarticle1(request):
    if request.user.is_active:
        print(request.user)
        ar = articles.objects.all()
        ser = []
        for i in ar:
            if i.series != '':
                ser.append(i.series)
            ser = list(set(ser))
        return render(request, 'newarticle1.html', {'ser': ser})
    else:
        return redirect('/verification')


def seriesselect(request):
    print('#####loginc#####')
    response_data = {}
    response_data['access_granted'] = False
    errors = []
    if request.method == 'POST':
        email = request.POST['email'].strip()
        if len(email) != 0:
            obj = articles.objects.create(
                start_time=datetime.now(), series=email)
            response_data['access_granted'] = True
            print(obj.pk)
            response_data['key'] = obj.pk
        else:
            errors = []
            errors.append('Select a series')

        print(errors, response_data['access_granted'])
        response_data['errors'] = errors
        return JsonResponse(response_data)
    else:
        return redirect('/verification')


def newarticle2(request, key):
    if request.user.is_active:
        print(request.user)
        article = articles.objects.get(pk=key)
        articles.objects.get(pk=key)
        print(article.series)
        cnt = articles.objects.all().exclude(
            episode=None).filter(series=article.series).count()
        ar = articles.objects.all()
        eps = []
        eps = articles.objects.all().exclude(
            episode=None).filter(series=article.series)
        prev = (eps)
        no = []
        for i in eps:
            if i.episode != '' and i.episode != None:
                print(i)
                no.append(i.episode)
        print(no)
        if len(no) != 0:
            prev = max(no)+1
        else:
            prev = 1
        return render(request, 'newarticle2.html', {'article': article, 'eps': eps, 'cnt': cnt, 'prev': prev})
    else:
        return redirect('/verification')


def episodeselect(request):
    print('#####loginc#####')
    response_data = {}
    response_data['access_granted'] = False
    errors = []
    if request.method == 'POST':
        email = request.POST['email'].strip()
        key = request.POST['key'].strip()
        if len(email) != 0:
            obj = articles.objects.get(pk=key)
            obj.episode = email
            obj.save()
            print('#####loginc#####')

            print(obj.episode)
            response_data['access_granted'] = True
            print(obj.pk)

            response_data['key'] = obj.pk
        else:
            errors = []
            errors.append('Select a series')

        print(errors, response_data['access_granted'])
        response_data['errors'] = errors
        return JsonResponse(response_data)
    else:
        return redirect('/verification')


def newarticle3(request, key):
    if request.user.is_active:
        # print(request.user)
        article = articles.objects.get(pk=key)
        articles.objects.get(pk=key)
        # print(article.series)
        cnt = articles.objects.all().filter(series=article.series, completed=True).count()
        ar = articles.objects.all()
        eps = []
        eps = articles.objects.all().filter(series=article.series, completed=True)
        prev = (eps)
        no = []
        for i in eps:
            if i.episode != '' and i.episode != None:
                # print(i)
                no.append(i.episode)
        # print(no)
        if len(no) != 0:
            prev = max(no)+1
        else:
            prev = 1

        time = datetime.now()
        # print(time)
        # print(article.start_time)
        naive = article.start_time.replace(tzinfo=None)
        difference = time - naive
        seconds = difference.total_seconds()
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        time = {'hour': hours, 'min': minutes,
                'sec': int(seconds)}
        # print(time)
        if len(article.stops.all()) == 0:
            # tim=stoptime.objects.create()
            # article.stops.add(tim.pk)
            btn = 'Take a Break'
            btnclr = 'success'
        else:
            for i in article.stops.all():
                if i.t1 != None and i.t2 != None:
                    def ordinal(n): return "%d%s" % (
                        n, "tsnrhtdd"[(n/10 % 10 != 1)*(n % 10 < 4)*n % 10::4])

                    btn = 'Take '+ordinal(len(article.stops.all())+1)+' break'
                    btnclr = 'success'
                else:
                    btn = 'Resume'
                    btnclr = 'danger'

        return render(request, 'newarticle3.html', {'article': article, 'eps': eps, 'cnt': cnt, 'prev': prev, 'time': time, 'btn': btn, 'btnclr': btnclr})
    else:
        return redirect('/verification')


def tbreak(request, key):
    print('#####delete#####')
    errors = []
    if request.method == 'GET':
        article = articles.objects.get(pk=key)
        if len(article.stops.all()) == 0:
            tim = stoptime.objects.create()
            tim.t1 = datetime.now()
            tim.save()
            article.stops.add(tim.pk)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        else:
            incomplete = None
            for i in article.stops.all():
                if i.t1 != None and i.t2 != None:
                    pass
                else:
                    incomplete = i
            print(incomplete)
            if incomplete == None:
                tim = stoptime.objects.create()
                tim.t1 = datetime.now()
                tim.save()
                article.stops.add(tim.pk)
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
            else:
                if incomplete.t1 == None:
                    incomplete.t1 = datetime.now()
                    incomplete.save()
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
                elif incomplete.t2 == None:
                    incomplete.t2 = datetime.now()
                    incomplete.save()
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def lnikselect(request):
    print('#####loginc#####')
    response_data = {}
    response_data['access_granted'] = False
    errors = []
    if request.method == 'POST':
        email = request.POST['email'].strip()
        key = request.POST['key'].strip()
        if len(email) != 0:
            article = articles.objects.get(pk=key)
            article.link = email
            article.save()
            detlinkdata(email)

            response_data['access_granted'] = True
            response_data['key'] = key
        else:
            errors = []
            errors.append('Paste the Link')

        print(errors, response_data['access_granted'])
        response_data['errors'] = errors
        return JsonResponse(response_data)
    else:
        return redirect('/verification')


def newarticle4(request, key):

    if request.method == 'POST':
        email = request.POST['email']
        article = articles.objects.get(pk=key)
        article.richtext = email
        # print(email)
        soup = BeautifulSoup(email)
        title = soup.select('h1')[0].text.strip()
        try:
            subtitle = soup.select('h2')[0].text.strip()
        except:
            subtitle = 'No Subtitle'
        print(title)
        print(subtitle)
        article.title = title
        article.subtitle = subtitle
        article.endtime = datetime.now()
        if len(article.stops.all()) == 0:
            pass
        else:
            incomplete = None
            for i in article.stops.all():
                if i.t1 != None and i.t2 != None:
                    pass
                else:
                    incomplete = i
            print(incomplete)
            if incomplete == None:
                pass
            else:
                if incomplete.t1 == None:
                    incomplete.t1 = datetime.now()
                    incomplete.save()
                elif incomplete.t2 == None:
                    incomplete.t2 = datetime.now()
                    incomplete.save()
        # print(soup.prettify())
        article.save()
        messages.add_message(request, messages.INFO,
                             'Article Has Been Backed Up')

        return redirect('/')

    else:
        print(request.user)
        article = articles.objects.get(pk=key)
        articles.objects.get(pk=key)
        print(article.series)
        cnt = articles.objects.all().exclude(
            episode=None).filter(series=article.series).count()
        ar = articles.objects.all()
        eps = []
        eps = articles.objects.all().exclude(
            episode=None).filter(series=article.series)
        prev = (eps)
        no = []
        for i in eps:
            if i.episode != '' and i.episode != None:
                print(i)
                no.append(i.episode)
        print(no)
        if len(no) != 0:
            prev = max(no)+1
        else:
            prev = 1
        return render(request, 'newarticle4.html', {'article': article, 'eps': eps, 'cnt': cnt, 'prev': prev})


def updatearticle4(request, key):
    if request.method == 'POST':
        email = request.POST['email']
        article = articles.objects.get(pk=key)
        article.richtext = email
        # print(email)
        soup = BeautifulSoup(email)
        title = soup.select('h1')[0].text.strip()
        subtitle = soup.select('h2')[0].text.strip()
        print(title)
        print(subtitle)
        article.title = title
        article.subtitle = subtitle

        # print(soup.prettify())
        article.save()
        messages.add_message(request, messages.INFO,
                             'Article Has Been Updated')

        return redirect('/')

    else:
        print(request.user)
        article = articles.objects.get(pk=key)
        articles.objects.get(pk=key)
        print(article.series)
        cnt = articles.objects.all().exclude(
            episode=None).filter(series=article.series).count()
        ar = articles.objects.all()
        eps = []
        eps = articles.objects.all().exclude(
            episode=None).filter(series=article.series)
        prev = (eps)
        no = []
        for i in eps:
            if i.episode != '' and i.episode != None:
                print(i)
                no.append(i.episode)
        print(no)
        if len(no) != 0:
            prev = max(no)+1
        else:
            prev = 1
        return render(request, 'newarticle4.html', {'article': article, 'eps': eps, 'cnt': cnt, 'prev': prev})


def pageup(request, key):
    print('#####page#####')
    errors = []
    if request.method == 'POST':
        number = request.POST['page']
        b = books.objects.get(pk=key)
        page = pages.objects.create()
        page.page = int(number)
        page.date = datetime.now()
        page.save()
        b.pages.add(page.pk)

        messages.add_message(request, messages.INFO,
                             'Page Has Been Added')
        return redirect('/')


'''v
    start_time = models.DateTimeField()newarticle4
    endtime = models.DateTimeField(blank=True, null=True)
    link = models.URLField(max_length=300, blank=True)
    completed = models.BooleanField(default=False, blank=True)
    series = models.CharField(max_length=100, blank=True)
    episode = models.IntegerField(max_length=100, blank=True)
    richtext = models.TextField(blank=True)
    title = models.CharField(max_length=200, blank=True)
    subtitle = models.CharField(max_length=200, blank=True)
'''
