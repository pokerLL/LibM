from django.urls import path

from . import views

app_name = "lm"

urlpatterns = [
    path('', views.index, name="index"),

    path('user/ul', views.userlist, name="userlist"),
    path('user/uahl', views.authoritylist, name="authoritylist"),
    path('user/upl', views.userrepsdlist, name="userrepsdlist"),
    path('user/ud/<int:id>', views.userdetail, name="userdetail"),

    path('book/bl', views.booklist, name="booklist"),
    path('book/bd/<int:id>', views.bookdetail, name="bookdetail"),
    path('book/bc/<int:id>', views.bookcomment, name="bookcomments"),
    path('book/catgs', views.bookcategorys, name="bookcategorys"),
    path('book/catg/<int:id>', views.bookcategory, name="bookcategory"),

    path('bb/borrow', views.borrowlist, name="borrowlist"),
    path('bb/back', views.backlist, name="backlist"),
    path('bb/bbdetail/<int:type>/<int:id>', views.bbdetail, name="bbdetail"),
    path('bb/badborrow', views.badborrow, name="badborrow"),

    path('oth/ann', views.announcement, name="announcement"),
    path('oth/bcc', views.commentconfirm, name="commentconfirm"),
    path('oth/msg', views.messages, name="messages"),

    path('operation', views.operation, name="operation"),

    path("user/search/<str:kw>", views.usersearch, name="usersearch"),
    path("book/search/<str:kw>", views.booksearch, name="booksearch"),

    path('api', views._api)
]
