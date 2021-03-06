"""ivreg URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from ivreg import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^registration/$', views.registration, name='registration'),
    url(r'^credentials/$', views.credentials, name='credentials'),
    url(r'^authorization/(?P<voter_id>[0-9a-zA-Z]+)/$', views.authorization, name='authorization_complete'),
    url(r'^validate/$', views.validate, name='validate'),
    url(r'^ballot/(?P<ballot_id>[0-9a-zA-Z]+)/$', views.ballot, name='ballot'),
    url(r'^admin/', admin.site.urls),
]
