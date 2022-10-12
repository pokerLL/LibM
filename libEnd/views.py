import datetime

from django.core import serializers
from django.db.models import Q
from django.utils.timezone import now

from Utils.decorators import *
from Utils.redis_lrucache import *
# from LibM.scripts.decorators import *
# from LibM.scripts.redis_lrucache import *
from libFront import models as md
from libFront.templatetags.mytemplate import timediff


# Create your views here.


def getUnreadedNews():
    msgss = md.libMessage.objects.filter(readed=False).order_by("-c_time")
    msgs = msgss[:6]
    msgnum = msgss.count()
    return msgs, msgnum


@auth_administrator_required
@login_required
def index(request):
    website_title = "书苑-后台"
    page_title = "主页"
    messages, msgnum = getUnreadedNews()

    uc = md.libUser.objects.all().count()
    bc = md.libBook.objects.all().count()
    brc = md.libBorrow.objects.all().filter(p_time__lt=now()).count()
    ccc = md.libComment.objects.filter(has_confirmed=False).count()

    return render(request, "libEnd/index.html", locals())


#@cache_it_httpresponse(10, prefix="lm")
def userlist(request):
    website_title = "用户管理"
    page_title = "用户信息"
    messages, msgnum = getUnreadedNews()

    one_page_item_num = 10
    page = 1
    if request.method == "POST":
        one_page_item_num = int(request.POST.get("one_page_item_num", 10))
        page = int(request.POST.get("page", 1))

    page -= 1
    start = page * one_page_item_num + 1
    end = page * one_page_item_num + one_page_item_num
    users = md.libUser.objects.exclude(id=request.session.get("user_id")).order_by("-c_time")[start - 1:end]
    obj_num = md.libUser.objects.all().count()
    page_num = int(round(obj_num / one_page_item_num + 0.49))
    return render(request, "libEnd/userlist.html", locals())


#@cache_it_httpresponse(10, prefix="lm")
def booklist(request):
    website_title = "书籍管理"
    page_title = "书籍信息"
    messages, msgnum = getUnreadedNews()

    one_page_item_num = 10
    page = 1
    if request.method == "POST":
        one_page_item_num = int(request.POST.get("one_page_item_num", 10))
        page = int(request.POST.get("page", 1))

    page -= 1
    start = page * one_page_item_num + 1
    end = page * one_page_item_num + one_page_item_num

    books = md.libBook.objects.all().order_by("-c_time")[start - 1:end]

    obj_num = md.libBook.objects.all().count()
    page_num = int(round(obj_num / one_page_item_num + 0.49))
    return render(request, "libEnd/booklist.html", locals())


#@cache_it_httpresponse(10, prefix="lm")
def messages(request):
    website_title = "书苑-留言板"
    page_title = "留言板"
    messages, msgnum = getUnreadedNews()

    messages_all = md.libMessage.objects.all().order_by("-c_time")
    return render(request, "libEnd/messages.html", locals())


#@cache_it_httpresponse(10, prefix="lm")
def userdetail(request, id):
    website_title = "用户管理"
    page_title = "新建用户"
    messages, msgnum = getUnreadedNews()

    if id != 0:
        page_title = "用户详细资料"
        user = md.libUser.objects.filter(id=id)[0]
    return render(request, "libEnd/userdetail.html", locals())


#@cache_it_httpresponse(10, prefix="lm")
def authoritylist(request):
    website_title = "用户管理"
    page_title = "管理员设置"
    messages, msgnum = getUnreadedNews()

    one_page_item_num = 10
    page = 1
    if request.method == "POST":
        one_page_item_num = int(request.POST.get("one_page_item_num", 10))
        page = int(request.POST.get("page", 1))

    page -= 1
    start = page * one_page_item_num + 1
    end = page * one_page_item_num + one_page_item_num
    users = md.libUser.objects.filter(type__in=[0, 1])[start - 1:end]
    obj_num = md.libUser.objects.all().count()
    page_num = int(round(obj_num / one_page_item_num + 0.49))
    return render(request, "libEnd/userlist.html", locals())


