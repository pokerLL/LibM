"""rzybz URL Configuration

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
from django.contrib import admin
from django.urls import path, include
from users import urls as USERS_RUL
from lifeandfun import urls as LIFE_URL
from homep import urls as HOME_URL
from webchat import urls as CHAT_URL
from todo import urls as TODO_URL
from libFront import urls as LIBFRONT_URL

urlpatterns = [
    path('', include(HOME_URL)),
    path('users/', include(USERS_RUL)),
    path('life/', include(LIFE_URL)),
    path('chat/', include(CHAT_URL)),
    path('todo/', include(TODO_URL)),
    path('lf/', include(LIBFRONT_URL)),
    path('captcha/', include('captcha.urls')),
    path('admin/', admin.site.urls),
]
