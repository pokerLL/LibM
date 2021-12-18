from django.contrib import admin
from django.urls import path, include

from . import views

app_name = "libfront"

urlpatterns = [
    path('', views.login),
    path('index', views.index, name="index"),
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),
    path('register', views.register, name="register"),
    path('user/<int:id>', views.userdetail, name="userdetail"),
    path('book/<int:bookid>', views.bookdetail, name="bookdetail"),
    path('rank/<str:st>/<int:pg>', views.ranklist, name="ranklist"),
    path('category/<int:categid>/<int:pg>', views.categorylist, name="category"),
    path('categorys', views.categorys, name="categorys"),
    path('book/borrow', views.borrow_ajax, name="borrow"),
    path('book/back', views.back_ajax, name="back"),
    path('search/<str:kw>/<int:pg>', views.search, name="search"),
    path('operation', views.operation),
    path('confirm/', views.user_confirm),
]