#@cache_it_httpresponse(10, prefix="lm")
def userrepsdlist(request):
    website_title = "用户管理"
    page_title = "待更改密码用户列表"
    messages, msgnum = getUnreadedNews()

    users = md.libUser.objects.all().filter(change_password_required=True)[: 10]
    return render(request, "libEnd/userlist.html", locals())


#@cache_it_httpresponse(10, prefix="lm")
def usersearch(request, kw):
    website_title = "用户管理"
    page_title = "搜索结果 - " + kw
    messages, msgnum = getUnreadedNews()

    ob = md.libUser.objects.all().filter(
        Q(nickname__icontains=kw) | Q(account__icontains=kw) | Q(description__icontains=kw))

    one_page_item_num = 10
    page = 1
    if request.method == "POST":
        one_page_item_num = int(request.POST.get("one_page_item_num", 10))
        page = int(request.POST.get("page", 1))

    page -= 1
    start = page * one_page_item_num + 1
    end = page * one_page_item_num + one_page_item_num
    users = ob[start - 1:end]
    obj_num = ob.count()
    page_num = int(round(obj_num / one_page_item_num + 0.49))

    return render(request, "libEnd/userlist.html", locals())


#@cache_it_httpresponse(10, prefix="lm")
def booksearch(request, kw):
    website_title = "书籍管理"
    page_title = "搜索结果 - " + kw
    messages, msgnum = getUnreadedNews()

    ob = md.libBook.objects.all().filter(
        Q(name__icontains=kw) | Q(author__icontains=kw) | Q(description__icontains=kw) | Q(publisher__icontains=kw))

    one_page_item_num = 10
    page = 1
    if request.method == "POST":
        one_page_item_num = int(request.POST.get("one_page_item_num", 10))
        page = int(request.POST.get("page", 1))

    page -= 1
    start = page * one_page_item_num + 1
    end = page * one_page_item_num + one_page_item_num
    books = ob[start - 1:end]
    obj_num = ob.count()
    page_num = int(round(obj_num / one_page_item_num + 0.49))
    return render(request, "libEnd/booklist.html", locals())


#@cache_it_httpresponse(10, prefix="lm")
def bookdetail(request, id):
    website_title = "书籍管理"
    page_title = "新建书籍"
    messages, msgnum = getUnreadedNews()
    catgs = md.libCategory.objects.all()

    if id != 0:
        page_title = "书籍详细信息"
        book = md.libBook.objects.select_related().filter(id=id)[0]
    return render(request, "libEnd/bookdetail.html", locals())


#@cache_it_httpresponse(60 * 10)
def bookcategory(request, id):
    cat = md.libCategory.objects.get(id=id)
    website_title = "书籍管理"
    page_title = "分类 - " + cat.name
    messages, msgnum = getUnreadedNews()

    ob = cat.libbook_set.all().order_by('-p_num')

    one_page_item_num = 10
    page = 1
    if request.method == "POST":
        one_page_item_num = int(request.POST.get("one_page_item_num", 10))
        page = int(request.POST.get("page", 1))

    page -= 1
    start = page * one_page_item_num + 1
    end = page * one_page_item_num + one_page_item_num
    books = ob[start - 1:end]
    obj_num = ob.count()
    page_num = int(round(obj_num / one_page_item_num + 0.49))
    return render(request, "libEnd/booklist.html", locals())


