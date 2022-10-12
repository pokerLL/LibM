import os
import random
import sys
import time

import django

import fake_tool as fk

# 将项目根目录添加到 Python 的模块搜索路径中
back = os.path.dirname
BASE_DIR = back(back(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# 启动django 便于使用orm系统
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "HZULibM.settings")
django.setup()

from libFront.models import *


##########################
# 全局生成数据规模控制
USER_NUM = 100
BOOK_NUM = 200
LEAST_TAG_NUM = 1
MAX_TAG_NUM = 5
COMMENT_NUM = 500
BORROW_NUM = 100
BACK_NUM = 100
BOOK_FAV_NUM = 1000
COMMENT_FAV_NUM = 2000
MESSAGE_NUM = 100


#########################


def fakecategory():
    libCategory.objects.all().delete()
    category = fk.categorylist()
    cls = []
    for it in category:
        print("\r**生成类别".format(it), end="")
        categ = libCategory()
        categ.name = it
        categ.description = fk.sentence()
        cls.append(categ)
    libCategory.objects.bulk_create(cls)
    print()


def fakeuser():
    libUser.objects.all().delete()
    uls = []
    for it in range(USER_NUM):
        print("\r**生成第{}位用户".format(it + 1), end="")
        user = libUser()
        user.nickname = fk.username()
        user.account = fk.account()
        user.email = user.account + "@qq.com"
        user.birthday = fk.datebefore()
        user.gender = fk.gender()
        user.type = 2
        uls.append(user)
    libUser.objects.bulk_create(uls)
    print()


def fakebook():
    libBook.objects.all().delete()
    catgs = libCategory.objects.all()
    cc = catgs.count()
    bls1 = []
    bls2 = []
    for it in range(BOOK_NUM):
        print("\r**生成第{}本书籍".format(it + 1), end="")
        book = libBook()
        book.name = fk.bookname()
        book.author = fk.username()
        book.publisher = fk.publisher()
        book.pubdate = fk.datebefore()
        book.stock_all = random.randint(10, 100)
        book.stock_now = random.randint(0, book.stock_all)
        book.borrow_num = random.randint(0, 100)
        book.description = fk.sentence()
        book.score = random.randint(1, 10)
        book.comment_num = random.randint(1, 50)
        book.chapters = fk.chapters()
        bls1.append(book)
    libBook.objects.bulk_create(bls1)
    print()
    books = libBook.objects.all()
    cnt = 0
    for book in books:
        cnt = cnt + 1
        print("\r**正在为第{}本书添加标签".format(cnt), end="")
        for i in range(random.randint(LEAST_TAG_NUM, MAX_TAG_NUM)):
            book.categ.add(catgs[random.randint(0, cc - 1)])
        book.save()
    print()


def fakecomment():
    libComment.objects.all().delete()
    users = libUser.objects.all()
    books = libBook.objects.all()
    uc = users.count()
    bc = books.count()
    cls = []
    for it in range(COMMENT_NUM):
        print("\r**生成第{}条评论".format(it + 1), end="")
        comm = libComment()
        comm.user = users[random.randint(1, uc - 1)]
        comm.book = books[random.randint(1, bc - 1)]
        comm.comment = fk.sentence()
        comm.has_confirmed = True
        cls.append(comm)
    libComment.objects.bulk_create(cls)
    print()


def fakeborrow():
    libBorrow.objects.all().delete()
    books = libBook.objects.all()
    users = libUser.objects.all()
    bc = books.count()
    uc = users.count()
    bols = []
    for it in range(BORROW_NUM):
        print("\r**正在生成第{}条借书记录".format(it + 1), end="")
        borrow = libBorrow()
        borrow.user = users[random.randint(1, uc - 1)]
        borrow.book = books[random.randint(1, bc - 1)]
        borrow.c_time = fk.datebefore()
        borrow.p_time = fk.dateafter()
        bols.append(borrow)
    libBorrow.objects.bulk_create(bols)
    print()


def fakeback():
    libBorrow.objects.all().delete()
    books = libBook.objects.all()
    users = libUser.objects.all()
    bc = books.count()
    uc = users.count()
    bcls = []
    for it in range(BORROW_NUM):
        print("\r**正在生成第{}条还书记录".format(it + 1), end="")
        back = libBorrow()
        back.user = users[random.randint(1, uc - 1)]
        back.book = books[random.randint(1, bc - 1)]
        back.c_time = fk.datebefore()
        back.p_time = fk.dateafter()
        back.f_time = fk.datebefore()
        bcls.append(back)
    libBack.objects.bulk_create(bcls)
    print()


def fakebookfav():
    libBookFavourite.objects.all().delete()
    users = libUser.objects.all()
    books = libBook.objects.all()
    uc = users.count()
    bc = books.count()
    ls = []
    for it in range(0, BOOK_FAV_NUM):
        print("\r**生成第{}条书籍点赞记录".format(it + 1), end="")
        lbf = libBookFavourite()
        lbf.user = users[random.randint(0, uc - 1)]
        lbf.book = books[random.randint(0, bc - 1)]
        ls.append(lbf)
    libBookFavourite.objects.bulk_create(ls)
    print()


def fakecommentfav():
    libCommentFavourite.objects.all().delete()
    users = libUser.objects.all()
    cms = libComment.objects.all()
    uc = users.count()
    bc = cms.count()
    ls = []
    for it in range(0, COMMENT_FAV_NUM):
        print("\r**生成第{}条评论点赞记录".format(it + 1), end="")
        lcf = libCommentFavourite()
        lcf.user = users[random.randint(0, uc - 1)]
        lcf.comment = cms[random.randint(0, bc - 1)]
        ls.append(lcf)
    libCommentFavourite.objects.bulk_create(ls)
    print()


def fakeMessage():
    users = libUser.objects.all()
    uc = users.count()
    ls = []
    for it in range(0, MESSAGE_NUM):
        print("\r**生成第{}条留言".format(it + 1), end="")
        lm = libMessage()
        lm.user = users[random.randint(0, uc - 1)]
        lm.message = fk.sentence()[:6]
        lm.message = fk.sentence()
        ls.append(lm)
    libMessage.objects.bulk_create(ls)
    print()


def correctbook():
    books = libBook.objects.all()
    cnt = 0
    for book in books:
        cnt = cnt + 1
        print("\r**正在修正第{}本书的信息".format(cnt), end="")
        bw = book.libborrow_set.all().count()
        hs = book.libback_set.all().count()
        book.borrow_num = bw + hs
        book.stock_now = book.stock_all - bw
        book.comment_num = book.libcomment_set.all().count()
        book.p_num = book.libbookfavourite_set.all().count()
        book.save()
    print()


def correctcomment():
    comments = libComment.objects.all()
    cnt = 0
    for comment in comments:
        cnt = cnt + 1
        print("\r**正在修正第{}条评论的信息".format(cnt), end="")
        comment.p_num = comment.libcommentfavourite_set.all().count()
        comment.save()
    print()


def fakeTestData():
    try:
        libUser.objects.create(nickname="super", account="s", password="1", has_confirmed=True,
                               email=fk.account() + "@qq.com", birthday=fk.datebefore(),
                               gender=fk.gender(), type=0)
        libUser.objects.create(nickname="poker", account="p", password="1", has_confirmed=True,
                               email=fk.account() + "@qq.com", birthday=fk.datebefore(),
                               gender=fk.gender(), type=1)
        libUser.objects.create(nickname="qbit", account="q", password="1", has_confirmed=True,
                               email=fk.account() + "@qq.com", birthday=fk.datebefore(),
                               gender=fk.gender(), type=1)
    except BaseException:
        pass
    books = libBook.objects.all()
    user_p = libUser.objects.get(account="p")
    user_q = libUser.objects.get(account="q")
    for i in range(20):
        libComment.objects.create(book=random.choice(books), comment=fk.sentence(),
                                  user=user_p, has_confirmed=True)
        libComment.objects.create(book=random.choice(books), comment=fk.sentence(),
                                  user=user_q, has_confirmed=True)
        libComment.objects.create(book=random.choice(books), comment=fk.sentence(),
                                  user=user_p, has_confirmed=False)
        libComment.objects.create(book=random.choice(books), comment=fk.sentence(),
                                  user=user_q, has_confirmed=False)
        libBorrow.objects.create(book=random.choice(books), user=user_p,
                                 c_time=fk.datebefore(), p_time=fk.dateafter())
        libBorrow.objects.create(book=random.choice(books), user=user_q,
                                 c_time=fk.datebefore(), p_time=fk.dateafter())
        libBorrow.objects.create(book=random.choice(books), user=user_p,
                                 c_time=fk.datebefore(), p_time=fk.datebefore())
        libBorrow.objects.create(book=random.choice(books), user=user_q,
                                 c_time=fk.datebefore(), p_time=fk.datebefore())
        libBack.objects.create(book=random.choice(books), user=user_p, c_time=fk.datebefore(),
                               p_time=fk.dateafter(), f_time=fk.dateafter())
        libBack.objects.create(book=random.choice(books), user=user_q, c_time=fk.datebefore(),
                               p_time=fk.dateafter(), f_time=fk.dateafter())


if __name__ == "__main__":
    fakecategory()
    fakeuser()
    fakebook()
    fakecomment()
    fakeborrow()
    fakeback()
    fakebookfav()
    fakecommentfav()
    correctbook()
    correctcomment()
    fakeMessage()
    fakeTestData()
