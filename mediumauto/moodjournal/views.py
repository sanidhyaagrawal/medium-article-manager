

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
from django_summernote.fields import SummernoteTextFormField, SummernoteTextField
from datetime import datetime
from django.contrib import messages
from django.http import HttpResponseRedirect


signer = Signer()
# Create your views here.


def mood(request):
    return render(request, 'mood.html')
