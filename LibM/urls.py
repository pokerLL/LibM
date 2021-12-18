"""LibM URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf.urls import url, static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

import libEnd.urls as ENDURL
import libFront.urls as FRONTURL
from LibM import settings

urlpatterns = [
    path('', include(FRONTURL)),
    path('lf/', include(FRONTURL)),
    path('lm/', include(ENDURL)),
    path('admin/', admin.site.urls),
    url(r'^static/(?P<path>.*)$', static.serve,
        {'document_root': settings.STATIC_ROOT}, name='static'),
    url(r'^favicon.ico$', RedirectView.as_view(url=r'static/favicon.ico')),
    path('captcha/', include('captcha.urls')),
]
