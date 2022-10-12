from django.urls import path, include
from . import views
from django.conf.urls import url
# from rest_framework_jwt.views import obtain_jwt_token
app_name = "libfront"
urlpatterns = [
    path('', views.login),
    path('login', views.login, name="login"),
    path('index',views.index,name="index"),
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



    #前后端分离api接口
    # url(r'^authorization/$',obtain_jwt_token),
    # url(r'^api/v1/$',views.AuthView.as_view()),
    # url(r'^api/v2/$',views.OrderView.as_view()),
]