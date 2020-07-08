"""mediumauto URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views
urlpatterns = [
    path('', views.gateway, name='gateway'),
    path('home', views.home, name='home'),
    path('verification', views.verification, name='verification'),
    path('loginc/$', views.loginc, name='loginc'),
    path('seriesselect/$', views.seriesselect, name='seriesselect'),
    path('newarticle-step1', views.newarticle1, name='newarticle1'),
    path('newarticle-step2/<int:key>/', views.newarticle2, name='newarticle2'),
    path('episodeselect/$', views.episodeselect, name='episodeselect'),
    path('newarticle-step3/<int:key>/', views.newarticle3, name='newarticle3'),
    path('lnikselect/$', views.lnikselect, name='lnikselect'),
    path('newarticle-step4/<int:key>/', views.newarticle4, name='newarticle4'),
    path('updatearticle/<int:key>/', views.updatearticle4, name='updatearticle4'),
    path('delete/<int:key>/', views.delete, name='delete'),
    path('complete/<int:key>/', views.complete, name='complete'),
    path('view/<int:key>/', views.view, name='view'),
    path('update/<int:key>/', views.update, name='update'),
    path('tbreak/<int:key>/', views.tbreak, name='tbreak'),
    path('update-page/<int:key>/', views.pageup, name='pageup'),
    path('stats', views.stats, name='stats'),

    #path('newarticle-step5/<int:key>/', views.newarticle4, name='newarticle4'),
    #path('pastetext/$', views.episodeselect, name='episodeselect'),
]
