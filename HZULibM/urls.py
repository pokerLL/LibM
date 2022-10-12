"""HZULibM URL Configuration

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
import libFront.urls as FRONTURL
import libEnd.urls as ENDURL
from HZULibM import settings
from django.views.generic import RedirectView
from captcha.views import captcha_refresh
# from rest_framework import routers
from libFront.views import *
from django.conf.urls import url, static
# from rest_framework_jwt.views import obtain_jwt_token
# 验证码刷新功能，captcha_refresh为captcha.views内置方法，不需要我们单独写


# 前后端分离api的路由
# router = routers.DefaultRouter()
# router.register(r'libBook', BookViewSet)
# router.register(r'libCategory', CategoryViewSet)
# router.register(r'libUser', UserViewSet)
# router.register(r'libBookFavourite', BooklikeViewSet)
# router.register(r'libBookCollection', BookCollectionViewSet)
# router.register(r'libComment', CommentViewSet)
# router.register(r'libCommentFavourite', CommentlikeViewSet)
# router.register(r'libBack', BackViewSet)
# router.register(r'libMessage', MessageViewSet)
# router.register(r'libAnnouncement', AnnouncementViewSet)
# router.register(r'libConfirmString', ConfirmStringViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('lf/', include(FRONTURL)),
    path('captcha/', include('captcha.urls')),
    path('lm/', include(ENDURL)),
    url(r'^static/(?P<path>.*)$', static.serve,
        {'document_root': settings.STATIC_ROOT}, name='static'),
    url(r'^favicon.ico$', RedirectView.as_view(url=r'static/picture/favicon.ico')),
    path('refresh/', captcha_refresh),

    # path('api/',include(router.urls)),
]