@auth_administrator_required_json
@login_required_json
def operation(request):
    if request.method == "GET":
        return HttpResponse(json.dumps({}))

    global catgs, ob
    data = request.POST.dict()
    # print(data)
    obj = request.POST.get("object")
    op = request.POST.get("operation")
    id = request.POST.get("id", 0)

    typ = request.POST.get("type", "1")
    if obj == "book":
        ob = md.libBook
    elif obj == "user":
        ob = md.libUser
    elif obj == "bb":
        if typ == "1" or typ == "3":
            ob = md.libBorrow
        else:
            ob = md.libBack
    elif obj == "message":
        ob = md.libMessage
    elif obj == "comment":
        ob = md.libComment
    elif obj == "announcement":
        ob = md.libAnnouncement

    if id != 0:
        del data['id']
    del data['object']
    del data['operation']
    keys = data.keys()
    # print(data)
    if obj == "user":
        if "l_time" in keys:
            data['l_time'] = data['l_time'][:10] + " " + data["l_time"][11:] + ":00"
        if "c_time" in keys:
            data['c_time'] = data['c_time'][:10] + " " + data["c_time"][11:] + ":00"
    elif obj == "bb":
        if "c_time" in keys:
            data['c_time'] = data['c_time'][:10] + " " + data["c_time"][11:] + ":00"
        if "p_time" in keys:
            data['p_time'] = data['p_time'][:10] + " " + data["p_time"][11:] + ":00"
        if "f_time" in keys:
            if len(data['f_time']) > 5:
                data['f_time'] = data['f_time'][:10] + " " + data["f_time"][11:] + ":00"
            else:
                del data['f_time']
        del data['type']

    # print(data)
    res = {"code": 200}

    # print(data)
    if op == "delete":
        res['msg'] = "删除成功"
        ob.objects.filter(id=id).delete()
    elif op == "update":
        res['msg'] = "信息更改成功"
        ob.objects.filter(id=id).update(**data)
    elif op == "change_password_required":
        res['msg'] = "操作成功"
        user = ob.objects.get(id=id)
        if user.change_password_required == False:
            ob.objects.filter(id=id).update(change_password_required=True)
        else:
            ob.objects.filter(id=id).update(change_password_required=False)
    elif op == "pass":
        res['msg'] = "操作成功"
        if ob.objects.filter(id=id)[0].has_confirmed:
            ob.objects.filter(id=id).update(has_confirmed=False)
        else:
            ob.objects.filter(id=id).update(has_confirmed=True)
    elif op == "create":
        res['msg'] = "创建成功"
        if obj == "book":
            data['stock_now'] = data['stock_all']
        cob = ob.objects.create(**data)
    elif op == "back_book_required":
        res['msg'] = "操作成功"
        lb = ob.objects.get(id=id)
        bookname = lb.book.name
        tf = timediff(lb.p_time, datetime.datetime.now())
        msg = "您在{}借的书《{}》超时未归还(约定于{})，目前已逾期{}".format(
            lb.c_time.strftime("%Y-%m-%d %H:%M"), bookname,
            lb.p_time.strftime("%Y-%m-%d %H:%M"), tf)
        md.libAnnouncement.objects.create(from_user=md.libUser.objects.get(id=request.session.get("user_id")),
                                          for_user=lb.user, title="还书提醒", content=msg, type=4)
        if lb.user.type == 2:
            md.libUser.objects.filter(id=lb.user.id).update(type=3)

    elif op == "book_catgs_change":
        if id != 0:
            print("id=0")
            book = md.libBook.objects.get(id=id)
        else:
            name = data['name']
            print("name:", name)
            book = md.libBook.objects.get(name=name)
        book.categ.clear()
        catgs = data['catgs']
        # print(catgs.split(",")[:-1])
        for _id in catgs.split(",")[:-1]:
            book.categ.add(md.libCategory.objects.get(id=_id))
    return JsonResponse(res)


#@cache_it_httpresponse(10, prefix="lm")
def bbdetail(request, type, id):
    website_title = "借阅管理"

    messages, msgnum = getUnreadedNews()

    # 1借 2还
    global obj
    global catgs

    if type == 1:
        page_title = "在借管理"
        obj = md.libBorrow
    elif type == 2:
        page_title = "历史借阅"
        obj = md.libBack
    else:
        pass
    if id != 0:
        bb = obj.objects.select_related().filter(id=id)[0]

    return render(request, "libEnd/bbdetail.html", locals())


#@cache_it_httpresponse(10, prefix="lm")
def borrowlist(request):
    website_title = "借阅管理"
    page_title = "在借"
    messages, msgnum = getUnreadedNews()

    type = 1
    ob = md.libBorrow.objects.select_related().all()

    one_page_item_num = 10
    page = 1
    if request.method == "POST":
        one_page_item_num = int(request.POST.get("one_page_item_num", 10))
        page = int(request.POST.get("page", 1))

    page -= 1
    start = page * one_page_item_num + 1
    end = page * one_page_item_num + one_page_item_num
    bbs = ob.order_by("-c_time")[start - 1:end]
    obj_num = ob.count()
    page_num = int(round(obj_num / one_page_item_num + 0.49))

    return render(request, "libEnd/bblist.html", locals())


#@cache_it_httpresponse(10, prefix="lm")
def backlist(request):
    website_title = "借阅管理"
    page_title = "历史记录"
    messages, msgnum = getUnreadedNews()

    type = 2
    ob = md.libBack.objects.select_related().all()

    one_page_item_num = 10
    page = 1
    if request.method == "POST":
        one_page_item_num = int(request.POST.get("one_page_item_num", 10))
        page = int(request.POST.get("page", 1))

    page -= 1
    start = page * one_page_item_num + 1
    end = page * one_page_item_num + one_page_item_num
    bbs = ob.order_by("-c_time")[start - 1:end]
    obj_num = ob.count()
    page_num = int(round(obj_num / one_page_item_num + 0.49))

    return render(request, "libEnd/bblist.html", locals())


#@cache_it_httpresponse(10, prefix="lm")
def bookcomment(request, id):
    website_title = "书籍管理"
    page_title = "书籍评论"
    messages, msgnum = getUnreadedNews()

    book = md.libBook.objects.get(id=id)
    page_title += "-" + book.name
    comments = md.libComment.objects.select_related().filter(book=book).order_by('-c_time')
    return render(request, "libEnd/bookcomment.html", locals())


#@cache_it_httpresponse(10, prefix="lm")
def commentconfirm(request):
    website_title = "网站管理"
    page_title = "评论审核"
    messages, msgnum = getUnreadedNews()

    comments = md.libComment.objects.select_related().filter(has_confirmed=False).order_by('-c_time')
    return render(request, "libEnd/commentconfirm.html", locals())


#@cache_it_httpresponse(10, prefix="lm")
def badborrow(request):
    website_title = "借阅管理"
    page_title = "逾期"
    messages, msgnum = getUnreadedNews()

    ob = md.libBorrow
    type = 3

    one_page_item_num = 10
    page = 1
    if request.method == "POST":
        one_page_item_num = int(request.POST.get("one_page_item_num", 10))
        page = int(request.POST.get("page", 1))

    page -= 1
    start = page * one_page_item_num + 1
    end = page * one_page_item_num + one_page_item_num
    bbs = ob.objects.all().filter(p_time__lt=now()).order_by('-c_time')[start - 1:end]
    obj_num = ob.objects.all().filter(p_time__lt=now()).order_by('-c_time').count()
    page_num = int(round(obj_num / one_page_item_num + 0.49))

    return render(request, "libEnd/bblist.html", locals())


#@cache_it_httpresponse(10, prefix="lm")
def bookcategorys(request):
    website_title = "书籍管理"
    page_title = "全部分类"
    messages, msgnum = getUnreadedNews()
    catgs = md.libCategory.objects.all().order_by("-c_time")
    book_num = [it.libbook_set.count() for it in catgs]
    catgs = list(zip(catgs, book_num))

    return render(request, "libEnd/bookcategorys.html", locals())


#@cache_it_httpresponse(10, prefix="lm")
def announcement(request):
    website_title = "网站管理"
    page_title = "网站公告"
    return render(request, "libEnd/announcement.html", locals())


def _api(request):
    operation = request.POST.get("operation", None)
    if request.method == "GET" or operation is None:
        return JsonResponse({})

    if operation == "get":
        return _api_get(request)


#@cache_it_json(expiration=60)
def _api_get(request):
    global ob
    obj = request.POST.get("object", None)
    if obj is None:
        return JsonResponse({})
    data = request.POST.dict()
    del data['operation']
    del data['object']

    if obj == "book":
        ob = md.libBook

    result = ob.objects.filter(**data)

    res = serializers.serialize('json', result)
    res = json.loads(res)

    return JsonResponse(res, safe=False)
